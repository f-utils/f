from f.mods.entity_         import entity_
from f.mods.err_            import SpecErr
from f.mods.methods.update_ import Update
from f.mods.methods.init_   import Init
from f.mods.methods.get_    import Get
from f.mods.methods.info_   import Info
from f.mods.helper_         import acceptable_types_, repr_

def spec_(at, att):
    Entity = entity_(at, att)
    class Spec(Entity):
        def __new__(cls, spec_name, base_at=None):
            specs_dict = base_at if base_at is not None else at
            if spec_name not in specs_dict:
                raise SpecErr(f"Spectrum '{spec_name}' not found in database '{base_at}'.")
            def exec_func(*args, **kwargs):
                spec = specs_dict[spec_name]
                for arg_types, funcinfo in spec['spec']['body'].items():
                    acceptable_types = acceptable_types_()
                    if not len(args) == len(arg_types):
                        raise SpecErr(f"Expected '{len(arg_types)}' arguments. Received: '{len(args)}'.")
                    if all(isinstance(arg, typ) for arg, typ in zip(args, arg_types) if typ in acceptable_types):
                        return funcinfo['func'](*args, **kwargs)
                mismatch_types = [type(arg).__name__ for arg in args if type(arg) not in arg_types]
                if mismatch_types:
                    raise SpecErr(f"Types '{mismatch_types}' are not in the domain of spectrum '{spec_name}'.")
            return exec_func

        @staticmethod
        def init(spec_name, description, std):
            if spec_name in at:
                raise SpecErr(f"Spectrum '{spec_name}' is already registered.")
            at[spec_name] = {'metadata': {'tags': [], 'comments': {}}}
            Init.desc(at[spec_name], description)
            Init.std(at[spec_name], std)
        i = init

        @staticmethod
        def extend(spec_name, arg_types, func):
            from itertools import product
            if not callable(func):
                raise SpecErr(f"The provided function must be callable.")
            expanded_arg_types = []
            if isinstance(arg_types, tuple):
                for typ in arg_types:
                    if typ in ('any', 'Any'):
                        expanded_types = acceptable_types_(default_types, allow_subtypes, allow_ops)
                    else:
                        if not isinstance(typ, type):
                            raise SpecErr(f"'{typ}' is not a valid type.")
                        expanded_types = (typ,)
                    for t in expanded_types:
                        if t not in att:
                            raise SpecErr(f"Type '{t.__name__}' is not an accessible type.")

                    expanded_arg_types.append(expanded_types)
            elif isinstance(arg_types, type):
                if arg_types not in att:
                    raise SpecErr(f"Type '{arg_types.__name__}' is not an accessible type.")
                expanded_arg_types.append((arg_types,))
            else:
                raise SpecErr(f"'{type(arg_types)}' is not 'type' or 'tuple'.")

            type_combinations = list(product(*expanded_arg_types))

            for combo in type_combinations:
                if spec_name not in at:
                    raise SpecErr(f"Specification '{spec_name}' not found.")
                spec_info = at[spec_name]
                if 'spec' not in spec_info:
                    spec_info['spec'] = {'body': {}}
                if 'body' not in spec_info['spec']:
                    spec_info['spec']['body'] = {}

                combo_key = tuple(combo)

                if combo_key not in spec_info['spec']['body']:
                    spec_info['spec']['body'][combo_key] = {
                        'func': func,
                        'repr': repr_(func)
                    }
                else:
                    raise SpecErr(f"Combination '{combo_key}' already exists in spec '{spec_name}'.") 
        e = extend

        class get(Entity.get):
            @staticmethod
            def std(spec_name):
                entity = at.get(spec_name, {})
                return Get.std(entity)

            @staticmethod
            def domain(spec_name):
                entity = at.get(spec_name, {})
                return Get.domain(entity)

            @staticmethod
            def body(spec_name):
                entity = at.get(spec_name, {})
                return Get.body(entity)
        g = get

        class update(Entity.update):
            @staticmethod
            def std(spec_name, new_std):
                def updater(spec_info):
                    return Update.std(spec_info, new_std)
                if spec_name in at:
                    return updater(at[spec_name])
                else:
                    raise SpecErr(f"Spectrum '{spec_name}' not found in database.")
            s = std

            @staticmethod
            def body(spec_name, domain, new_func):
                def updater(spec_info):
                    return Update.body(spec_info, domain, new_func)
                if spec_name in at:
                    return updater(at[spec_name])
                else:
                    raise SpecErr(f"Spectrum '{spec_name}' not found in database.")
            b = body
        u = update

        class info(Entity.info):
            @staticmethod
            def std(spec_name):
                entity = at.get(spec_name, {})
                return f"Kind: spec\n" + Info.std(entity)

            @staticmethod
            def domain(spec_name):
                entity = at.get(spec_name, {})
                return f"Kind: spec\n" + Info.domain(entity)

            @staticmethod
            def body(spec_name):
                entity = at.get(spec_name, {})
                return f"Kind: spec\n" + Info.body(entity)

            @staticmethod
            def all(spec_name):
                entity = at.get(spec_name, {})
                return"\n  ".join([
                    Info.name(spec_name),
                    'Kind: spec',
                    Info.desc(entity),
                    Info.tags(entity),
                    Info.comments(entity),
                    Info.domain(entity),
                    Info.body(entity)
                ])
        I = info

    return Spec
