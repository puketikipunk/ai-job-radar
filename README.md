# CareerPilot

CareerPilot is a personal, configurable job radar. It collects roles from permitted public ATS feeds, removes duplicates, explains how a role matches your search profile, stores what it has seen, and can send an email digest of new opportunities.

The first profile is set up for an Ireland-based Engineering Project Manager / Technical Program Manager search. It is deliberately configuration-driven: change `config/profile.yaml` rather than changing code.

## What works in v0.1

- Greenhouse and Lever public-job-board collectors.
- Transparent title, location, skill, and exclusion scoring.
- SQLite persistence and repeat-safe deduplication.
- Terminal digest, dry-run mode, and optional SMTP email delivery.
- Scheduled GitHub Actions workflow, ready once secrets and durable storage are configured.

It intentionally does not scrape LinkedIn, Indeed, IrishJobs, or Jobs.ie. Those sites' automation rules and access patterns are not a stable or responsible foundation. Add company ATS feeds, public RSS feeds, or a licensed job-search API instead.

## Quick start

```bash
cd /Users/ozlemirkli/Documents/Codex/ai-job-radar
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp .env.example .env
cp config/profile.example.yaml config/profile.yaml
careerpilot validate-config
careerpilot run --dry-run
```

Add real, authorised source board identifiers in `config/profile.yaml`, then run `careerpilot run`. The first run records matching roles; subsequent runs show only new matches in the digest.

## Email setup

Set `CAREERPILOT_SMTP_*`, `CAREERPILOT_EMAIL_FROM`, and `CAREERPILOT_EMAIL_TO` in `.env`. For Outlook/Hotmail, use an app password if your account requires it. Test safely with `careerpilot run --dry-run`; use `careerpilot run --send-email` only after checking the terminal digest.

## Commands

```bash
careerpilot validate-config
careerpilot run --dry-run
careerpilot run --send-email
careerpilot jobs --limit 20
```

## Deployment

See [docs/deployment.md](docs/deployment.md). GitHub Actions runners are ephemeral, so configure durable storage before enabling a scheduled email digest. Do not put SMTP credentials in the repository.

