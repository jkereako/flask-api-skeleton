#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~
    Utility methods.
    I'm including this file in the skeleton because it contains methods I've
    found useful.

    The goal is to keep this file as lean as possible.

    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
from flask import request
import app

def prepare_json_response(success, message, data):
    response = {"meta":{"success":success, "request":request.url}}
    if data:
        response["data"] = data
        response["meta"]["data_count"] = len(data)

    if message:
        response["meta"]["message"] = message

    return response

def fetch_cached_data(args=None):
    """
    Retrieves a cache object when given an optional cache key.
    Because most cache keys within this app are URL dependent, the
    code which retrieves the cache has been refactored here to maximize
    consistency.
    :param cache_key: The identifier for the cache object. This must be unique
    :type cache_key: str
    :returns: A dictionary of JSON data
    :rtype: dict
    """
    cache_key = request.base_url

    if args:
        cache_key += args

    cache_key = sha224(cache_key).hexdigest()

    rv = cache.get(cache_key)

    # if rv is not None:
    #     rv = "<!-- served from cache -->" + rv
    return rv

def cache_data(data, args=None, timeout=None):
    """
    Stores data in the application cache using the base URL as the main
    cache key.
    To prevent all URLs from being cached, such as
    /teams/nba?this_is_not_a_real_param=2
    The base URL along with optional arguments are used. This ensures
    that URLS passed with arbitrary query string arguments will not
    break the cache.
    Because most cache keys within this app are URL dependent, the
    code which stores the cache has been refactored here to maximize
    consistency.
    :param data: The data object to cache
    :type data: dict
    :param cache_key: The identifier for the cache object. This must be unique
    :type cache_key: str
    :param timeout: The expiry for the cache
    :type timeout: int
    :returns: None
    :rtype: None
    """
    cache_key = request.base_url

    if args:
        cache_key += args

    cache_key = sha224(cache_key).hexdigest()

    timeout = app.config["CACHE_TIMEOUT"] if timeout is None else timeout

    cache.set(cache_key, data, timeout)
