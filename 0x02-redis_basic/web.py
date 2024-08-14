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

r = redis.Redis()


def count_url_calls(method: Callable) -> Callable:
    """
    tracks how many times a particular URL was accessed in
    the key "count:{url}" and cache
    the result with an expiration time of 10 seconds.
    """

    @wraps(method)
    def wrapper(url):
        key = f'count:{url}'
        r.incr(key)
        cached_res = r.get(f'cached:{url}')
        if cached_res:
            return cached_res.decode('utf-8')
        res = method(url)
        r.set(f'catched:{url}', 10, res)
        return res

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
