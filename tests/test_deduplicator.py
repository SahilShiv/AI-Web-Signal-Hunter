"""Unit tests for URL and content deduplication."""

from core.deduplicator import Deduplicator


def test_url_canonicalization():
    dedup = Deduplicator()
    url1 = "https://getwati.com/blog/pricing?utm_source=twitter&utm_medium=social#faq"
    url2 = "https://getwati.com/blog/pricing/"
    assert dedup.canonicalize_url(url1) == "https://getwati.com/blog/pricing"
    assert dedup.canonicalize_url(url2) == "https://getwati.com/blog/pricing"


def test_url_duplicate_detection():
    dedup = Deduplicator()
    url = "https://respond.io/features"
    assert dedup.is_url_duplicate(url) is False
    assert dedup.is_url_duplicate(url) is True
    # Equivalent tracking query
    assert dedup.is_url_duplicate("https://respond.io/features?utm_source=email") is True


def test_content_hash_deduplication():
    dedup = Deduplicator()
    text = "This is a substantial piece of cleaned article content describing WhatsApp automation issues across small businesses." * 2

    assert dedup.is_content_duplicate(text) is False
    assert dedup.is_content_duplicate(text) is True
    # Slight casing difference or spaces
    assert dedup.is_content_duplicate(text.upper()) is True

