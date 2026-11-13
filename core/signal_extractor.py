"""Batch signal extraction pipeline with filtering and progress updates."""

from typing import Callable, List, Optional
from models.page import CrawledPage
from models.signal import Signal
from core.ai_analyzer import AIAnalyzer
from utils.logger import logger


class SignalExtractor:
    """Orchestrates extraction of signals across crawled pages."""

    def __init__(self, analyzer: AIAnalyzer, min_relevance: float = 60.0):
        self.analyzer = analyzer
        self.min_relevance = min_relevance

    def extract_from_pages(
        self,
        topic: str,
        pages: List[CrawledPage],
        progress_callback: Optional[Callable[[dict], None]] = None
    ) -> List[Signal]:
        """Runs signal extraction across crawled pages."""
        all_signals: List[Signal] = []
        total_pages = len(pages)

        logger.info(f"Beginning signal extraction on {total_pages} pages...")

        for idx, page in enumerate(pages):
            pct = int(((idx + 1) / total_pages) * 100) if total_pages > 0 else 100

            if progress_callback:
                progress_callback({
                    "step": "analyzing",
                    "current_index": idx + 1,
                    "total_pages": total_pages,
                    "percent": pct,
                    "page_title": page.title,
                    "domain": page.domain,
                    "signals_found_so_far": len(all_signals),
                    "status_text": f"Extracting signals from {page.domain} ({idx + 1}/{total_pages})"
                })

            page_signals = self.analyzer.analyze_page(
                topic=topic,
                page_url=page.url,
                page_title=page.title,
                cleaned_text=page.cleaned_text
            )

            # Filter by relevance threshold
            for sig in page_signals:
                if sig.relevance_score >= self.min_relevance:
                    all_signals.append(sig)

        logger.info(f"Signal extraction complete. Total signals extracted: {len(all_signals)}")
        return all_signals

