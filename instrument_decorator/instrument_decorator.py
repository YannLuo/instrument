import os
import functools


def instrument_decorator(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with open("trace.log", mode="a", encoding="utf-8") as wf:
                wf.write("Enter#%s#%s#%s\n" %
                         (path, "", func.__name__))
            result = func(*args, **kwargs)
            with open("trace.log", mode="a", encoding="utf-8") as wf:
                wf.write("Exit#%s#%s#%s\n" %
                         (path, "", func.__name__))
            return result
        return wrapper
    return decorator
