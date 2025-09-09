# Placeholder for branding enrichment (logo fetch, color extraction)
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class BrandInfo:
    company_name: Optional[str]
    logo_url: Optional[str]
    primary_color: Optional[str]
    confidence: float

def get_brand_info(domain: str) -> BrandInfo:
    # MVP stub: return neutral branding with low confidence
    return BrandInfo(company_name=None, logo_url=None, primary_color=None, confidence=0.0)
