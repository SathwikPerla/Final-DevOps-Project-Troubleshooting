from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SevZero SRE Incident API"
    database_url: str = "postgresql+psycopg://sevzero:sevzero@postgres:5432/sevzero"
    environment: str = "production"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
