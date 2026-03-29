"""Plus source — fetches products via their OutSystems API.

Plus uses OutSystems with a session-based auth flow:
1. GET any page to obtain Incapsula WAF session cookies
2. POST to the DataAction endpoint with product search parameters

The API returns paginated product data (12 per page) with full details
including SKU, brand, name, prices, images, categories, and packaging.
"""
import asyncio
import logging
from typing import Optional

import aiohttp

from .base import BaseSource, ScrapedProduct
from ..pricing import parse_weight_grams, parse_volume_ml, calculate_unit_price
from ..config import REQUEST_TIMEOUT

logger = logging.getLogger("scraper")

BASE_URL = "https://www.plus.nl"
PRODUCT_API = f"{BASE_URL}/screenservices/ECP_Composition_CW/ProductLists/PLP_Content/DataActionGetProductListAndCategoryInfo"
PRODUCT_URL = f"{BASE_URL}/producten/{{}}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
}

# Module version — may need updating if Plus deploys a new version
MODULE_VERSION = "rTx3FW_c3z_FB_rCjX8EEQ"
API_VERSION = "cafT+CKg7ockKx+9Kx_BsQ"

# Category URLs for full catalog crawl
CATEGORY_URLS = [
    "zuivel-eieren-boter",
    "kaas-vleeswaren",
    "vlees-kip-vis-vega",
    "aardappelen-groente-fruit",
    "brood-bakkerij",
    "ontbijt-granen-beleg",
    "pasta-rijst-wereldkeuken",
    "soepen-sauzen-kruiden-olie",
    "snoep-koek-chips",
    "frisdrank-sap-water",
    "koffie-thee",
    "bier-wijn-sterke-drank",
    "diepvries",
    "drogisterij-baby",
    "huishouden-huisdier",
]

SEARCH_QUERIES = [
    "melk", "kaas", "yoghurt", "brood", "vlees", "kip", "gehakt",
    "groente", "fruit", "pasta", "rijst", "saus", "soep",
    "koffie", "thee", "bier", "wijn", "chips", "chocolade",
    "wasmiddel", "shampoo",
]


