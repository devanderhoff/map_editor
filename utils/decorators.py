#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# utils/debuggers.py
import functools
import time

from utils.log import get_logger

logger = get_logger(__name__)


def debugmethod(func):
    """ Debug a method and return it back"""

    # Gejat van https://tech.serhatteker.com/post/2019-07/python-debug-decorators/

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)

        logger.debug(f'Calling : {func.__name__}')
        logger.debug(f'args, kwargs: {args, kwargs}')
        logger.debug(f'{func.__name__} returned {return_value}')

        return return_value

    return wrapper


def timerun(func):
    """ Calculate the execution time of a method and return it back"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start

        logger.debug(f"Duration of {func.__name__} function was {duration}.")
        return result

    return wrapper
