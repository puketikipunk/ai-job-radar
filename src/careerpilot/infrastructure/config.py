"""Typed YAML configuration loading."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, ValidationError

from careerpilot.domain.models import SearchProfile


class ProfileConfig(BaseModel):
    """Profile section of the YAML file."""

    name: str
    target_roles: list[str] = Field(min_length=1)
    preferred_locations: list[str] = Field(min_length=1)
    excluded_locations: list[str] = []
    include_keywords: list[str] = []
    exclude_keywords: list[str] = []
    minimum_score: int = Field(default=45, ge=0, le=100)

    def to_domain(self) -> SearchProfile:
        """Map validated configuration to a domain object."""
        return SearchProfile(
            name=self.name,
            target_roles=tuple(self.target_roles),
            preferred_locations=tuple(self.preferred_locations),
            excluded_locations=tuple(self.excluded_locations),
            include_keywords=tuple(self.include_keywords),
            exclude_keywords=tuple(self.exclude_keywords),
            minimum_score=self.minimum_score,
        )


class GreenhouseSourceConfig(BaseModel):
    """A public Greenhouse board source."""

    name: str
    type: Literal["greenhouse"]
    board_token: str
    enabled: bool = True


class LeverSourceConfig(BaseModel):
    """A public Lever board source."""

    name: str
    type: Literal["lever"]
    site: str
    enabled: bool = True


SourceConfig = GreenhouseSourceConfig | LeverSourceConfig


class StorageConfig(BaseModel):
    """Storage settings."""

    sqlite_path: Path = Path("data/careerpilot.sqlite3")


class EmailConfig(BaseModel):
    """Digest presentation settings (credentials stay in environment variables)."""

    subject_prefix: str = "CareerPilot"
    max_jobs_per_digest: int = Field(default=15, ge=1, le=100)


class AppConfig(BaseModel):
    """Whole application configuration."""

    profile: ProfileConfig
    sources: list[SourceConfig] = []
    storage: StorageConfig = StorageConfig()
    email: EmailConfig = EmailConfig()


def load_config(path: Path) -> AppConfig:
    """Load and validate YAML configuration from a local path."""
    with path.open("r", encoding="utf-8") as config_file:
        raw = yaml.safe_load(config_file) or {}
    try:
        return AppConfig.model_validate(raw)
    except ValidationError as error:
        raise ValueError(f"Invalid configuration in {path}: {error}") from error
