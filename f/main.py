import inspect

class f:
    _default_types = None
    _default_specs = None
    _aliases = {
        'description': ['d', 'desc', 'description'],
        'std': ['s', 'std', 'standard'],
        'body': ['b', 'body'],
        'tags': ['t', 'tag', 'tags'],
        'comments': ['c', 'comment', 'comments'],
        'all': ['a', 'any', 'every']
    }

    class spec:
        @classmethod
        def SPECS(cls):
            return f._default_specs or {}

        @classmethod
        def init(cls, custom_specs=None):
            f._default_specs = custom_specs
        i = init

        @classmethod
        def set(cls, *args, **kwargs):
            specs_dict = kwargs.get('SPECS', None)
            if specs_dict is not None:
                cls._default_specs = specs_dict
                return
            if len(args) == 1 and isinstance(args[0], str):
                function_name = args[0]
                custom_specs = kwargs.get('at', None)
                specs_dict = custom_specs if custom_specs is not None else cls._default_specs
                if function_name in specs_dict:
                    return specs_dict[function_name]['exec']
                raise ValueError(f"Function '{function_name}' not found.")
        s = set

        @classmethod
        def extend(cls, name, arg_types, func, at=None):
            specs_dict = at if at is not None else cls.SPECS()
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

            specs_dict = at if at is not None else f._default_specs or cls.SPECS()

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

            specs_dict = at if at is not None else f._default_specs or cls.SPECS()

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

            specs_dict = at if at is not None else f._default_specs or cls.SPECS()

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
        def info(cls, f, what='spec'):
            attribute = next(
                (key for key, aliases in f._aliases.items() if what in aliases), what)

            def _typestr_(typetuple, kwarg_dict):
                if not typetuple:
                    typetuple = ()
                if not kwarg_dict:
                    kwarg_dict = {}

                arg_str = ', '.join(t.__name__ if hasattr(t, '__name__') else str(t) for t in typetuple)
                kwarg_str = ', '.join(f"{key}: {t.__name__}" for key, t in kwarg_dict.items())
                return ', '.join(filter(None, [arg_str, kwarg_str]))

            spec = cls.SPECS()[f]
            info_string = ""
            if attribute == 'all':
                wrapped_desc = textwrap.fill(f"{spec['description']}", width=84)
                info_string += f"Spectrum of function '{spec['name']}':\n"
                info_string += f"  DESC:\n    {wrapped_desc}\n"
                info_string += f"  STD:\n    {spec['std_repr']}\n"
                info_string += f"  TAGS: {', '.join(spec.get('tags', []))}\n"
                info_string += "  DOMAIN:\n"
                for i, (arg_types, kwarg_types) in enumerate(spec['domain'], 1):
                    kwarg_types = dict(kwarg_types)
                    info_string += f"    {i}. {_typestr_(arg_types, kwarg_types)}\n"
                info_string += "  BODY:\n"
                for i, ((arg_combo, kwarg_combo), funcinfo) in enumerate(spec['body'].items(), 1):
                    info_string += f"    {i}. {_typestr_(arg_combo, dict(kwarg_combo))} => {funcinfo['repr']}\n"
                info_string += f"  COMMENTS:\n"
                for comment_id, comment in spec.get('comments', {}).items():
                    wrapped_comment = textwrap.fill(comment, width=84)
                    info_string += f"    {comment_id}: {wrapped_comment}\n"
            elif attribute == 'domain':
                info_string += f"Domain of spectrum '{spec['name']}':\n"
                for i, (arg_types, kwarg_types) in enumerate(spec['domain'], 1):
                    kwarg_types = dict(kwarg_types)
                    info_string += f"    {i}. {_typestr_(arg_types, kwarg_types)}\n"
            elif attribute == 'std':
                info_string += f"Standard return for spectrum '{spec['name']}':\n"
                info_string += f"    {spec['std_repr']}\n"
            elif attribute == 'body':
                info_string += f"Body of spectrum '{spec['name']}':\n"
                for i, ((arg_combo, kwarg_combo), funcinfo) in enumerate(spec['body'].items(), 1):
                    info_string += f"    {i}. {_typestr_(arg_combo, dict(kwarg_combo))} => {funcinfo['repr']}\n"
            elif attribute == 'tags':
                info_string += f"Tags for spectrum '{spec['name']}':\n"
                for i, tag in enumerate(spec.get('tags', []), 1):
                    info_string += f"    {i}. {tag}\n"
            elif attribute == 'comments':
                info_string += f"Comments for spectrum '{spec['name']}':\n"
                for comment_id, comment in spec.get('comments', {}).items():
                    wrapped_comment = textwrap.fill(comment, width=84)
                    info_string += f"    {comment_id}: {wrapped_comment}\n"
            elif attribute == 'description':
                wrapped_desc = textwrap.fill(spec['description'], width=84)
                info_string += f"Description of spectrum '{spec['name']}':\n"
                info_string += f"    {wrapped_desc}\n"
            else:
                raise ValueError(f"Unknown attribute '{what}' to print.")
            return info_string
        i = info

        @classmethod
        def mk(cls, name, at=None):
            specs_dict = at if at is not None else cls.SPECS()
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
        @classmethod
        def TYPES(cls):
            return f._default_types

        @classmethod
        def init(cls, custom_types=None):
            f._default_types = custom_types if custom_types is not None else {}

        @classmethod
        def extend(cls, typename, description, tags=None, comments=None, at=None):
            types_dict = at if at is not None else f._default_types
            if typename not in types_dict:
                types_dict[typename] = {
                    'description': description,
                    'tags': tags or [],
                    'comments': comments or {}
                }
            else:
                raise ValueError(f"Type '{typename}' is already registered.") 
        e = extend
        @classmethod
        def set(cls, *args, **kwargs):
            TYPES = kwargs.get('TYPES', None)

            if TYPES is not None:
                f._default_types = TYPES
        s = set

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

        @classmethod
        def info(cls, typename, what='all'):
            attribute = next(
                (key for key, aliases in f._aliases.items() if what in aliases), what)

            type_info = cls.TYPES().get(typename, None)
            if not type_info:
                raise ValueError(f"Type '{typename}' not found.")

            info_string = f"Type '{typename}':\n"
            if attribute == 'description':
                wrapped_desc = textwrap.fill(type_info['description'], width=84)
                info_string += f"Type '{typename} description':\n"
                info_string += f"    {wrapped_desc}\n"
            elif attribute == 'tags':
                info_string += f"Type '{typename} tags':\n"
                for i, tag in enumerate(type_info.get('tags', []), 1):
                    info_string += f"    {i}. {tag}\n"
            elif attribute == 'comments':
                info_string += f"Type '{typename} comments':\n"
                for comment_id, comment in type_info.get('comments', {}).items():
                    wrapped_comment = textwrap.fill(comment, width=84)
                    info_string += f"    {comment_id}: {wrapped_comment}\n"
            elif attribute == 'all':
                wrapped_desc = textwrap.fill(type_info['description'], width=84)
                info_string += f"Type '{typename}  info:\n"
                info_string += f"    DESC: {wrapped_desc}\n"
                info_string += f"    TAGS: \n"
                for i, tag in enumerate(type_info.get('tags', []), 1):
                    info_string += f"    {i}. {tag}\n"
                info_string += f"    COMMENTS:\n"
                for comment_id, comment in type_info.get('comments', {}).items():
                    wrapped_comment = textwrap.fill(comment, width=84)
                    info_string += f"    {comment_id}: {wrapped_comment}\n"
            else:
                raise ValueError(f"Unknown attribute '{what}' to print.")
            return info_string
        I = info
    t = type

