"""Ingest job listings from user-authorised job-alert emails over IMAP."""

from __future__ import annotations

import imaplib
import os
import re
from datetime import UTC, datetime
from email import message_from_bytes
from email.message import Message
from email.utils import parseaddr, parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
from typing import cast

from careerpilot.domain.models import Job

_JOB_URL = re.compile(r"/(?:jobs?|careers?|positions?|vacanc(?:y|ies))/", re.IGNORECASE)


class _LinkParser(HTMLParser):
    """Extract links and readable text without executing email HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.text: list[str] = []
        self._href: str | None = None
        self._anchor_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._anchor_text = []

    def handle_data(self, data: str) -> None:
        clean = " ".join(data.split())
        if clean:
            self.text.append(clean)
            if self._href:
                self._anchor_text.append(clean)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href:
            self.links.append((self._href, " ".join(self._anchor_text)))
            self._href = None
            self._anchor_text = []


class ImapAlertsCollector:
    """Read official alert emails from a dedicated user-authorised mailbox folder."""

    def __init__(
        self,
        name: str,
        folder: str,
        allowed_sender_domains: tuple[str, ...],
        max_messages: int,
    ) -> None:
        self.name = name
        self._folder = folder
        self._allowed_sender_domains = tuple(domain.casefold() for domain in allowed_sender_domains)
        self._max_messages = max_messages

    def collect(self) -> list[Job]:
        """Fetch recent alert messages and convert their job links to listings."""
        host = self._required("CAREERPILOT_IMAP_HOST", "outlook.office365.com")
        port = int(os.getenv("CAREERPILOT_IMAP_PORT", "993"))
        username = self._required("CAREERPILOT_IMAP_USERNAME")
        password = self._required("CAREERPILOT_IMAP_PASSWORD")
        with imaplib.IMAP4_SSL(host, port) as client:
            client.login(username, password)
            status, _ = client.select(self._folder, readonly=True)
            if status != "OK":
                raise RuntimeError(f"Unable to open IMAP folder: {self._folder}")
            status, data = client.search(None, "ALL")
            if status != "OK":
                raise RuntimeError("Unable to search IMAP folder")
            ids = data[0].split()[-self._max_messages :]
            jobs: list[Job] = []
            for message_id in ids:
                status, raw_data = client.fetch(message_id, "(RFC822)")
                if status != "OK" or not raw_data:
                    continue
                payload = cast(tuple[bytes, bytes], raw_data[0])[1]
                jobs.extend(self._jobs_from_message(message_from_bytes(payload)))
            return jobs

    def _jobs_from_message(self, message: Message) -> list[Job]:
        sender_name, sender_email = parseaddr(message.get("From", ""))
        domain = sender_email.rsplit("@", 1)[-1].casefold()
        if self._allowed_sender_domains and not any(
            domain == allowed or domain.endswith(f".{allowed}") for allowed in self._allowed_sender_domains
        ):
            return []
        subject = str(message.get("Subject", "Job alert")).strip()
        posted_at = _message_date(message)
        parser = _LinkParser()
        parser.feed(_message_body(message))
        description = " ".join(parser.text)[:4_000]
        company = sender_name or domain
        jobs: list[Job] = []
        seen_urls: set[str] = set()
        for url, link_text in parser.links:
            if not url.startswith("http") or not _JOB_URL.search(url) or url in seen_urls:
                continue
            seen_urls.add(url)
            title = link_text.strip() or subject
            jobs.append(
                Job(
                    company=company,
                    title=unescape(title)[:300],
                    location="See alert email",
                    url=url,
                    source=f"imap_alerts:{domain}",
                    description=description,
                    posted_at=posted_at,
                )
            )
        return jobs

    @staticmethod
    def _required(name: str, default: str | None = None) -> str:
        value = os.getenv(name, default)
        if not value:
            raise ValueError(f"Missing required environment variable: {name}")
        return value


def _message_body(message: Message) -> str:
    """Return the richest non-attachment message body available."""
    for part in message.walk():
        if part.get_content_disposition() == "attachment":
            continue
        if part.get_content_type() in {"text/html", "text/plain"}:
            content = part.get_payload(decode=True)
            if content:
                return content.decode(part.get_content_charset() or "utf-8", errors="replace")
    return ""


def _message_date(message: Message) -> datetime | None:
    """Parse a message date without making alert ingestion fail on malformed headers."""
    try:
        return parsedate_to_datetime(message["Date"]).astimezone(UTC) if message.get("Date") else None
    except (TypeError, ValueError, IndexError):
        return None
