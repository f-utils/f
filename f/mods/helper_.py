from f.mods.err_ import HelperErr

def type_checker_(func):
    def wrapper(*args):
        if not all(isinstance(arg, type) for arg in args):
            raise Meta.err(f"All arguments of '{func.__name__}' must be types.")
        result = func(*args)
        if not isinstance(result, type):
            raise HelperErr(f"The function '{func.__name__}' must return a type.")
        return result
    return wrapper
