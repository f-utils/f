from f.mods.meta import meta

class _spec(type):
    def __new__(mcs, name, bases, dct, **kwargs):
        cls = super().__new__(mcs, name, bases, dct)
        cls.at = kwargs.get('at', None)
        cls.att = kwargs.get('att', None)
        return cls

    def database(cls, *args):
        return meta.database(cls.at, *args)
    db = database

    def init(cls, spec_name, description, std):
        return meta.init(spec_name, description, std, cls.at)
    i = init

    def extend(cls, spec_name, arg_types, func):
        from f.main import f
        from itertools import product
        expanded_arg_types = []
        for typ in arg_types:
            if isinstance(typ, list):
                if not all(isinstance(t, type) for t in typ):
                    raise TypeError("All elements in the list must be types.")
                expanded_arg_types.append(tuple(typ))
            elif typ in ('any', 'Any'):
                expanded_arg_types.append(f.acceptable_types_())
            else:
                if not isinstance(typ, type):
                    raise TypeError(f"'{typ}' is not a valid type.")
                expanded_arg_types.append((typ,))
        type_combinations = product(*expanded_arg_types)
        for combo in type_combinations:
            meta.extend(spec_name, combo, func, cls.at, cls.att)
    e = extend

    def add(cls, spec_name, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.add(spec_name, attribute, cls.at, aliases)
    a = add

    def delete(cls, spec_name, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.delete(spec_name, attribute, cls.at, aliases)
    d = delete

    def update(cls, spec_name, attribute):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'std': ['s', 'std', 'standard'],
            'body': ['b', 'body']
        }
        return meta.update(spec_name, attribute, cls.at, aliases)
    u = update

    def export(cls):
        return meta.export(cls.at)
    E = export

    def check(cls, spec_names):
        return meta.check(spec_names, cls.at)
    c = check

    def search(cls, term, where):
        aliases = {
            'description': ['d', 'desc'],
            'tags': ['t', 'tag'],
            'comments': ['c', 'comment'],
        }
        return meta.search(term, where, cls.at, aliases)
    s = search

    def info(cls, spec_name):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'std': ['s', 'std', 'standard'],
            'body': ['b', 'body'],
            'domain': ['dm', 'domain']
        }
        return meta.info(spec_name, cls.at, aliases)
    I = info
