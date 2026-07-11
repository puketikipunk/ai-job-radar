# CareerPilot Roadmap

This roadmap is outcome-led rather than date-led. Complete and verify each phase before broadening scope.

## Phase 1 — Foundation

- Repository tooling, configuration, logging, and local developer workflow.
- Shared job domain model, persistence boundary, and SQLite implementation.
- Collector, scoring, email, and scheduler interfaces.
- CLI command that can run a complete pipeline against deterministic test data.

## Phase 2 — Trusted discovery

- Add a small set of permitted, maintainable company/ATS collectors.
- Normalise, validate, deduplicate, and persist discovered roles.
- Record source, retrieval timestamp, and collector status.
- Provide source-level error isolation and tests using fixtures.

## Phase 3 — Transparent matching and digest

- Configuration-driven role, location, skill, and exclusion rules.
- Explainable score and reason codes for each recommendation.
- HTML and plain-text email digest containing only new qualifying roles.
- Local dry-run mode and safe SMTP/provider configuration.

## Phase 4 — Scheduled deployment

- GitHub Actions scheduled workflow and manual dispatch.
- Encrypted repository secrets, persistent data strategy, and operational documentation.
- Monitoring through workflow logs and failure notification.

## Phase 5 — Assisted job-search workflow

- Application status tracking and notes.
- Optional AI scoring for shortlisted roles, with cost controls and clear fallbacks.
- Human-reviewed CV, cover-letter, outreach, and interview-prep generation.

## Phase 6 — Product evolution

- Read-only dashboard and analytics.
- Profile feedback signals to refine rankings.
- Additional users or profiles only after privacy, tenancy, and consent requirements are designed.

