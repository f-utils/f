from f.mods.meta import meta
import inspect

class _dspec(type):
    def __new__(mcs, name, bases, dct, **kwargs):
        cls = super().__new__(mcs, name, bases, dct)
        cls.at = kwargs.get('at', None)
        cls.att = kwargs.get('att', None)
        cls.any = kwargs.get('any', None)
        return cls

    def database(cls, *args):
        return meta.database(cls.at, *args)
    db = database

    def init(cls, dspec_name, description, std):
        return meta.init(dspec_name, description, std, cls.at)
    i = init

    def extend(cls, dspec_name, arg_types, func):
        from f.main import f
        from itertools import product

        if not callable(func):
            raise meta.err("The function must be callable.")
        func_signature = inspect.signature(func)

        expanded_arg_types = []
        for typ in arg_types:
            if isinstance(typ, list):
                if not all(isinstance(t, type) or t in ('any', 'Any') for t in typ):
                    raise TypeError("All elements in the list must be types or 'Any'.")
                expanded_arg_types.append(tuple(f.acceptable_types_() if t in ('any', 'Any') else t for t in typ))
            elif typ in ('any', 'Any'):
                expanded_arg_types.append(tuple(f.acceptable_types_()))
            else:
                if not isinstance(typ, type):
                    raise TypeError(f"'{typ}' is not a valid type.")
                expanded_arg_types.append((typ,))

        type_combinations = product(*expanded_arg_types)

        dspec_body = cls.at[dspec_name]['spec']['body']

        for combo in type_combinations:
            if len(combo) == len(func_signature.parameters):
                tuple_combo = tuple(
                    tuple(inner) if isinstance(inner, list) else inner
                    for inner in combo
                )
            elif len(combo) == len(func_signature.parameters) - 1:
                *prefix_combo, varargs_combo = combo
                if isinstance(varargs_combo, tuple):
                    list_combo = [tuple(prefix_combo) + (vararg,) for vararg in varargs_combo]
                    for tuple_combo in list_combo:
                        if any(existing == tuple_combo for existing in dspec_body.keys()):
                            raise meta.err("Argument types match an existing dspec entry.")
                        meta.extend(dspec_name, tuple_combo, func, cls.at, cls.att)
                    continue
                else:
                    raise TypeError("The last element of arg_types should be a list of acceptable types for *args.")
            else:
                raise TypeError("Mismatch between number of fixed arguments and provided types in the definition.")

            if any(existing == tuple_combo for existing in dspec_body.keys()):
                raise meta.err("Argument types match an existing dspec entry.")
            meta.extend(dspec_name, tuple_combo, func, cls.at, cls.att)
    e = extend

    def add(cls, dspec_name, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.add(dspec_name, attribute, cls.at, aliases)
    a = add

    def delete(cls, dspec_name, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.delete(dspec_name, attribute, cls.at, aliases)
    d = delete

    def update(cls, dspec_name, attribute):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'std': ['s', 'std', 'standard'],
            'body': ['b', 'body']
        }
        return meta.update_metadata(dspec_name, attribute, cls.at, aliases)
    u = update

    def export(cls):
        return meta.export(cls.at)
    E = export

    def check(cls, dspec_names):
        return meta.check(dspec_names, cls.at)
    c = check

    def search(cls, term, where):
        aliases = {
            'description': ['d', 'desc'],
            'tags': ['t', 'tag'],
            'comments': ['c', 'comment'],
        }
        return meta.search(term, where, cls.at, aliases)
    s = search

    def info(cls, dspec_name):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'std': ['s', 'std', 'standard'],
            'body': ['b', 'body'],
            'domain': ['dm', 'domain']
        }
        return meta.info(dspec_name, cls.at, aliases)
    I = info
