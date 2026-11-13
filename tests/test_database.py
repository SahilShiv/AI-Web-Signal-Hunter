"""Unit tests for SQLite database operations."""

import os
from pathlib import Path
from database.database import DatabaseManager
from services.database_service import DatabaseService
from data.sample_data import build_sample_session


def test_database_lifecycle(tmp_path):
    test_db_path = tmp_path / "test_signals.db"
    db_mgr = DatabaseManager(db_path=test_db_path)
    db_service = DatabaseService(db_mgr)

    # 1. Build sample session
    session, pages = build_sample_session()

    # 2. Save session
    save_ok = db_service.save_session(session, pages=pages)
    assert save_ok is True

    # 3. List sessions
    sessions_list = db_service.list_sessions()
    assert len(sessions_list) == 1
    assert sessions_list[0]["id"] == session.id

    # 4. Load full session
    loaded = db_service.get_session(session.id)
    assert loaded is not None
    assert loaded.topic == session.topic
    assert len(loaded.signals) == len(session.signals)
    assert len(loaded.opportunities) == len(session.opportunities)

    # 5. Delete session
    del_ok = db_service.delete_session(session.id)
    assert del_ok is True
    assert len(db_service.list_sessions()) == 0

