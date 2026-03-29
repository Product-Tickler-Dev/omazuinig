"""Dirk source — fetches products via their public GraphQL API.

Dirk's API at web-gateway.dirk.nl/graphql requires no authentication.
Discovery: search by broad queries (no category listing without auth).
Prices: fetched per product via productAssortment(productId, storeId).
"""
import asyncio
import logging
from typing import Optional

import aiohttp

from .base import BaseSource, ScrapedProduct
from ..pricing import parse_weight_grams, parse_volume_ml, calculate_unit_price
from ..config import CONCURRENT_REQUESTS, REQUEST_TIMEOUT

logger = logging.getLogger("scraper")

GRAPHQL_URL = "https://web-gateway.dirk.nl/graphql"
IMAGE_BASE = "https://web-fileserver.dirk.nl/static-images/dirk/web/"
PRODUCT_URL = "https://www.dirk.nl/boodschappen/product/{}"

# Default store ID for pricing (storeId=1 works for standard prices)
DEFAULT_STORE_ID = 1

SEARCH_QUERY = """
query SearchProducts($search: String!, $limit: Int!) {
  searchProducts(search: $search, limit: $limit) {
    products {
      product {
        productId
        headerText
        subText
        brand
        packaging
        image
        department
        webgroup
        isWeightProduct
      }
      ranking
    }
  }
}
"""

PRICE_QUERY = """
query ProductAssortment($productId: Int!, $storeId: Int!) {
  productAssortment(productId: $productId, storeId: $storeId) {
    normalPrice
    offerPrice
    startDate
    endDate
  }
}
"""

DISCOVERY_QUERIES = [
    "melk", "kaas", "yoghurt", "boter", "eieren",
    "brood", "groente", "fruit", "aardappel", "tomaat", "komkommer",
    "vlees", "kip", "gehakt", "vis", "zalm", "worst",
    "pasta", "rijst", "saus", "soep", "olie",
    "koffie", "thee", "frisdrank", "bier", "wijn", "sap", "water",
    "chips", "chocolade", "koek", "snoep", "noten",
    "diepvries", "pizza", "ijs",
    "wasmiddel", "shampoo", "tandpasta", "luiers", "toiletpapier",
    "muesli", "pindakaas", "hagelslag", "jam",
    "mayonaise", "ketchup", "mosterd", "pesto",
    "appel", "banaan", "sinaasappel",
]


class DirkSource(BaseSource):
    store_id = "dirk"
    store_name = "Dirk"

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._sem = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async def _graphql(self, query: str, variables: dict = None) -> dict:
        async with self._sem:
            try:
                async with self._session.post(
                    GRAPHQL_URL,
                    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
                    json={"query": query, "variables": variables or {}},
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
                ) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    if "errors" in data:
                        logger.warning("Dirk GraphQL error: %s", data["errors"][0].get("message", ""))
                        return {}
                    return data.get("data", {})
            except Exception as e:
                logger.warning("Dirk request failed: %s", e)
                return {}

    async def _search(self, query: str, limit: int = 100) -> list[dict]:
        data = await self._graphql(SEARCH_QUERY, {"search": query, "limit": limit})
        products = data.get("searchProducts", {}).get("products", [])
        return [p["product"] for p in products if p.get("product")]

    async def _get_price(self, product_id: int) -> dict:
        data = await self._graphql(PRICE_QUERY, {
            "productId": product_id,
            "storeId": DEFAULT_STORE_ID,
        })
        return data.get("productAssortment") or {}

    async def fetch_all(self) -> list[ScrapedProduct]:
        async with aiohttp.ClientSession() as session:
            self._session = session

            seen: set = set()
            raw_products: list[dict] = []

            # Phase 1: discover products via search
            logger.info("Dirk: running %d discovery queries", len(DISCOVERY_QUERIES))
            for query in DISCOVERY_QUERIES:
                results = await self._search(query, limit=100)
                for raw in results:
                    pid = raw.get("productId")
                    if pid and pid not in seen:
                        seen.add(pid)
                        raw_products.append(raw)

            logger.info("Dirk: discovered %d unique products", len(raw_products))

            # Phase 2: fetch prices in batches
            logger.info("Dirk: fetching prices for %d products", len(raw_products))
            price_tasks = [self._get_price(p["productId"]) for p in raw_products]
            prices = await asyncio.gather(*price_tasks, return_exceptions=True)

            # Combine products with prices
            all_products = []
            for raw, price_data in zip(raw_products, prices):
                if isinstance(price_data, Exception):
                    price_data = {}
                p = self._parse_product(raw, price_data)
                if p:
                    all_products.append(p)

            logger.info(
                "Dirk: total %d products (%d deals)",
                len(all_products),
                sum(1 for p in all_products if p.is_deal),
            )

            self._session = None
            return all_products

    def _parse_product(self, raw: dict, price_data: dict) -> Optional[ScrapedProduct]:
        name = raw.get("headerText")
        product_id = raw.get("productId")
        if not name or not product_id:
            return None

        # Price
        normal_price = price_data.get("normalPrice") or 0
        offer_price = price_data.get("offerPrice") or 0
        is_deal = offer_price > 0 and offer_price < normal_price
        current_price = offer_price if is_deal else normal_price
        original_price = normal_price if is_deal else None

        if current_price <= 0:
            return None

        # Weight/volume from packaging
        packaging = raw.get("packaging") or ""
        weight_grams = parse_weight_grams(f"{name} {packaging}")
        volume_ml = parse_volume_ml(f"{name} {packaging}") if not weight_grams else None
        unit_price = calculate_unit_price(current_price, weight_grams, volume_ml)

        # Image
        image = raw.get("image") or ""
        image_url = f"{IMAGE_BASE}{image}" if image else None

        return ScrapedProduct(
            store_id=self.store_id,
            external_id=str(product_id),
            name=name,
            brand=raw.get("brand"),
            category=self._map_category(raw.get("department")),
            current_price=round(current_price, 2),
            original_price=round(original_price, 2) if original_price else None,
            unit_price=round(unit_price, 2) if unit_price else None,
            weight_grams=weight_grams,
            volume_ml=volume_ml,
            unit_size=packaging,
            is_deal=is_deal,
            deal_start=price_data.get("startDate"),
            deal_end=price_data.get("endDate"),
            url=PRODUCT_URL.format(product_id),
            image_url=image_url,
        )

    @staticmethod
    def _map_category(department: Optional[str]) -> Optional[str]:
        if not department:
            return None
        d = department.lower()
        if any(k in d for k in ("zuivel", "kaas")):
            return "zuivel"
        if any(k in d for k in ("vlees", "kip", "vega")):
            return "vlees"
        if any(k in d for k in ("groente", "fruit", "aardappel")):
            return "groente"
        if any(k in d for k in ("brood", "bakkerij")):
            return "brood"
        if any(k in d for k in ("drank", "bier", "wijn", "koffie", "thee")):
            return "dranken"
        if any(k in d for k in ("pasta", "rijst", "wereld")):
            return "pasta"
        if any(k in d for k in ("conserv", "saus", "soep")):
            return "conserven"
        if any(k in d for k in ("snoep", "chips", "koek")):
            return "snacks"
        if any(k in d for k in ("diepvries",)):
            return "diepvries"
        if any(k in d for k in ("huishoud", "schoonmaak")):
            return "huishouden"
        if any(k in d for k in ("drogist", "gezondheid")):
            return "drogist"
        if any(k in d for k in ("verzorging", "baby")):
            return "verzorging"
        return "overig"
