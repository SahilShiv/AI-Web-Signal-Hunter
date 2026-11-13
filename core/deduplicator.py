"""Deduplication engine for URLs and web page content."""

import re
from typing import Set, Dict
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from utils.helpers import compute_sha256
from utils.logger import logger


class Deduplicator:
    """Handles URL canonicalization and content hash/similarity deduplication."""

    def __init__(self):
        self.seen_urls: Set[str] = set()
        self.seen_hashes: Set[str] = set()
        self.domain_page_counts: Dict[str, int] = {}

    def canonicalize_url(self, url: str) -> str:
        """
        Normalizes a URL by stripping tracking parameters, fragments, and standardizing scheme/casing.
        """
        if not url:
            return ""
        try:
            parsed = urlparse(url.strip())
            # Lowercase scheme and hostname
            scheme = parsed.scheme.lower()
            netloc = parsed.netloc.lower()
            if netloc.startswith("www."):
                netloc = netloc[4:]

            # Strip port 80/443
            if ":80" in netloc:
                netloc = netloc.replace(":80", "")
            if ":443" in netloc:
                netloc = netloc.replace(":443", "")

            # Filter out tracking query parameters (utm_*, ref, fbclid, etc.)
            filtered_query = []
            tracking_prefixes = ("utm_", "ref", "source", "fbclid", "gclid", "campaign", "affiliate")
            for key, val in parse_qsl(parsed.query):
                if not any(key.lower().startswith(p) for p in tracking_prefixes):
                    filtered_query.append((key, val))

            new_query = urlencode(filtered_query)
            # Remove trailing slash from path unless it is root
            path = parsed.path.rstrip("/") if parsed.path != "/" else "/"

            canonical = urlunparse((scheme, netloc, path, "", new_query, ""))
            return canonical
        except Exception:
            return url.strip()

    def is_url_duplicate(self, url: str) -> bool:
        """Checks if URL (after canonicalization) has already been processed."""
        canonical = self.canonicalize_url(url)
        if canonical in self.seen_urls:
            return True
        self.seen_urls.add(canonical)
        return False

    def is_content_duplicate(self, cleaned_text: str) -> bool:
        """Checks if cleaned text matches an already seen SHA-256 hash or is too short."""
        if not cleaned_text or len(cleaned_text.strip()) < 80:
            return True

        # Normalized text (alphanumeric only) for stable hashing
        normalized = re.sub(r"\W+", " ", cleaned_text.lower()).strip()
        content_hash = compute_sha256(normalized)

        if content_hash in self.seen_hashes:
            logger.info("Exact or near-duplicate content hash identified; skipping.")
            return True

        self.seen_hashes.add(content_hash)
        return False

    def reset(self):
        """Resets tracking cache for new session."""
        self.seen_urls.clear()
        self.seen_hashes.clear()
        self.domain_page_counts.clear()

