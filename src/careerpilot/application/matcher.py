"""Transparent, deterministic matching rules."""

from __future__ import annotations

from careerpilot.domain.models import Job, JobMatch, SearchProfile


def _contains(text: str, phrase: str) -> bool:
    return phrase.casefold() in text


class RuleBasedMatcher:
    """Score listings using profile rules and explain every positive signal."""

    def match(self, job: Job, profile: SearchProfile) -> JobMatch:
        """Evaluate a job against the supplied profile."""
        text = job.searchable_text
        title = job.title.casefold()
        location = job.location.casefold()
        excluded_terms = [term for term in profile.exclude_keywords if _contains(text, term)]
        excluded_location = [term for term in profile.excluded_locations if _contains(location, term)]
        if excluded_terms or excluded_location:
            reasons = tuple(
                [f"Excluded keyword: {term}" for term in excluded_terms] + [f"Excluded location: {term}" for term in excluded_location]
            )
            return JobMatch(job=job, score=0, reasons=reasons, excluded=True)

        score = 0
        reasons: list[str] = []
        role_hits = [role for role in profile.target_roles if _contains(title, role)]
        if role_hits:
            score += 45
            reasons.append(f"Target role: {role_hits[0]}")

        location_hits = [location_name for location_name in profile.preferred_locations if _contains(location, location_name)]
        if location_hits:
            score += 20
            reasons.append(f"Preferred location: {location_hits[0]}")

        keyword_hits = [keyword for keyword in profile.include_keywords if _contains(text, keyword)]
        for keyword in keyword_hits[:5]:
            score += 7
            reasons.append(f"Relevant skill: {keyword}")

        return JobMatch(job=job, score=min(score, 100), reasons=tuple(reasons))
