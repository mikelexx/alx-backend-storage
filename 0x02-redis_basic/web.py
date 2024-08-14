#!/usr/bin/env python3
"""
n this tasks, we will implement a get_page
function (prototype: def get_page(url: str) -> str:).
The core of the function is very simple. It uses the
requests module to obtain the HTML content of a particular
URL and returns it.

Start in a new file named web.py and do not reuse the
code written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.
"""
import requests
import redis
from functools import wraps
from typing import Callable


def count_url_calls(method: Callable) -> Callable:
    """
    tracks how many times a particular URL was accessed in
    the key "count:{url}" and cache
    the result with an expiration time of 10 seconds.
    """
    r = redis.Redis()

    @wraps(method)
    def wrapper(url):
        key = f'count:{url}'
        if not r.get(key):
            r.set(key, 0)
        r.incr(key)
        cached_res = r.get(f'cached:{url}')
        print(r.get(key))
        if cached_res:
            return cached_res.decode('utf-8')
        r.set(f'catched:{url}', 10, method(url))

    return wrapper


@count_url_calls
def get_page(url: str) -> str:
    """
    uses the requests module to obtain the HTML content of
    a particular URL and returns it.
    """
    try:
        return requests.get(url).text
    except Exception as e:
        print(f"error occured: {e}")
        return str(e)
