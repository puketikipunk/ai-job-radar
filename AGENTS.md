# CareerPilot — Agent Guide

CareerPilot is the application name; `ai-job-radar` remains the repository name. The product helps experienced technology professionals discover, assess, and manage relevant job opportunities.

## Working agreement

Before making a change, read `PROJECT.md`, `ROADMAP.md`, and the relevant files in `docs/`. Treat the architecture decision records in `docs/decisions/` as binding unless the task explicitly changes a decision.

Work in small, coherent increments. Inspect the existing code before proposing a design. Explain the approach, implement it, run the relevant checks, and report the files changed and verification performed. Do not make unrelated refactors or overwrite user changes.

## Engineering principles

- Optimise for useful, reliable daily job discovery before speculative product features.
- Keep domain and application logic independent of HTTP clients, databases, email providers, and web frameworks.
- Prefer composition, explicit dependencies, and small interfaces over inheritance and global state.
- Add dependencies only when their value exceeds their maintenance cost.
- Use configuration and secrets through environment variables; never commit credentials, CVs, personal contact data, or database contents.
- Collect only from sources that are publicly accessible and permitted by their terms or documented APIs/feeds. Do not automate LinkedIn or bypass access controls.

## Implementation expectations

- Python 3.13 with complete type hints for public APIs.
- Use `ruff` and `pytest`; add focused tests with new behaviour.
- Keep side effects at the infrastructure edge. Domain code should be deterministic and straightforward to unit test.
- Log operational events and failures with useful context, never sensitive values.
- Make collectors idempotent and normalise their output into a shared job model.
- Preserve a clear audit trail: source URL, discovery time, and a stable deduplication key for each job.

## Delivery constraints

The initial release is a scheduled CLI workflow and email digest, not a dashboard or autonomous application-submission bot. A feature that expands data collection, sends external communication, or introduces AI costs requires explicit configuration and documentation.

