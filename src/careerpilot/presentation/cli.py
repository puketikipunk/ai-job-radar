"""CareerPilot command-line interface."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import typer

from careerpilot.application.matcher import RuleBasedMatcher
from careerpilot.application.runner import JobRadar
from careerpilot.infrastructure.collectors.greenhouse import GreenhouseCollector
from careerpilot.infrastructure.collectors.lever import LeverCollector
from careerpilot.infrastructure.config import GreenhouseSourceConfig, LeverSourceConfig, load_config
from careerpilot.infrastructure.digest import HtmlDigestRenderer
from careerpilot.infrastructure.email import SmtpDigestSender
from careerpilot.infrastructure.repository import SQLiteJobRepository

app = typer.Typer(help="CareerPilot — responsible, configurable job discovery.", no_args_is_help=True)


def _config_path() -> Path:
    return Path(os.getenv("CAREERPILOT_CONFIG_PATH", "config/profile.yaml"))


def _configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def _collectors(config: object) -> list[object]:
    sources = config.sources
    collectors: list[object] = []
    for source in sources:
        if not source.enabled:
            continue
        if isinstance(source, GreenhouseSourceConfig):
            collectors.append(GreenhouseCollector(source.name, source.board_token))
        elif isinstance(source, LeverSourceConfig):
            collectors.append(LeverCollector(source.name, source.site))
    return collectors


@app.command("validate-config")
def validate_config() -> None:
    """Validate the configured job-search profile without accessing any source."""
    config = load_config(_config_path())
    typer.echo(f"Configuration valid: {len(config.sources)} source(s), minimum score {config.profile.minimum_score}.")


@app.command()
def run(
    dry_run: bool = typer.Option(False, help="Print the digest but do not send email."),
    send_email: bool = typer.Option(False, help="Send the digest through configured SMTP."),
) -> None:
    """Collect, match, deduplicate, store, and optionally deliver jobs."""
    if dry_run and send_email:
        raise typer.BadParameter("Choose either --dry-run or --send-email, not both.")
    _configure_logging()
    config = load_config(_config_path())
    collectors = _collectors(config)
    if not collectors:
        typer.echo("No enabled sources. Add authorised Greenhouse or Lever sources to config/profile.yaml.")
        raise typer.Exit(code=1)
    repository = SQLiteJobRepository(config.storage.sqlite_path)
    result = JobRadar(
        collectors=collectors,
        repository=repository,
        matcher=RuleBasedMatcher(),
        profile=config.profile.to_domain(),
    ).run()
    renderer = HtmlDigestRenderer(config.email.max_jobs_per_digest)
    plain_text, html = renderer.render(result.new_matches)
    typer.echo(plain_text)
    if send_email:
        JobRadar.deliver(
            result,
            renderer,
            SmtpDigestSender(),
            f"{config.email.subject_prefix}: {len(result.new_matches)} new opportunity(s)",
        )
        typer.echo("Email sent." if result.new_matches else "No new matching roles; no email sent.")
    if result.failed_collectors:
        typer.echo(f"Failed sources: {', '.join(result.failed_collectors)}", err=True)
    typer.echo(f"Collected {result.collected} listing(s); new matches: {len(result.new_matches)}.")


@app.command()
def jobs(limit: int = typer.Option(20, min=1, max=100)) -> None:
    """Show recent matching jobs already stored by CareerPilot."""
    config = load_config(_config_path())
    for match in SQLiteJobRepository(config.storage.sqlite_path).recent(limit):
        typer.echo(f"{match.score:3}%  {match.job.company} — {match.job.title} ({match.job.location})\n     {match.job.url}")
