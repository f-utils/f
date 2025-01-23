from f.mods.meta import meta

class specErr(Exception):
    pass

class spec:
    @staticmethod
    def init(spec_name, description, std_return_function, at):
        return meta.init(spec_name, description, std_return_function, at)
    i = init

    @staticmethod
    def extend(spec_name, arg_types, func, at):
        return meta.extend(spec_name, arg_types, func, at)
    e = extend

    @staticmethod
    def add(spec_name, attribute, at):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.add(spec_name, attribute, at, aliases)
    a = add

    @staticmethod
    def delete(spec_name, attribute, at):
        aliases = {
            'comments': ['c', 'comment'],
            'tags': ['t', 'tag']
        }
        return meta.delete(spec_name, attribute, at, aliases)
    d = delete

    @staticmethod
    def update(spec_name, attribute, at):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'std': ['s', 'std', 'standard'],
            'body': ['b', 'body']
        }
        return meta.update_metadata(spec_name, attribute, at, aliases)
    u = update

    @staticmethod
    def export(at):
        return meta.export(at)
    E = export

    @staticmethod
    def check(spec_names, at):
        return meta.check(spec_names, at)
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
    def info(spec_name, at):
        aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'std': ['s', 'std', 'standard'],
            'body': ['b', 'body'],
            'domain': ['dm', 'domain']
        }
        return meta.info(spec_name, at, aliases)
    I = info
