from f.mods.entity_ import entity_
from f.mods.methods.init_ import Init
from f.mods.err_  import TypeErr


def type_(att):
    Entity = entity_(att)
    class Type(Entity):
        @staticmethod
        def init(some_type, description):
            if not isinstance(some_type, type) and some_type is not None:
                raise TypeErr(f"'{some_type}' is not a type neither None.")
            if some_type in att:
                raise TypeErr(f"'{some_type}' is already registered.")
            att[some_type] = {'metadata': {'tags': [], 'comments': {}}}
            Init.desc(att[some_type], description)
        i = init
    return Type
