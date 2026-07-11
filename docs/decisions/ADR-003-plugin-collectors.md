# ADR-003: Use Plugin-Style Collector Adapters

## Status

Accepted

## Context

Job sources differ in data shape, reliability, access method, and terms of use. A monolithic collector would make failures hard to isolate and adding a company source unnecessarily risky.

## Decision

Define a shared collector port that returns normalised job candidates and source metadata. Implement each approved source as an independent infrastructure adapter, enabled through configuration. Each collector owns only retrieval and source-to-domain mapping; filtering, scoring, deduplication, and persistence are shared application concerns.

## Consequences

Sources can be added, disabled, tested with fixtures, and retried independently. A broken source will not break the whole digest. The project must maintain versioned fixtures and clear source documentation, and it must avoid treating a plugin interface as permission to scrape disallowed sites.

