from __future__ import annotations
from typing import Any, Callable, Optional, List, Awaitable, Union
from redis.asyncio import Redis, RedisError
from redis.asyncio.lock import Lock as RedisLock
from redis.typing import FieldT
import logging

from .connection_manager import RedisConnectionManager

logger = logging.getLogger(__name__)


class AsyncRedisClient:
    def __init__(self, namespace: str, connection_manager: RedisConnectionManager):
        self.namespace = namespace
        self._pool = connection_manager.get_pool()
        self._lock = None
        self._conn = None

    def __await__(self):
        return self.init().__await__()

    async def init(self) -> AsyncRedisClient:
        """
        Lazily initialize the Redis connection.
        """
        try:
            self._conn = await Redis(connection_pool=self._pool)
            self._lock = RedisLock(self._conn, f"{self.namespace}:lock")
            logger.debug(
                f"Initialized Redis connection for namespace {self.namespace}")
        except RedisError as e:
            logger.error(
                f"Error initializing Redis connection for {self.namespace}: {str(e)}")
            raise
        return self

    async def close(self) -> None:
        """
        Explicitly close the Redis connection for this client.
        """
        if self._conn:
            try:
                await self._conn.aclose()
                logger.info(
                    f"Closed Redis connection for namespace {self.namespace}")
            except RedisError as e:
                logger.error(
                    f"Error closing Redis connection for {self.namespace}: {str(e)}")
            finally:
                self._conn = None  # Ensure the connection is marked as closed

    async def __aenter__(self) -> AsyncRedisClient:
        if self._conn is None:
            await self.init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._conn:
            await self._conn.aclose()

    async def set(self, key: str, value: Any, ex: Optional[int] = None) -> None:
        async with self._lock:
            try:
                await self._conn.set(key, value, ex=ex)
                logger.debug(f"Set key {key} in namespace {self.namespace}")
            except RedisError as e:
                logger.error(
                    f"Error setting key {key} in Redis for {self.namespace}: {str(e)}")

    async def get(self, key: str) -> Optional[str]:
        try:
            value = await self._conn.get(key)
            logger.debug(f"Got key {key} in namespace {self.namespace}")
            return value
        except RedisError as e:
            logger.error(
                f"Error getting key {key} in Redis for {self.namespace}: {str(e)}")
            return None

    async def keys(self, pattern: str) -> List[str]:
        try:
            keys = await self._conn.keys(pattern)
            logger.debug(
                f"Got keys matching pattern {pattern} in namespace {self.namespace}")
            return keys
        except RedisError as e:
            logger.error(
                f"Error getting keys matching pattern {pattern} in Redis for {self.namespace}: {str(e)}")
            return []

    async def publish(self, channel: str, message: Any) -> None:
        try:
            await self._conn.publish(channel, message)
            logger.debug(
                f"Published message to channel {channel} in namespace {self.namespace}")
        except RedisError as e:
            logger.error(
                f"Error publishing message to channel {channel} in Redis for {self.namespace}: {str(e)}")

    async def subscribe(self, channel: str, callback: Callable[[Any], None]) -> None:
        try:
            async with self._conn.pubsub() as pubsub:
                await pubsub.subscribe(channel)
                logger.info(
                    f"Subscribed to channel: {channel} in namespace {self.namespace}")

                async for message in pubsub.listen():
                    if message['type'] == 'message':
                        logger.debug(
                            f"Received message from {channel} in namespace {self.namespace}: {message['data']}")
                        await callback(message['data'])
        except RedisError as e:
            logger.error(
                f"Error subscribing to channel {channel} in Redis for {self.namespace}: {str(e)}")

    async def sadd(self, key: str, *values: FieldT) -> Union[Awaitable[int], int]:
        async with self._lock:
            try:
                await self._conn.sadd(key, *values)
                logger.debug(
                    f"Added {values} to set {key} in namespace {self.namespace}")
            except RedisError as e:
                logger.error(
                    f"Error adding value to set {key} in Redis for {self.namespace}: {str(e)}")
