from f.mods.meta import meta

class dspecErr(Exception):
    pass

class dspec:
    @staticmethod
    def init(dspec_name, description, std_return_function, at):
        return meta.init(dspec_name, description, std_return_function, at)
    i = init

    @staticmethod
    def extend(dspec_name, arg_types, func, at):
        return meta.extend(dspec_name, arg_types, func, at, any_class=meta.any)
    e = extend

    @staticmethod
    def add(dspec_name, attribute, at):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.add(dspec_name, attribute, at, aliases)
    a = add

    @staticmethod
    def delete(dspec_name, attribute, at):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.delete(dspec_name, attribute, at, aliases)
    d = delete

    @staticmethod
    def update(dspec_name, attribute, at):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'std': ['s', 'std', 'standard'],
            'body': ['b', 'body']
        }
        return meta.update_metadata(dspec_name, attribute, at, aliases)
    u = update

    @staticmethod
    def export(at):
        return meta.export(at)
    E = export

    @staticmethod
    def check(dspec_names, at):
        return meta.check(dspec_names, at)
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
    def info(dspec_name, at):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'std': ['s', 'std', 'standard'],
            'body': ['b', 'body'],
            'domain': ['dm', 'domain']
        }
        return meta.info(dspec_name, at, aliases)
    I = info
