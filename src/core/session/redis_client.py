import redis.asyncio as redis
from src.core import get_logger
from src.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
from redis.exceptions import RedisError


logger = get_logger("session.redis_client")

_redis_connection: redis.Redis | None = None

async def get_redis_connection() -> redis.Redis | None:
    """ Return the active Redis connection if already initialized """
    global _redis_connection
    return _redis_connection


async def connect_to_redis():
    """ Initialize the Redis connection at startup"""
    global _redis_connection
    if _redis_connection is None:
        try:
            _redis_connection = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                decode_responses=True,
            )
            await _redis_connection.ping()
            logger.info("Connected to Redis successfully.")
        except RedisError as e:
            logger.error(f"RedisError while connecting: {e}")
            _redis_connection = None
        except Exception as e:
            logger.error(f"Exception during Redis connection: {e}")
            _redis_connection = None


async def close_redis_connection():
    """ Close the Redis connection at shutdown"""
    global _redis_connection
    if _redis_connection:
        await _redis_connection.close()
        _redis_connection = None
        logger.info("Redis connection closed.")
