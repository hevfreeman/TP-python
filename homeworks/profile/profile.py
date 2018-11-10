import time


def profile(func):
    def new_func(*args, **kwargs):
        print(f"`{func.__name__}` started")
        start = time.time()
        ret = func(*args, **kwargs)
        print(f"`{func.__name__}` finished in {time.time() - start}")
        return ret
    return new_func