class PlusSource(BaseSource):
    store_id = "plus"
    store_name = "PLUS"

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        # Conservative — Plus has WAF protection
        self._sem = asyncio.Semaphore(3)

    async def _init_session(self):
        """Get WAF session cookies by visiting a page."""
        async with self._session.get(
            f"{BASE_URL}/producten",
            headers=HEADERS,
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
        ) as resp:
            logger.info("Plus: session init %d, cookies: %d", resp.status, len(self._session.cookie_jar))

    async def _fetch_page(self, search_term: str = "", category_url: str = "", page: int = 1) -> dict:
        """Fetch one page of products."""
        body = {
            "versionInfo": {
                "moduleVersion": MODULE_VERSION,
                "apiVersion": API_VERSION,
            },
            "viewName": "MainFlow.SearchPage" if search_term else "MainFlow.ProductListPage",
            "screenData": {
                "variables": {
                    "AppliedFiltersList": {"List": []},
                    "LocalCategoryID": 0,
                    "IsLoadingMore": page > 1,
                    "IsFirstDataFetched": page > 1,
                    "IsShowData": True,
                    "StoreNumber": 0,
                    "ProductList_All": {"List": []},
                    "TotalCount": 0,
                    "SearchTerm": search_term,
                    "PageNumber": page,
                }
            },
            "inputParameters": {
                "SearchTerm": search_term,
                "CategoryURL": category_url,
                "PageNumber": page,
            },
        }

        async with self._sem:
            try:
                async with self._session.post(
                    PRODUCT_API,
                    json=body,
                    headers={
                        **HEADERS,
                        "Content-Type": "application/json; charset=UTF-8",
                        "Accept": "application/json",
                        "X-CSRFToken": "",
                        "OutSystems-locale": "nl-NL",
                    },
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
                ) as resp:
                    if resp.status != 200:
                        logger.warning("Plus: page %d returned %d", page, resp.status)
                        return {}
                    return await resp.json()
            except Exception as e:
                logger.warning("Plus: request failed: %s", e)
                return {}

    async def _crawl_category(self, category_url: str, seen: set) -> list[ScrapedProduct]:
        """Paginate through all products in a category."""
        products = []
        page = 1

        while True:
            data = await self._fetch_page(category_url=category_url, page=page)
            response_data = data.get("data", {})

            product_list = self._extract_products(response_data)
            if not product_list:
                break

            for raw in product_list:
                plp = raw.get("PLP_Str", {})
                sku = plp.get("SKU")
                if sku and sku not in seen:
                    seen.add(sku)
                    p = self._parse_product(plp)
                    if p:
                        products.append(p)

            total_pages = response_data.get("TotalPages", 1)
            if page >= total_pages or page >= 50:  # Safety cap
                break
            page += 1

            # Be polite
            await asyncio.sleep(0.5)

        return products

    async def _crawl_search(self, query: str, seen: set) -> list[ScrapedProduct]:
        """Search and paginate results."""
        products = []
        page = 1

        while True:
            data = await self._fetch_page(search_term=query, page=page)
            response_data = data.get("data", {})

            product_list = self._extract_products(response_data)
            if not product_list:
                break

            for raw in product_list:
                plp = raw.get("PLP_Str", {})
                sku = plp.get("SKU")
                if sku and sku not in seen:
                    seen.add(sku)
                    p = self._parse_product(plp)
                    if p:
                        products.append(p)

            total_pages = response_data.get("TotalPages", 1)
            if page >= total_pages or page >= 20:
                break
            page += 1
            await asyncio.sleep(0.5)

        return products

    def _extract_products(self, data: dict) -> list:
        """Find the product list in the response data."""
        # Products are nested: data.ProductList.List or similar
        def find_list(obj):
            if isinstance(obj, dict):
                if "ProductList" in obj:
                    pl = obj["ProductList"]
                    if isinstance(pl, dict) and "List" in pl:
                        return pl["List"]
                for v in obj.values():
                    result = find_list(v)
                    if result:
                        return result
            return None

        return find_list(data) or []

    async def fetch_all(self) -> list[ScrapedProduct]:
        async with aiohttp.ClientSession() as session:
            self._session = session
            await self._init_session()

            seen: set = set()
            all_products: list[ScrapedProduct] = []

            # Phase 1: category crawl
            logger.info("Plus: crawling %d categories", len(CATEGORY_URLS))
            for cat_url in CATEGORY_URLS:
                products = await self._crawl_category(cat_url, seen)
                all_products.extend(products)
                logger.info("Plus: category '%s' → %d products", cat_url, len(products))

            # Phase 2: supplementary search
            logger.info("Plus: running %d search queries", len(SEARCH_QUERIES))
            for query in SEARCH_QUERIES:
                products = await self._crawl_search(query, seen)
                all_products.extend(products)

            logger.info(
                "Plus: total %d products (%d deals)",
                len(all_products),
                sum(1 for p in all_products if p.is_deal),
            )
            self._session = None
            return all_products

    def _parse_product(self, plp: dict) -> Optional[ScrapedProduct]:
        """Parse a PLP_Str dict into a ScrapedProduct."""
        name = plp.get("Name")
        sku = plp.get("SKU")
        if not name or not sku:
            return None

        # Price
        original_price_str = plp.get("OriginalPrice", "0")
        new_price_str = plp.get("NewPrice", "0")
        try:
            original_price = float(original_price_str)
            new_price = float(new_price_str)
        except (ValueError, TypeError):
            original_price = 0
            new_price = 0

        is_deal = new_price > 0 and new_price < original_price
        current_price = new_price if is_deal else original_price

        if current_price <= 0:
            return None

        # Weight/volume from subtitle
        subtitle = plp.get("Product_Subtitle", "")
        weight_text = f"{name} {subtitle}"
        weight_grams = parse_weight_grams(weight_text)
        volume_ml = parse_volume_ml(weight_text) if not weight_grams else None
        unit_price = calculate_unit_price(current_price, weight_grams, volume_ml)

        # Category
        categories = plp.get("Categories", {}).get("List", [])
        top_category = categories[0].get("Name", "") if categories else ""
        category = self._map_category(top_category)

        # Deal info
        deal_desc = plp.get("PromotionLabel") or plp.get("PromotionBasedLabel") or None
        deal_start = plp.get("PromotionStartDate")
        deal_end = plp.get("PromotionEndDate")
        if deal_start == "1900-01-01":
            deal_start = None
            deal_end = None

        return ScrapedProduct(
            store_id=self.store_id,
            external_id=sku,
            name=name,
            brand=plp.get("Brand"),
            category=category,
            current_price=round(current_price, 2),
            original_price=round(original_price, 2) if is_deal else None,
            unit_price=round(unit_price, 2) if unit_price else None,
            weight_grams=weight_grams,
            volume_ml=volume_ml,
            unit_size=subtitle,
            is_deal=is_deal,
            deal_description=deal_desc,
            deal_start=deal_start,
            deal_end=deal_end,
            url=PRODUCT_URL.format(plp.get("Slug", sku)),
            image_url=plp.get("ImageURL"),
        )

    @staticmethod
    def _map_category(plus_category: str) -> Optional[str]:
        if not plus_category:
            return None
        c = plus_category.lower()
        if any(k in c for k in ("zuivel", "eieren", "boter")):
            return "zuivel"
        if any(k in c for k in ("kaas", "vleeswaren")):
            return "zuivel"
        if any(k in c for k in ("vlees", "kip", "vis", "vega")):
            return "vlees"
        if any(k in c for k in ("groente", "fruit", "aardappel")):
            return "groente"
        if any(k in c for k in ("brood", "bakkerij")):
            return "brood"
        if any(k in c for k in ("ontbijt", "granen", "beleg")):
            return "brood"
        if any(k in c for k in ("pasta", "rijst", "wereld")):
            return "pasta"
        if any(k in c for k in ("soep", "saus", "kruiden", "olie")):
            return "conserven"
        if any(k in c for k in ("snoep", "koek", "chips")):
            return "snacks"
        if any(k in c for k in ("frisdrank", "sap", "water")):
            return "dranken"
        if any(k in c for k in ("koffie", "thee")):
            return "dranken"
        if any(k in c for k in ("bier", "wijn", "drank")):
            return "dranken"
        if any(k in c for k in ("diepvries",)):
            return "diepvries"
        if any(k in c for k in ("drogisterij", "baby")):
            return "drogist"
        if any(k in c for k in ("huishouden", "huisdier")):
            return "huishouden"
        return "overig"
