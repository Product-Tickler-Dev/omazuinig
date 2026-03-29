"""Product matching algorithm — matches products across stores.

Strategy (in priority order):
1. EAN match — exact barcode match (most reliable, but rarely available from APIs)
2. Brand + normalized name + weight — high confidence match
3. Normalized name + weight — for private labels within same brand family
4. Fuzzy name similarity + weight — catches spelling variations

Products are matched to canonical products in the database. When no match
is found, a new canonical product is created.

This module works with JSON files (offline) or database (online).
"""
import re
import logging
from dataclasses import dataclass
from typing import Optional
from difflib import SequenceMatcher

from .sources.base import ScrapedProduct

logger = logging.getLogger("scraper")


def normalize_name(name: str) -> str:
    """Normalize a product name for matching.

    - Lowercase
    - Remove store brand prefixes (AH, Jumbo, Lidl, etc.)
    - Remove common filler words
    - Collapse whitespace
    - Remove weight/size info (parsed separately)
    """
    n = name.lower().strip()

    # Remove store brand prefixes
    store_prefixes = [
        r'^ah\s+', r'^jumbo\s+', r'^lidl\s+', r'^aldi\s+', r'^plus\s+',
        r'^dirk\s+', r'^spar\s+', r'^hoogvliet\s+', r'^vomar\s+',
        r'^ah\s+excellent\s+', r'^ah\s+terra\s+', r'^ah\s+biologisch\s+',
        r'^jumbo\s+', r"^jumbo's\s+",
    ]
    for prefix in store_prefixes:
        n = re.sub(prefix, '', n)

    # Remove weight/size patterns (they're parsed separately)
    n = re.sub(r'\d+\s*x\s*\d+\s*(?:g|gram|ml|l|cl|kg|liter)\b', '', n)
    n = re.sub(r'\d+[.,]?\d*\s*(?:g|gram|ml|l|cl|kg|liter|stuks?|st)\b', '', n)
    n = re.sub(r'ca\.?\s*\d+', '', n)
    n = re.sub(r'\d+\s*(?:stuks?|st)\b', '', n)

    # Remove common filler words
    fillers = ['de', 'het', 'een', 'en', 'met', 'van', 'voor', 'in', 'per', 'stuk']
    words = n.split()
    words = [w for w in words if w not in fillers]

    # Collapse whitespace and strip
    return ' '.join(words).strip()


def normalize_brand(brand: Optional[str]) -> Optional[str]:
    """Normalize brand name."""
    if not brand:
        return None
    b = brand.lower().strip()

    # Map store brands to a common name
    store_brands = {
        'ah': 'huismerk', 'ah excellent': 'huismerk-premium',
        'ah biologisch': 'huismerk-bio', 'ah terra': 'huismerk-plant',
        'jumbo': 'huismerk', "jumbo's": 'huismerk',
        'lidl': 'huismerk', 'aldi': 'huismerk',
        'plus': 'huismerk', 'dirk': 'huismerk',
        'spar': 'huismerk', 'hoogvliet': 'huismerk',
        'vomar': 'huismerk',
    }

    return store_brands.get(b, b)


def name_similarity(name1: str, name2: str) -> float:
    """Calculate similarity between two normalized product names (0.0 - 1.0)."""
    return SequenceMatcher(None, name1, name2).ratio()


@dataclass
class MatchResult:
    """Result of a product matching attempt."""
    matched: bool
    confidence: float       # 0.0 - 1.0
    method: str             # 'ean', 'brand_name_weight', 'name_weight', 'fuzzy'
    canonical_id: Optional[str] = None  # UUID of matched canonical product


