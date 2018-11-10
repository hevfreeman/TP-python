
# ВЕРНИ В TIMEIT reutrn функции
from functools import wraps



def when(func):
    print("[when]")
    self.list_when.append(func)
    return None


def then(func):
    print("[then]")
    self.list_then.append(func)
    return None


class whenthen(object):
    def __init__(self, func):
        self.list_when = []
        self.list_then = []

        @wraps
        def new_func(*args, **kwargs):
            print("[new_func]")
            for when, then in zip(self.list_when, self.list_when):
                if when(*args, **kwargs):
                    return then(*args, **kwargs)
            return func(*args, **kwargs)
        self.func = new_func
        self.when = when
        self.then = then

    def __call__(self):
        print("Entering", self.f.__name__)
        self.f()
        print("Exited", self.f.__name__)





# def whenthen(func):
#     list_when = []
#     list_then = []
#     print("[whenthen]")
#
#     @wraps
#     def new_func(*args, **kwargs):
#         print("[new_func]")
#         for when, then in zip(list_when, list_when):
#             if when(*args, **kwargs):
#                 return then(*args, **kwargs)
#         return func(*args, **kwargs)
#
#     @wraps
#     def when(f):
#         print("[when]")
#         list_when.append(f)
#         return None
#
#     @wraps
#     def then(f):
#         print("[then]")
#         list_then.append(f)
#         return None
#
#     new_func.when = when
#     new_func.then = then
#
#     # new_func.__name__ = func.__name__
#     return new_func


@whenthen
def fract(x):
    return x * fract(x - 1)

import sys
current_module = sys.modules[__name__]
import inspect
all_functions = inspect.getmembers(fract, inspect.isfunction)
print(all_functions)
# print(fract.__name__)
print(dir(fract))


@fract.when
def fract(x):
    return x == 0

print(dir(fract))

@fract.then
def fract(x):
    return 1


@fract.when
def fract(x):
    return x > 5


@fract.then
def fract(x):
    return x * (x - 1) * (x - 2) * (x - 3) * (x - 4) * fract(x - 5)















