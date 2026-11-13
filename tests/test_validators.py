"""Unit tests for URL and input validators."""

from utils.validators import is_valid_url, extract_domain, clean_keywords, normalize_score


def test_is_valid_url():
    assert is_valid_url("https://getwati.com/blog/pricing") is True
    assert is_valid_url("http://respond.io/features") is True
    assert is_valid_url("ftp://example.com") is False
    assert is_valid_url("not a url") is False
    assert is_valid_url("") is False
    assert is_valid_url("https://") is False


def test_extract_domain():
    assert extract_domain("https://www.getwati.com/blog") == "getwati.com"
    assert extract_domain("https://respond.io:8080/features") == "respond.io"
    assert extract_domain("http://techcrunch.com/article?ref=123") == "techcrunch.com"
    assert extract_domain("invalid") == "unknown"


def test_clean_keywords():
    raw = "pricing, bans, CRM, integration, PRICING, crm, ,"
    cleaned = clean_keywords(raw)
    assert cleaned == ["pricing", "bans", "crm", "integration"]
    assert clean_keywords("") == []


def test_normalize_score():
    assert normalize_score(85.34) == 85.3
    assert normalize_score(150) == 100.0
    assert normalize_score(-10) == 0.0
    assert normalize_score("invalid") == 0.0

