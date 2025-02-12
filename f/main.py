from f.mods.type  import _type
from f.mods.op    import _op
from f.mods.spec  import _spec
from f.mods.dspec import _dspec

class f:
    _default_types = {}
    _default_ops = {}
    _default_specs = {}
    _default_dspecs = {}
    _allow_ops = False
    _allow_subtypes = False

    class err(Exception):
        pass

    class type(metaclass=_type, at=_default_types):
        pass
    t = type

    class op(metaclass=_op, at=_default_ops):
        def __new__(cls, op_name, *args, **kwargs):
            ops_dict = cls.at
            if op_name in ops_dict:
                return ops_dict[op_name]['op']['func']
            raise f.err(f"Type operation '{op_name}' not found in database '{at}'.")
    o = op

    class spec(metaclass=_spec, at=_default_specs, att=_default_types):
        def __new__(cls, spec_name, at=None):
            specs_dict = at if at is not None else f._default_specs
            if spec_name not in specs_dict:
                raise f.err(f"Spectrum '{spec_name}' not found in database '{at}'.")
            def exec_func(*args, **kwargs):
                spec = specs_dict[spec_name]
                for arg_types, funcinfo in spec['spec']['body'].items():
                    acceptable_types = f.acceptable_types_()
                    if not len(args) == len(arg_types):
                        raise f.err(f"Expected '{len(arg_types)}' arguments. Received: '{len(args)}'.")
                    if all(isinstance(arg, typ) for arg, typ in zip(args, arg_types) if typ in acceptable_types):
                        return funcinfo['func'](*args, **kwargs)
                mismatch_types = [type(arg).__name__ for arg in args if type(arg) not in arg_types]
                if mismatch_types:
                    raise f.err(f"Types '{mismatch_types}' are not in the domain of spectrum '{spec_name}'.")
            return exec_func
    s = spec

    class dspec(metaclass=_dspec, at=_default_dspecs, att=_default_types):
        def __new__(cls, dspec_name, at=None):
            dspecs_dict = at if at is not None else f._default_dspecs
            if dspec_name not in dspecs_dict:
                raise f.err(f"Dynamic spectrum '{dspec_name}' not found in database '{at}'.")
            def exec_func(*args, **kwargs):
                dspec = dspecs_dict[dspec_name]
                acceptable_types = f.acceptable_types_()
                type_mismatches = []
                for arg_types, funcinfo in dspec['spec']['body'].items():
                    if len(args) != len(arg_types):
                        continue
                    type_mismatches = [
                        type(arg).__name__
                        for arg, expected_types in zip(args, arg_types)
                        if expected_types not in ('any', 'Any') and not isinstance(arg, expected_types)
                    ]
                if not type_mismatches:
                    return funcinfo['func'](*args, **kwargs)
                raise f.err(f"Types '{[type(arg).__name__ for arg in args]}' are allowed for dspec '{dspec_name}'.")
            return exec_func
    ds = dspec

    @classmethod
    def conf(cls, allow_ops=False, allow_subtypes=False):
        cls._allow_ops = allow_ops
        cls._allow_subtypes = allow_subtypes
    c = conf

    @classmethod
    def acceptable_types_(cls):
        base_types = set(cls._default_types.keys())
        if cls._allow_subtypes:
            base_types.update({subtype for basetype in base_types for subtype in basetype.__subclasses__()})

        if cls._allow_ops is False:
            return base_types

        allowed_ops = {}
        if isinstance(cls._allow_ops, list):
            allowed_ops = {op_name: op['op']['func'] for op_name, op in cls._default_ops.items() if op_name in cls._allow_ops}
        elif cls._allow_ops is True:
            allowed_ops = {op_name: op['op']['func'] for op_name, op in cls._default_ops.items()}

        derived_types = set()
        for op_func in allowed_ops.values():
            for base_type in base_types:
                try:
                    new_type = op_func(base_type)
                    if isinstance(new_type, type):
                        derived_types.add(new_type)
                except:
                    continue
        return base_types.union(derived_types)
