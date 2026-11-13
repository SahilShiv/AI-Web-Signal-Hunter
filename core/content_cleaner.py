"""HTML parser and content cleaning pipeline to extract clean readable text."""

import re
from typing import Optional, Tuple
from bs4 import BeautifulSoup
from utils.logger import logger


# HTML tags to completely remove
DISALLOWED_TAGS = [
    "script", "style", "noscript", "svg", "iframe", "form",
    "nav", "footer", "header", "aside", "menu", "canvas"
]

# Common CSS classes / IDs indicating boilerplate or ads
BOILERPLATE_SELECTORS = [
    ".cookie", ".cookie-banner", ".cookie-notice", ".cookie-consent",
    "#cookie-law-info-bar", "#onetrust-banner-sdk", ".consent-modal",
    ".sidebar", ".advertisement", ".ad-container", ".advert",
    ".site-footer", ".main-navigation", ".newsletter-signup",
    ".social-share", ".share-buttons", ".related-posts", ".comments-closed"
]


class ContentCleaner:
    """Cleans raw HTML into normalized, readable text suitable for LLM analysis."""

    def clean_html(self, raw_html: str, url: str = "") -> Tuple[str, str, Optional[str]]:
        """
        Cleans HTML document.
        Returns:
            (title, cleaned_text, published_date)
        """
        if not raw_html or not raw_html.strip():
            return "Untitled Page", "", None

        try:
            soup = BeautifulSoup(raw_html, "html.parser")
        except Exception as e:
            logger.warning(f"HTML parsing failed for {url}: {e}")
            return "Error Parsing", "", None

        # 1. Extract Title
        title = self._extract_title(soup)

        # 2. Extract Publication Date
        published_date = self._extract_published_date(soup)

        # 3. Strip Disallowed Tags
        for tag_name in DISALLOWED_TAGS:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        # 4. Strip boilerplate elements by CSS selector
        for selector in BOILERPLATE_SELECTORS:
            try:
                for el in soup.select(selector):
                    el.decompose()
            except Exception:
                continue

        # 5. Extract text from primary body or main article container
        article_node = soup.find("article") or soup.find("main") or soup.find(role="main") or soup.find("body") or soup

        # Extract structured paragraphs and headings
        lines = []
        for element in article_node.find_all(["h1", "h2", "h3", "h4", "p", "li", "blockquote"]):
            text = element.get_text(separator=" ", strip=True)
            if not text or len(text) < 15:
                continue

            # Skip common cookie/nav remnants
            lower_text = text.lower()
            if any(term in lower_text for term in ["accept cookies", "privacy policy", "all rights reserved", "terms of use"]):
                continue

            # Format headings
            if element.name in ["h1", "h2", "h3", "h4"]:
                lines.append(f"\n## {text}\n")
            else:
                lines.append(text)

        cleaned_text = "\n".join(lines)
        # Normalize whitespace
        cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)
        cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text).strip()

        return title, cleaned_text, published_date

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extracts cleanest page title."""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
            # Clean common title suffixes like " | Wati" or " - G2"
            title = re.split(r" [|\-–—] ", title)[0].strip()
            if title:
                return title

        h1 = soup.find("h1")
        if h1:
            h1_text = h1.get_text(strip=True)
            if h1_text:
                return h1_text

        meta_og = soup.find("meta", property="og:title")
        if meta_og and meta_og.get("content"):
            return meta_og["content"].strip()

        return "Untitled Page"

    def _extract_published_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extracts publication date from metadata or time tag."""
        # Check standard meta tags
        for prop in ["article:published_time", "og:published_time", "datePublished", "pubdate"]:
            meta = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
            if meta and meta.get("content"):
                date_val = meta["content"].strip()[:10]  # Take YYYY-MM-DD
                if re.match(r"^\d{4}-\d{2}-\d{2}", date_val):
                    return date_val

        # Check <time> tag
        time_tag = soup.find("time")
        if time_tag:
            dt_val = time_tag.get("datetime") or time_tag.get_text(strip=True)
            if dt_val and len(dt_val) >= 4:
                match = re.search(r"\b(20\d{2})[-\/.](\d{1,2})[-\/.](\d{1,2})\b", dt_val)
                if match:
                    return f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"

        return None

