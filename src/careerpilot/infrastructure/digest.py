"""Safe plain-text and HTML digest rendering."""

from __future__ import annotations

from collections.abc import Iterable
from html import escape

from careerpilot.domain.models import JobMatch


class HtmlDigestRenderer:
    """Render concise job recommendations without external template dependencies."""

    def __init__(self, max_jobs: int) -> None:
        self._max_jobs = max_jobs

    def render(self, matches: Iterable[JobMatch]) -> tuple[str, str]:
        """Return equivalent plain-text and HTML digests."""
        selected = sorted(matches, key=lambda match: match.score, reverse=True)[: self._max_jobs]
        if not selected:
            return "CareerPilot found no new matching jobs today.", "<p>CareerPilot found no new matching jobs today.</p>"
        text_lines = [f"CareerPilot found {len(selected)} new matching job(s):", ""]
        html_cards: list[str] = []
        for match in selected:
            job = match.job
            reasons = "; ".join(match.reasons) or "Matched your profile"
            text_lines.extend(
                (
                    f"{job.company} — {job.title}",
                    f"Match: {match.score}% | {job.location}",
                    f"Why: {reasons}",
                    f"Apply: {job.url}",
                    "",
                )
            )
            html_cards.append(
                "<article style='margin:16px 0;padding:16px;border:1px solid #ddd;border-radius:8px'>"
                f"<h2 style='margin:0'>{escape(job.company)} — {escape(job.title)}</h2>"
                f"<p><strong>Match: {match.score}%</strong> · {escape(job.location)}</p>"
                f"<p><strong>Why:</strong> {escape(reasons)}</p>"
                f"<p><a href='{escape(job.url, quote=True)}'>View and apply</a></p>"
                "</article>"
            )
        html = "<main><h1>CareerPilot: new opportunities</h1>" + "".join(html_cards) + "</main>"
        return "\n".join(text_lines), html
