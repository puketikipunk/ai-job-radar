"""Collector for Greenhouse's documented public job-board endpoint."""

from __future__ import annotations

from datetime import UTC, datetime

import httpx

from careerpilot.domain.models import Job


class GreenhouseCollector:
    """Retrieve roles from a public Greenhouse board token."""

    def __init__(self, name: str, board_token: str, client: httpx.Client | None = None) -> None:
        self.name = name
        self._board_token = board_token
        self._client = client or httpx.Client(timeout=30.0, follow_redirects=True)

    def collect(self) -> list[Job]:
        """Fetch and normalise all currently advertised Greenhouse jobs."""
        response = self._client.get(
            f"https://boards-api.greenhouse.io/v1/boards/{self._board_token}/jobs",
            params={"content": "true"},
        )
        response.raise_for_status()
        jobs: list[Job] = []
        for item in response.json().get("jobs", []):
            updated_at = item.get("updated_at")
            posted_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00")) if updated_at else None
            jobs.append(
                Job(
                    company=self.name,
                    title=item["title"],
                    location=item.get("location", {}).get("name", "Unspecified"),
                    url=item["absolute_url"],
                    source=f"greenhouse:{self._board_token}",
                    description=item.get("content", ""),
                    posted_at=posted_at.astimezone(UTC) if posted_at else None,
                )
            )
        return jobs
