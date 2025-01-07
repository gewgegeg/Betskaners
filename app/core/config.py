from typing import List
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./betskaners.db")

    # Application
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

    # API Settings
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")

    # Match Update Settings
    LIVE_UPDATE_INTERVAL: int = int(os.getenv("LIVE_UPDATE_INTERVAL", "30"))
    MATCH_CLEANUP_INTERVAL: int = int(os.getenv("MATCH_CLEANUP_INTERVAL", "86400"))

    # Prediction Settings
    MIN_MATCHES_FOR_PREDICTION: int = int(os.getenv("MIN_MATCHES_FOR_PREDICTION", "5"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.75"))

settings = Settings() 