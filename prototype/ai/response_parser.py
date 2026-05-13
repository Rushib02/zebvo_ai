from utils.helpers import extract_json

def parse(raw: str | dict) -> dict:
    """Accept either a raw string or already-parsed dict."""
    if isinstance(raw, dict):
        return raw
    return extract_json(raw)
