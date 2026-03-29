"""Export scraped data to frontend-compatible TypeScript files.

Reads JSON from scraper/data/, converts to the Product/Deal format the
SvelteKit app expects, and writes directly to app/src/lib/data/.

Usage:
    python -m scraper.export_to_frontend
    python -m scraper.export_to_frontend --max-products 500
"""
import json
import logging
import re
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger("scraper")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

SCRAPER_DATA = Path(__file__).parent / "data"
FRONTEND_DATA = Path(__file__).parent.parent / "app" / "src" / "lib" / "data"


def load_latest_scrape(store_id: str) -> dict | None:
    """Load the most recent scrape file for a store."""
    files = sorted(SCRAPER_DATA.glob(f"{store_id}_*.json"), reverse=True)
    if not files:
        logger.warning("No scrape data found for %s", store_id)
        return None
    logger.info("Loading %s", files[0].name)
    return json.loads(files[0].read_text(encoding="utf-8"))


def recategorize(product: dict) -> str:
    """Re-categorize a product based on its name when the original category is 'overig'.

    This is a stopgap until we have a fresh scrape with the fixed AH category mapper.
    """
    if product.get("category") and product["category"] != "overig":
        return product["category"]

    name = (product.get("name") or "").lower()
    brand = (product.get("brand") or "").lower()
    combined = f"{name} {brand}"

    if any(k in combined for k in ("melk", "yoghurt", "kwark", "vla", "room", "boter", "kaas", "ei ", "eieren", "zuivel", "slagroom", "crème", "alpro", "plakken", "geraspte", "belegen", "jong ", "oud ")):
        return "zuivel"
    if any(k in combined for k in ("kip", "kipfilet", "gehakt", "biefstuk", "worst", "ham", "bacon", "vlees", "filet", "schnitzel", "spare", "karbonade", "scharrel", "drumstick", "rollade", "speklap", "slavink", "rookworst", "plantaardig", "vega", "terra", "tofu", "tempeh")):
        return "vlees"
    if any(k in combined for k in ("zalm", "tonijn", "garnaal", "vis", "haring", "makreel", "kabeljauw", "pangasius", "forel", "mosselen", "kibbeling")):
        return "vis"
    if any(k in combined for k in ("brood", "croissant", "beschuit", "cracker", "toast", "stokbrood", "volkoren", "spelt", "rogge", "bagel", "wrap", "tortilla", "pita")):
        return "brood"
    if any(k in combined for k in ("hagelslag", "pindakaas", "jam", "stroop", "beleg", "muesli", "cereals", "ontbijt", "haver", "granola", "cornflakes")):
        return "brood"
    if any(k in combined for k in ("groente", "tomaat", "sla", "komkommer", "paprika", "ui ", "wortel", "aardappel", "champignon", "broccoli", "bloemkool", "courgette", "spinazie", "salade")):
        return "groente"
    if any(k in combined for k in ("appel", "banaan", "peer", "aardbei", "sinaasappel", "druif", "mango", "ananas", "fruit", "avocado", "citroen", "kiwi")):
        return "groente"
    if any(k in combined for k in ("pasta", "spaghetti", "macaroni", "penne", "rijst", "noodle", "couscous", "lasagne")):
        return "pasta"
    if any(k in combined for k in ("saus", "ketchup", "mayonaise", "mosterd", "olie", "azijn", "bouillon", "kruiden", "peper", "zout", "pesto", "curry", "sambal")):
        return "conserven"
    if any(k in combined for k in ("soep", "blik", "conserv", "bonen", "mais", "tomatenpuree", "passata", "kokosmelk")):
        return "conserven"
    if any(k in combined for k in ("bier", "wijn", "pils", "radler", "prosecco")):
        return "dranken"
    if any(k in combined for k in ("cola", "fanta", "sap", "water", "limonade", "ice tea", "frisdrank", "energy", "tonic", "cassis")):
        return "dranken"
    if any(k in combined for k in ("koffie", "thee", "cacao", "cappuccino", "espresso", "capsule", "senseo", "nespresso")):
        return "dranken"
    if any(k in name for k in ("chips", "noten", "chocola", "koek", "snoep", "drop", "pepernoot", "speculaas", "reep")):
        return "snacks"
    if any(k in name for k in ("ijs", "pizza", "diepvries", "bami", "nasi")):
        return "diepvries"

    return "overig"


def select_products(all_products: list[dict], max_products: int = 300) -> list[dict]:
    """Select a diverse set of products for the frontend.

    Prioritizes:
    1. Products with deals (most interesting to users)
    2. Products with weight/unit_price (most useful for comparison)
    3. Spread across categories
    4. Recognizable brands over unknown ones
    """
    # Score each product
    scored = []
    for p in all_products:
        if p["current_price"] <= 0:
            continue
        score = 0
        if p.get("is_deal"):
            score += 50
        if p.get("weight_grams") or p.get("volume_ml"):
            score += 20
        if p.get("unit_price"):
            score += 10
        if p.get("brand") and p["brand"].lower() not in ("ah", "ah excellent", "ah biologisch", "ah terra"):
            score += 15  # Known brands are more recognizable
        if p.get("image_url"):
            score += 5
        scored.append((score, p))

    # Sort by score descending
    scored.sort(key=lambda x: -x[0])

    # Take top products, but ensure diversity
    selected = []
    category_counts: dict[str, int] = defaultdict(int)
    seen_names: set = set()  # Deduplicate similar product names
    max_per_category = max_products // 8

    for score, p in scored:
        cat = p.get("category") or "overig"

        # Skip if too many from this category
        if category_counts[cat] >= max_per_category and len(selected) > max_products // 2:
            continue

        # Deduplicate: skip products with very similar names
        # Use first 3 words as key to catch product families
        words = p["name"].lower().split()[:3]
        name_key = " ".join(words)
        if name_key in seen_names:
            continue
        seen_names.add(name_key)

        selected.append(p)
        category_counts[cat] += 1
        if len(selected) >= max_products:
            break

    return selected


