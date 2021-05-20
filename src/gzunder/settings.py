from pydantic import BaseSettings


class Settings(BaseSettings):
    pg_user: str
    pg_pass: str
    pg_db: str
    pg_host: str
    pg_port: int

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
