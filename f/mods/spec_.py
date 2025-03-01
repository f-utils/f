from f.mods.meta_ import Meta
from f.mods.err_  import SpecErr
from f.mods.update_ import Update

def spec_(at, att):
    class Spec(Meta):
        def __new__(cls, spec_name, base_at=None):
            specs_dict = base_at if base_at is not None else at
            if spec_name not in specs_dict:
                raise SpecErr(f"Spectrum '{spec_name}' not found in database '{base_at}'.")
            def exec_func(*args, **kwargs):
                spec = specs_dict[spec_name]
                for arg_types, funcinfo in spec['spec']['body'].items():
                    acceptable_types = f.acceptable_types_()
                    if not len(args) == len(arg_types):
                        raise SpecErr(f"Expected '{len(arg_types)}' arguments. Received: '{len(args)}'.")
                    if all(isinstance(arg, typ) for arg, typ in zip(args, arg_types) if typ in acceptable_types):
                        return funcinfo['func'](*args, **kwargs)
                mismatch_types = [type(arg).__name__ for arg in args if type(arg) not in arg_types]
                if mismatch_types:
                    raise SpecErr(f"Types '{mismatch_types}' are not in the domain of spectrum '{spec_name}'.")
            return exec_func

        @staticmethod
        def database(*args):
            return Meta.database(at, *args)
        db = database

        @staticmethod
        def init(spec_name, description, std):
            return Meta.init(spec_name, description, std, at)
        i = init

        @staticmethod
        def extend(spec_name, arg_types, func):
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
                Meta.extend(spec_name, combo, func, at, att)
        e = extend

        @staticmethod
        def add(spec_name, attribute):
            aliases = {'comments': ['c', 'comment'], 'tags': ['t', 'tag']}
            return Meta.add(spec_name, attribute, at, aliases)
        a = add

        @staticmethod
        def delete(spec_name, attribute):
            aliases = {'comments': ['c', 'comment'], 'tags': ['t', 'tag']}
            return Meta.delete(spec_name, attribute, at, aliases)
        d = delete

        @staticmethod
        def export():
            return Meta.export(at)
        E = export

        @staticmethod
        def check(spec_names):
            return Meta.check(spec_names, at)

        @staticmethod
        def get(spec_name, attribute):
            aliases = {
                'description': ['d', 'desc', 'description'],
                'tags': ['t', 'tag', 'tags'],
                'comments': ['c', 'comment', 'comments'],
                'std': ['s', 'std', 'standard'],
                'body': ['b', 'body']
            }
            return Meta.get(spec_name, attribute, at, aliases)
        g = get

        @staticmethod
        def search(term, where):
            aliases = {
                'description': ['d', 'desc'],
                'tags': ['t', 'tag'],
                'comments': ['c', 'comment'],
            }
            return Meta.search(term, where, at, aliases)
        s = search

        @staticmethod
        def info(spec_name):
            aliases = {
                'description': ['d', 'desc', 'description'],
                'tags': ['t', 'tag', 'tags'],
                'comments': ['c', 'comment', 'comments'],
                'std': ['s', 'std', 'standard'],
                'body': ['b', 'body'],
                'domain': ['dm', 'domain']
            }
            return Meta.info(spec_name, at, aliases)
        I = info

        class update:
            aliases_ = {
                'std': ['s', 'std', 'standard'],
                'body': ['b', 'body']
            }
            updaters_ = {
                'std': lambda spec_info, new_std: Update.std(spec_info, new_std),
                'body': lambda spec_info, domain, new_func: Update.body(spec_info, domain, new_func)
            }

            @staticmethod
            def desc(spec_name, new_description):
                return Meta.update(spec_name, 'description', at)(new_description)

            @staticmethod
            def tag(spec_name, old_tag, new_tag):
                return Meta.update(spec_name, 'tags', at)(old_tag, new_tag)

            @staticmethod
            def comment(spec_name, comment_id, new_comment_value):
                return Meta.update(spec_name, 'comments', at)(comment_id, new_comment_value)

            @staticmethod
            def std(spec_name, new_std):
                def updater(spec_info):
                    return Spec.update.updaters_['std'](spec_info, new_std)

                # Retrieve the specific entry from `at`
                if spec_name in at:
                    return updater(at[spec_name])
                else:
                    raise SpecErr(f"Spectrum '{spec_name}' not found in database '{at}'.") 

            @staticmethod
            def body(spec_name, domain, new_func):
                resolved_body = Spec.update.aliases_['body'][0]
                return Meta.update(spec_name, resolved_body, at, Spec.update.updaters_, Spec.aliases_)(domain, new_func)
        u = update

    return Spec
