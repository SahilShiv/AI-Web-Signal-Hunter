"""Validation utilities for URLs, domains, and scores."""

import re
from urllib.parse import urlparse
from typing import List, Optional


def is_valid_url(url: str) -> bool:
    """Validates that a URL is well-formed with http or https scheme and valid netloc."""
    if not url or not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc) and "." in parsed.netloc
    except Exception:
        return False


def extract_domain(url: str) -> str:
    """Extracts clean hostname/domain from a URL."""
    try:
        parsed = urlparse(url.strip())
        netloc = parsed.netloc.lower()
        # Remove port if present
        if ":" in netloc:
            netloc = netloc.split(":")[0]
        # Remove www prefix
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc if netloc else "unknown"
    except Exception:
        return "unknown"


def clean_keywords(raw_keywords: str) -> List[str]:
    """Parses a comma or newline-separated string into a deduplicated list of clean keywords."""
    if not raw_keywords:
        return []
    parts = re.split(r"[,;\n]+", raw_keywords)
    cleaned = []
    for part in parts:
        cleaned_part = part.strip().lower()
        if cleaned_part and len(cleaned_part) > 1 and cleaned_part not in cleaned:
            cleaned.append(cleaned_part)
    return cleaned


def normalize_score(score: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Clamps a numeric score within min_val and max_val."""
    try:
        val = float(score)
        return round(max(min_val, min(max_val, val)), 1)
    except (ValueError, TypeError):
        return 0.0
