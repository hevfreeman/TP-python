def whenthen(func):
    list_when = []
    list_then = []
    print("[whenthen]")

    # @wraps
    def new_func(*args, **kwargs):
        for when, then in zip(list_when, list_then):
            if when(*args, **kwargs):
                return then(*args, **kwargs)
        return func(*args, **kwargs)

    def when(f):
        list_when.append(f)
        return new_func

    def then(f):
        list_then.append(f)
        return new_func

    new_func.when = when
    new_func.then = then

    return new_func
