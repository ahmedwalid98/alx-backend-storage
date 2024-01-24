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
