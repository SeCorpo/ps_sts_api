from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.exc import ArgumentError
from src.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_ECHO
from src.core import get_logger


logger = get_logger("database.engine")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
