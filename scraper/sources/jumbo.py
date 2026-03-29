"""Jumbo source — crawls Jumbo catalog via their GraphQL API.

Jumbo's website uses a GraphQL API at /api/graphql.
Required headers:
  apollographql-client-name: ECOMMERCE_HEADER
  apollographql-client-version: V3

Discovery: search by category slugs and broad queries, paginate with offSet.
Note: Jumbo rate-limits aggressively — use conservative concurrency.
"""
import asyncio
import logging
from typing import Optional

import aiohttp

from .base import BaseSource, ScrapedProduct
from ..pricing import parse_weight_grams, parse_volume_ml, calculate_unit_price
from ..config import REQUEST_TIMEOUT

logger = logging.getLogger("scraper")

GRAPHQL_URL = "https://www.jumbo.com/api/graphql"
PRODUCT_PAGE_URL = "https://www.jumbo.com/producten/{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "apollographql-client-name": "ECOMMERCE_HEADER",
    "apollographql-client-version": "V3",
}

# Product search query — field names discovered via error messages
# TODO: discover more fields (price, image, category) once rate limit resets
SEARCH_QUERY = """
query SearchProducts($input: ProductSearchInput!) {
  searchProducts(input: $input) {
    products {
      id
      title
      link
    }
    totalCount
    numberOfPages
  }
}
"""

# Category slugs from Jumbo's website navigation
CATEGORY_SLUGS = [
    "aardappelen,-groente-en-fruit",
    "zuivel,-eieren,-boter",
    "vlees,-vis,-vega",
    "kaas,-vleeswaren,-tapas",
    "brood,-gebak",
    "ontbijt,-granen,-beleg",
    "pasta,-rijst,-wereldkeuken",
    "soepen,-sauzen,-kruiden",
    "snoep,-koek,-chips",
    "frisdrank,-sappen",
    "koffie,-thee",
    "bier,-wijn",
    "diepvries",
    "drogisterij,-baby",
    "huishouden,-dieren",
]

DISCOVERY_QUERIES = [
    "melk", "kaas", "yoghurt", "boter", "eieren",
    "brood", "groente", "fruit", "aardappel",
    "vlees", "kip", "gehakt", "vis", "zalm",
    "pasta", "rijst", "saus", "soep",
    "koffie", "thee", "frisdrank", "bier", "wijn",
    "chips", "chocolade", "koek", "snoep",
    "diepvries", "pizza", "ijs",
    "wasmiddel", "shampoo", "tandpasta", "luiers",
]


