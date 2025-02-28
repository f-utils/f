from f.mods.meta_ import Meta
from f.mods.err_  import TypeErr

class _type(type):
    def __new__(mcs, name, bases, dct, **kwargs):
        cls = super().__new__(mcs, name, bases, dct)
        cls.at = kwargs.get('at', None)
        return cls

    class any:
        pass

    def database(cls, *args):
        return Meta.database(cls.at, *args)
    db = database

    def init(cls, some_type, description):
        if not isinstance(some_type, type) and some_type is not None:
            raise TypeErr(f"'{some_type}' is not a type neither None.")
        return Meta.init(some_type, description, at=cls.at)
    i = init

    def add(cls, typename, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return Meta.add(typename, attribute, cls.at, aliases)
    a = add

    def delete(cls, typename, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return Meta.delete(typename, attribute, cls.at, aliases)
    d = delete

    def update(cls, typename, attribute):
        aliases = {
            'description': ['d', 'desc'],
            'tags': ['t', 'tag'],
            'comments': ['c', 'comment']
        }
        return Meta.update(typename, attribute, cls.at, aliases)
    u = update

    def export(cls):
        return Meta.export(cls.at)
    E = export

    def check(cls, type_names):
        return Meta.check(type_names, cls.at)
    c = check

    def search(cls, term, where):
        aliases = {
            'description': ['d', 'desc'],
            'tags': ['t', 'tag'],
            'comments': ['c', 'comment'],
        }
        return Meta.search(term, where, cls.at, aliases)
    s = search

    def info(cls, type_name):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments']
        }
        return Meta.info(type_name, cls.at, aliases)
    I = info
