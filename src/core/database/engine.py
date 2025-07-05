import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.exc import ArgumentError
from src.core.utils.logger import get_logger

load_dotenv()

DB_USER: str | None = os.getenv("DB_USER")
DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
DB_HOST: str | None = os.getenv("DB_HOST")
DB_PORT: str | None = os.getenv("DB_PORT")
DB_NAME: str | None = os.getenv("DB_NAME")
DB_ECHO: bool = os.getenv("DB_ECHO", "false").lower() == "true"

logger = get_logger("database.engine")

missing_vars = [v for v in ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"] if not locals()[v]]
if missing_vars:
    logger.error(f"Missing database environment variables: {', '.join(missing_vars)}")
    raise RuntimeError(f"Missing DB environment variables: {', '.join(missing_vars)}")

DATABASE_URL: str = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

try:
    engine: AsyncEngine = create_async_engine(
        DATABASE_URL,
        echo=DB_ECHO,
        future=True,
    )
    logger.info("Async engine created successfully.")
except ArgumentError as e:
    logger.error(f"SQLAlchemy ArgumentError (bad connection string?): {e}")
    raise
except ImportError as e:
    logger.error(f"ImportError (is asyncpg installed?): {e}")
    raise
except Exception as e:
    logger.error(f"Failed to create async engine: {e}")
    raise