class JumboSource(BaseSource):
    store_id = "jumbo"
    store_name = "Jumbo"

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        # Conservative concurrency — Jumbo rate-limits aggressively
        self._sem = asyncio.Semaphore(3)

    async def _graphql(self, operation: str, query: str, variables: dict) -> dict:
        """Execute a GraphQL query."""
        async with self._sem:
            try:
                async with self._session.post(
                    GRAPHQL_URL,
                    headers=HEADERS,
                    json={
                        "operationName": operation,
                        "query": query,
                        "variables": variables,
                    },
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
                ) as resp:
                    if resp.status == 429:
                        retry_after = int(resp.headers.get("Retry-After", "5"))
                        logger.warning("Jumbo: rate limited, waiting %ds", retry_after)
                        await asyncio.sleep(retry_after)
                        return await self._graphql(operation, query, variables)
                    resp.raise_for_status()
                    data = await resp.json()
                    if "errors" in data:
                        logger.warning("Jumbo GraphQL error: %s", data["errors"][0].get("message", "unknown"))
                        return {}
                    return data.get("data", {})
            except asyncio.TimeoutError:
                logger.warning("Jumbo: request timed out")
                return {}
            except Exception as e:
                logger.warning("Jumbo: request failed: %s", e)
                return {}

    async def _search_page(self, search_terms: str, search_type: str = "keyword", offset: int = 0, limit: int = 24) -> dict:
        """Search for products."""
        return await self._graphql(
            "SearchProducts",
            SEARCH_QUERY,
            {
                "input": {
                    "searchTerms": search_terms,
                    "searchType": search_type,
                    "limit": limit,
                    "offSet": offset,
                }
            },
        )

    async def _crawl_query(self, query: str, seen: set) -> list[ScrapedProduct]:
        """Paginate through all results for a query."""
        products = []
        offset = 0
        limit = 24

        while True:
            data = await self._search_page(query, offset=offset, limit=limit)
            search_result = data.get("searchProducts", {})
            raw_products = search_result.get("products", [])

            if not raw_products:
                break

            for raw in raw_products:
                pid = raw.get("id")
                if pid and pid not in seen:
                    seen.add(pid)
                    p = self._parse_product(raw)
                    if p:
                        products.append(p)

            total_pages = search_result.get("numberOfPages", 1)
            current_page = offset // limit
            if current_page + 1 >= total_pages:
                break
            offset += limit

            # Be polite
            await asyncio.sleep(0.5)

        return products

    async def fetch_all(self) -> list[ScrapedProduct]:
        """Discover and fetch all Jumbo products."""
        async with aiohttp.ClientSession() as session:
            self._session = session

            seen: set = set()
            all_products: list[ScrapedProduct] = []

            # Phase 1: category crawl
            logger.info("Jumbo: crawling %d categories", len(CATEGORY_SLUGS))
            for slug in CATEGORY_SLUGS:
                products = await self._crawl_query(slug, seen)
                all_products.extend(products)
                logger.info("Jumbo: category '%s' → %d new products", slug, len(products))

            logger.info("Jumbo: category crawl found %d products", len(all_products))

            # Phase 2: supplementary search queries
            logger.info("Jumbo: running %d discovery queries", len(DISCOVERY_QUERIES))
            for query in DISCOVERY_QUERIES:
                products = await self._crawl_query(query, seen)
                all_products.extend(products)

            logger.info(
                "Jumbo: total %d products (%d deals)",
                len(all_products),
                sum(1 for p in all_products if p.is_deal),
            )

            self._session = None
            return all_products

    def _parse_product(self, raw: dict) -> Optional[ScrapedProduct]:
        """Parse a Jumbo GraphQL product into a ScrapedProduct.

        Note: field availability depends on what the GraphQL query requests.
        The query will be expanded as we discover more fields.
        """
        title = raw.get("title")
        product_id = raw.get("id")
        if not title or not product_id:
            return None

        # Price — try various field names (schema not fully discovered yet)
        current_price = None
        original_price = None
        is_deal = False

        # Try nested price objects
        price_data = raw.get("price") or raw.get("prices") or {}
        if isinstance(price_data, dict):
            current_price = price_data.get("amount") or price_data.get("price", {}).get("amount")
            promo = price_data.get("promotionalPrice", {})
            if promo and promo.get("amount"):
                original_price = current_price
                current_price = promo["amount"]
                is_deal = True
        elif isinstance(price_data, (int, float)):
            current_price = price_data

        # Prices might be in cents
        if current_price and current_price > 100:
            current_price = current_price / 100
        if original_price and original_price > 100:
            original_price = original_price / 100

        # If no price found, still create the product (price can be filled later)
        if current_price is None:
            current_price = 0.0

        # Weight/volume from title
        weight_grams = parse_weight_grams(title)
        volume_ml = parse_volume_ml(title) if not weight_grams else None
        unit_price = calculate_unit_price(current_price, weight_grams, volume_ml) if current_price > 0 else None

        # Unit size from title
        unit_size = raw.get("unitSize") or raw.get("quantityOptions", [{}])[0].get("unit") if isinstance(raw.get("quantityOptions"), list) else None

        # Image
        image_url = raw.get("imageUrl") or raw.get("image", {}).get("url") if isinstance(raw.get("image"), dict) else raw.get("image")

        # Link
        link = raw.get("link") or ""
        url = f"https://www.jumbo.com{link}" if link and not link.startswith("http") else link

        return ScrapedProduct(
            store_id=self.store_id,
            external_id=str(product_id),
            name=title,
            brand=raw.get("brand"),
            category=self._map_category(raw.get("topLevelCategory") or raw.get("category")),
            current_price=round(current_price, 2) if current_price else 0.0,
            original_price=round(original_price, 2) if original_price else None,
            unit_price=round(unit_price, 2) if unit_price else None,
            weight_grams=weight_grams,
            volume_ml=volume_ml,
            unit_size=unit_size,
            is_deal=is_deal,
            url=url or PRODUCT_PAGE_URL.format(product_id),
            image_url=image_url,
        )

    @staticmethod
    def _map_category(jumbo_category: Optional[str]) -> Optional[str]:
        """Map Jumbo category to our category IDs."""
        if not jumbo_category:
            return None
        c = jumbo_category.lower()
        if any(k in c for k in ("kaas", "zuivel", "melk", "yoghurt", "boter", "eieren")):
            return "zuivel"
        if any(k in c for k in ("vlees", "kip", "gehakt", "worst", "vis", "vega")):
            return "vlees"
        if any(k in c for k in ("groente", "fruit", "aardappel", "salade")):
            return "groente"
        if any(k in c for k in ("brood", "bakkerij", "gebak", "ontbijt", "beleg", "cereals")):
            return "brood"
        if any(k in c for k in ("bier", "wijn", "frisdrank", "sap", "water", "drank", "koffie", "thee")):
            return "dranken"
        if any(k in c for k in ("pasta", "rijst", "noodles", "wereld", "italiaans")):
            return "pasta"
        if any(k in c for k in ("conserv", "saus", "soep", "kruiden", "olie")):
            return "conserven"
        if any(k in c for k in ("snoep", "chips", "koek", "chocola", "noten", "snack")):
            return "snacks"
        if any(k in c for k in ("diepvries", "ijs", "pizza")):
            return "diepvries"
        if any(k in c for k in ("huishoud", "schoonmaak", "wasmiddel")):
            return "huishouden"
        if any(k in c for k in ("drogist", "medicijn", "vitamine")):
            return "drogist"
        if any(k in c for k in ("verzorging", "shampoo", "tandpasta", "baby", "luier")):
            return "verzorging"
        return "overig"
