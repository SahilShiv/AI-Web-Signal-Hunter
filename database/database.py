"""SQLite database manager for persistent research sessions and intelligence findings."""

import sqlite3
from pathlib import Path
from typing import Optional
from config.settings import settings
from utils.logger import logger


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS research_sessions (
    id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    keywords TEXT,
    ai_provider TEXT,
    ai_model TEXT,
    crawl_limit INTEGER,
    min_relevance_threshold REAL,
    pages_discovered INTEGER DEFAULT 0,
    pages_crawled_count INTEGER DEFAULT 0,
    pages_skipped_count INTEGER DEFAULT 0,
    signals_count INTEGER DEFAULT 0,
    opportunities_count INTEGER DEFAULT 0,
    unique_domains_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS crawled_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    url TEXT NOT NULL,
    domain TEXT NOT NULL,
    title TEXT,
    word_count INTEGER,
    content_hash TEXT,
    crawl_date TIMESTAMP,
    published_date TEXT,
    status_code INTEGER,
    FOREIGN KEY (session_id) REFERENCES research_sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS extracted_signals (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    source_url TEXT NOT NULL,
    source_domain TEXT NOT NULL,
    page_title TEXT,
    signal_category TEXT NOT NULL,
    summary TEXT NOT NULL,
    evidence TEXT NOT NULL,
    evidence_verified INTEGER DEFAULT 1,
    relevance_score REAL,
    urgency_score REAL,
    confidence_score REAL,
    reasoning TEXT,
    is_relevant INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_date TEXT,
    FOREIGN KEY (session_id) REFERENCES research_sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    title TEXT NOT NULL,
    problem_description TEXT,
    target_audience TEXT,
    why_it_matters TEXT,
    possible_solution TEXT,
    validation_strategy TEXT,
    supporting_signal_count INTEGER,
    unique_domains_count INTEGER,
    supporting_domains TEXT,
    frequency_score REAL,
    relevance_score REAL,
    urgency_score REAL,
    confidence_score REAL,
    recency_score REAL,
    opportunity_score REAL,
    score_breakdown TEXT,
    score_explanation TEXT,
    brief_json TEXT,
    FOREIGN KEY (session_id) REFERENCES research_sessions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_signals_session ON extracted_signals(session_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_session ON opportunities(session_id);
CREATE INDEX IF NOT EXISTS idx_pages_session ON crawled_pages(session_id);
"""


class DatabaseManager:
    """SQLite Database manager with connection lifecycle handling."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or settings.database_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Returns SQLite connection with row factory enabled."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        """Initializes tables and indexes."""
        try:
            with self.get_connection() as conn:
                conn.executescript(SCHEMA_SQL)
                conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

