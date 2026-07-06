from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str
    port: int
    db: int
    username: str | None = None
    password: str | None = None
    ssl: bool = False
    ssl_cert_reqs: str = "required"


class Settings(BaseSettings):
    bot_token: str
    db_dsn: str
    redis: RedisSettings

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_nested_delimiter": "__",
        "extra": "ignore",
    }


config = Settings()  # type: ignore
