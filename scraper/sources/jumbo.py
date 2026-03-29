"""Jumbo source — crawls the full Jumbo catalog via mobile API.

Jumbo's mobile API (v17) requires no authentication.
Discovery: fetch all categories, paginate through each one.
Supplement with search queries for coverage.
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

BASE_URL = "https://mobileapi.jumbo.com/v17"
SEARCH_URL = f"{BASE_URL}/search"
CATEGORIES_URL = f"{BASE_URL}/categories"
PROMOTIONS_URL = f"{BASE_URL}/promotion-overview"
PRODUCT_PAGE_URL = "https://www.jumbo.com/producten/{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
}

# Broad queries for supplementary discovery
DISCOVERY_QUERIES = [
    "melk", "kaas", "yoghurt", "boter", "eieren",
    "brood", "groente", "fruit", "aardappel",
    "vlees", "kip", "gehakt", "vis", "zalm",
    "pasta", "rijst", "saus", "soep",
    "koffie", "thee", "frisdrank", "bier", "wijn", "sap", "water",
    "chips", "chocolade", "koek", "snoep", "noten",
    "diepvries", "pizza", "ijs",
    "wasmiddel", "schoonmaak", "shampoo", "tandpasta",
    "luiers", "toiletpapier",
]


class JumboSource(BaseSource):
    store_id = "jumbo"
    store_name = "Jumbo"

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._sem = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async def _get(self, url: str, params: dict = None) -> dict:
        """Make a GET request with rate limiting."""
        async with self._sem:
            async with self._session.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
            ) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def _fetch_categories(self) -> list[dict]:
        """Fetch all product categories."""
        try:
            data = await self._get(CATEGORIES_URL)
            return data.get("categories", {}).get("data", [])
        except Exception as e:
            logger.warning("Jumbo: categories fetch failed (%s)", e)
            return []

    def _extract_leaf_ids(self, categories: list[dict]) -> list[str]:
        """Extract leaf category IDs from Jumbo's category tree."""
        ids = []
        for cat in categories:
            children = cat.get("categories", {}).get("data", [])
            if children:
                ids.extend(self._extract_leaf_ids(children))
            else:
                cat_id = cat.get("id")
                if cat_id:
                    ids.append(cat_id)
        return ids

    async def _search_page(self, query: str = "", offset: int = 0, limit: int = 30) -> dict:
        """Fetch one page of search results."""
        params = {"offset": offset, "limit": limit}
        if query:
            params["q"] = query
        return await self._get(SEARCH_URL, params)

    async def _crawl_query(self, query: str, seen: set) -> list[ScrapedProduct]:
        """Paginate through all results for a query."""
        products = []
        offset = 0
        limit = 30

        while True:
            try:
                data = await self._search_page(query=query, offset=offset, limit=limit)
            except Exception as e:
                logger.warning("Jumbo: query '%s' offset %d failed: %s", query, offset, e)
                break

            raw_products = data.get("products", {}).get("data", [])
            if not raw_products:
                break

            for raw in raw_products:
                pid = raw.get("id")
                if pid and pid not in seen:
                    seen.add(pid)
                    p = self._parse_product(raw)
                    if p:
                        products.append(p)

            total = data.get("products", {}).get("total", 0)
            offset += limit
            if offset >= total:
                break

        return products

    async def _fetch_promotions(self) -> list[dict]:
        """Fetch current promotions."""
        try:
            data = await self._get(PROMOTIONS_URL)
            return data.get("tabs", [])
        except Exception as e:
            logger.warning("Jumbo: promotions fetch failed (%s)", e)
            return []

    async def fetch_all(self) -> list[ScrapedProduct]:
        """Discover and fetch all Jumbo products."""
        async with aiohttp.ClientSession() as session:
            self._session = session

            seen: set = set()
            all_products: list[ScrapedProduct] = []

            # Phase 1: category crawl
            categories = await self._fetch_categories()
            leaf_ids = self._extract_leaf_ids(categories)

            if leaf_ids:
                logger.info("Jumbo: crawling %d leaf categories", len(leaf_ids))
                tasks = [self._crawl_query(cid, seen) for cid in leaf_ids]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in results:
                    if isinstance(result, list):
                        all_products.extend(result)
                logger.info("Jumbo: category crawl found %d products", len(all_products))

            # Phase 2: search queries for supplementary coverage
            logger.info("Jumbo: running %d discovery queries", len(DISCOVERY_QUERIES))
            tasks = [self._crawl_query(q, seen) for q in DISCOVERY_QUERIES]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            supplement = 0
            for result in results:
                if isinstance(result, list):
                    all_products.extend(result)
                    supplement += len(result)

            logger.info(
                "Jumbo: total %d products (%d from search, %d deals)",
                len(all_products),
                supplement,
                sum(1 for p in all_products if p.is_deal),
            )

            self._session = None
            return all_products

    def _parse_product(self, raw: dict) -> Optional[ScrapedProduct]:
        """Parse a raw Jumbo API product into a ScrapedProduct."""
        title = raw.get("title")
        product_id = raw.get("id")
        if not title or not product_id:
            return None

        # Price
        prices = raw.get("prices", {})
        current_price = prices.get("price", {}).get("amount")
        if current_price is None:
            return None

        # Jumbo prices may be in cents or euros depending on version
        if current_price > 100:
            current_price = current_price / 100

        # Promotions
        promo_price = prices.get("promotionalPrice", {}).get("amount")
        original_price = None
        is_deal = False
        deal_desc = None

        if promo_price is not None:
            if promo_price > 100:
                promo_price = promo_price / 100
            original_price = current_price
            current_price = promo_price
            is_deal = True

        # Also check for sticker/badge promotions
        badge = raw.get("badge")
        if badge and not is_deal:
            is_deal = True
            deal_desc = badge.get("description")

        # Quantity/size
        qty = raw.get("quantityOptions", [{}])
        unit_size = None
        if qty:
            default = qty[0] if isinstance(qty, list) else qty
            unit = default.get("unit", "")
            amount = default.get("defaultAmount", 1)
            if unit:
                unit_size = f"{amount} {unit}" if amount != 1 else unit

        # Unit price from API
        unit_price_data = raw.get("unitPrice", {})
        unit_price = unit_price_data.get("price")
        if unit_price and unit_price > 100:
            unit_price = unit_price / 100

        # Weight/volume from title + unit_size
        weight_text = f"{title} {unit_size or ''}"
        weight_grams = parse_weight_grams(weight_text)
        volume_ml = parse_volume_ml(weight_text) if not weight_grams else None

        # Calculate unit price if not from API
        if unit_price is None:
            unit_price = calculate_unit_price(current_price, weight_grams, volume_ml)

        # Image
        image_info = raw.get("imageInfo", {})
        primary = image_info.get("primaryView", [])
        image_url = primary[0].get("url") if primary else None

        return ScrapedProduct(
            store_id=self.store_id,
            external_id=str(product_id),
            name=title,
            brand=raw.get("brand"),
            category=self._map_category(raw.get("topLevelCategory")),
            current_price=round(current_price, 2),
            original_price=round(original_price, 2) if original_price else None,
            unit_price=round(unit_price, 2) if unit_price else None,
            weight_grams=weight_grams,
            volume_ml=volume_ml,
            unit_size=unit_size,
            is_deal=is_deal,
            deal_description=deal_desc,
            url=PRODUCT_PAGE_URL.format(product_id),
            image_url=image_url,
        )

    @staticmethod
    def _map_category(jumbo_category: Optional[str]) -> Optional[str]:
        """Map Jumbo's topLevelCategory to our category IDs."""
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
