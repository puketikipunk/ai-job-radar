# Coding Standards

## Python

- Target Python 3.13 and use modern typing syntax.
- Provide type annotations and concise docstrings for public functions, classes, and protocols.
- Prefer immutable value objects and small, focused functions where practical.
- Validate data at boundaries using Pydantic models; do not pass unvalidated scraper output into the domain.
- Do not use bare `except`, mutable default arguments, hidden global state, or `Any` to avoid design work.

## Project structure

Domain entities, application use cases, and ports must not import concrete database, HTTP, email, or CLI code. Infrastructure adapters implement ports. The CLI is a thin composition and presentation layer.

Keep modules cohesive. Name code after the business concept it represents, not a temporary implementation detail. Favour explicit constructor injection over service locators.

## Tests and quality gates

- Write unit tests for domain logic and application services; use fixtures/mocks for HTTP and email boundaries.
- Add regression tests for fixed defects.
- Tests must not contact live job sites or send email by default.
- Run `ruff check`, `ruff format --check`, and `pytest` before considering a change complete.
- Use pre-commit hooks and CI to enforce the same checks.

## Logging and errors

Use structured, contextual logs for run IDs, collector names, job counts, and failures. Never log secrets, full CV content, access tokens, or raw personal data. Raise meaningful domain/application errors; catch exceptions at boundaries where a safe degraded outcome is possible.

## Security and privacy

Keep settings in versioned examples and actual secrets in environment variables or deployment secrets. Add new data collection only when its retention and purpose are documented. Validate URLs and untrusted content before rendering them into emails or a future UI.

