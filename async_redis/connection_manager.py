from typing import Dict
from redis.asyncio import BlockingConnectionPool, RedisError
import logging

from .utils import SingletonMeta

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RedisConnectionManager(metaclass=SingletonMeta):
    """
    Manages Redis connection pooling.
    """

    def __init__(self, host='localhost', port=6379, db=0, max_connections=10):
        self.pool = BlockingConnectionPool(
            host=host, port=port, db=db,
            max_connections=max_connections,
            decode_responses=True
        )

    def get_pool(self) -> BlockingConnectionPool:
        return self.pool

    async def close(self) -> None:
        """
        Close the Redis connection pool.
        """
        try:
            if self.pool:
                await self.pool.disconnect()
                logger.info("Closed Redis connection pool")
        except RedisError as e:
            logger.error(f"Error closing Redis connection pool: {str(e)}")
