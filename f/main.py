import inspect
import textwrap
import re

class f:
    _default_types = None
    _default_specs = None

    class spec:
        _aliases = {
            'metadata': {
                'description': ['d', 'desc', 'description'],
                'tags': ['t', 'tag', 'tags'],
                'comments': ['c', 'comment', 'comments']
                },
            'spec': {
                'std': ['s', 'std', 'standard'],
                'domain': ['d', 'domain'],
                'body': ['b', 'body']
            },
            'all': ['a', 'any', 'every', 'all']
        }

        def __init__(self, spec, at=None):
            self.spec_name = spec
            self.at = at
            self.attach_ = self.attach_()

        def attach_(self):
            custom_specs = self.at or self.__class__.export()
            if self.spec_name in custom_specs:
                return self.__class__.mk(self.spec_name, at=custom_specs)
            else:
                raise ValueError(f"Function '{self.spec_name}' not found.")

        def __call__(self, *args, **kwargs):
            return self.attach_(*args, **kwargs)

        @classmethod
        def _resolve_alias(cls, where):
            for category, sub_aliases in cls._aliases.items():
                if category == where:
                    return category
                for key, aliases in sub_aliases.items():
                    if where in aliases:
                        return key
            return where

        @classmethod
        def export(cls):
            return f._default_specs or {}
        E = export

        @classmethod
        def database(cls, *args):
            if len(args) == 1:
                f._default_specs = args[0]
            elif len(args) == 0:
                f._default_specs = {}
            else:
                raise AttributeError(f"Provided '{len(args)}' arguments. Expecting at most one argument.")
        db = database

        @classmethod
        def init(cls, name, description, std_return_function, at=None):
            if not isinstance(name, str):
                raise TypeError("The name must be a string.")
            if not isinstance(description, str):
                raise TypeError("The description must be a string.")
            if not callable(std_return_function):
                raise TypeError("The std_return_function must be a function or a lambda.")

            spec_dict = at if at is not None else f._default_specs
            if name in spec_dict:
                raise ValueError(f"Specification '{name}' is already registered.")

            spec_dict[name] = {
                'metadata': {
                    'description': description,
                    'tags': [],
                    'comments': {}
                },
                'spec': {
                    'std': {
                        'func': std_return_function,
                        'repr': cls.repr(std_return_function)
                    },
                    'domain': [],
                    'body': {},
                    'exec': ''
                }
            }
        i = init

        @classmethod
        def set(cls, *args, **kwargs):
            if len(args) == 1 and isinstance(args[0], str):
                function_name = args[0]
                custom_specs = kwargs.get('at', None)
                specs_dict = custom_specs if custom_specs is not None else cls.export()
                if function_name in specs_dict:
                    return specs_dict[function_name]['spec']['exec']
                raise ValueError(f"Function '{function_name}' not found.")
        s = set

        @classmethod
        def extend(cls, name, arg_types, func, at=None):
            specs_dict = at if at is not None else cls.export()
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
            if (pos_types, kwarg_items) not in spec['spec']['domain']:
                spec['spec']['domain'].append((pos_types, kwarg_items))

            spec['spec']['body'][(pos_types, kwarg_items)] = {
                'func': func,
                'repr': cls.repr(func)
            }
            spec['spec']['exec'] = cls.mk(name, at=specs_dict)
        e = extend

        @classmethod
        def update(cls, spec_name, attribute, at=None):
            attribute = cls._resolve_alias(attribute)
            specs_dict = at if at is not None else f._default_specs
            if spec_name not in specs_dict:
                raise ValueError(f"Specification '{spec_name}' is not registered.")

            spec_info = specs_dict[spec_name]

            if attribute == 'description':
                def _update_desc_(new_description):
                    if not isinstance(new_description, str):
                        raise TypeError("The new description must be a string.")
                    spec_info['metadata']['description'] = new_description
                return _update_desc_

            if attribute == 'tags':
                def _update_tag_(old_tag, new_tag):
                    if not isinstance(old_tag, str) or not isinstance(new_tag, str):
                        raise TypeError("Both old tag and new tag must be strings.")
                    if not spec_info['metadata']['tags']:
                        raise ValueError("Cannot update tag as the tags list is empty.")
                    if new_tag in spec_info['metadata']['tags']:
                        raise ValueError(f"Tag '{new_tag}' already exists in specification '{spec_name}'.")
                    if old_tag in spec_info['metadata']['tags']:
                        spec_info['metadata']['tags'][spec_info['metadata']['tags'].index(old_tag)] = new_tag
                    else:
                        raise ValueError(f"Tag '{old_tag}' not found in specification '{spec_name}'.")
                return _update_tag_

            if attribute == 'comments':
                def _update_comment_(comment_id, new_comment_value):
                    if not isinstance(comment_id, str) or not isinstance(new_comment_value, str):
                        raise TypeError("Both comment ID and new comment value must be strings.")
                    if not spec_info['metadata']['comments']:
                        raise ValueError("Cannot update comment as the comments dictionary is empty.")
                    if comment_id in spec_info['metadata']['comments']:
                        spec_info['metadata']['comments'][comment_id] = new_comment_value
                    else:
                        raise ValueError(f"Comment ID '{comment_id}' not found in specification '{spec_name}'.")
                return _update_comment_

            if attribute == 'std':
                def _update_std_(new_standard_return):
                    if not callable(new_standard_return):
                        raise TypeError("The new standard return must be a function or a lambda.")
                    spec_info['spec']['std'] = new_standard_return
                    spec_info['spec']['std_repr'] = cls.repr(new_standard_return)
                return _update_std_

            if attribute == 'body':
                def _update_body_(given_type, new_return_for_given_type):
                    if not callable(new_return_for_given_type):
                        raise TypeError("The new return for given type must be a function or a lambda.")
                    for (arg_types, kwarg_types), func in spec_info['spec']['body'].items():
                        if given_type in arg_types:
                            spec_info['spec']['body'][(arg_types, kwarg_types)] = {
                                'func': new_return_for_given_type,
                                'repr': cls.repr(new_return_for_given_type)
                            }
                            return
                    raise ValueError(f"Type '{given_type}' not found in domain for specification '{spec_name}'.")
                return _update_body_

            raise ValueError(f"Unknown or unsupported update attribute '{attribute}'.")
        u = update

        @classmethod
        def add(cls, entity, attribute, at=None):
            attribute = cls._resolve_alias(attribute)
            specs_dict = at if at is not None else cls.export()

            if entity in specs_dict:
                spec = specs_dict[entity]['metadata']
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
            attribute = cls._resolve_alias(attribute)
            specs_dict = at if at is not None else cls.export()
            if entity in specs_dict:
                spec = specs_dict[entity]['metadata']
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
        def get(cls, spec_name, entry, at=None):
            specs_dict = at if at is not None else f._default_specs
            if spec_name not in specs_dict:
                raise ValueError(f"Specification '{spec_name}' not found.")

            entry_path = entry.split('.')
            current = specs_dict[spec_name]

            for part in entry_path:
                alias = cls._resolve_alias(part)

                for key in ['metadata', 'spec']:
                    if key in current and alias in current[key]:
                        current = current[key][alias]
                        break
                else:
                    if isinstance(current, dict) and alias in current:
                        current = current[alias]
                    else:
                        raise ValueError(f"Entry '{part}' not found in specification '{spec_name}'.")

            if isinstance(current, dict):
                return current
            return current

        g = get

        @classmethod
        def info(cls, spec_name, what='all'):
            info_string = f"Spectrum '{spec_name}':\n"

            if what == 'all':
                attributes = ['description', 'std', 'tags', 'domain', 'body', 'comments']
            else:
                attributes = [cls._resolve_alias(what)]

            for attribute in attributes:
                entry = cls.get(spec_name, attribute)
                if attribute == 'description':
                    wrapped_entry = textwrap.fill(entry, width=84)
                    info_string += f"  DESC:\n    {wrapped_entry}\n"
                elif attribute == 'std':
                    info_string += f"  STD:\n    {entry}\n"
                elif attribute == 'tags':
                    info_string += f"  TAGS: {', '.join(entry)}\n"
                elif attribute == 'domain':
                    info_string += "  DOMAIN:\n"
                    for i, (arg_types, _) in enumerate(entry, 1):
                        type_names = ', '.join(str(t.__name__) if hasattr(t, '__name__') else str(t) for t in arg_types)
                        info_string += f"    {i}. {type_names}\n"
                elif attribute == 'body':
                    body_info = f"  BODY:\n"
                    for i, ((arg_combo, _), funcinfo) in enumerate(entry.items(), 1):
                        some_type = next(iter(arg_combo), 'Unknown')
                        info_string += f"    {i}. {some_type.__name__ if hasattr(some_type, '__name__') else some_type} => {funcinfo['repr']}\n" 
                elif attribute == 'comments':
                    info_string += f"  COMMENTS:\n"
                    for comment_id, comment in entry.items():
                        wrapped_comment = textwrap.fill(comment, width=84)
                        info_string += f"    {comment_id}: {wrapped_comment}\n"

            return info_string
        I = info

        @classmethod
        def search(cls, term, where='description', at=None):
            where_key = cls._resolve_alias(where)
            specs_dict = at if at is not None else cls.export()
            results = []

            pattern = re.compile(term, re.IGNORECASE)

            for spec_name, info in specs_dict.items():
                entry_value = cls.get(spec_name, where_key)
                if isinstance(entry_value, list):
                    entry_value = ' '.join(entry_value)
                elif isinstance(entry_value, dict):
                    entry_value = ' '.join(entry_value.values())
                if pattern.search(entry_value):
                    results.append(spec_name)
            return results
        S = search

        @classmethod
        def check(cls, spec_name, at=None):
            specs_dict = at if at is not None else cls.export()
            return spec_name in specs_dict
        c = check

        @classmethod
        def mk(cls, spec_name, at=None):
            specs_dict = at if at is not None else cls.export()
            def exec_func(*args, **kwargs):
                spec = specs_dict[spec_name]
                for (arg_types, kwarg_types_tuple), funcinfo in spec['spec']['body'].items():
                    kwarg_types = dict(kwarg_types_tuple)
                    if len(args) == len(arg_types) and all(isinstance(arg, typ) for arg, typ in zip(args, arg_types)):
                        if all(isinstance(kwargs.get(key), typ) for key, typ in kwarg_types.items()):
                            return funcinfo['func'](*args, **kwargs)
                raise TypeError("No matching function signature found.")
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
        r = repr

    s = spec

    class type:
        _aliases = {
            'description': ['d', 'desc', 'description'],
            'tags': ['t', 'tag', 'tags'],
            'comments': ['c', 'comment', 'comments'],
            'all': ['a', 'any', 'every']
        }

        @classmethod
        def _resolve_alias(cls, where):
            for key, aliases in cls._aliases.items():
                if where in aliases:
                    return key
            raise ValueError(f"Invalid alias '{where}'.")


        @classmethod
        def export(cls):
            return f._default_types
        E = export

        @classmethod
        def database(cls, *args):
            if len(args) == 1:
                f._default_types = args[0]
            elif len(args) == 0:
                f._default_types = {}
            else:
                raise AttributeError(f"Provided '{len(args)}' arguments. Expecting at most one argument.")
        db = database

        @classmethod
        def init(cls, some_type, description, at=None):
            types_dict = at if at is not None else cls.export()
            if some_type in types_dict:
                raise ValueError(f"Type '{some_type}' is already registered.")

            types_dict[some_type] = {
                'description': description,
                'tags': [],
                'comments': {}
            }
        i = init

        @classmethod
        def update(cls, typename, attribute, at=None):
            attribute = cls._resolve_alias(attribute)
            types_dict = at if at is not None else f._default_types
            if typename not in types_dict:
                raise ValueError(f"Type '{typename}' is not registered.")
            type_info = types_dict[typename]

            if attribute == 'description':
                def _update_desc_(new_description):
                    type_info['description'] = new_description
                return _update_desc_
            if attribute == 'tags':
                def _update_tag_(old_tag, new_tag):
                    if not type_info['tags']:
                        raise ValueError("Cannot update tag as the tags list is empty.")
                    if new_tag in type_info['tags']:
                        raise ValueError(f"Tag '{new_tag}' already exists in type '{typename}'.")
                    if old_tag in type_info['tags']:
                        type_info['tags'][type_info['tags'].index(old_tag)] = new_tag
                    else:
                        raise ValueError(f"Tag '{old_tag}' not found in type '{typename}'.")
                return _update_tag_
            if attribute == 'comments':
                def _update_comment_(comment_id, new_comment_value):
                    if not type_info['comments']:
                        raise ValueError("Cannot update comment as the comments dictionary is empty.")
                    if comment_id in type_info['comments']:
                        type_info['comments'][comment_id] = new_comment_value
                    else:
                        raise ValueError(f"Comment ID '{comment_id}' not found in type '{typename}'.")
                return _update_comment_

            raise ValueError(f"Unknown or unsupported update attribute '{attribute}'.")
        u = update

        @classmethod
        def add(cls, typename, attribute, at=None):
            attribute = cls._resolve_alias(attribute)
            types_dict = at if at is not None else f._default_types
            if typename not in types_dict:
                raise ValueError(f"Type '{typename}' is not registered.")
            type_info = types_dict[typename]

            if attribute == 'tags':
                def _add_tag_(tag):
                    if tag not in type_info['tags']:
                        type_info['tags'].append(tag)
                return _add_tag_
            if attribute == 'comments':
                def _add_comment_(comment_id, comment_text):
                    type_info['comments'][comment_id] = comment_text
                return _add_comment_
            raise ValueError(f"Unknown or unsupported add attribute '{attribute}'.")
        a = add

        @classmethod
        def delete(cls, typename, attribute, at=None):
            attribute = cls._resolve_alias(attribute)
            types_dict = at if at is not None else f._default_types
            if typename not in types_dict:
                raise ValueError(f"Type '{typename}' is not registered.")
            type_info = types_dict[typename]

            if attribute == 'tags':
                def _delete_tag_(tag):
                    if tag in type_info['tags']:
                        type_info['tags'].remove(tag)
                return _delete_tag_

            if attribute == 'comments':
                def _delete_comment_(comment_id):
                    if comment_id in type_info['comments']:
                        del type_info['comments'][comment_id]
                return _delete_comment_

            raise ValueError(f"Unknown or unsupported delete attribute '{attribute}'.")
        d = delete

        @classmethod
        def get(cls, obj, entry, at=None):
            entry_key = cls._resolve_alias(entry)
            types_dict = at if at is not None else cls.export()

            if obj not in types_dict:
                raise ValueError(f"Type '{obj}' not found.")

            type_info = types_dict[obj]
            if entry_key in type_info:
                return type_info[entry_key]
            else:
                raise ValueError(f"Entry '{entry_key}' not found in type '{obj}'.")
        g = get

        @classmethod
        def info(cls, typename, what='all'):
            info_string = ""

            if what == 'all':
                attributes = ['description', 'tags', 'comments']
            else:
                attributes = [cls._resolve_alias(what)]

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
            where_key = cls._resolve_alias(where)
            types_dict = at if at is not None else cls.export()
            pattern = re.compile(term)
            results = []

            for typename, info in types_dict.items():
                entry_value = info.get(where_key, '')
                if isinstance(entry_value, list):
                    entry_value = ' '.join(entry_value)
                if pattern.search(entry_value):
                    results.append(typename)

            return results
        S = search

        @classmethod
        def check(cls, typename, at=None):
            types_dict = at if at is not None else cls.export()
            return typename in types_dict
        c = check
    t = type

