from f.mods.meta_ import Meta
from f.mods.err_ import OpErr
from f.mods.helper_ import type_checker_


class _op(type):
    def __new__(mcs, name, bases, dct, **kwargs):
        cls = super().__new__(mcs, name, bases, dct)
        cls.at = kwargs.get('at', None)
        return cls

    def database(cls, *args):
        return Meta.database(cls.at, *args)
    db = database

    def init(cls, op_name, desc, func):
        if not callable(func):
            raise OpErr(f"The operation '{op_name}' must be a function or a lambda.")
        checked_func_ = type_checker_(func)
        cls.at[op_name] = {
            'metadata': {
                'desc': desc,
                'tags': [],
                'comments': {}
            },
            'op': {
                'func': func,
                'repr': Meta.repr(func)
            }
        }
    i = init

    def add(cls, op_name, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return Meta.add(op_name, attribute, cls.at, aliases)
    a = add

    def delete(cls, op_name, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return Meta.delete(op_name, attribute, cls.at, aliases)
    d = delete

    def update(cls, op_name, attribute):
        aliases = {
            'desc': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'func': ['f', 'func', 'function', 'o', 'op']
        }
        attribute = Meta.resolve(attribute, aliases)
        if attribute == 'func':
            def _update_func_(new_func):
                if not callable(new_func):
                    raise OpErr(f"The new function '{new_func.__name__}' must be callable.")
                checked_func_ = type_checker_(new_func)
                cls.at[op_name]['op']['func'] = new_func
                cls.at[op_name]['op']['repr'] = Meta.repr(new_func)
            return _update_func_

        return Meta.update(op_name, attribute, cls.at, aliases)
    u = update

    def export(cls):
        return Meta.export(cls.at)
    E = export
