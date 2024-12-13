import inspect
import textwrap

class _:
    TYPES = {}
    FUNCS = {}

    @classmethod
    def type(cls, typename, description):
        if typename in cls.TYPES:
            raise ValueError(f"Type '{typename}' is already registered.")
        cls.TYPES[typename] = description
    t = type

    @classmethod
    def func(cls, name, description, std_func):
        if name in cls.FUNCS:
            raise ValueError(f"Function '{name}' is already initialized.")
        funcstructure = {
            'name': name,
            'description': description,
            'std': std_func,
            'body': {},
            'exec': None,
            'domain': [],
            'std_repr': cls.repr(std_func)
        }
        exec_func = cls.mk(name)
        globals()[name] = exec_func
        cls.FUNCS[name] = funcstructure
    f = func

    @classmethod
    def extend(cls, name, arg_and_kwarg_types, case_func):
        if not callable(case_func):
            raise ValueError("case_func must be callable.")

        arg_types, kwarg_types = cls.parse(arg_and_kwarg_types)

        if (tuple(arg_types), frozenset(kwarg_types.items())) in cls.FUNCS[name]['body']:
            raise ValueError(f"The type combination '{arg_types}' with '{kwarg_types}' is already in domain for function '{name}'.")

        cls.FUNCS[name]['body'][(tuple(arg_types), frozenset(kwarg_types.items()))] = {
            'func': case_func,
            'repr': cls.repr(case_func)
        }
        cls.FUNCS[name]['domain'].append((arg_types, kwarg_types))

        cls.FUNCS[name]['exec'] = cls.mk(name)
        globals()[name] = cls.mk(name)
    ext = extend
    e = ext

    @classmethod
    def mk(cls, name):
        def exec_func(*args, **kwargs):
            funcspec = cls.spec(name)
            if funcspec['exec']:
                return funcspec['exec'](*args, **kwargs)
            return funcspec['std'](*args, **kwargs)
        return exec_func

    @classmethod
    def parse(cls, arg_and_kwarg_types):
        if isinstance(arg_and_kwarg_types, dict):
            return (), arg_and_kwarg_types
        elif isinstance(arg_and_kwarg_types, tuple):
            split_index = next((i for i, t in enumerate(arg_and_kwarg_types) if isinstance(t, dict)), len(arg_and_kwarg_types))
            arg_types = arg_and_kwarg_types[:split_index]
            kwarg_types = arg_and_kwarg_types[split_index] if split_index < len(arg_and_kwarg_types) else {}
            return arg_types, kwarg_types
        elif isinstance(arg_and_kwarg_types, type):
            return (arg_and_kwarg_types,), {}
        else:
            raise ValueError("Invalid format for argument types. Must be a type, dict, or tuple.")

    @classmethod
    def repr(cls, func):
        try:
            source = inspect.getsource(func).strip()
        except (OSError, TypeError):
            source = repr(func)

        if "lambda" in source:
            lambda_idx = source.index("lambda")
            return source[lambda_idx:].strip().rstrip(')')
        return source

    @classmethod
    def spec(cls, f):
        if f in cls.FUNCS:
            return cls.FUNCS[f]
        raise ValueError(f"Function specification for '{f}' not found.")
    s = spec

    @classmethod
    def info(cls, f, what='spec'):
        def _typestr_(typetuple, kwarg_dict):
            arg_str = ', '.join(t.__name__ for t in typetuple)
            kwarg_str = ', '.join(f"{key}: {t.__name__}" for key, t in kwarg_dict.items())
            return ', '.join(filter(None, [arg_str, kwarg_str]))

        spec = cls.spec(f)
        if what == 'spec':
            wrapped_desc = textwrap.fill(f"{spec['description']}", width=84)
            print(f"Spectrum of function '{spec['name']}':")
            print("  DESC:")
            print(f"    {wrapped_desc}")
            print("  STD:")
            print(f"    {spec['std_repr']}")
            print("  DOMAIN:")
            for i, (arg_types, kwarg_types) in enumerate(spec['domain'], 1):
                print(f"    {i}. {_typestr_(arg_types, kwarg_types)}")
            print("  BODY:")
            for i, ((arg_combo, kwarg_combo), funcinfo) in enumerate(spec['body'].items(), 1):
                print(f"    {i}. {_typestr_(arg_combo, dict(kwarg_combo))} => {funcinfo['repr']}")
        elif what == 'domain':
            print(f"Domain of function '{spec['name']}':")
            for i, (arg_types, kwarg_types) in enumerate(spec['domain'], 1):
                print(f"    {i}. {_typestr_(arg_types, kwarg_types)}")
        elif what == 'std':
            print(f"Standard return for function '{spec['name']}':")
            print(f"    {spec['std_repr']}")
        elif what == 'body':
            print(f"Body of function '{spec['name']}':")
            for i, ((arg_combo, kwarg_combo), funcinfo) in enumerate(spec['body'].items(), 1):
                print(f"    {i}. {_typestr_(arg_combo, dict(kwarg_combo))} => {funcinfo['repr']}")
        elif what == 'desc':
            print(f"Description of function '{spec['name']}':")
            print(f"    {spec['description']}")
        else:
            raise ValueError(f"Unknown attribute '{what}' to print.")
    i = info

    @classmethod
    def update(cls, f, attribute):
        spec = cls.spec(f)

        if attribute == 'desc':
            def _update_desc_(new_description):
                spec['description'] = new_description
            return _update_desc_

        if attribute == 'std':
            def _update_std_(new_std_func):
                spec['std'] = new_std_func
                spec['std_repr'] = cls.repr(new_std_func)
                globals()[spec['name']] = cls.mk(spec['name'])
                cls.FUNCS[spec['name']] = spec
            return _update_std_

        if attribute == 'body':
            def _update_body_(typeargument, new_argument_function):
                if typeargument not in cls.TYPES:
                    raise ValueError(f"Type '{typeargument}' not registered.")
                for (arg_types, kwarg_types), func in spec['body'].items():
                    if typeargument in arg_types:
                        spec['body'][(arg_types, kwarg_types)] = {
                            'func': new_argument_function,
                            'repr': cls.repr(new_argument_function)
                        }
                        globals()[spec['name']] = cls.mk(spec['name'])
                        cls.FUNCS[spec['name']] = spec
                        return
                raise ValueError(f"Type '{typeargument}' not found in domain.")
            return _update_body_

        raise ValueError(f"Unknown update attribute '{attribute}'.")
    u = update

