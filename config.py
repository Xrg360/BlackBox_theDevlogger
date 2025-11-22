"""
Blackbox Configuration Management
Loads settings from environment variables with sensible defaults
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./devbox.db")

# CLI Configuration
BLACKBOX_API_URL = os.getenv("BLACKBOX_API_URL", "http://localhost:8000")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Project Root
PROJECT_ROOT = Path(__file__).parent
