"""Get settings from `.env` file."""
from pathlib import Path
from typing import Dict

from fqdn import FQDN  # type: ignore[import]
from pydantic import BaseSettings
from pydantic import conint
from pydantic import constr
from pydantic import validator
from ruamel.yaml import YAML


class Settings(BaseSettings):
    """Validated settings, loaded from `.env`."""

    pg_user: str
    pg_pass: str
    pg_db: str
    pg_host: str
    pg_port: conint(ge=0, le=65535)  # type: ignore
    tg_token: str
    tg_id_keril: int
    tg_id_lesha: int

    # TODO add `pg_url: PostgresDsn` computed field
    # when https://github.com/samuelcolvin/pydantic/pull/2625 ready

    # TODO Fix conint: https://github.com/samuelcolvin/pydantic/issues/239

    @validator("pg_host")
    def pg_host_is_fqdn(cls, v: str) -> str:
        """Validate pg_host is a valid FQDN."""
        assert FQDN(v).is_valid, "pg_host is not a valid FQDN"
        return v

    class Config:
        """Config settings."""

        env_file = ".env"


class Talks(BaseSettings):
    """Bot's text messages."""

    meet: Dict[constr(regex=r"^[a-z_]*$"), str]  # type: ignore
    my: Dict[constr(regex=r"^[a-z_]*$"), str]  # type: ignore


settings = Settings()
talks = Talks(**YAML(typ="safe").load(Path("talks.yaml")))


TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{settings.pg_user}:{settings.pg_pass}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db}"
    },
    "apps": {
        "models": {
            "models": ["gzunder.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
