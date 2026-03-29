"""Albert Heijn source — crawls the full AH catalog via mobile API.

Discovery strategy: AH's search API supports browsing by taxonomy ID.
We fetch the taxonomy tree (all categories), then paginate through each
leaf category to discover every product. This is open-ended — we don't
need a predefined product list.

Fallback: if taxonomy endpoint is unavailable, we use broad search terms
covering all major grocery categories to maximize coverage.
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

AUTH_URL = "https://api.ah.nl/mobile-auth/v1/auth/token/anonymous"
SEARCH_URL = "https://api.ah.nl/mobile-services/product/search/v2"
TAXONOMY_URL = "https://api.ah.nl/mobile-services/v1/product-shelves/categories"
PRODUCT_URL = "https://www.ah.nl/producten/product/wi{}"

# Broad search terms covering all grocery categories — used as fallback
# if taxonomy crawl fails, or as supplementary discovery
DISCOVERY_QUERIES = [
    "zuivel", "melk", "kaas", "yoghurt", "boter",
    "brood", "bakkerij", "crackers", "beschuit",
    "groente", "fruit", "sla", "tomaat", "aardappel",
    "vlees", "kip", "gehakt", "biefstuk", "worst",
    "vis", "zalm", "garnaal", "tonijn",
    "pasta", "rijst", "noodles", "couscous",
    "saus", "ketchup", "mayonaise", "olie",
    "koffie", "thee", "cacao",
    "frisdrank", "sap", "water", "bier", "wijn",
    "chips", "noten", "koek", "chocolade", "snoep",
    "diepvries", "pizza", "ijsje",
    "ontbijt", "cereals", "muesli", "haver",
    "conserven", "bonen", "soep",
    "wasmiddel", "schoonmaak", "vaatwas",
    "shampoo", "tandpasta", "zeep",
    "luiers", "tissues", "toiletpapier",
    "huisdier", "kattenvoer", "hondenvoer",
]

HEADERS = {
    "User-Agent": "Appie/8.22.3",
    "x-application": "AHWEBSHOP",
    "Content-Type": "application/json",
}


class AHSource(BaseSource):
    store_id = "ah"
    store_name = "Albert Heijn"

    def __init__(self):
        self._token: Optional[str] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self._sem = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async def _get_token(self):
        """Get anonymous access token."""
        async with self._session.post(
            AUTH_URL,
            json={"clientId": "appie"},
            headers=HEADERS,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            self._token = data["access_token"]

    def _auth_headers(self) -> dict:
        return {**HEADERS, "Authorization": f"Bearer {self._token}"}

    async def _search_page(self, query: str = "", page: int = 0, size: int = 50, taxonomy_id: Optional[str] = None) -> dict:
        """Fetch one page of search results."""
        params = {"size": size, "page": page}
        if taxonomy_id:
            params["taxonomyId"] = taxonomy_id
        elif query:
            params["query"] = query
            params["sortOn"] = "RELEVANCE"

        async with self._sem:
            async with self._session.get(
                SEARCH_URL,
                params=params,
                headers=self._auth_headers(),
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
            ) as resp:
                if resp.status == 401:
                    await self._get_token()
                    return await self._search_page(query, page, size, taxonomy_id)
                resp.raise_for_status()
                return await resp.json()

    async def _fetch_taxonomy(self) -> list[dict]:
        """Fetch the AH category taxonomy tree."""
        try:
            async with self._session.get(
                TAXONOMY_URL,
                headers=self._auth_headers(),
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
            ) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception as e:
            logger.warning("AH: taxonomy fetch failed (%s), falling back to search queries", e)
            return []

    def _extract_leaf_ids(self, categories: list[dict]) -> list[str]:
        """Recursively extract leaf category IDs from taxonomy tree."""
        ids = []
        for cat in categories:
            children = cat.get("children", [])
            if children:
                ids.extend(self._extract_leaf_ids(children))
            else:
                cat_id = cat.get("id")
                if cat_id:
                    ids.append(str(cat_id))
        return ids

    async def _crawl_category(self, taxonomy_id: str, seen: set) -> list[ScrapedProduct]:
        """Paginate through all products in a category."""
        products = []
        page = 0
        while True:
            try:
                data = await self._search_page(taxonomy_id=taxonomy_id, page=page)
            except Exception as e:
                logger.warning("AH: category %s page %d failed: %s", taxonomy_id, page, e)
                break

            raw_products = data.get("products", [])
            if not raw_products:
                break

            for raw in raw_products:
                wid = raw.get("webshopId")
                if wid and wid not in seen:
                    seen.add(wid)
                    p = self._parse_product(raw)
                    if p:
                        products.append(p)

            page_info = data.get("page", {})
            total_pages = page_info.get("totalPages", 1)
            if page + 1 >= total_pages:
                break
            page += 1

        return products

    async def _crawl_query(self, query: str, seen: set) -> list[ScrapedProduct]:
        """Paginate through all results for a search query."""
        products = []
        page = 0
        while True:
            try:
                data = await self._search_page(query=query, page=page)
            except Exception as e:
                logger.warning("AH: query '%s' page %d failed: %s", query, page, e)
                break

            raw_products = data.get("products", [])
            if not raw_products:
                break

            for raw in raw_products:
                wid = raw.get("webshopId")
                if wid and wid not in seen:
                    seen.add(wid)
                    p = self._parse_product(raw)
                    if p:
                        products.append(p)

            page_info = data.get("page", {})
            total_pages = page_info.get("totalPages", 1)
            if page + 1 >= total_pages:
                break
            page += 1

        return products

    async def fetch_all(self) -> list[ScrapedProduct]:
        """Discover and fetch all AH products.

        Strategy:
        1. Try taxonomy crawl (all categories) for full coverage
        2. Supplement with search queries to catch anything taxonomy missed
        """
        async with aiohttp.ClientSession() as session:
            self._session = session
            await self._get_token()

            seen: set = set()
            all_products: list[ScrapedProduct] = []

            # Phase 1: taxonomy crawl
            taxonomy = await self._fetch_taxonomy()
            leaf_ids = self._extract_leaf_ids(taxonomy)

            if leaf_ids:
                logger.info("AH: crawling %d leaf categories", len(leaf_ids))
                tasks = [self._crawl_category(cid, seen) for cid in leaf_ids]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in results:
                    if isinstance(result, list):
                        all_products.extend(result)
                logger.info("AH: taxonomy crawl found %d products", len(all_products))

            # Phase 2: search queries for supplementary coverage
            logger.info("AH: running %d discovery queries", len(DISCOVERY_QUERIES))
            tasks = [self._crawl_query(q, seen) for q in DISCOVERY_QUERIES]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            supplement = 0
            for result in results:
                if isinstance(result, list):
                    all_products.extend(result)
                    supplement += len(result)

            logger.info(
                "AH: total %d products (%d from search, %d deals)",
                len(all_products),
                supplement,
                sum(1 for p in all_products if p.is_deal),
            )

            self._session = None
            return all_products

    def _parse_product(self, raw: dict) -> Optional[ScrapedProduct]:
        """Parse a raw AH API product dict into a ScrapedProduct."""
        title = raw.get("title")
        webshop_id = raw.get("webshopId")
        if not title or not webshop_id:
            return None

        is_bonus = bool(raw.get("isBonus"))

        # Price resolution
        original_price = raw.get("priceBeforeBonus")
        current_price = self._resolve_price(raw) if is_bonus else original_price

        if current_price is None and original_price is None:
            return None

        price = current_price or original_price
        if not is_bonus:
            original_price = None

        # Deal description
        deal_desc = None
        if is_bonus:
            labels = raw.get("discountLabels", [])
            if labels:
                deal_desc = labels[0].get("defaultDescription")
            if not deal_desc:
                deal_desc = "BONUS"

        # Weight, volume, unit price
        weight_text = (raw.get("salesUnitSize") or "") + " " + title
        weight_grams = parse_weight_grams(weight_text)
        volume_ml = parse_volume_ml(weight_text) if not weight_grams else None
        unit_price = calculate_unit_price(price, weight_grams, volume_ml)

        # Fallback: extract per-kg from unitPriceDescription
        if unit_price is None:
            upd = raw.get("unitPriceDescription") or ""
            match = re.search(r'per\s+kg\s+[€]\s*([\d,.]+)', upd)
            if match:
                unit_price = float(match.group(1).replace(',', '.'))

        # Category
        category = self._map_category(raw.get("mainCategory"))

        # Image
        images = raw.get("images", [])
        image_url = images[0]["url"] if images else None

        return ScrapedProduct(
            store_id=self.store_id,
            external_id=str(webshop_id),
            name=title,
            brand=raw.get("brand"),
            category=category,
            current_price=round(price, 2),
            original_price=round(original_price, 2) if original_price else None,
            unit_price=unit_price,
            weight_grams=weight_grams,
            volume_ml=volume_ml,
            unit_size=raw.get("salesUnitSize"),
            is_deal=is_bonus,
            deal_description=deal_desc,
            deal_start=raw.get("bonusStartDate"),
            deal_end=raw.get("bonusEndDate"),
            url=PRODUCT_URL.format(webshop_id),
            image_url=image_url,
        )

    @staticmethod
    def _resolve_price(raw: dict) -> Optional[float]:
        """Resolve the actual deal price from AH's discount structures."""
        labels = raw.get("discountLabels", [])
        if labels:
            label = labels[0]
            label_price = label.get("price")
            code = label.get("code", "")
            if label_price is not None and code != "DISCOUNT_WEIGHT":
                label_price = float(label_price)
                count = label.get("count", 1) or 1
                if code == "DISCOUNT_X_FOR_Y" and count > 1:
                    return round(label_price / count, 2)
                return label_price

        current = raw.get("currentPrice")
        if current is not None:
            return float(current)

        return raw.get("priceBeforeBonus")

    @staticmethod
    def _map_category(ah_category: Optional[str]) -> Optional[str]:
        """Map AH's mainCategory to our category IDs."""
        if not ah_category:
            return None
        mapping = {
            "Zuivel, plantaardig en eieren": "zuivel",
            "Kaas, vleeswaren en tapas": "zuivel",
            "Aardappel, groente en fruit": "groente",
            "Vlees, kip, vis en vega": "vlees",
            "Brood en gebak": "brood",
            "Ontbijtgranen en beleg": "brood",
            "Pasta, rijst en wereldkeuken": "pasta",
            "Soepen, sauzen en kruiden": "conserven",
            "Snoep, koek en chips": "snacks",
            "Frisdrank en sappen": "dranken",
            "Koffie en thee": "dranken",
            "Bier en wijn": "dranken",
            "Diepvries": "diepvries",
            "Bewuste voeding": "overig",
            "Drogisterij": "drogist",
            "Baby en kind": "verzorging",
            "Huishouden": "huishouden",
            "Huisdier": "overig",
        }
        return mapping.get(ah_category, "overig")
