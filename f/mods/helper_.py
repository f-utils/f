from f.mods.err_ import HelperErr
from inspect import getsource

def type_checker_(func):
    def wrapper(*args):
        if not all(isinstance(arg, type) for arg in args):
            raise HelperErr(f"All arguments of '{func.__name__}' must be types.")
        result = func(*args)
        if not isinstance(result, type):
            raise HelperErr(f"The function '{func.__name__}' must return a type.")
        return result
    return wrapper

def resolve_(attribute, aliases):
    for key, alias_list in aliases.items():
        if attribute in alias_list:
            return key
    return attribute

def repr_(func):
    try:
        source = getsource(func).strip()
    except:
        source = repr(func)

    if "lambda" in source:
        lambda_idx = source.index("lambda")
        return source[lambda_idx:].strip().rstrip(')')
    return source
