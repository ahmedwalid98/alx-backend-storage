#!/usr/bin/env python3
"""
module
"""

import uuid
from typing import Callable, Union
import redis


class Cache:
    """class"""
    def __init__(self):
        """ constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def storage(self, data: Union[str, bytes, int, float]) -> str:
        """ store data to redis """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
