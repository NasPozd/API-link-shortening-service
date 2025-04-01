from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "your_default_secret_key"
    DATABASE_URL: str = "sqlite:///test.db"
    LOGGING_LEVEL: str = "INFO"

    model_config = ConfigDict(env_file=".env")

settings = Settings()