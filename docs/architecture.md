# Architecture

CareerPilot uses a pragmatic clean architecture. The goal is not ceremonial layering; it is to make collectors, persistence, email delivery, and future AI providers replaceable without rewriting core job-search behaviour.

## Layers

```text
Presentation (CLI / scheduled entry point)
        ↓
Application (orchestration and use cases)
        ↓
Domain (jobs, profiles, scoring rules, value objects)
        ↑
Infrastructure (collectors, SQLite, SMTP, templates, providers)
```

Dependencies point inward. The domain imports no infrastructure libraries. Application services depend on interfaces (ports); infrastructure implements them. The composition root wires implementations together from settings.

## Core concepts

- **Job:** normalised role data, including title, company, location, description, source URL, discovery time, and a stable identity/deduplication key.
- **Profile:** target roles, locations, keywords, exclusions, and delivery preferences loaded from configuration.
- **Collector:** a source-specific adapter returning validated, normalised jobs. Each collector is independently failure-tolerant.
- **Repository:** an interface for persistence and querying; SQLite is the initial adapter.
- **Matcher:** a pure service that filters, scores, and creates human-readable match reasons.
- **Digest service:** selects new qualifying jobs and renders a plain-text/HTML report through an email port.

## Pipeline

1. Load validated configuration and construct dependencies.
2. Run enabled collectors independently.
3. Normalise and validate jobs, then deduplicate against the batch and stored records.
4. Filter and score new jobs against the profile.
5. Persist all appropriate records and their matching evidence.
6. Render and send a digest, or print it in dry-run mode.

## Data and reliability

SQLite is the local development store. The persistence implementation must enforce a unique stable job key and preserve source metadata. A failed collector is logged and reported, but must not discard results from other collectors. Re-running a completed run must not create duplicate jobs or duplicate digest entries.

See the ADRs in [decisions](decisions/) for rationale behind key choices.

