"""Weight parsing and unit price calculation.

Adapted from C:\\shopper\\shopper\\pricing.py — handles Dutch grocery
weight formats: grams, kg, ranges, multipacks, liters.
"""
import re
from typing import Optional


def parse_weight_grams(text: str) -> Optional[int]:
    """Extract weight in grams from product text. Returns None if unparseable."""
    text = text.lower()

    # Multiplied grams: "2 x 100 gram", "3x200g"
    mult_match = re.search(r'(\d+)\s*x\s*(\d+)\s*g(?:ram(?:s)?)?\b', text)
    if mult_match:
        return int(mult_match.group(1)) * int(mult_match.group(2))

    # Gram range: "180 - 220 gram", "500 – 600 g" (midpoint)
    range_g = re.search(r'(\d+)\s*[-–—]\s*(\d+)\s*g(?:ram(?:s)?)?\b', text)
    if range_g:
        lo, hi = int(range_g.group(1)), int(range_g.group(2))
        return (lo + hi) // 2

    # Kg range: "1.5 - 2 kg" (midpoint)
    range_kg = re.search(r'(\d+[.,]?\d*)\s*[-–—]\s*(\d+[.,]?\d*)\s*kg\b', text)
    if range_kg:
        lo = float(range_kg.group(1).replace(',', '.'))
        hi = float(range_kg.group(2).replace(',', '.'))
        return int((lo + hi) / 2 * 1000)

    # Kg: "1kg", "1.5kg", "1,5 kg"
    kg = re.search(r'(\d+[.,]?\d*)\s*kg\b', text)
    if kg:
        return int(float(kg.group(1).replace(',', '.')) * 1000)

    # Grams: "500g", "500 gram"
    g = re.search(r'(\d+)\s*g(?:ram(?:s)?)?\b', text)
    if g:
        return int(g.group(1))

    return None


def parse_volume_ml(text: str) -> Optional[int]:
    """Extract volume in ml from product text."""
    text = text.lower()

    # Multiplied: "6 x 330 ml"
    mult = re.search(r'(\d+)\s*x\s*(\d+)\s*ml\b', text)
    if mult:
        return int(mult.group(1)) * int(mult.group(2))

    # Liters: "1.5l", "1,5 liter", "2 l"
    liter = re.search(r'(\d+[.,]?\d*)\s*l(?:iter)?\b', text)
    if liter:
        return int(float(liter.group(1).replace(',', '.')) * 1000)

    # Milliliters: "330ml", "500 ml"
    ml = re.search(r'(\d+)\s*ml\b', text)
    if ml:
        return int(ml.group(1))

    return None


def calculate_unit_price(price: float, weight_grams: Optional[int] = None, volume_ml: Optional[int] = None) -> Optional[float]:
    """Calculate EUR per kg (weight) or EUR per L (volume). Returns None if unknown."""
    if weight_grams and weight_grams > 0:
        return round(price / weight_grams * 1000, 2)
    if volume_ml and volume_ml > 0:
        return round(price / volume_ml * 1000, 2)
    return None
