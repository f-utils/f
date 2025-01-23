from f.mods.meta import meta

class typeErr(Exception):
    pass

class type:
    @staticmethod
    def init(some_type, description, at):
        return meta.init(some_type, description, at)
    i = init

    @staticmethod
    def add(typename, attribute, at):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.add(typename, attribute, at, aliases)
    a = add

    @staticmethod
    def delete(typename, attribute, at):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.delete(typename, attribute, at, aliases)
    d = delete

    @staticmethod
    def update(typename, attribute, at):
        aliases = {
            'description': ['d', 'desc'],
            'tags': ['t', 'tag'],
            'comments': ['c', 'comment']
        }
        return meta.update(typename, attribute, at, aliases)
    u = update

    @staticmethod
    def export(at):
        return meta.export(at)
    E = export

    @staticmethod
    def check(type_names, at):
        return meta.check(type_names, at)
    c = check

    @staticmethod
    def search(term, where, at):
        aliases = {
            'description': ['d', 'desc'],
            'tags': ['t', 'tag'],
            'comments': ['c', 'comment'],
        }
        return meta.search(term, where, at, aliases)
    s = search

    @staticmethod
    def info(type_name, at):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments']
        }
        return meta.info(type_name, at, aliases)
    I = info
