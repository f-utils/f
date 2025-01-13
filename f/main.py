import inspect

class f:
    TYPES = {}
    FUNCS = {}

    _default_types = None
    _default_funcs = None

    @classmethod
    def init(cls, custom_types=None, custom_funcs=None):
        cls._default_types = custom_types
        cls._default_funcs = custom_funcs

    @classmethod
    def set(cls, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            function_name = args[0]
            funcs_dict = cls._default_funcs or cls.FUNCS
            if function_name not in funcs_dict:
                raise ValueError(f"Function '{function_name}' is not registered.")
            return funcs_dict[function_name]['exec']

        TYPES = kwargs.get('TYPES', None)
        FUNCS = kwargs.get('FUNCS', None)

        if TYPES is not None:
            cls._default_types = TYPES
        if FUNCS is not None:
            cls._default_funcs = FUNCS

    @classmethod
    def type(cls, typename, description, at=None):
        types_dict = at if at is not None else (cls._default_types or cls.TYPES)
        if typename in types_dict:
            raise ValueError(f"Type '{typename}' is already registered.")
        types_dict[typename] = description
    t = type

    @classmethod
    def func(cls, name, description, std_func, tags=None, comments=None, at=None):
        funcs_dict = at if at is not None else (cls._default_funcs or cls.FUNCS)
        if name in funcs_dict:
            raise ValueError(f"Function '{name}' is already initialized.")
        funcstructure = {
            'name': name,
            'description': description,
            'std': std_func,
            'body': {},
            'exec': None,
            'domain': [],
            'tags': tags or [],
            'comments': comments or {},
            'std_repr': cls.repr(std_func)
        }
        funcs_dict[name] = funcstructure
    f = func

    @classmethod
    def extend(cls, name, arg_types, func, at=None):
        funcs_dict = at if at is not None else (cls._default_funcs or cls.FUNCS)
        if name not in funcs_dict:
            raise ValueError(f"Function '{name}' is not registered.")
        spec = funcs_dict[name]

        kwarg_types = {}
        if isinstance(arg_types, tuple):
            if len(arg_types) == 2 and isinstance(arg_types[1], dict):
                pos_types, kwarg_types = arg_types
            else:
                pos_types = arg_types
                kwarg_types = {}
        else:
            pos_types = (arg_types,) if not isinstance(arg_types, tuple) else arg_types
            kwarg_types = {}

        kwarg_items = tuple(kwarg_types.items())
        if (pos_types, kwarg_items) not in spec['domain']:
            spec['domain'].append((pos_types, kwarg_items))

        spec['body'][(pos_types, kwarg_items)] = {
            'func': func,
            'repr': cls.repr(func)
        }
        spec['exec'] = cls.mk(name, at=funcs_dict)
    e = extend

    @classmethod
    def update(cls, f, attribute, at=None):
        attribute_aliases = {
            'description': ['d', 'desc', 'description'],
            'std': ['s', 'std', 'standard'],
            'body': ['b', 'body'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments']
        }

        attribute = next((key for key, aliases in attribute_aliases.items() if attribute in aliases), attribute)

        funcs_dict = at if at is not None else (cls._default_funcs or cls.FUNCS)
        spec = funcs_dict.get(f)

        if attribute == 'description':
            def _update_desc_(new_description):
                spec['description'] = new_description
            return _update_desc_

        if attribute == 'std':
            def _update_std_(new_std_func):
                spec['std'] = new_std_func
                spec['std_repr'] = cls.repr(new_std_func)
                cls.set(spec['name'])
                funcs_dict[spec['name']] = spec
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
                        cls.set(spec['name'])
                        funcs_dict[spec['name']] = spec
                        return
                raise ValueError(f"Type '{typeargument}' not found in domain.")
            return _update_body_

        if attribute == 'tags':
            def _update_tags_(*args):
                if len(args) == 1:
                    tag = args[0]
                    if tag not in spec['tags']:
                        spec['tags'].append(tag)
                elif len(args) == 2:
                    old_tag, new_tag = args
                    if old_tag in spec['tags']:
                        spec['tags'].remove(old_tag)
                        spec['tags'].append(new_tag)
            return _update_tags_

        if attribute == 'comments':
            def _update_comments_(comment_id, comment_text):
                spec['comments'][comment_id] = comment_text
            return _update_comments_

        raise ValueError(f"Unknown update attribute '{attribute}'.")
    u = update

    @classmethod
    def mk(cls, name, at=None):
        funcs_dict = at if at is not None else (cls._default_funcs or cls.FUNCS)
        def exec_func(*args, **kwargs):
            funcspec = funcs_dict[name]
            for (arg_types, kwarg_types_tuple), funcinfo in funcspec['body'].items():
                kwarg_types = dict(kwarg_types_tuple)
                if all(isinstance(arg, typ) for arg, typ in zip(args, arg_types)) and \
                        all(isinstance(kwargs.get(key), typ) for key, typ in kwarg_types.items()):
                    return funcinfo['func'](*args, **kwargs)
            return funcspec['std'](*args, **kwargs)
        return exec_func

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
    def spec(cls, f, at=None):
        funcs_dict = at if at is not None else cls.FUNCS
        if f in funcs_dict:
            return funcs_dict[f]
        raise ValueError(f"Function specification for '{f}' not found.")
    s = spec

    @classmethod
    def get(cls, f, entry, at=None):
        entry_aliases = {
            'description': ['d', 'desc', 'description'],
            'domain': ['D', 'domain'],
            'body': ['b', 'body'],
            'std': ['s', 'std', 'standard'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'spec': ['S', 'spec', 'spectrum']
        }

        entry = next((key for key, aliases in entry_aliases.items() if entry in aliases), entry)

        spec = cls.spec(f, at=at)

        if entry == 'description':
            return lambda: spec['description']

        if entry == 'domain':
            return lambda: spec['domain']

        if entry == 'body':
            def _get_body_(type_name=None):
                if type_name is None:
                    return spec['body']
                for (arg_types, _), func in spec['body'].items():
                    if type_name in arg_types:
                        return func['func']
                raise ValueError(f"Type '{type_name}' not found in body.")
            return _get_body_

        if entry == 'std':
            return lambda: spec['std']

        if entry == 'tags':
            return spec['tags']

        if entry == 'comments':
            def _get_comments_(comment_id=None):
                if comment_id is None:
                    return spec['comments']
                return spec['comments'].get(comment_id, f"Comment ID '{comment_id}' not found.")
            return _get_comments_

        if entry == 'spec':
            return lambda: spec

        raise ValueError(f"Unknown entry '{entry}'.")
    g = get
