"""SMTP email delivery adapter."""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


class SmtpDigestSender:
    """Send multipart email using credentials kept in environment variables."""

    def __init__(self) -> None:
        self._host = self._required("CAREERPILOT_SMTP_HOST")
        self._port = int(os.getenv("CAREERPILOT_SMTP_PORT", "587"))
        self._username = self._required("CAREERPILOT_SMTP_USERNAME")
        self._password = self._required("CAREERPILOT_SMTP_PASSWORD")
        self._sender = self._required("CAREERPILOT_EMAIL_FROM")
        self._recipient = self._required("CAREERPILOT_EMAIL_TO")

    def send(self, subject: str, plain_text: str, html: str) -> None:
        """Deliver an email using STARTTLS."""
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self._sender
        message["To"] = self._recipient
        message.set_content(plain_text)
        message.add_alternative(html, subtype="html")
        with smtplib.SMTP(self._host, self._port, timeout=30) as server:
            server.starttls()
            server.login(self._username, self._password)
            server.send_message(message)

    @staticmethod
    def _required(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise ValueError(f"Missing required environment variable: {name}")
        return value
