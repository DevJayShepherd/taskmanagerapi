# Core
import os

# Imports
from dotenv import load_dotenv
from pathlib import Path


env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_TITLE: str = "Task Manager API"
    PROJECT_VERSION: str = "0.1.0"
    ENVIRONMENT: str = os.getenv('ENVIRONMENT')

    # Settings for domain and protocol
    API_DOMAIN: str = os.getenv("API_DOMAIN")
    API_PROTOCOL: str = os.getenv("API_PROTOCOL")
    BASE_URL = f"{API_PROTOCOL}://{API_DOMAIN}"
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "").split(',')

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings = Settings()
