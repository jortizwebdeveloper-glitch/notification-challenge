from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    SECRET_KEY_JWT: str

    DB_USER: str
    DB_PASS: str
    DB_NAME: str


settings = Settings()
