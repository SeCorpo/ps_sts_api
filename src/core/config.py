import os
from dotenv import load_dotenv

load_dotenv()

SESSION_EXPIRE_TIME_SECONDS: int = int(os.getenv("SESSION_EXPIRE_TIME_SECONDS", "3600"))
SESSION_EXPIRE_TIME_SECONDS_TRUST_DEVICE: int = int(os.getenv("SESSION_EXPIRE_TIME_SECONDS_TRUST_DEVICE", "2592000"))

REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD: str | None = os.getenv("REDIS_PASSWORD")

DB_USER: str | None = os.getenv("DB_USER")
DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
DB_HOST: str | None = os.getenv("DB_HOST")
DB_PORT: str | None = os.getenv("DB_PORT")
DB_NAME: str | None = os.getenv("DB_NAME")
DB_ECHO: bool = os.getenv("DB_ECHO", "false").lower() == "true"

def check_db_env():
    required = ["DB_USER", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing = [v for v in required if not globals()[v]]
    if missing:
        raise RuntimeError(f"Missing DB environment variables: {', '.join(missing)}")

check_db_env()
