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
        signature = inspect.signature(func)
        for param in inspect.signature(func).parameters.values():
            if param.kind == param.VAR_POSITIONAL:
                return meta.extend(dspec_name, arg_types, func, cls.at, cls.att, cls.any)
        raise meta.err('To extend a dspec, provide a dynamic function.')
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
