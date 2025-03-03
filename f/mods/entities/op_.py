from f.mods.entity_       import entity_
from f.mods.methods.init_ import Init
from f.mods.methods.get_  import Get
from f.mods.methods.info_ import Info
from f.mods.err_          import EntityErr

def op_(at):
    Entity = entity_(at)
    class Op(Entity):
        def __new__(cls, op_name, at_=None):
            ops_dict = at_ if at_ is not None else at
            if op_name not in ops_dict:
                raise OpErr(f"Operation '{op_name}' not found in database '{at_}'.")
            return ops_dict[op_name]['op']['func']

        @staticmethod
        def init(op_name, desc, func):
            if op_name in at:
                raise OpErr(f"Operation '{op_name}' is already registered.")
            at[op_name] = {'metadata': {'tags': [], 'comments': {}}}
            Init.desc(at[op_name], desc)
            Init.func(at[op_name], func)
        i = init

        class get(Entity.get):
            @staticmethod
            def func(op_name):
                entity = at.get(op_name, {})
                return Get.func(entity)
        g = get

        class update(Entity.update):
            @staticmethod
            def func(op_name, new_func):
                resolved_func = 'func'
                if op_name in at:
                    op_info = at[op_name]
                    return Update.func(op_info, new_func)
                else:
                    raise OpErr(f"Operation '{op_name}' not found in the database.")
        u = update

        class info(Entity.info):
            @staticmethod
            def func(op_name):
                entity = at.get(op_name, {})
                return Info.func(entity)

            @staticmethod
            def all(op_name):
                entity = at.get(op_name, {})
                return "\n".join([
                    Info.name(entity),
                    Info.desc(entity),
                    Info.tags(entity),
                    Info.comments(entity),
                    Info.func(entity)
                ])
        I = info
    return Op
