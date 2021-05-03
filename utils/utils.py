import inspect
from typing import Any


def funcname():
    return inspect.currentframe().f_back.f_code.co_name


def default_repr(instance: Any) -> str:
    """
    Returns a default string for an instance's __repr__ function, using all attribute key, value pairs in vars(instance).

    instance: Any instantiated object

    :returns: str
    """
    return f"""{type(instance).__name__}({', '.join([f'{key}={val}' for key, val in vars(instance).items()])})"""
