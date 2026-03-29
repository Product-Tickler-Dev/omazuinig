"""Database sync module — pushes ScrapedProducts into Supabase/PostgreSQL.

This module handles:
1. Connecting to the database
2. Finding or creating canonical products
3. Upserting store_products (via the DB function upsert_store_product)
4. Marking stale products as out of stock
5. Refreshing materialized views
6. Logging fetch runs

Not functional until a database is provisioned. The scraper falls back
to JSON output when DATABASE_URL is not set.
"""
import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

from .sources.base import ScrapedProduct
from .config import DATABASE_URL, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

logger = logging.getLogger("scraper")

try:
    import asyncpg
except ImportError:
    asyncpg = None
    logger.debug("asyncpg not installed — DB sync disabled")


def is_db_configured() -> bool:
    """Check if database connection is configured."""
    return bool(DATABASE_URL or (DB_HOST and DB_PASSWORD))


async def create_pool() -> Optional["asyncpg.Pool"]:
    """Create a connection pool."""
    if not asyncpg:
        logger.warning("asyncpg not installed, cannot connect to database")
        return None

    try:
        if DATABASE_URL:
            pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        else:
            pool = await asyncpg.create_pool(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                min_size=1,
                max_size=10,
            )
        logger.info("Database pool created")
        return pool
    except Exception as e:
        logger.error("Failed to create database pool: %s", e)
        return None


async def find_or_create_product(conn, product: ScrapedProduct) -> str:
    """Find a canonical product by EAN or name+brand, or create a new one.

    Returns the product UUID.
    """
    # Try EAN match first (most reliable)
    # Note: we don't have EAN from AH's search API, but other sources might provide it
    # For now, match by brand + name
    if product.brand:
        row = await conn.fetchrow(
            "SELECT id FROM products WHERE brand = $1 AND name = $2 LIMIT 1",
            product.brand, product.name,
        )
        if row:
            return str(row["id"])

    # Try exact name match (for private labels with no brand)
    row = await conn.fetchrow(
        "SELECT id FROM products WHERE name = $1 AND (brand IS NULL OR brand = $2) LIMIT 1",
        product.name, product.brand,
    )
    if row:
        return str(row["id"])

    # Create new canonical product
    row = await conn.fetchrow(
        """INSERT INTO products (name, brand, category_id, unit_size, weight_grams, volume_ml, image_url)
           VALUES ($1, $2, $3, $4, $5, $6, $7)
           RETURNING id""",
        product.name,
        product.brand,
        product.category,
        product.unit_size,
        product.weight_grams,
        product.volume_ml,
        product.image_url,
    )
    return str(row["id"])


async def sync_products(pool, products: list[ScrapedProduct], store_id: str):
    """Sync a batch of scraped products to the database.

    Workflow:
    1. Start a fetch_log entry
    2. For each product: find/create canonical product, upsert store_product
    3. Mark stale products as out of stock
    4. Complete the fetch_log
    5. Refresh materialized views
    """
    fetch_start = datetime.now(timezone.utc)

    async with pool.acquire() as conn:
        # Start fetch log
        log_id = await conn.fetchval(
            """INSERT INTO fetch_logs (store_id, started_at, status)
               VALUES ($1, $2, 'running') RETURNING id""",
            store_id, fetch_start,
        )

    new_count = 0
    updated_count = 0
    errors = 0

    # Process in batches to avoid holding connections too long
    batch_size = 100
    for i in range(0, len(products), batch_size):
        batch = products[i:i + batch_size]

        async with pool.acquire() as conn:
            async with conn.transaction():
                for product in batch:
                    try:
                        # Find or create canonical product
                        product_id = await find_or_create_product(conn, product)

                        # Upsert store_product via DB function
                        sp_id = await conn.fetchval(
                            """SELECT upsert_store_product(
                                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
                            )""",
                            product_id,
                            product.store_id,
                            product.external_id,
                            product.store_name or product.name,
                            product.current_price,
                            product.original_price,
                            product.unit_price,
                            product.is_deal,
                            product.deal_description,
                            product.deal_start,
                            product.deal_end,
                            product.url,
                            product.image_url,
                        )

                        # Count new vs updated (rough — sp_id being new means new)
                        updated_count += 1

                    except Exception as e:
                        errors += 1
                        if errors <= 5:
                            logger.warning("Error syncing %s: %s", product.name, e)

        logger.info(
            "Synced batch %d-%d of %d (%d errors so far)",
            i, min(i + batch_size, len(products)), len(products), errors,
        )

    # Mark stale products
    async with pool.acquire() as conn:
        stale_count = await conn.fetchval(
            "SELECT mark_stale_products($1, $2)",
            store_id, fetch_start,
        )
        if stale_count:
            logger.info("Marked %d stale products as out of stock", stale_count)

        # Complete fetch log
        await conn.execute(
            """UPDATE fetch_logs
               SET completed_at = now(),
                   products_fetched = $2,
                   products_updated = $3,
                   status = $4,
                   error_message = $5
               WHERE id = $1""",
            log_id,
            len(products),
            updated_count,
            "error" if errors > len(products) * 0.5 else "success",
            f"{errors} errors" if errors else None,
        )

    # Refresh materialized views
    try:
        async with pool.acquire() as conn:
            await conn.execute("SELECT refresh_views()")
            logger.info("Materialized views refreshed")
    except Exception as e:
        logger.warning("Failed to refresh views: %s", e)

    logger.info(
        "Sync complete: %d products, %d updated, %d errors, %d stale marked",
        len(products), updated_count, errors, stale_count or 0,
    )
