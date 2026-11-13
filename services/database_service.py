"""Database service for storing, loading, and querying research runs."""

import json
from datetime import datetime
from typing import List, Optional
from database.database import DatabaseManager
from models.opportunity import ResearchSession, Opportunity, OpportunityBrief, EvidenceReference
from models.signal import Signal
from models.page import CrawledPage
from utils.logger import logger


class DatabaseService:
    """Manages persistence of research sessions, signals, pages, and opportunities."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()

    def save_session(
        self,
        session: ResearchSession,
        pages: Optional[List[CrawledPage]] = None
    ) -> bool:
        """Persists a complete research session with all associated data."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()

                # 1. Insert session record
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO research_sessions (
                        id, topic, keywords, ai_provider, ai_model,
                        crawl_limit, min_relevance_threshold, pages_discovered,
                        pages_crawled_count, pages_skipped_count, signals_count,
                        opportunities_count, unique_domains_count, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        session.id,
                        session.topic,
                        json.dumps(session.keywords),
                        session.ai_provider,
                        session.ai_model,
                        session.crawl_limit,
                        session.min_relevance_threshold,
                        session.pages_discovered,
                        session.pages_crawled_count,
                        session.pages_skipped_count,
                        len(session.signals),
                        len(session.opportunities),
                        session.unique_domains_count,
                        session.created_at.isoformat()
                    )
                )

                # 2. Insert crawled pages
                if pages:
                    for page in pages:
                        cursor.execute(
                            """
                            INSERT INTO crawled_pages (
                                session_id, url, domain, title, word_count,
                                content_hash, crawl_date, published_date, status_code
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                session.id,
                                page.url,
                                page.domain,
                                page.title,
                                page.word_count,
                                page.content_hash,
                                page.crawl_date.isoformat(),
                                page.published_date,
                                page.status_code
                            )
                        )

                # 3. Insert signals
                for sig in session.signals:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO extracted_signals (
                            id, session_id, source_url, source_domain, page_title,
                            signal_category, summary, evidence, evidence_verified,
                            relevance_score, urgency_score, confidence_score,
                            reasoning, is_relevant, created_at, published_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            sig.id,
                            session.id,
                            sig.source_url,
                            sig.source_domain,
                            sig.page_title,
                            sig.signal_category,
                            sig.summary,
                            sig.evidence,
                            1 if sig.evidence_verified else 0,
                            sig.relevance_score,
                            sig.urgency_score,
                            sig.confidence_score,
                            sig.reasoning,
                            1 if sig.is_relevant else 0,
                            sig.created_at.isoformat(),
                            sig.published_date
                        )
                    )

                # 4. Insert opportunities
                for opp in session.opportunities:
                    brief_json = opp.brief.model_dump_json() if opp.brief else ""
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO opportunities (
                            id, session_id, title, problem_description, target_audience,
                            why_it_matters, possible_solution, validation_strategy,
                            supporting_signal_count, unique_domains_count, supporting_domains,
                            frequency_score, relevance_score, urgency_score, confidence_score,
                            recency_score, opportunity_score, score_breakdown, score_explanation,
                            brief_json
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            opp.id,
                            session.id,
                            opp.title,
                            opp.problem_description,
                            opp.target_audience,
                            opp.why_it_matters,
                            opp.possible_solution,
                            opp.validation_strategy,
                            opp.supporting_signal_count,
                            opp.unique_domains_count,
                            json.dumps(opp.supporting_domains),
                            opp.frequency_score,
                            opp.relevance_score,
                            opp.urgency_score,
                            opp.confidence_score,
                            opp.recency_score,
                            opp.opportunity_score,
                            json.dumps(opp.score_breakdown),
                            opp.score_explanation,
                            brief_json
                        )
                    )

                conn.commit()
            logger.info(f"Successfully saved research session {session.id} to SQLite.")
            return True
        except Exception as e:
            logger.error(f"Failed to save session {session.id}: {e}")
            return False

    def list_sessions(self) -> List[dict]:
        """Returns metadata list of all saved sessions."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, topic, ai_provider, pages_crawled_count,
                           signals_count, opportunities_count, unique_domains_count, created_at
                    FROM research_sessions
                    ORDER BY created_at DESC
                    """
                )
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to list sessions: {e}")
            return []

    def get_session(self, session_id: str) -> Optional[ResearchSession]:
        """Loads a complete session with its signals and opportunities."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()

                # Get session metadata
                cursor.execute("SELECT * FROM research_sessions WHERE id = ?", (session_id,))
                s_row = cursor.fetchone()
                if not s_row:
                    return None

                # Get signals
                cursor.execute("SELECT * FROM extracted_signals WHERE session_id = ?", (session_id,))
                signal_rows = cursor.fetchall()
                signals: List[Signal] = []
                for sr in signal_rows:
                    signals.append(
                        Signal(
                            id=sr["id"],
                            session_id=sr["session_id"],
                            source_url=sr["source_url"],
                            source_domain=sr["source_domain"],
                            page_title=sr["page_title"] or "Source",
                            signal_category=sr["signal_category"],
                            summary=sr["summary"],
                            evidence=sr["evidence"],
                            evidence_verified=bool(sr["evidence_verified"]),
                            relevance_score=sr["relevance_score"] or 0.0,
                            urgency_score=sr["urgency_score"] or 0.0,
                            confidence_score=sr["confidence_score"] or 0.0,
                            reasoning=sr["reasoning"] or "",
                            is_relevant=bool(sr["is_relevant"]),
                            published_date=sr["published_date"]
                        )
                    )

                # Get opportunities
                cursor.execute("SELECT * FROM opportunities WHERE session_id = ?", (session_id,))
                opp_rows = cursor.fetchall()
                opportunities: List[Opportunity] = []
                for opr in opp_rows:
                    brief = None
                    if opr["brief_json"]:
                        try:
                            brief = OpportunityBrief.model_validate_json(opr["brief_json"])
                        except Exception:
                            pass

                    # Filter signals belonging to this opportunity
                    opp_title = opr["title"]
                    # Match signals
                    opp_signals = [s for s in signals if s.summary in (opr["problem_description"] or "") or len(signals) <= 10]
                    if not opp_signals:
                        opp_signals = signals[:3]

                    breakdown = {}
                    if opr["score_breakdown"]:
                        try:
                            breakdown = json.loads(opr["score_breakdown"])
                        except Exception:
                            pass

                    supporting_domains = []
                    if opr["supporting_domains"]:
                        try:
                            supporting_domains = json.loads(opr["supporting_domains"])
                        except Exception:
                            pass

                    opportunities.append(
                        Opportunity(
                            id=opr["id"],
                            session_id=opr["session_id"],
                            research_topic=s_row["topic"],
                            title=opp_title,
                            problem_description=opr["problem_description"] or "",
                            target_audience=opr["target_audience"] or "",
                            why_it_matters=opr["why_it_matters"] or "",
                            possible_solution=opr["possible_solution"] or "",
                            validation_strategy=opr["validation_strategy"] or "",
                            signals=opp_signals,
                            supporting_signal_count=opr["supporting_signal_count"] or len(opp_signals),
                            unique_domains_count=opr["unique_domains_count"] or len(supporting_domains),
                            supporting_domains=supporting_domains,
                            frequency_score=opr["frequency_score"] or 0.0,
                            relevance_score=opr["relevance_score"] or 0.0,
                            urgency_score=opr["urgency_score"] or 0.0,
                            confidence_score=opr["confidence_score"] or 0.0,
                            recency_score=opr["recency_score"] or 0.0,
                            opportunity_score=opr["opportunity_score"] or 0.0,
                            score_breakdown=breakdown,
                            score_explanation=opr["score_explanation"] or "",
                            brief=brief
                        )
                    )

                # Parse keywords
                keywords = []
                if s_row["keywords"]:
                    try:
                        keywords = json.loads(s_row["keywords"])
                    except Exception:
                        pass

                return ResearchSession(
                    id=s_row["id"],
                    topic=s_row["topic"],
                    keywords=keywords,
                    ai_provider=s_row["ai_provider"] or "Groq",
                    ai_model=s_row["ai_model"] or "",
                    crawl_limit=s_row["crawl_limit"] or 25,
                    min_relevance_threshold=s_row["min_relevance_threshold"] or 60.0,
                    pages_discovered=s_row["pages_discovered"] or 0,
                    pages_crawled_count=s_row["pages_crawled_count"] or 0,
                    pages_skipped_count=s_row["pages_skipped_count"] or 0,
                    signals_count=len(signals),
                    opportunities_count=len(opportunities),
                    unique_domains_count=s_row["unique_domains_count"] or 0,
                    signals=signals,
                    opportunities=opportunities
                )
        except Exception as e:
            logger.error(f"Failed to retrieve session {session_id}: {e}")
            return None

    def delete_session(self, session_id: str) -> bool:
        """Deletes a session and cascading children."""
        try:
            with self.db.get_connection() as conn:
                conn.execute("DELETE FROM research_sessions WHERE id = ?", (session_id,))
                conn.commit()
            logger.info(f"Deleted session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            return False

