"""SQLite persistence adapter."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from careerpilot.domain.models import Job, JobMatch


class SQLiteJobRepository:
    """Persist matching roles in a lightweight local SQLite database."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                identity_key TEXT PRIMARY KEY,
                company TEXT NOT NULL,
                title TEXT NOT NULL,
                location TEXT NOT NULL,
                url TEXT NOT NULL,
                source TEXT NOT NULL,
                description TEXT NOT NULL,
                posted_at TEXT,
                discovered_at TEXT NOT NULL,
                score INTEGER NOT NULL,
                reasons_json TEXT NOT NULL
            )
            """
        )
        self._connection.commit()

    def save_if_new(self, job: Job, match: JobMatch) -> bool:
        """Insert a matched job once, returning whether it is new."""
        cursor = self._connection.execute(
            """
            INSERT OR IGNORE INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.identity_key,
                job.company,
                job.title,
                job.location,
                job.url,
                job.source,
                job.description,
                job.posted_at.isoformat() if job.posted_at else None,
                job.discovered_at.isoformat(),
                match.score,
                json.dumps(match.reasons),
            ),
        )
        self._connection.commit()
        return cursor.rowcount == 1

    def recent(self, limit: int) -> list[JobMatch]:
        """Return recently discovered matching jobs in descending order."""
        rows = self._connection.execute("SELECT * FROM jobs ORDER BY discovered_at DESC LIMIT ?", (limit,)).fetchall()
        return [self._row_to_match(row) for row in rows]

    @staticmethod
    def _row_to_match(row: sqlite3.Row) -> JobMatch:
        job = Job(
            company=row["company"],
            title=row["title"],
            location=row["location"],
            url=row["url"],
            source=row["source"],
            description=row["description"],
            posted_at=datetime.fromisoformat(row["posted_at"]) if row["posted_at"] else None,
            discovered_at=datetime.fromisoformat(row["discovered_at"]),
        )
        return JobMatch(job=job, score=row["score"], reasons=tuple(json.loads(row["reasons_json"])))
