"""The job-discovery use case."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from careerpilot.application.matcher import RuleBasedMatcher
from careerpilot.application.ports import DigestRenderer, DigestSender, JobCollector, JobRepository
from careerpilot.domain.models import JobMatch, SearchProfile

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RunResult:
    """Summary emitted after a collection run."""

    collected: int
    new_matches: tuple[JobMatch, ...]
    failed_collectors: tuple[str, ...]


class JobRadar:
    """Coordinate collection, matching, persistence, and optional delivery."""

    def __init__(
        self,
        collectors: list[JobCollector],
        repository: JobRepository,
        matcher: RuleBasedMatcher,
        profile: SearchProfile,
    ) -> None:
        self._collectors = collectors
        self._repository = repository
        self._matcher = matcher
        self._profile = profile

    def run(self) -> RunResult:
        """Collect each source independently and store qualifying new listings."""
        collected = 0
        failures: list[str] = []
        new_matches: list[JobMatch] = []
        seen_in_run: set[str] = set()
        for collector in self._collectors:
            try:
                jobs = collector.collect()
                logger.info("collector completed", extra={"collector": collector.name, "jobs": len(jobs)})
            except Exception:  # Boundary: a source must not halt the full daily run.
                logger.exception("collector failed", extra={"collector": collector.name})
                failures.append(collector.name)
                continue
            for job in jobs:
                collected += 1
                if job.identity_key in seen_in_run:
                    continue
                seen_in_run.add(job.identity_key)
                match = self._matcher.match(job, self._profile)
                if match.excluded or match.score < self._profile.minimum_score:
                    continue
                if self._repository.save_if_new(job, match):
                    new_matches.append(match)
        return RunResult(collected=collected, new_matches=tuple(new_matches), failed_collectors=tuple(failures))

    @staticmethod
    def deliver(
        result: RunResult,
        renderer: DigestRenderer,
        sender: DigestSender,
        subject: str,
    ) -> None:
        """Render and send a digest only when there are new matching jobs."""
        if not result.new_matches:
            logger.info("no new matches; skipping email")
            return
        plain_text, html = renderer.render(result.new_matches)
        sender.send(subject, plain_text, html)
