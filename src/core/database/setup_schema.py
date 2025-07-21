from sqlalchemy.exc import SQLAlchemyError, OperationalError
from src.core.database import engine
from src.core.base import Base
from src.core import get_logger

logger = get_logger("database.setup_schema")

async def setup_schema() -> None:
    logger.info("Starting table creation (if missing)...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created successfully (if missing).")
    except OperationalError as e:
        logger.error(f"Database operational error during table creation: {e}")
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error during table creation: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during table creation: {e}")