from pydantic import BaseSettings, PostgresDsn, validator, conint
from fqdn import FQDN  # type: ignore[import]


class Settings(BaseSettings):
    pg_user: str
    pg_pass: str
    pg_db: str
    pg_host: str
    pg_port: conint(ge=0, le=65535)  # type: ignore
    tg_token: str

    # TODO add `pg_url: PostgresDsn` computed field
    # when https://github.com/samuelcolvin/pydantic/pull/2625 ready

    # TODO Fix conint: https://github.com/samuelcolvin/pydantic/issues/239

    @validator("pg_host")
    def pg_host_is_fqdn(cls, v: str) -> str:
        assert FQDN(v).is_valid, "pg_host is not a valid FQDN"
        return v

    class Config:
        env_file = ".env"


settings = Settings()


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
