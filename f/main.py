from f.mods.func  import func
from f.mods.type  import _type
from f.mods.spec  import _spec
from f.mods.dspec import _dspec

class f:
    _default_types = {}
    _default_specs = {}
    _default_dspecs = {}

    func = func
    f = func

    class type(metaclass=_type, at=_default_types):
        pass
    t = type

    class spec(metaclass=_spec, at=_default_specs):
        pass
    s = spec

    class dspec(metaclass=_dspec, at=_default_dspecs):
        pass

    ds = dspec
