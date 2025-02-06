from f.mods.meta import meta

def type_checker_(func):
    def wrapper(*args):
        if not all(isinstance(arg, type) for arg in args):
            raise meta.err(f"All arguments of '{func.__name__}' must be types.")
        result = func(*args)
        if not isinstance(result, type):
            raise meta.err(f"The function '{func.__name__}' must return a type.")
        return result
    return wrapper

class _op(type):
    def __new__(mcs, name, bases, dct, **kwargs):
        cls = super().__new__(mcs, name, bases, dct)
        cls.at = kwargs.get('at', None)
        return cls

    def database(cls, *args):
        return meta.database(cls.at, *args)
    db = database

    def init(cls, op_name, desc, func):
        if not callable(func):
            raise meta.err(f"The operation '{op_name}' must be a function or a lambda.")
        checked_func_ = type_checker_(func)
        cls.at[op_name] = {
            'metadata': {
                'desc': desc,
                'tags': [],
                'comments': {}
            },
            'op': {
                'func': func,
                'repr': meta.repr(func)
            }
        }
    i = init

    def add(cls, op_name, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.add(op_name, attribute, cls.at, aliases)
    a = add

    def delete(cls, op_name, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.delete(op_name, attribute, cls.at, aliases)
    d = delete

    def update(cls, op_name, attribute):
        aliases = {
            'desc': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'func': ['f', 'func', 'function', 'o', 'op']
        }
        attribute = meta.resolve(attribute, aliases)
        if attribute == 'func':
            def _update_func_(new_func):
                if not callable(new_func):
                    raise meta.err(f"The new function '{new_func.__name__}' must be callable.")
                checked_func_ = type_checker_(new_func)
                cls.at[op_name]['op']['func'] = new_func
                cls.at[op_name]['op']['repr'] = meta.repr(new_func)
            return _update_func_

        return meta.update(op_name, attribute, cls.at, aliases)
    u = update

    def export(cls):
        return meta.export(cls.at)
    E = export
