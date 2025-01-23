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
        def __new__(cls, spec_name, at=None):
            specs_dict = at or f._default_specs
            if spec_name not in specs_dict:
                raise _spec.err(f"Function '{spec_name}' not found.")
            def exec_func(*args, **kwargs):
                for arg_types, funcinfo in specs_dict[spec_name]['spec']['body'].items():
                    return funcinfo['func'](*args, **kwargs)
            return func(exec_func)
    s = spec

    class dspec(metaclass=_dspec, at=_default_dspecs):
        pass

    ds = dspec
