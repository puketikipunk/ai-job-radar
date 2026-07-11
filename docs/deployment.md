# Deployment Philosophy

CareerPilot should be deployable without operating a server. The initial target is a scheduled GitHub Actions workflow, with manual dispatch for testing and a local CLI workflow for development.

## Configuration and secrets

Commit a safe configuration template and `.env.example`; never commit `.env`, credentials, recipient email addresses, API keys, or real job-search data. Store delivery credentials and any future AI keys as GitHub Actions secrets. Use separate development and production settings where needed.

## Scheduling

Use a workflow schedule expressed in UTC and document the Ireland-time expectation, including daylight-saving implications. The workflow must also support `workflow_dispatch` and a dry-run mode. Scheduled workflows are best-effort; review logs and add failure notifications before treating the system as unattended.

## State and persistence

GitHub Actions runners are ephemeral. Do not assume a local SQLite file survives between scheduled runs. Before enabling production email, choose and document a durable state store (for example, a managed database or deliberately versioned encrypted state) that prevents repeat alerts. The choice must preserve privacy and provide a backup/recovery path.

## Release practice

Run linting and tests in CI on pull requests and the default branch. Deploy only from a tested default branch. Use least-privilege tokens, pin action versions, and review dependency updates. A deployment change must include a rollback plan and an operational verification step.

