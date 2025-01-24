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

    class err(Exception):
        class ArgNumber(Exception):
            pass
        class ArgType(Exception):
            pass
        class NotFound(Exception):
            pass

    class type(metaclass=_type, at=_default_types):
        pass
    t = type

    class spec(metaclass=_spec, at=_default_specs, att=_default_types):
        def __new__(cls, spec_name, at=None):
            specs_dict = at if at is not None else f._default_specs
            def exec_func(*args, **kwargs):
                spec = specs_dict[spec_name]
                for arg_types, funcinfo in spec['spec']['body'].items():
                    if not len(args) == len(arg_types):
                        raise cls.f.ArgNumber(f"Expected '{len(arg_types)}' arguments. Received: '{len(args)}'.")
                    if all(isinstance(arg, typ) for arg, typ in zip(args, arg_types)):
                        return funcinfo['func'](*args, **kwargs)
                mismatch_types = [type(arg).__name__ for arg in args if type(arg) not in arg_types]
                if mismatch_types:
                    raise f.err.ArgType(f"Types '{mismatch_types}' are not in the domain of spectrum '{spec_name}'.")
                raise f.err.NotFound(f"Spectrum '{spec_name}' not found in database {at}.")
            return func(exec_func)
    s = spec

    class dspec(metaclass=_dspec, at=_default_dspecs, att=_default_types):
        def __new__(cls, dspec_name, at=None):
            dspecs_dict = at if at is not None else f._default_dspecs
            def exec_func(*args, **kwargs):
                dspec = dspecs_dict[dspec_name]
                for arg_types, funcinfo in dspec['spec']['body'].items():
                    if all(isinstance(arg, arg_types) or arg is None for arg in args):
                        return funcinfo['func'](*args, **kwargs)
                mismatch_args = [arg for arg in args if type(arg) not in arg_types]
                mismatch_types = [type(arg).__name__ for arg in mismatch_args]
                raise f.err.ArgType(f"Types '{mismatch_types}' for arguments '{mismatch_args}' are not allowed for dspec '{dspec_name}'.")
            return func(exec_func)
    ds = dspec
