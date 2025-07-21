from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from src.core.database import AsyncSessionLocal
from src.core import get_logger

logger = get_logger("database.test_connection")

async def test_connection() -> None:
    async with AsyncSessionLocal() as session:
        try:
            await session.execute(text('SELECT 1'))
            # await session.commit()
            logger.info("Successfully connected to the database.")
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error during connection test: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during DB connection test: {e}")
