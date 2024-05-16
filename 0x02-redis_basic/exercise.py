#!/usr/bin/env python
"""module that implements redis"""

import redis
import uuid
from typing import Union, Callable, Optional
"""
import string
import secrets
"""


def count_calls(method: callable) -> callable:
    """returns a Callable"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorated function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the decorated function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """display the history of calls of a particular function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    # print(f"{function_name} was called {value} times")
    print("{} was called {} times:".format(function_name, value))
    # inputs = r.lrange(f"{function_name}:inputs", 0, -1)
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    # outputs = r.lrange(f"{function_name}:outputs", 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        # print(f"{function_name}(*{input}) -> {output}")
        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    """Cache class for interacting with Redis"""

    def __init__(self):
        """Constructor to initialize the Redis connection"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls  
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the cache and return the stored key
        letters = string.ascii_letters + string.digits
        key = ''.join(secrets.choice(letters) for _ in range(16))"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: optional[callable] = None) -> Union[str, bytes, int, float]:
        """convert the data back to the desired format"""
        val = self._redis.get(key)
        if fn:
            val = fn(val)
        return val
    def get_str(self, key: str) -> str:
