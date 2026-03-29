"""Oma Zuinig Scraper — discover and fetch grocery products from Dutch supermarkets.

Usage:
    python -m scraper                  # run all active sources
    python -m scraper --store ah       # run only AH
    python -m scraper --dry-run        # fetch but don't write to DB (save JSON instead)

When no database is configured, results are automatically saved to scraper/data/.
"""
import asyncio
import json
import logging
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .config import DATA_DIR, LOG_DIR
from .sources import ALL_SOURCES

# ── Logging ──────────────────────────────────────────────

logger = logging.getLogger("scraper")
logger.setLevel(logging.INFO)

# Console
console = logging.StreamHandler()
console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(console)

# File
log_file = LOG_DIR / "scraper.log"
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s"))
logger.addHandler(file_handler)


def save_to_json(products: list, store_id: str):
    """Save scraped products to a JSON file for inspection / later DB import."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = DATA_DIR / f"{store_id}_{timestamp}.json"

    data = {
        "store_id": store_id,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "product_count": len(products),
        "deal_count": sum(1 for p in products if p.is_deal),
        "products": [asdict(p) for p in products],
    }

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Saved %d products to %s", len(products), path.name)
    return path


async def run(store_filter: str | None = None):
    """Run all (or filtered) source adapters."""
    sources = ALL_SOURCES
    if store_filter:
        sources = [s for s in sources if s.store_id == store_filter]
        if not sources:
            logger.error("Unknown store: %s", store_filter)
            return

    for source_cls in sources:
        source = source_cls()
        logger.info("━" * 50)
        logger.info("Starting: %s (%s)", source.store_name, source.store_id)

        start = time.monotonic()
        try:
            products = await source.fetch_all()
        except Exception as e:
            logger.error("%s failed: %s", source.store_id, e, exc_info=True)
            continue

        elapsed = time.monotonic() - start
        logger.info(
            "%s: %d products fetched in %.1fs (%d deals)",
            source.store_id,
            len(products),
            elapsed,
            sum(1 for p in products if p.is_deal),
        )

        # Save to JSON (always, for now — DB push added later)
        save_to_json(products, source.store_id)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Oma Zuinig grocery scraper")
    parser.add_argument("--store", type=str, help="Only run this store (e.g. 'ah')")
    args = parser.parse_args()

    asyncio.run(run(store_filter=args.store))


if __name__ == "__main__":
    main()