def build_frontend_data(stores_data: dict[str, list[dict]], max_products: int = 300):
    """Build frontend-compatible products and deals from scraped data.

    When we have multiple stores, products with matching names+brands get
    merged into one Product with prices from each store.
    """
    # For now: single store, each scraped product becomes a frontend Product
    all_scraped = []
    for store_id, products in stores_data.items():
        for p in products:
            p["_store_id"] = store_id
            p["category"] = recategorize(p)
            all_scraped.append(p)

    selected = select_products(all_scraped, max_products)

    frontend_products = []
    frontend_deals = []

    for i, p in enumerate(selected, start=1):
        store_id = p["_store_id"]
        price = p["current_price"]

        # Build prices dict — only the store we have data from
        prices = {store_id: price}

        # Clean up the display name
        name = p["name"]
        # Remove "AH " prefix for cleaner display
        name = re.sub(r'^AH\s+(?:Excellent\s+|Biologisch\s+|Terra\s+)?', '', name)

        # Use smaller image rendition for performance
        img_url = p.get("image_url") or ""
        if img_url and "800x800" in img_url:
            img_url = img_url.replace("800x800", "200x200")

        frontend_products.append({
            "id": i,
            "name": name,
            "brand": p.get("brand") or "Huismerk",
            "size": p.get("unit_size") or "",
            "category": p.get("category") or "overig",
            "image": "",
            "imageUrl": img_url,
            "prices": prices,
        })

        # Create deal entry if it's a deal
        if p.get("is_deal") and p.get("original_price") and p["original_price"] > price:
            discount = round((1 - price / p["original_price"]) * 100)
            frontend_deals.append({
                "productId": i,
                "store": store_id,
                "oldPrice": p["original_price"],
                "newPrice": price,
                "discount": discount,
            })

    # Sort deals by discount descending
    frontend_deals.sort(key=lambda d: -d["discount"])

    return frontend_products, frontend_deals


def write_products_ts(products: list[dict]):
    """Write products.ts file."""
    lines = ["import type { Product } from './types';", "", "export const PRODUCTS: Product[] = ["]
    for p in products:
        prices_str = ", ".join(f"{k}: {v}" for k, v in p["prices"].items())
        # Escape single quotes in names
        name = p["name"].replace("'", "\\'")
        brand = p["brand"].replace("'", "\\'")
        size = p["size"].replace("'", "\\'")
        img_url = p.get("imageUrl", "").replace("'", "\\'")
        lines.append(
            f"  {{ id: {p['id']}, name: '{name}', brand: '{brand}', "
            f"size: '{size}', category: '{p['category']}', "
            f"image: '', imageUrl: '{img_url}', prices: {{ {prices_str} }} }},"
        )
    lines.append("];")
    lines.append("")
    lines.append("export function getProduct(id: number): Product | undefined {")
    lines.append("  return PRODUCTS.find(p => p.id === id);")
    lines.append("}")
    lines.append("")

    path = FRONTEND_DATA / "products.ts"
    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote %d products to %s", len(products), path.name)


def write_deals_ts(deals: list[dict]):
    """Write deals.ts file."""
    lines = ["import type { Deal } from './types';", "", "export const DEALS: Deal[] = ["]
    for d in deals:
        lines.append(
            f"  {{ productId: {d['productId']}, store: '{d['store']}', "
            f"oldPrice: {d['oldPrice']}, newPrice: {d['newPrice']}, "
            f"discount: {d['discount']} }},"
        )
    lines.append("];")
    lines.append("")

    path = FRONTEND_DATA / "deals.ts"
    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote %d deals to %s", len(deals), path.name)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Export scraped data to frontend")
    parser.add_argument("--max-products", type=int, default=300, help="Max products to export")
    args = parser.parse_args()

    # Load all available store data
    stores_data = {}
    for store_id in ["ah", "jumbo", "lidl", "aldi", "plus", "dirk"]:
        data = load_latest_scrape(store_id)
        if data and data.get("products"):
            stores_data[store_id] = data["products"]
            logger.info("  %s: %d products loaded", store_id, len(data["products"]))

    if not stores_data:
        logger.error("No scrape data found! Run the scraper first: python -m scraper --store ah")
        return

    products, deals = build_frontend_data(stores_data, max_products=args.max_products)

    write_products_ts(products)
    write_deals_ts(deals)

    # Stats
    cats = defaultdict(int)
    for p in products:
        cats[p["category"]] += 1
    logger.info("Category distribution: %s", dict(sorted(cats.items(), key=lambda x: -x[1])))
    logger.info("Done! Run 'npm run dev' in app/ to see the real data.")


if __name__ == "__main__":
    main()
