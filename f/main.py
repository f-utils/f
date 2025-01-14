import inspect

class f:
    _default_types = None
    _default_specs = None

    class spec:
        SPECS = f._default_specs or {}

        @classmethod
        def init(cls, custom_specs=None):
            f._default_specs = custom_specs
        i = init

        @classmethod
        def set(cls, *args, **kwargs):
            if len(args) == 1 and isinstance(args[0], str):
                function_name = args[0]
                specs_dict = f._default_specs or cls.SPECS
                if function_name not in specs_dict:
                    raise ValueError(f"Function '{function_name}' is not registered.")
                return specs_dict[function_name]['exec']

            SPECS = kwargs.get('SPECS', None)

            if SPECS is not None:
                f._default_specs = SPECS
        s = set

        @classmethod
        def extend(cls, name, arg_types, func, at=None):
            specs_dict = at if at is not None else cls.SPECS
            if name not in specs_dict:
                raise ValueError(f"Function '{name}' is not registered.")
            spec = specs_dict[name]

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
            spec['exec'] = cls.mk(name, at=specs_dict)
        e = extend

        @classmethod
        def update(cls, entity, attribute, at=None):
            attribute_aliases = {
                'description': ['d', 'desc', 'description'],
                'std': ['s', 'std', 'standard'],
                'body': ['b', 'body'],
                'tags': ['t', 'tag', 'tags'],
                'comments': ['c', 'comment', 'comments']
            }

            attribute = next((key for key, aliases in attribute_aliases.items() if attribute in aliases), attribute)

            specs_dict = at if at is not None else f._default_specs or cls.SPECS

            if entity in specs_dict:
                spec = specs_dict[entity]
            else:
                raise ValueError(f"Entity '{entity}' not found in specs.")

            if attribute == 'description':
                def _update_desc_(new_description):
                    spec['description'] = new_description
                return _update_desc_

            if attribute == 'std' and spec in specs_dict.values():
                def _update_std_(new_std_func):
                    spec['std'] = new_std_func
                    spec['std_repr'] = cls.repr(new_std_func)
                    cls.set(spec['name'])
                    specs_dict[spec['name']] = spec
                return _update_std_

            if attribute == 'body' and spec in specs_dict.values():
                def _update_body_(typeargument, new_argument_function):
                    for (arg_types, kwarg_types), func in spec['body'].items():
                        if typeargument in arg_types:
                            spec['body'][(arg_types, kwarg_types)] = {
                                'func': new_argument_function,
                                'repr': cls.repr(new_argument_function)
                            }
                            cls.set(spec['name'])
                            specs_dict[spec['name']] = spec
                            return
                    raise ValueError(f"Type '{typeargument}' not found in domain.")
                return _update_body_

            raise ValueError(f"Unknown or unsupported update attribute '{attribute}'.")
        u = update

        @classmethod
        def add(cls, entity, attribute, at=None):
            attribute_aliases = {
                'tags': ['t', 'tag', 'tags'],
                'comments': ['c', 'comment', 'comments']
            }

            attribute = next((key for key, aliases in attribute_aliases.items() if attribute in aliases), attribute)

            specs_dict = at if at is not None else f._default_specs or cls.SPECS

            if entity in specs_dict:
                spec = specs_dict[entity]
            else:
                raise ValueError(f"Entity '{entity}' not found in specs.")

            if attribute == 'tags':
                def _add_tags_(tag):
                    if tag not in spec['tags']:
                        spec['tags'].append(tag)
                return _add_tags_

            if attribute == 'comments':
                def _add_comments_(comment_id, comment_text):
                    spec['comments'][comment_id] = comment_text
                return _add_comments_

            raise ValueError(f"Unknown or unsupported add attribute '{attribute}'.")
        a = add

        @classmethod
        def delete(cls, entity, attribute, at=None):
            attribute_aliases = {
                'tags': ['t', 'tag', 'tags'],
                'comments': ['c', 'comment', 'comments']
            }

            attribute = next((key for key, aliases in attribute_aliases.items() if attribute in aliases), attribute)

            specs_dict = at if at is not None else f._default_specs or cls.SPECS

            if entity in specs_dict:
                spec = specs_dict[entity]
            else:
                raise ValueError(f"Entity '{entity}' not found in specs.")

            if attribute == 'tags':
                def _delete_tags_(tag):
                    if tag in spec['tags']:
                        spec['tags'].remove(tag)
                return _delete_tags_

            if attribute == 'comments':
                def _delete_comments_(comment_id):
                    if comment_id in spec['comments']:
                        del spec['comments'][comment_id]
                return _delete_comments_

            raise ValueError(f"Unknown or unsupported delete attribute '{attribute}'.")
        d = delete

        @classmethod
        def mk(cls, name, at=None):
            specs_dict = at if at is not None else cls.SPECS
            def exec_func(*args, **kwargs):
                funcspec = specs_dict[name]
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
    s = spec

    class type:
        TYPES = f._default_types or {}

        @classmethod
        def init(cls, custom_types=None):
            f._default_types = custom_types
        i = init

        @classmethod
        def set(cls, *args, **kwargs):
            TYPES = kwargs.get('TYPES', None)

            if TYPES is not None:
                f._default_types = TYPES
        s = set

        @classmethod
        def extend(cls, typename, description, tags=None, comments=None, at=None):
            types_dict = at if at is not None else f._default_types or cls.TYPES
            if typename in types_dict:
                raise ValueError(f"Type '{typename}' is already registered.")
            types_dict[typename] = {
                'description': description,
                'tags': tags or [],
                'comments': comments or {}
            }
        e = extend

        @classmethod
        def update(cls, typename, description=None, tags=None, comments=None, at=None):
            types_dict = at if at is not None else f._default_types or cls.TYPES
            if typename not in types_dict:
                raise ValueError(f"Type '{typename}' is not registered.")

            if description is not None:
                types_dict[typename]['description'] = description

            if tags is not None:
                types_dict[typename]['tags'] = tags

            if comments is not None:
                types_dict[typename]['comments'] = comments
        u = update

        @classmethod
        def add(cls, typename, tags=None, comments=None, at=None):
            types_dict = at if at is not None else f._default_types or cls.TYPES
            if typename not in types_dict:
                raise ValueError(f"Type '{typename}' is not registered.")

            if tags:
                types_dict[typename]['tags'].extend(tags)

            if comments:
                types_dict[typename]['comments'].update(comments)
        a = add

        @classmethod
        def delete(cls, typename, tags=None, comments=None, at=None):
            types_dict = at if at is not None else f._default_types or cls.TYPES
            if typename not in types_dict:
                raise ValueError(f"Type '{typename}' is not registered.")

            if tags:
                for tag in tags:
                    if tag in types_dict[typename]['tags']:
                        types_dict[typename]['tags'].remove(tag)

            if comments:
                for comment in comments:
                    if comment in types_dict[typename]['comments']:
                        del types_dict[typename]['comments'][comment]
        d = delete 
    t = type

