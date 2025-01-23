from f.mods.func  import func as func_
from f.mods.type  import type as type_
from f.mods.spec  import spec as spec_
from f.mods.dspec import dspec as dspec_

class f:
    _default_types = None
    _default_specs = None
    _default_dspec = None

    func = func_
    f = func
    type = type_
    t = type
    spec = spec_
    s = spec
    dspec = dspec_
    ds = dspec
