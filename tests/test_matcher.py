from careerpilot.application.matcher import RuleBasedMatcher
from careerpilot.domain.models import Job, SearchProfile


def profile() -> SearchProfile:
    return SearchProfile(
        name="Ozlem",
        target_roles=("Engineering Project Manager", "Technical Program Manager"),
        preferred_locations=("Cork", "Remote"),
        excluded_locations=("Dublin",),
        include_keywords=("agile", "software", "sdlc"),
        exclude_keywords=("construction", "sap"),
        minimum_score=45,
    )


def test_matcher_scores_relevant_role() -> None:
    job = Job(
        company="Example",
        title="Engineering Project Manager",
        location="Cork, Ireland",
        url="https://example.test/job",
        source="test",
        description="Lead Agile software delivery and SDLC planning.",
    )
    result = RuleBasedMatcher().match(job, profile())
    assert result.score == 86
    assert not result.excluded
    assert "Target role: Engineering Project Manager" in result.reasons


def test_matcher_excludes_unrelated_role() -> None:
    job = Job(
        company="Example",
        title="Construction Project Manager",
        location="Cork, Ireland",
        url="https://example.test/job",
        source="test",
    )
    result = RuleBasedMatcher().match(job, profile())
    assert result.excluded
    assert result.score == 0
