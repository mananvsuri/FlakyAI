"""Application configuration."""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "FlakeGuard AI"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./flakeguard.db"
    
    # Directories
    MODEL_DIR: Path = Path("../models")
    EXPERIMENT_DIR: Path = Path("../experiments")
    DATASET_DIR: Path = Path("../datasets")
    
    # Upload limits
    MAX_UPLOAD_SIZE_MB: int = 100
    
    # ML Configuration
    RANDOM_SEED: int = 42
    MIN_EXECUTIONS_FOR_PREDICTION: int = 5
    
    # Optional LLM
    OPENAI_API_KEY: str = ""
    ENABLE_LLM_RECOMMENDATIONS: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
settings.MODEL_DIR.mkdir(parents=True, exist_ok=True)
settings.EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
settings.DATASET_DIR.mkdir(parents=True, exist_ok=True)
