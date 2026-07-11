"""Domain entities kept independent from delivery and storage concerns."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from hashlib import sha256


def _normalise(value: str) -> str:
    return " ".join(value.casefold().split())


@dataclass(frozen=True, slots=True)
class Job:
    """A validated, source-neutral job listing."""

    company: str
    title: str
    location: str
    url: str
    source: str
    description: str = ""
    posted_at: datetime | None = None
    discovered_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def identity_key(self) -> str:
        """Return a stable key used to suppress duplicate listings."""
        basis = self.url.strip() or "|".join(
            (_normalise(self.company), _normalise(self.title), _normalise(self.location), _normalise(self.source))
        )
        return sha256(basis.encode("utf-8")).hexdigest()

    @property
    def searchable_text(self) -> str:
        """Return normalised text used by deterministic matching rules."""
        return _normalise(" ".join((self.title, self.company, self.location, self.description)))


@dataclass(frozen=True, slots=True)
class SearchProfile:
    """User-defined targeting rules loaded from configuration."""

    name: str
    target_roles: tuple[str, ...]
    preferred_locations: tuple[str, ...]
    excluded_locations: tuple[str, ...]
    include_keywords: tuple[str, ...]
    exclude_keywords: tuple[str, ...]
    minimum_score: int


@dataclass(frozen=True, slots=True)
class JobMatch:
    """A job with an explainable relevance score."""

    job: Job
    score: int
    reasons: tuple[str, ...]
    excluded: bool = False
