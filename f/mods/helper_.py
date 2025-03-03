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

def acceptable_types_(default_types, allow_subtypes=False, allow_ops=False, default_ops=None):
    base_types = set(default_types.keys())
    if allow_subtypes:
        base_types.update({
            subtype for basetype in base_types for subtype in basetype.__subclasses__()
        })
    if not allow_ops:
        return base_types
    allowed_ops = {}
    if isinstance(allow_ops, list):
        allowed_ops = {
            op_name: op['op']['func']
            for op_name, op in default_ops.items() if op_name in allow_ops
        }
    elif allow_ops is True:
        allowed_ops = {op_name: op['op']['func'] for op_name, op in default_ops.items()}
    derived_types = set()
    for op_func in allowed_ops.values():
        for base_type in base_types:
            try:
                new_type = op_func(base_type)
                if isinstance(new_type, type):
                    derived_types.add(new_type)
            except:
                continue
    return base_types.union(derived_types)

def expand_types_(typ):
    if isinstance(typ, list):
        if not all(isinstance(t, type) or t in ('any', 'Any') for t in typ):
            raise TypeError("All elements in the list must be types or 'Any'.")
        return tuple(acceptable_types_() if t in ('any', 'Any') else t for t in typ)
    elif typ in ('any', 'Any'):
        return tuple(acceptable_types_())
    else:
        if not isinstance(typ, type):
            raise TypeError(f"'{typ}' is not a valid type.")
        return (typ,)

def get_entry_value_(info, key):
    for main_key in ['metadata', 'spec']:
        if main_key in info and key in info[main_key]:
            return info[main_key][key]
    return info.get(key, '')
