"""DekaMarkt source — same GraphQL API pattern as Dirk (same parent: Detailresult).

API: web-deka-gateway.dekamarkt.nl/graphql
Products: searchProducts works without auth
Prices: productAssortment needs a storeId — currently returns null without auth
         so prices are fetched but may be unavailable. Products still valuable
         for matching and catalog completeness.
"""
import asyncio
import logging
from typing import Optional

import aiohttp

from .base import BaseSource, ScrapedProduct
from ..pricing import parse_weight_grams, parse_volume_ml, calculate_unit_price
from ..config import CONCURRENT_REQUESTS, REQUEST_TIMEOUT

logger = logging.getLogger("scraper")

GRAPHQL_URL = "https://web-deka-gateway.dekamarkt.nl/graphql"
IMAGE_BASE = "https://web-fileserver.dirk.nl/static-images/deka/web/"
PRODUCT_URL = "https://www.dekamarkt.nl/boodschappen/product/{}"

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
      }
    }
  }
}
"""

# Same discovery queries as Dirk
DISCOVERY_QUERIES = [
    "melk", "kaas", "yoghurt", "boter", "eieren",
    "brood", "groente", "fruit", "aardappel", "tomaat",
    "vlees", "kip", "gehakt", "vis", "zalm", "worst",
    "pasta", "rijst", "saus", "soep", "olie",
    "koffie", "thee", "frisdrank", "bier", "wijn", "sap", "water",
    "chips", "chocolade", "koek", "snoep", "noten",
    "diepvries", "pizza", "ijs",
    "wasmiddel", "shampoo", "tandpasta", "luiers", "toiletpapier",
    "muesli", "pindakaas", "hagelslag",
    "mayonaise", "ketchup", "pesto",
    "appel", "banaan",
]


class DekaMarktSource(BaseSource):
    store_id = "dekamarkt"
    store_name = "DekaMarkt"

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
                        return {}
                    return data.get("data", {})
            except Exception as e:
                logger.warning("DekaMarkt request failed: %s", e)
                return {}

    async def _search(self, query: str, limit: int = 100) -> list[dict]:
        data = await self._graphql(SEARCH_QUERY, {"search": query, "limit": limit})
        products = data.get("searchProducts", {}).get("products", [])
        return [p["product"] for p in products if p.get("product")]

    async def fetch_all(self) -> list[ScrapedProduct]:
        async with aiohttp.ClientSession() as session:
            self._session = session
            seen: set = set()
            all_products: list[ScrapedProduct] = []

            logger.info("DekaMarkt: running %d discovery queries", len(DISCOVERY_QUERIES))
            for query in DISCOVERY_QUERIES:
                results = await self._search(query, limit=100)
                for raw in results:
                    pid = raw.get("productId")
                    if pid and pid not in seen:
                        seen.add(pid)
                        p = self._parse_product(raw)
                        if p:
                            all_products.append(p)

            logger.info("DekaMarkt: total %d products", len(all_products))
            self._session = None
            return all_products

    def _parse_product(self, raw: dict) -> Optional[ScrapedProduct]:
        name = raw.get("headerText")
        product_id = raw.get("productId")
        if not name or not product_id:
            return None

        packaging = raw.get("packaging") or ""
        weight_grams = parse_weight_grams(f"{name} {packaging}")
        volume_ml = parse_volume_ml(f"{name} {packaging}") if not weight_grams else None

        image = raw.get("image") or ""
        image_url = f"{IMAGE_BASE}{image}" if image else None

        return ScrapedProduct(
            store_id=self.store_id,
            external_id=str(product_id),
            name=name,
            brand=raw.get("brand"),
            category=self._map_category(raw.get("department")),
            current_price=0.0,  # Prices unavailable without store auth
            unit_size=packaging,
            weight_grams=weight_grams,
            volume_ml=volume_ml,
            url=PRODUCT_URL.format(product_id),
            image_url=image_url,
        )

    @staticmethod
    def _map_category(department: Optional[str]) -> Optional[str]:
        if not department:
            return None
        d = department.lower()
        if any(k in d for k in ("zuivel", "kaas")): return "zuivel"
        if any(k in d for k in ("vlees", "kip", "vega")): return "vlees"
        if any(k in d for k in ("groente", "fruit")): return "groente"
        if any(k in d for k in ("brood", "bakkerij")): return "brood"
        if any(k in d for k in ("drank", "bier", "wijn", "koffie", "thee")): return "dranken"
        if any(k in d for k in ("pasta", "rijst")): return "pasta"
        if any(k in d for k in ("conserv", "saus", "soep")): return "conserven"
        if any(k in d for k in ("snoep", "chips", "koek")): return "snacks"
        if any(k in d for k in ("diepvries",)): return "diepvries"
        if any(k in d for k in ("huishoud",)): return "huishouden"
        if any(k in d for k in ("drogist",)): return "drogist"
        if any(k in d for k in ("verzorging", "baby")): return "verzorging"
        return "overig"
