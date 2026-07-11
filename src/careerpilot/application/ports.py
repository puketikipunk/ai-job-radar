"""Ports implemented by external adapters."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from careerpilot.domain.models import Job, JobMatch


class JobCollector(Protocol):
    """Collect jobs from one permitted source."""

    name: str

    def collect(self) -> list[Job]:
        """Return normalised jobs or raise a source-specific error."""


class JobRepository(Protocol):
    """Store and query job records."""

    def save_if_new(self, job: Job, match: JobMatch) -> bool:
        """Persist a job and return true only if it had not been seen before."""

    def recent(self, limit: int) -> list[JobMatch]:
        """Return recently discovered matching jobs."""


class DigestSender(Protocol):
    """Deliver a rendered digest."""

    def send(self, subject: str, plain_text: str, html: str) -> None:
        """Deliver the digest."""


class DigestRenderer(Protocol):
    """Render a set of matching jobs for a human reader."""

    def render(self, matches: Iterable[JobMatch]) -> tuple[str, str]:
        """Return plain text and HTML representations."""
