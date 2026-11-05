from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    SECRET_KEY_JWT: str
    REDIS_HOST: str | None = None

    DB_USER: str
    DB_PASS: str
    DB_NAME: str


settings = Settings()
