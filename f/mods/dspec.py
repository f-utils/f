from f.mods.meta import meta

class dspecErr(Exception):
    pass

class _dspec(type):
    def __new__(mcs, name, bases, dct, **kwargs):
        cls = super().__new__(mcs, name, bases, dct)
        cls.at = kwargs.get('at', None)
        return cls

    def database(cls, *args):
        return meta.database(cls.at, *args)
    db = database

    def init(cls, dspec_name, description, std_return_function):
        return meta.init(dspec_name, description, std_return_function, cls.at)
    i = init

    def extend(cls, dspec_name, arg_types, func):
        return meta.extend(dspec_name, arg_types, func, cls.at)
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
