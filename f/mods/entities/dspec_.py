import inspect
from f.mods.entity_         import entity_
from f.mods.methods.update_ import Update
from f.mods.methods.init_   import Init
from f.mods.methods.get_    import Get
from f.mods.methods.info_   import Info
from f.mods.err_            import DSpecErr
from f.mods.helper_         import repr_, expand_types_

def dspec_(at, att):
    Entity = entity_(at, att)
    class DSpec(Entity):
        def __new__(cls, dspec_name, at_=None):
            dspecs_dict = at_ if at_ is not None else at
            if dspec_name not in dspecs_dict:
                raise DSpecErr(f"Dynamic spectrum '{dspec_name}' not found in database '{at_}'.")
            def exec_func(*args, **kwargs):
                dspec = dspecs_dict[dspec_name]
                for arg_types, funcinfo in dspec['spec']['body'].items():
                    fixed_part_types = [typ for typ in arg_types if not isinstance(typ, list)]
                    dynamic_part_types = []
                    if len(arg_types) > len(fixed_part_types):
                        dynamic_part_types = arg_types[len(fixed_part_types):][0]
                    if len(args) < len(fixed_part_types) or not all(isinstance(arg, typ) for arg, typ in zip(args[:len(fixed_part_types)], fixed_part_types)):
                        continue
                    remaining_args = args[len(fixed_part_types):]
                    if not dynamic_part_types or all(any(isinstance(arg, typ) for typ in dynamic_part_types) for arg in remaining_args):
                        return funcinfo['func'](*args, **kwargs)
                raise DSpecErr(f"Types '{[type(arg).__name__ for arg in args]}' are not in the domain of dynamic spectrum '{dspec_name}'.")
            return exec_func

        @staticmethod
        def init(dspec_name, description, std):
            if dspec_name in at:
                raise DSpecErr(f"Dynamic spectrum '{dspec_name}' is already registered.")
            at[dspec_name] = {'metadata': {'tags': [], 'comments': {}}}
            Init.desc(at[dspec_name], description)
            Init.std(at[dspec_name], std)
        i = init

        @staticmethod
        def extend(dspec_name, arg_types, func):
            from itertools import product
            from f.main import f

            if not callable(func):
                raise DSpecErr(f'{func} must be callable.')

            func_signature = inspect.signature(func)
            expanded_arg_types = []

            if isinstance(arg_types, tuple):
                for typ in arg_types:
                    expanded_arg_types.append(expand_types_(typ))
                fixed_part = tuple(typ for typ in arg_types if not isinstance(typ, list))
            else:
                expanded_arg_types.append(expand_types_(arg_types))
                fixed_part = ()

            type_combinations = product(*expanded_arg_types)
            dspec_body = at[dspec_name]['spec']['body']
            for combo in type_combinations:
                combo_key = tuple(combo)
                if isinstance(arg_types, tuple):
                    if not (combo_key[:len(fixed_part)] == tuple(next(iter(expand_types_(typ))) for typ in fixed_part) 
                            and len(combo_key) == len(func_signature.parameters)):
                        continue
                dynamic_part_sorted = tuple(sorted(combo_key[len(fixed_part):], key=lambda x: x.__name__))
                dynamic_part_key = combo_key[:len(fixed_part)] + dynamic_part_sorted

                if dynamic_part_key in dspec_body:
                    raise DSpecErr(f"Combination '{dynamic_part_key}' already exists in dspec '{dspec_name}'.")

                dspec_body[dynamic_part_key] = {
                    'func': func,
                    'repr': repr_(func)
                }
        e = extend

        class get(Entity.get):
            @staticmethod
            def std(dspec_name):
                entity = at.get(dspec_name, {})
                return Get.std(entity)

            @staticmethod
            def domain(dspec_name):
                entity = at.get(dspec_name, {})
                return Get.domain(entity)

            @staticmethod
            def body(dspec_name):
                entity = at.get(dspec_name, {})
                return Get.body(entity)
        g = get

        class update(Entity.update):
            @staticmethod
            def std(dspec_name, new_std):
                def updater(dspec_info):
                    return Update.std(dspec_info, new_std)
                if dspec_name in at:
                    return updater(at[dspec_name])
                else:
                    raise DSpecErr(f"Dynamic spectrum '{dspec_name}' not found in database '{at}'.")

            @staticmethod
            def body(dspec_name, arg_types, new_func):
                def updater(dspec_info):
                    return Update.dbody(dspec_info, arg_types, new_func)
                if dspec_name in at:
                    return updater(at[dspec_name])
                else:
                    raise DSpecErr(f"Dynamic spectrum '{dspec_name}' not found in database.")
        u = update

        class info(Entity.info):
            @staticmethod
            def std(dspec_name):
                entity = at.get(dspec_name, {})
                return Info.std(entity)

            @staticmethod
            def domain(dspec_name):
                entity = at.get(dspec_name, {})
                return Info.domain(entity)

            @staticmethod
            def body(dspec_name):
                entity = at.get(dspec_name, {})
                return Info.body(entity)

            @staticmethod
            def all(dspec_name):
                entity = at.get(dspec_name, {})
                return "\n".join([
                    Info.name(entity),
                    Info.desc(entity),
                    Info.tags(entity),
                    Info.comments(entity),
                    Info.domain(entity),
                    Info.body(entity)
                ])
        I = info
    return DSpec
