from f.mods.entities.type_  import type_
from f.mods.entities.op_    import op_
from f.mods.entities.spec_  import spec_
from f.mods.entities.dspec_ import dspec_
from f.mods.err_   import (
    TypeErr,
    OpErr,
    SpecErr,
    DSpecErr
)
from f.mods.db_ import Db
from f.mods.conf_ import Conf

class f:
    Type  = type_(Db._default_types)
    Op    = op_(Db._default_ops)
    Spec  = spec_(Db._default_specs, Db._default_types)
    DSpec = spec_(Db._default_dspecs, Db._default_types)
    t  = Type
    o  = Op
    s  = Spec
    ds = DSpec

    @classmethod
    def conf(cls, allow_ops=False, allow_subtypes=False):
        cls._allow_ops = allow_ops
        cls._allow_subtypes = allow_subtypes
