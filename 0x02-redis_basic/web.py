#!/usr/bin/env python3
"""Module to implement a get_page function that caches HTML content."""

import redis
import requests
from functools import wraps


r = redis.Redis()


def url_access_count(method):
    """Decorator to track URL access and cache HTML content."""
    @wraps(method)
    def wrapper(url):
        """Wrapper function to handle caching and counting."""
        cache_key = "cached:" + url
        count_key = "count:" + url

        cached_value = r.get(cache_key)
        if cached_value:
            return cached_value.decode("utf-8")

        html_content = method(url)
        r.incr(count_key)
        r.set(cache_key, html_content, ex=10)
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":

    print(get_page('http://slowwly.robertomurray.co.uk'))
