# ADR-002: Adopt a Lightweight Python Tooling Stack

## Status

Accepted

## Context

The first release is a scheduled CLI application, not a web platform. It needs reliable validation, persistence, HTTP access, templating, tests, and automated quality checks while remaining approachable on macOS and GitHub Actions.

## Decision

Use Python 3.13 with Pydantic v2 for boundary validation, SQLModel/SQLAlchemy-compatible persistence, Typer for the CLI, Rich for terminal output, Jinja2 for email templates, PyYAML for user-editable configuration, httpx for HTTP, pytest for tests, and Ruff for linting and formatting. Keep dependencies minimal and select a structured logging library only when its value is demonstrated.

## Consequences

This stack supports typed, testable code with a small operational footprint. SQLite is appropriate for local development but does not solve persistent scheduled-run state in GitHub Actions; production persistence remains a deployment decision. Browser automation is intentionally excluded until a permitted, stable use case requires it.

