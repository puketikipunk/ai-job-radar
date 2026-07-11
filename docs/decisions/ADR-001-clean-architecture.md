# ADR-001: Use Pragmatic Clean Architecture

## Status

Accepted

## Context

CareerPilot needs to integrate multiple job sources, persistence options, email delivery mechanisms, and potentially AI providers. Coupling matching rules to a scraper or database would make changes risky and reduce testability.

## Decision

Organise the code into domain, application, infrastructure, and presentation layers. Define ports at the application boundary for repositories, collectors, email delivery, and scheduling. Infrastructure adapters implement those ports; dependency wiring occurs in the composition root.

## Consequences

Core matching and digest logic can be tested without the network, database, or email service. New collectors and providers can be introduced with limited change. This adds modest interface and wiring overhead, which is justified by the expected integration churn. The approach is pragmatic: do not create abstractions until a meaningful boundary exists.