def match_product(product: ScrapedProduct, candidates: list[dict]) -> MatchResult:
    """Try to match a scraped product against a list of canonical product candidates.

    Each candidate is a dict with keys: id, name, brand, ean, weight_grams, volume_ml.

    Returns a MatchResult with the best match or no match.
    """
    norm_name = normalize_name(product.name)
    norm_brand = normalize_brand(product.brand)

    best_match: Optional[MatchResult] = None
    best_score = 0.0

    for candidate in candidates:
        # Method 1: EAN match (perfect match)
        if product.external_id and candidate.get("ean") and product.external_id == candidate["ean"]:
            return MatchResult(
                matched=True,
                confidence=1.0,
                method="ean",
                canonical_id=candidate["id"],
            )

        # Method 2: Brand + name + weight
        cand_norm_name = normalize_name(candidate.get("name", ""))
        cand_norm_brand = normalize_brand(candidate.get("brand"))

        # Weight must match (within 10% tolerance for ranges)
        weight_matches = _weight_matches(
            product.weight_grams, candidate.get("weight_grams"),
            product.volume_ml, candidate.get("volume_ml"),
        )

        if not weight_matches:
            continue

        # Brand match
        brand_matches = (
            norm_brand and cand_norm_brand and norm_brand == cand_norm_brand
        )

        # Name similarity
        sim = name_similarity(norm_name, cand_norm_name)

        if brand_matches and sim >= 0.85:
            score = 0.9 + (sim * 0.1)  # 0.9 - 1.0
            if score > best_score:
                best_score = score
                best_match = MatchResult(
                    matched=True,
                    confidence=round(score, 3),
                    method="brand_name_weight",
                    canonical_id=candidate["id"],
                )

        elif sim >= 0.80:
            score = 0.7 + (sim * 0.2)  # 0.7 - 0.9
            if score > best_score:
                best_score = score
                best_match = MatchResult(
                    matched=True,
                    confidence=round(score, 3),
                    method="name_weight",
                    canonical_id=candidate["id"],
                )

        elif sim >= 0.65:
            score = 0.4 + (sim * 0.3)  # 0.4 - 0.7
            if score > best_score:
                best_score = score
                best_match = MatchResult(
                    matched=True,
                    confidence=round(score, 3),
                    method="fuzzy",
                    canonical_id=candidate["id"],
                )

    return best_match or MatchResult(matched=False, confidence=0.0, method="none")


def _weight_matches(
    w1: Optional[int], w2: Optional[int],
    v1: Optional[int], v2: Optional[int],
    tolerance: float = 0.10,
) -> bool:
    """Check if two weights (or volumes) match within tolerance."""
    # If both have weight, compare
    if w1 and w2:
        return abs(w1 - w2) <= max(w1, w2) * tolerance

    # If both have volume, compare
    if v1 and v2:
        return abs(v1 - v2) <= max(v1, v2) * tolerance

    # If one has weight and other has volume, can't compare
    if (w1 and v2) or (v1 and w2):
        return False

    # If neither has weight/volume, can't use weight as filter
    # Return True to allow name-only matching (lower confidence)
    if not w1 and not w2 and not v1 and not v2:
        return True

    return False


def match_across_stores(products_by_store: dict[str, list[ScrapedProduct]]) -> list[dict]:
    """Match products across multiple stores, creating canonical groups.

    Input: { 'ah': [ScrapedProduct, ...], 'jumbo': [...], ... }
    Output: list of canonical product groups, each with store matches

    This is the offline version — works with JSON data, no database needed.
    """
    canonical_products: list[dict] = []
    canonical_id = 0

    for store_id, products in products_by_store.items():
        for product in products:
            # Try to match against existing canonical products
            result = match_product(product, canonical_products)

            if result.matched and result.confidence >= 0.7:
                # Add to existing canonical product
                for cp in canonical_products:
                    if cp["id"] == result.canonical_id:
                        cp["store_products"].append({
                            "store_id": store_id,
                            "name": product.name,
                            "price": product.current_price,
                            "original_price": product.original_price,
                            "unit_price": product.unit_price,
                            "is_deal": product.is_deal,
                            "match_confidence": result.confidence,
                            "match_method": result.method,
                        })
                        break
            else:
                # Create new canonical product
                canonical_id += 1
                canonical_products.append({
                    "id": str(canonical_id),
                    "name": product.name,
                    "brand": product.brand,
                    "ean": None,
                    "weight_grams": product.weight_grams,
                    "volume_ml": product.volume_ml,
                    "category": product.category,
                    "store_products": [{
                        "store_id": store_id,
                        "name": product.name,
                        "price": product.current_price,
                        "original_price": product.original_price,
                        "unit_price": product.unit_price,
                        "is_deal": product.is_deal,
                        "match_confidence": 1.0,
                        "match_method": "origin",
                    }],
                })

    # Stats
    multi_store = sum(1 for cp in canonical_products if len(cp["store_products"]) > 1)
    logger.info(
        "Matching complete: %d canonical products, %d matched across stores",
        len(canonical_products), multi_store,
    )

    return canonical_products
