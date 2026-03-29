"""Lidl source — fetches products via their search API.

Lidl's storefront uses a search API at /q/api/search that returns full
product JSON with prices, images, brands, and packaging info.
No authentication required.

Discovery: search with broad grocery queries filtered to "Eten & drinken" category.
"""
import asyncio
import logging
import re
from typing import Optional

import aiohttp

from .base import BaseSource, ScrapedProduct
from ..pricing import parse_weight_grams, parse_volume_ml, calculate_unit_price
from ..config import CONCURRENT_REQUESTS, REQUEST_TIMEOUT

logger = logging.getLogger("scraper")

SEARCH_URL = "https://www.lidl.nl/q/api/search"
PRODUCT_URL = "https://www.lidl.nl{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
}

DISCOVERY_QUERIES = [
    "melk", "kaas", "yoghurt", "boter", "eieren",
    "brood", "groente", "fruit", "aardappel", "tomaat",
    "vlees", "kip", "gehakt", "vis", "zalm", "worst",
    "pasta", "rijst", "saus", "soep", "olie",
    "koffie", "thee", "frisdrank", "bier", "wijn", "sap", "water",
    "chips", "chocolade", "koek", "snoep", "noten",
    "diepvries", "pizza", "ijs",
    "wasmiddel", "shampoo", "tandpasta", "luiers", "toiletpapier",
    "muesli", "pindakaas", "hagelslag", "jam",
    "mayonaise", "ketchup", "pesto",
    "appel", "banaan", "sinaasappel",
    "ham", "salami", "rookworst",
    "meel", "suiker", "bloem",
]


class LidlSource(BaseSource):
    store_id = "lidl"
    store_name = "Lidl"

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._sem = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async def _search(self, query: str, offset: int = 0, limit: int = 48) -> dict:
        """Search for products in the Eten & drinken category."""
        async with self._sem:
            try:
                async with self._session.get(
                    SEARCH_URL,
                    params={
                        "assortment": "NL",
                        "locale": "nl_NL",
                        "version": "v2.0.0",
                        "q": query,
                        "category": "Eten & drinken",
                        "store": "1",
                        "offset": str(offset),
                        "limit": str(limit),
                    },
                    headers=HEADERS,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
                ) as resp:
                    if resp.status != 200:
                        return {}
                    return await resp.json()
            except Exception as e:
                logger.warning("Lidl: search '%s' failed: %s", query, e)
                return {}

    async def _crawl_query(self, query: str, seen: set) -> list[ScrapedProduct]:
        """Paginate through all results for a query."""
        products = []
        offset = 0
        limit = 48

        while True:
            data = await self._search(query, offset=offset, limit=limit)
            items = data.get("items", [])
            if not items:
                break

            for item in items:
                gd = item.get("gridbox", {}).get("data", {})
                item_id = gd.get("itemId") or gd.get("erpNumber")
                if item_id and item_id not in seen:
                    seen.add(item_id)
                    p = self._parse_product(gd)
                    if p:
                        products.append(p)

            num_found = data.get("numFound", 0)
            offset += limit
            if offset >= num_found:
                break

        return products

    async def fetch_all(self) -> list[ScrapedProduct]:
        async with aiohttp.ClientSession() as session:
            self._session = session
            seen: set = set()
            all_products: list[ScrapedProduct] = []

            logger.info("Lidl: running %d discovery queries", len(DISCOVERY_QUERIES))
            tasks = [self._crawl_query(q, seen) for q in DISCOVERY_QUERIES]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, list):
                    all_products.extend(result)

            logger.info(
                "Lidl: total %d products (%d deals)",
                len(all_products),
                sum(1 for p in all_products if p.is_deal),
            )
            self._session = None
            return all_products

    def _parse_product(self, gd: dict) -> Optional[ScrapedProduct]:
        """Parse a gridbox data dict into a ScrapedProduct."""
        keyfacts = gd.get("keyfacts", {})
        title = keyfacts.get("fullTitle") or gd.get("fullTitle")
        item_id = gd.get("itemId") or gd.get("erpNumber")
        if not title or not item_id:
            return None

        # Price
        price_data = gd.get("price", {})
        current_price = price_data.get("price", 0)
        old_price = price_data.get("oldPrice", 0)
        is_deal = old_price > 0 and old_price > current_price

        if current_price <= 0:
            return None

        # Packaging / weight
        packaging = price_data.get("packaging", {}).get("text", "")
        weight_grams = parse_weight_grams(f"{title} {packaging}")
        volume_ml = parse_volume_ml(f"{title} {packaging}") if not weight_grams else None
        unit_price = calculate_unit_price(current_price, weight_grams, volume_ml)

        # Brand
        brand_data = gd.get("brand", {})
        brand = brand_data.get("name") if brand_data.get("showBrand") else None

        # Image
        image_url = gd.get("image")

        # URL
        canonical = gd.get("canonicalUrl") or gd.get("canonicalPath") or ""
        url = PRODUCT_URL.format(canonical) if canonical else ""

        # Category
        won_cat = keyfacts.get("wonCategoryPrimary", "")
        category = self._map_category(won_cat)

        # Deal description
        discount = price_data.get("discount", {})
        deal_desc = discount.get("discountText") if is_deal else None

        return ScrapedProduct(
            store_id=self.store_id,
            external_id=str(item_id),
            name=title,
            brand=brand,
            category=category,
            current_price=round(current_price, 2),
            original_price=round(old_price, 2) if is_deal else None,
            unit_price=round(unit_price, 2) if unit_price else None,
            weight_grams=weight_grams,
            volume_ml=volume_ml,
            unit_size=packaging,
            is_deal=is_deal,
            deal_description=deal_desc,
            url=url,
            image_url=image_url,
        )

    @staticmethod
    def _map_category(won_category: str) -> Optional[str]:
        if not won_category:
            return None
        c = won_category.lower()
        if any(k in c for k in ("zuivel", "kaas", "melk", "yoghurt", "boter", "eier")):
            return "zuivel"
        if any(k in c for k in ("vlees", "kip", "gehakt", "worst")):
            return "vlees"
        if any(k in c for k in ("vis", "zalm", "garnaal")):
            return "vis"
        if any(k in c for k in ("groente", "fruit", "aardappel")):
            return "groente"
        if any(k in c for k in ("brood", "bakkerij", "gebak", "ontbijt", "beleg")):
            return "brood"
        if any(k in c for k in ("drank", "bier", "wijn", "sap", "water", "koffie", "thee")):
            return "dranken"
        if any(k in c for k in ("pasta", "rijst", "noodle")):
            return "pasta"
        if any(k in c for k in ("saus", "soep", "kruiden", "conserv", "olie")):
            return "conserven"
        if any(k in c for k in ("snoep", "chips", "koek", "chocola", "noten")):
            return "snacks"
        if any(k in c for k in ("diepvries", "ijs")):
            return "diepvries"
        if any(k in c for k in ("huishoud", "schoonmaak")):
            return "huishouden"
        if any(k in c for k in ("drogist",)):
            return "drogist"
        if any(k in c for k in ("verzorging", "baby")):
            return "verzorging"
        return "overig"
