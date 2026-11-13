"""General helper functions for hashing, text manipulation, and formatting."""

import hashlib
import json
import re
from datetime import datetime
from typing import Any, Dict, Optional


def compute_sha256(text: str) -> str:
    """Computes SHA-256 hash of a string."""
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def truncate_text(text: str, max_chars: int = 150) -> str:
    """Safely truncates text to max_chars without breaking mid-word when possible."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars].rsplit(" ", 1)[0]
    return truncated + "..."


def count_words(text: str) -> int:
    """Returns word count of text."""
    if not text:
        return 0
    return len(text.split())


def safe_json_loads(json_str: str) -> Optional[Dict[str, Any]]:
    """Safely parses JSON strings, removing Markdown fences if present."""
    if not json_str:
        return None
    cleaned = json_str.strip()
    # Strip markdown code blocks
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\n", "", cleaned)
        cleaned = re.sub(r"\n```$", "", cleaned)
        cleaned = cleaned.strip()
    try:
        return json.loads(cleaned)
    except Exception:
        # Try extracting JSON object or array via regex
        match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
        return None


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Formats datetime to human-readable string."""
    if not dt:
        dt = datetime.utcnow()
    return dt.strftime("%b %d, %Y %H:%M UTC")

