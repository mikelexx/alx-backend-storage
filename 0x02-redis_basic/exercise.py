#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method,
store an instance of the Redis client as a private
variable named _redis (using redis.Redis()) and
flush the instance using flushdb.

Create a store method that takes a data argument and
returns a string. The method should generate a random
key (e.g. using uuid), store
the input data in Redis using the random key and
return the key.

Type-annotate store correctly. Remember that data can
be a str, bytes, int
"""
import redis
import uuid
from functools import wraps
from typing import Callable, List, Union, Any


def count_calls(method: Callable) -> Callable:
    """
    counts number of times the method is called
    """

    @wraps(method)
    def increment(self, data):
        self.incr(method.__qualname__)
        return method(self, data)

    return increment


def call_history(method: Callable) -> Callable:
    """
     stores the history of inputs and outputs for a particular function.
    """

    @wraps(method)
    def wrapper(*args):
        l_input = method.__qualname__ + ":inputs"
        l_output = method.__qualname__ + ":outputs"
        self = args[0]
        self.rpush(l_input, str(args[1::]))
        out = method(*args)
        self.rpush(l_output, str(out))
        return out

    return wrapper


class Cache:
    """
    basis for my redis client
    """

    def __init__(self) -> None:
        """
        initializes a clean db together with a client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def rpush(self, list_name, *values):
        self._redis.rpush(list_name, *values)

    def incr(self, key):
        """
        increments value of the key by 1 whenever called
        """
        self._redis.incr(key)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores data provided in redis using a random key
        """
        rand_key: str = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str, fn: Union[Callable, None] = None) -> Any:
        """
        take a key string argument and an optional Callable
        argument named fn. This callable will be used
        to convert the data back to the desired format.
        """
        val = self._redis.get(key)
        if val is None:
            return None
        return fn(val) if fn else val

    def get_str(self, key: str) -> str:
        """
        parameterizes get with str to convert result to
        string type
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        parameterizes get with integer to convert result
        to integer type
        """
        return self.get(key, lambda x: int(x.decode('utf-8')))
