"""Base class for store source adapters."""
from dataclasses import dataclass, field
from typing import Optional
import logging

logger = logging.getLogger("scraper")


@dataclass
class ScrapedProduct:
    """Unified product format — every source adapter outputs these."""
    store_id: str
    external_id: str              # store's own product ID
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    current_price: float = 0.0
    original_price: Optional[float] = None
    unit_price: Optional[float] = None
    weight_grams: Optional[int] = None
    volume_ml: Optional[int] = None
    unit_size: Optional[str] = None   # display string: "500g", "1.5L"
    is_deal: bool = False
    deal_description: Optional[str] = None
    deal_start: Optional[str] = None  # ISO date
    deal_end: Optional[str] = None    # ISO date
    url: Optional[str] = None
    image_url: Optional[str] = None


class BaseSource:
    """Base class for all store adapters.

    Each adapter must implement:
    - store_id: str
    - store_name: str
    - async fetch_all() -> list[ScrapedProduct]
    """
    store_id: str = ""
    store_name: str = ""

    async def fetch_all(self) -> list[ScrapedProduct]:
        raise NotImplementedError
