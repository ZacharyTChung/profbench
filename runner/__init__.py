"""ProfBench runner package.

Hosts the CLI eval runner and model API wrappers, plus shared SQLite helpers
that other packages (scorer, analysis, leaderboard, data export) reuse.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db" / "profbench.db"
QUESTIONS_PATH = PROJECT_ROOT / "data" / "questions.json"


SCHEMA = """
CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    category TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    question TEXT NOT NULL,
    context TEXT,
    ideal_answer TEXT,
    rubric TEXT NOT NULL,
    expected_failure_mode TEXT,
    created_at TEXT NOT NULL,
    -- FinanceQA-aligned tagging (added in v0.2.0; backfilled with ALTER TABLE for older DBs)
    question_type TEXT DEFAULT 'tactical',          -- 'tactical' | 'conceptual'
    requires_assumption INTEGER DEFAULT 0,          -- bool: question requires an unstated assumption
    source_grounded INTEGER DEFAULT 0,              -- bool: context drawn from a real public document
    source_doc TEXT                                 -- name of the source document (for source_grounded questions)
);

CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    model TEXT NOT NULL,
    response TEXT,
    tokens_used INTEGER,
    latency_ms INTEGER,
    run_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL,
    question_id TEXT NOT NULL,
    model TEXT NOT NULL,
    score INTEGER NOT NULL,
    scorer_type TEXT NOT NULL,
    scorer_notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (response_id) REFERENCES responses(id)
);

CREATE INDEX IF NOT EXISTS idx_responses_run ON responses(run_id);
CREATE INDEX IF NOT EXISTS idx_responses_model ON responses(model);
CREATE INDEX IF NOT EXISTS idx_scores_response ON scores(response_id);
CREATE INDEX IF NOT EXISTS idx_scores_scorer ON scores(scorer_type);
"""


def now_iso() -> str:
    """Return current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_db() -> sqlite3.Connection:
    """Open a SQLite connection with foreign keys on and Row row factory."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """Create all tables if they do not already exist; ALTER older DBs to add v0.2.0 columns."""
    with get_db() as conn:
        conn.executescript(SCHEMA)
        # Migrate older DBs that pre-date the FinanceQA-aligned columns.
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(questions)").fetchall()}
        migrations = [
            ("question_type",       "ALTER TABLE questions ADD COLUMN question_type TEXT DEFAULT 'tactical'"),
            ("requires_assumption", "ALTER TABLE questions ADD COLUMN requires_assumption INTEGER DEFAULT 0"),
            ("source_grounded",     "ALTER TABLE questions ADD COLUMN source_grounded INTEGER DEFAULT 0"),
            ("source_doc",          "ALTER TABLE questions ADD COLUMN source_doc TEXT"),
        ]
        for col, ddl in migrations:
            if col not in existing:
                conn.execute(ddl)
        conn.commit()


__all__ = [
    "DB_PATH",
    "PROJECT_ROOT",
    "QUESTIONS_PATH",
    "get_db",
    "init_db",
    "now_iso",
]
