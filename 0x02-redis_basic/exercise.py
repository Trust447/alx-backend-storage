#!/usr/bin/env python
"""module that implements redis"""

import redis
import uuid
from typing import Union, Callable, Optional
"""
import string
import secrets
"""


class Cache:
    """Cache class for interacting with Redis"""

    def __init__(self):
        """Constructor to initialize the Redis connection"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the cache and return the stored key
        letters = string.ascii_letters + string.digits
        key = ''.join(secrets.choice(letters) for _ in range(16))"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(key: str, fn: optional[callable] = None) -> Union[
            str, bytes, int, float]:
        """convert the data back to the desired format"""
        val = self._redis.get(key)
        if fn:
            val = fn(val)
        return val
