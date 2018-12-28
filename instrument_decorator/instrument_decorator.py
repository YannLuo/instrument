import functools


def instrument_decorator(path, type_):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tmp = ""
            if type_.lower() == "function":
                tmp = "#%s#%s#%s" % (path, "", func.__name__)
            elif type_.lower() == "method":
                self = args[0]
                tmp = "#%s#%s#%s" % (path, self.__class__.__name__, func.__name__)
            with open("trace.log", mode="a", encoding="utf-8") as wf:
                wf.write("Enter%s\n" % (tmp, ))
            result = func(*args, **kwargs)
            with open("trace.log", mode="a", encoding="utf-8") as wf:
                wf.write("Exit%s\n" % (tmp, ))
            return result
        return wrapper
    return decorator
