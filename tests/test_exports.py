"""Unit tests for CSV and JSON export services."""

import json
import io
import pandas as pd
from services.export_service import ExportService
from data.sample_data import build_sample_session


def test_csv_export():
    session, pages = build_sample_session()
    csv_str = ExportService.export_csv(session)

    assert csv_str is not None
    assert len(csv_str) > 100

    # Parse back with pandas to verify valid CSV structure
    df = pd.read_csv(io.StringIO(csv_str))
    expected_cols = [
        "Opportunity Name", "Signal Category", "Summary", "Evidence",
        "Relevance Score", "Urgency Score", "Confidence Score",
        "Opportunity Score", "Source Domain", "Source URL"
    ]
    for col in expected_cols:
        assert col in df.columns

    assert len(df) >= 20


def test_json_export():
    session, pages = build_sample_session()
    json_str = ExportService.export_json(session, crawled_pages=pages)

    assert json_str is not None
    data = json.loads(json_str)

    assert "research_metadata" in data
    assert "crawled_pages" in data
    assert "extracted_signals" in data
    assert "grouped_opportunities" in data

    assert len(data["crawled_pages"]) == len(pages)
    assert len(data["extracted_signals"]) == len(session.signals)
    assert len(data["grouped_opportunities"]) == len(session.opportunities)

