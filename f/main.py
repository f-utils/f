import inspect
import textwrap
import re

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

    @staticmethod
    def _resolve_alias(where):
        for key, aliases in f._aliases.items():
            if where in aliases:
                return key
        raise ValueError(f"Invalid alias '{where}'.")

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
        def get(cls, object, entry, at=None):
            entry_key = f._resolve_alias(entry)
            specs_dict = at if at is not None else cls.SPECS()

            if object not in specs_dict:
                raise ValueError(f"Spectra '{object}' not found.")

            spec = specs_dict[object]
            if entry_key in spec:
                return spec[entry_key]
            else:
                raise ValueError(f"Entry '{entry_key}' not found in spectra '{object}'.")

        @classmethod
        def info(cls, spectrum_name, what='all'):
            info_string = ""

            if what == 'all':
                attributes = ['description', 'std', 'tags', 'domain', 'body', 'comments']
            else:
                attributes = [f._resolve_alias(what)]

            info_string += f"Spectrum of function '{spectrum_name}':\n"

            for attribute in attributes:
                entry = cls.get(spectrum_name, attribute)
                if attribute == 'description':
                    wrapped_entry = textwrap.fill(entry, width=84)
                    info_string += f"  DESC:\n    {wrapped_entry}\n"
                elif attribute == 'std':
                    info_string += f"  STD:\n    {entry}\n"
                elif attribute == 'tags':
                    info_string += f"  TAGS: {', '.join(entry)}\n"
                elif attribute == 'domain':
                    info_string += "  DOMAIN:\n"
                    for i, (arg_types, kwarg_types) in enumerate(entry, 1):
                        kwarg_types = dict(kwarg_types)
                        info_string += f"    {i}. {_typestr_(arg_types, kwarg_types)}\n"
                elif attribute == 'body':
                    info_string += "  BODY:\n"
                    for i, ((arg_combo, kwarg_combo), funcinfo) in enumerate(entry.items(), 1):
                        info_string += f"    {i}. {_typestr_(arg_combo, dict(kwarg_combo))} => {funcinfo['repr']}\n"
                elif attribute == 'comments':
                    info_string += f"  COMMENTS:\n"
                    for comment_id, comment in entry.items():
                        wrapped_comment = textwrap.fill(comment, width=84)
                        info_string += f"    {comment_id}: {wrapped_comment}\n"
            return info_string
        I = info

        @classmethod
        def search(cls, term, where='description', at=None):
            where_key = f._resolve_alias(where)
            specs_dict = at if at is not None else cls.SPECS()
            pattern = re.compile(term)
            results = []

            for spec_name, info in specs_dict.items():
                entry_value = info.get(where_key, '')
                if isinstance(entry_value, list):
                    entry_value = ' '.join(entry_value)
                if pattern.search(entry_value):
                    results.append(info)
            return results

        @classmethod
        def check(cls, spec_name, at=None):
            specs_dict = at if at is not None else cls.SPECS()
            return spec_name in specs_dict

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
        def get(cls, object, entry, at=None):
            entry_key = f._resolve_alias(entry)
            types_dict = at if at is not None else cls.TYPES()

            if object not in types_dict:
                raise ValueError(f"Type '{object}' not found.")

            type_info = types_dict[object]
            if entry_key in type_info:
                return type_info[entry_key]
            else:
                raise ValueError(f"Entry '{entry_key}' not found in type '{object}'.")

        @classmethod
        def info(cls, typename, what='all'):
            info_string = ""

            if what == 'all':
                attributes = ['description', 'tags', 'comments']
            else:
                attributes = [f._resolve_alias(what)]

            info_string += f"Type '{typename.__name__}' info:\n"

            for attribute in attributes:
                entry = cls.get(typename, attribute)
                if attribute == 'description':
                    wrapped_entry = textwrap.fill(entry, width=84)
                    info_string += f"  DESC: {wrapped_entry}\n"
                elif attribute == 'tags':
                    info_string += f"  TAGS:\n"
                    for i, tag in enumerate(entry, 1):
                        info_string += f"    {i}. {tag}\n"
                elif attribute == 'comments':
                    info_string += f"  COMMENTS:\n"
                    for comment_id, comment in entry.items():
                        wrapped_comment = textwrap.fill(comment, width=84)
                        info_string += f"    {comment_id}: {wrapped_comment}\n"
            return info_string
        I = info

        @classmethod
        def search(cls, term, where='description', at=None):
            where_key = f._resolve_alias(where)
            types_dict = at if at is not None else cls.TYPES()
            pattern = re.compile(term)
            results = []

            for typename, info in types_dict.items():
                entry_value = info.get(where_key, '')
                if isinstance(entry_value, list):
                    entry_value = ' '.join(entry_value)
                if pattern.search(entry_value):
                    results.append(typename)

            return results

        @classmethod
        def check(cls, typename, at=None):
            types_dict = at if at is not None else cls.TYPES()
            return typename in types_dict
    t = type

