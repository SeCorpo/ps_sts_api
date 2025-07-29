import random
import string
from typing import Any, Optional
from pydantic import ValidationError
from src.core import get_logger
from src.core.session import get_redis_connection
from src.core.config import SESSION_EXPIRE_TIME_SECONDS, SESSION_EXPIRE_TIME_SECONDS_TRUST_DEVICE
from src.core.session import SessionDataObject

logger = get_logger("session.service.session_base_crud")

async def read_session(key: str) -> SessionDataObject | None:
    """ Get session data from Redis and reset its expiration """
    connection = await get_redis_connection()
    if connection is None:
        logger.error(f"Redis connection not available for key '{key}'")
        return None

    try:
        session_data = await connection.hgetall(key)
        if not session_data:
            logger.info(f"No session data found for key '{key}'")
            return None

        obj = SessionDataObject(**session_data)
        await _reset_session_expiration(key, trust_device=obj.trust_device)
        return obj
    except ValidationError as e:
        logger.error(f"Invalid session data for key '{key}': {e}")
    except Exception as e:
        logger.error(f"Error getting session data for key '{key}': {e}")
    return None


async def set_session(session_data: SessionDataObject, key: Optional[str] = None) -> bool:
    """ Save session data to Redis and set expiration, create new session and key if key is None """
    connection = await get_redis_connection()
    if connection is None:
        logger.error(f"Redis connection not available for key '{key}'")
        return False

    try:
        if key is None:
            key = await _generate_random_key()

        data_dict = {k: str(v) for k, v in session_data.model_dump(exclude_unset=True).items()}
        if not data_dict:
            logger.warning(f"No data to set for key '{key}'")
            return False

        await connection.hset(key, mapping=data_dict)
        await _reset_session_expiration(key, trust_device=session_data.trust_device)
        logger.info(f"Session '{key}' set with fields: {list(data_dict.keys())}")
        return True
    except Exception as e:
        logger.error(f"Error setting session data for key '{key}': {e}")
        return False
    #  todo: check for if sessions exist for same computer
    #  todo: find way to only call _reset_session_expiration if updating, not creating, maybe


async def update_session(key: str, updates: dict[str, Any]) -> bool:
    """ Update fields in an existing session and reset its expiration """
    session_data = await read_session(key)
    if session_data is None:
        logger.warning(f"No session found for key '{key}'")
        return False

    if not updates:
        logger.warning(f"No updates for session key '{key}'")
        return False

    try:
        updated_session_data = session_data.model_copy(update=updates)
        updated = await set_session(updated_session_data, key)
        if updated:
            logger.info(f"Session '{key}' updated with: {list(updates.keys())}")
        return updated
    except ValidationError as e:
        logger.error(f"Invalid session data format for key '{key}': {e}")
        return False
    except Exception as e:
        logger.error(f"Error updating session data for key '{key}': {e}")
        return False


async def delete_session(key: str) -> bool:
    """ Delete a session from Redis """
    connection = await get_redis_connection()
    if connection is None:
        logger.error(f"Redis connection not available for key '{key}'")
        return False

    try:
        deleted = await connection.delete(key)
        if deleted:
            logger.info(f"Session '{key}' deleted.")
            return True
        else:
            logger.info(f"Session '{key}' not found to delete.")
            return False
    except Exception as e:
        logger.error(f"Error deleting session for key '{key}': {e}")
        return False


async def _reset_session_expiration(key: str, trust_device: bool) -> None:
    """ Reset the session's expiration time in Redis """
    connection = await get_redis_connection()
    if connection is None:
        logger.error(f"Redis connection not available for key '{key}'")
        return

    expire_time = (
        SESSION_EXPIRE_TIME_SECONDS_TRUST_DEVICE
        if trust_device
        else SESSION_EXPIRE_TIME_SECONDS
    )
    try:
        await connection.expire(key, expire_time)
        logger.debug(f"Expiration for session '{key}' set to {expire_time}s.")
    except Exception as e:
        logger.error(f"Error setting expiration for key '{key}': {e}")


async def _generate_random_key(length: int = 16) -> str | None:
    """ Generates a unique, random alphanumeric session key """
    logger.info("Generating random key for session key")
    conn = await get_redis_connection()
    if conn is None:
        logger.error("Redis connection not available")
        return None

    letters_and_digits = string.ascii_letters + string.digits

    while True:
        key = ''.join(random.choice(letters_and_digits) for _ in range(length))
        exists = await conn.exists(key)
        if not exists:
            return key
