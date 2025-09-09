# Placeholder for DNS enrichment (MX/SPF to hint SaaS)
from dataclasses import dataclass
from typing import Optional

@dataclass
class SaaSHint:
    provider: Optional[str]  # 'm365' | 'google' | None
    confidence: float

def get_saas_hint(domain: str) -> SaaSHint:
    # MVP stub: unknown provider
    return SaaSHint(provider=None, confidence=0.0)
