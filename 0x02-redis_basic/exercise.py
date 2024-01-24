#!/usr/bin/env python3
"""
 Cache class module
"""

import uuid
from typing import Callable, Union
import redis


class Cache:
    """Create a Cache class."""

    def __init__(self):
        """
        store an instance of the Redis client as a private variable
        flush the instance using
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """set a uuid for a data and cache it"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Union[Callable, None] = None
    ) -> Union[str, bytes, int, float]:
        """get value and pass it to the callable"""
        value = self._redis.get(key)

        if fn is not None:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """parametrize method for getting a string from the cache"""
        return self.get(key, lambda x: x.decode("utf-8"))  # type: ignore

    def get_int(self, key: str) -> int:
        """parametrize method for getting an integer from the cache"""
        return self.get(key, int)  # type: ignore
