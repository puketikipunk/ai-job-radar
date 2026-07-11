from email import message_from_string

from careerpilot.infrastructure.collectors.imap_alerts import ImapAlertsCollector


def test_email_alert_extractor_creates_jobs_for_job_links() -> None:
    message = message_from_string(
        "From: LinkedIn Jobs <jobalerts-noreply@linkedin.com>\n"
        "Subject: Engineering Project Manager roles\n"
        "Date: Fri, 10 Jul 2026 08:00:00 +0000\n"
        "Content-Type: text/html\n\n"
        "<a href='https://www.linkedin.com/jobs/view/123'>Engineering Project Manager</a>"
    )
    collector = ImapAlertsCollector("Official job-alert inbox", "CareerPilot Job Alerts", ("linkedin.com",), 20)
    jobs = collector._jobs_from_message(message)
    assert len(jobs) == 1
    assert jobs[0].title == "Engineering Project Manager"
    assert jobs[0].source == "imap_alerts:linkedin.com"


def test_email_alert_extractor_ignores_unapproved_senders() -> None:
    message = message_from_string(
        "From: Unwanted <spam@example.com>\nContent-Type: text/html\n\n<a href='https://example.com/jobs/123'>Project Manager</a>"
    )
    collector = ImapAlertsCollector("Inbox", "Alerts", ("linkedin.com",), 20)
    assert collector._jobs_from_message(message) == []
