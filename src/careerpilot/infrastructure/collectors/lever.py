"""Collector for Lever's public job-postings endpoint."""

from __future__ import annotations

from datetime import UTC, datetime

import httpx

from careerpilot.domain.models import Job


class LeverCollector:
    """Retrieve roles from a public Lever site slug."""

    def __init__(self, name: str, site: str, client: httpx.Client | None = None) -> None:
        self.name = name
        self._site = site
        self._client = client or httpx.Client(timeout=30.0, follow_redirects=True)

    def collect(self) -> list[Job]:
        """Fetch and normalise all currently advertised Lever jobs."""
        response = self._client.get(f"https://api.lever.co/v0/postings/{self._site}", params={"mode": "json"})
        response.raise_for_status()
        jobs: list[Job] = []
        for item in response.json():
            created_ms = item.get("createdAt")
            posted_at = datetime.fromtimestamp(created_ms / 1000, tz=UTC) if created_ms else None
            categories = item.get("categories", {})
            location = categories.get("location") or "Unspecified"
            description = " ".join(part for part in (item.get("descriptionPlain"), item.get("additionalPlain")) if part)
            jobs.append(
                Job(
                    company=self.name,
                    title=item["text"],
                    location=location,
                    url=item["hostedUrl"],
                    source=f"lever:{self._site}",
                    description=description,
                    posted_at=posted_at,
                )
            )
        return jobs
