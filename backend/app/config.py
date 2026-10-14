from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "OpsPulse Incident Management API"
    database_url: str = "postgresql+psycopg://opspulse:opspulse@postgres:5432/opspulse"
    environment: str = "production"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
