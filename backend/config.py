"""
COREP Reporting Assistant - Configuration
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # ChromaDB Configuration
    chroma_persist_directory: str = "./data/chroma_db"
    
    # Application Settings
    app_name: str = "COREP Reporting Assistant"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
