from f.mods.meta import meta

class _type(type):
    def __new__(mcs, name, bases, dct, **kwargs):
        cls = super().__new__(mcs, name, bases, dct)
        cls.at = kwargs.get('at', None)
        return cls

    class any:
        pass

    def database(cls, *args):
        return meta.database(cls.at, *args)
    db = database

    def init(cls, some_type, description):
        if not isinstance(some_type, type) and some_type is not None:
            raise meta.err(f"'{some_type}' is not a type neither None.")
        return meta.init(some_type, description, at=cls.at)
    i = init

    def add(cls, typename, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.add(typename, attribute, cls.at, aliases)
    a = add

    def delete(cls, typename, attribute):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.delete(typename, attribute, cls.at, aliases)
    d = delete

    def update(cls, typename, attribute):
        aliases = {
            'description': ['d', 'desc'],
            'tags': ['t', 'tag'],
            'comments': ['c', 'comment']
        }
        return meta.update(typename, attribute, cls.at, aliases)
    u = update

    def export(cls):
        return meta.export(cls.at)
    E = export

    def check(cls, type_names):
        return meta.check(type_names, cls.at)
    c = check

    def search(cls, term, where):
        aliases = {
            'description': ['d', 'desc'],
            'tags': ['t', 'tag'],
            'comments': ['c', 'comment'],
        }
        return meta.search(term, where, cls.at, aliases)
    s = search

    def info(cls, type_name):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments']
        }
        return meta.info(type_name, cls.at, aliases)
    I = info
