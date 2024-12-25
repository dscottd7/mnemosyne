from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # Environment-specific settings
    ENVIRONMENT: str = "development"
    PORT: int = int(os.getenv("PORT", 8000))
    
    # API Keys and external service configuration
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENV: str
    PINECONE_INDEX_NAME: str
    PINECONE_HOST: str

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
