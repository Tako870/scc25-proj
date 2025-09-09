def is_allowed_domain(domain: str) -> bool:
    # MVP: allow localhost-style demo domains only; adjust per policy
    return any(domain.endswith(suffix) for suffix in (".local", ".test", "localhost", "example.com"))
