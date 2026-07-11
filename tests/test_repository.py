from pathlib import Path

from careerpilot.domain.models import Job, JobMatch
from careerpilot.infrastructure.repository import SQLiteJobRepository


def test_repository_only_saves_a_job_once(tmp_path: Path) -> None:
    repository = SQLiteJobRepository(tmp_path / "jobs.sqlite3")
    job = Job(company="Example", title="Technical Program Manager", location="Remote", url="https://example.test/1", source="test")
    match = JobMatch(job=job, score=80, reasons=("Target role",))
    assert repository.save_if_new(job, match)
    assert not repository.save_if_new(job, match)
    assert repository.recent(5)[0].job.title == "Technical Program Manager"
