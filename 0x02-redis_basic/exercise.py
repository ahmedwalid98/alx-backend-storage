#!/usr/bin/env python3
"""
 Cache class module
"""

import uuid
from functools import wraps
from typing import Any, Callable, Union
import redis


def count_calls(method: Callable) -> Callable:
    '''
        Counts the number of times a method is called.
    '''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
            Wrapper function.
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of inputs and
    outputs for a particular function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):  # sourcery skip: avoid-builtin-shadow
        """ Wrapper for decorator functionality """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    # sourcery skip: use-fstring-for-concatenation, use-fstring-for-formatting
    """
    Replays the history of a function
    Args:
        method: The function to be decorated
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


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
