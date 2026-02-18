from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SESSION_ID_EXPIRE_DAYS: int = 1
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str
    PROJECT_NAME: str
    DEBUG: bool

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    ALGORITHM: str = "HS256"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
