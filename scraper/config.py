"""Configuration from environment variables."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Database (Supabase / PostgreSQL)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Supabase direct connection string (alternative to individual fields)
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Scraper settings
CONCURRENT_REQUESTS = int(os.getenv("CONCURRENT_REQUESTS", "10"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
