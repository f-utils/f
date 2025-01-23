import inspect

class funcErr(Exception):
    pass

class func:
    def __init__(self, func):
        if not callable(func):
            raise funcErr(f"'{func}' is not a function.")
        self._func = func

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __mul__(self, other):
        if not isinstance(other, f.func):
            raise funcErr(f"'{other}'is not a function: the composition is defined only between functions.")
        def comp_(*args, **kwargs):
            return self._func(other(*args, **kwargs))
        return f.func(comp_)
