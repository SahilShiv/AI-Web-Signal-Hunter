"""Data models representing web pages crawled from the internet."""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class CrawledPage(BaseModel):
    """Represents a crawled and cleaned web page."""

    url: str = Field(..., description="Original URL of the crawled page")
    domain: str = Field(..., description="Hostname/domain of the source")
    title: str = Field(default="Untitled Page", description="Extracted HTML title")
    cleaned_text: str = Field(default="", description="Main readable body text with boilerplate stripped")
    word_count: int = Field(default=0, description="Word count of cleaned text")
    content_hash: str = Field(..., description="SHA-256 hash of cleaned text for deduplication")
    crawl_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="UTC timestamp of crawl")
    published_date: Optional[str] = Field(default=None, description="Extracted publication date if available")
    status_code: int = Field(default=200, description="HTTP response status code")
    is_valid: bool = Field(default=True, description="Whether content is valid for analysis")
    error_message: Optional[str] = Field(default=None, description="Error reason if crawl failed")

    @property
    def excerpt(self) -> str:
        """Returns a 200-character preview of the text."""
        if not self.cleaned_text:
            return ""
        return (self.cleaned_text[:200] + "...") if len(self.cleaned_text) > 200 else self.cleaned_text
