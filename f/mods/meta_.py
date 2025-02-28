import inspect
import re
import textwrap
from f.mods.err_ import MetaErr

class Meta:

    @staticmethod
    def database(db, *args):
        if len(args) == 1:
            db = args[0]
        elif len(args) == 0:
            db = {}
        else:
            raise MetaErr(f"Provided '{len(args)}' arguments. Expecting at most one argument.")

    @staticmethod
    def resolve(attribute, aliases):
        for key, alias_list in aliases.items():
            if attribute in alias_list:
                return key
        return attribute

    @staticmethod
    def add(attribute, at, type_dict):
        attribute = meta.resolve(attribute, type_dict)
        entity_dict = at

        if entity in entity_dict:
            spec = entity_dict[entity]['metadata']
        else:
            raise MetaErr(f"Entity '{entity}' not found.")

        if attribute == 'tags':
            def _add_tags_(tag):
                if tag not in spec['tags']:
                    spec['tags'].append(tag)
            return _add_tags_

        if attribute == 'comments':
            def _add_comments_(comment_id, comment_text):
                spec['comments'][comment_id] = comment_text
            return _add_comments_

        raise MetaErr(f"Unsupported attribute: '{attribute}'.")

    @staticmethod
    def delete(attribute, at, type_dict):
        attribute = meta.resolve(attribute, type_dict)
        entity_dict = at
        if entity in entity_dict:
            spec = entity_dict[entity]['metadata']
        else:
            raise MetaErr(f"Entity '{entity}' not found.")

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

        raise MetaErr(f"Unsupported attribute: '{attribute}'.")

    @staticmethod
    def update(attribute, at, type_dict):
        attribute = meta.resolve(attribute, type_dict)
        entity_dict = at
        if entity not in entity_dict:
            raise MetaErr(f"Entity '{entity}' is not registered.")

        spec_info = entity_dict[entity]
        if attribute not in type_dict:
            raise MetaErr(f"Attribute '{attribute}' is not allowed.")

        if attribute == 'description':
            def _update_desc_(new_description):
                if not isinstance(new_description, str):
                    raise MetaErr("The new description must be a string.")
                spec_info['metadata']['description'] = new_description
            return _update_desc_

        if attribute == 'std' and 'spec' in spec_info:
            def _update_std_(new_standard_return):
                if not callable(new_standard_return):
                    raise MetaErr("The new standard return must be a function or a lambda.")
                spec_info['spec']['std'] = {
                    'func': new_standard_return,
                    'repr': meta.repr(new_standard_return)
                }
            return _update_std_

        if attribute == 'body' and 'spec' in spec_info:
            def _update_body_(given_type, new_function):
                if not callable(new_function):
                    raise MetaErr("The new body function must be a function or a lambda.")
                spec_info['spec']['body'][given_type] = {
                    'func': new_function,
                    'repr': meta.repr(new_function)
                }
            return _update_body_

        if attribute == 'tags':
            def _update_tag_(old_tag, new_tag):
                if not isinstance(old_tag, str) or not isinstance(new_tag, str):
                    raise MetaErr("Both old tag and new tag must be strings.")
                if not spec_info['metadata']['tags']:
                    raise MetaErr("Cannot update tag as the tags list is empty.")
                if new_tag in spec_info['metadata']['tags']:
                    raise MetaErr(f"Tag '{new_tag}' already exists in entity '{entity}'.")
                if old_tag in spec_info['metadata']['tags']:
                    spec_info['metadata']['tags'][spec_info['metadata']['tags'].index(old_tag)] = new_tag
                else:
                    raise MetaErr(f"Tag '{old_tag}' not found in entity '{entity}'.")
            return _update_tag_

        if attribute == 'comments':
            def _update_comment_(comment_id, new_comment_value):
                if not isinstance(comment_id, str) or not isinstance(new_comment_value, str):
                    raise MetaErr("Both comment ID and new comment value must be strings.")
                if not spec_info['metadata']['comments']:
                    raise MetaErr("Cannot update comment as the comments dictionary is empty.")
                if comment_id in spec_info['metadata']['comments']:
                    spec_info['metadata']['comments'][comment_id] = new_comment_value
                else:
                    raise MetaErr(f"Comment ID '{comment_id}' not found in entity '{entity}'.")
            return _update_comment_

        raise MetaErr(f"Unsupported attribute '{attribute}' for entity '{entity}'.")

    @staticmethod
    def info(entity_name, at, aliases):
        entity_dict = at
        if entity_name not in entity_dict:
            raise MetaErr(entity_name.split('.')[0], f"Entity '{entity_name}' not found.")

        entity_info = entity_dict[entity_name]
        info_string = f"Entity '{entity_name}':\n"

        for attribute, alias_list in aliases.items():
            resolved_attr = meta.resolve(attribute, aliases)
            entry = meta.get_entry_value(entity_info, resolved_attr)

            if isinstance(entry, dict):
                if resolved_attr == 'body':
                    info_string += f"  {resolved_attr.upper()}:\n"
                    for domain, func_info in entry.items():
                        domain_names = ', '.join(typ.__name__ for typ in domain)
                        info_string += f"    {domain_names} => {func_info['repr']}\n"
                else:
                    for key, value in entry.items():
                        info_string += f"  {key.upper()}:\n"
                        wrapped_value = textwrap.fill(str(value), width=84)
                        info_string += f"    {wrapped_value}\n"
            elif isinstance(entry, list):
                if resolved_attr == 'domain' and all(isinstance(typ, type) for typ in entry):
                    info_string += f"  {resolved_attr.upper()}:\n"
                    for domain in entry:
                        domain_names = ', '.join(typ.__name__ for typ in domain)
                        info_string += f"    {domain_names}\n"
                else:
                    info_string += f"  {resolved_attr.upper()}:\n"
                    for item in entry:
                        info_string += f"    - {item}\n"
            else:
                wrapped_entry = textwrap.fill(str(entry), width=84)
                info_string += f"  {resolved_attr.upper()}:\n    {wrapped_entry}\n"

        return info_string

    @staticmethod
    def repr(func):
        try:
            source = inspect.getsource(func).strip()
        except:
            source = repr(func)

        if "lambda" in source:
            lambda_idx = source.index("lambda")
            return source[lambda_idx:].strip().rstrip(')')
        return source

    @staticmethod
    def export(at):
        return at

    @staticmethod
    def check(names, at):
        for name in names:
            if not isinstance(name, str):
                raise MetaErr(f"'{name}' is not a string.")
            if name not in at:
                raise MetaErr(f"'{name}' is not an accessible entity.")
        return True

    @staticmethod
    def search(term, where, at, aliases):
        where_key = meta.resolve(where, aliases)
        results = []
        pattern = re.compile(term, re.IGNORECASE)

        for entity_name, info in at.items():
            entry_value = meta.get_entry_value(info, where_key)
            if isinstance(entry_value, list):
                entry_value = ' '.join(entry_value)
            elif isinstance(entry_value, dict):
                entry_value = ' '.join(entry_value.values())
            if pattern.search(entry_value):
                results.append(entity_name)
        return results

    @staticmethod
    def get_entry_value(info, key):
        for main_key in ['metadata', 'spec']:
            if main_key in info and key in info[main_key]:
                return info[main_key][key]
        return info.get(key, '')

    @staticmethod
    def init(entity_name, description, std=None, at=None):
        if not isinstance(entity_name, (str, type)) and entity_name is not None:
            raise MetaErr("Entry must be a string, type or None.")
        if not isinstance(description, str):
            raise MetaErr("The description must be a string.")
        if std is not None and not callable(std):
            raise MetaErr("The std must be a function or a lambda.")

        entity_dict = at
        if entity_name in entity_dict:
            raise MetaErr(f"Entity '{entity_name}' is already registered.")

        entity_dict[entity_name] = {
            'metadata': {
                'description': description,
                'tags': [],
                'comments': {}
            }
        }

        if std is not None:
            entity_dict[entity_name]['spec'] = {
                'std': {
                    'func': std,
                    'repr': meta.repr(std)
                },
                'domain': [],
                'body': {}
            }

    @staticmethod
    def extend(entity_name, arg_types, func, at, att, any_cls=None):
        if not callable(func):
            raise MetaErr("The function must be callable.")
        entity_dict = at
        type_dict = att
        if entity_name not in entity_dict:
            raise MetaErr(f"Entity '{entity_name}' is not registered.")

        func_signature = inspect.signature(func)
        is_dspec = any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in func_signature.parameters.values())
        allowed_types = list(type_dict.keys())
        if is_dspec:
            if arg_types is not any_cls:
                flat_allowed_types = []
                for typ_group in arg_types:
                    if isinstance(typ_group, (tuple, list, set)):
                        flat_allowed_types.extend(tuple(typ_group))
                    else:
                        flat_allowed_types.append(typ_group)
                domain_tuple = tuple(flat_allowed_types)
            else:
                domain_tuple = tuple(type_dict.keys())
        else:
            domain_tuple = tuple(arg_types)

        if not all(typ in type_dict for typ in domain_tuple):
            raise MetaErr("All arg types must be accessible types.")

        current_domain = entity_dict[entity_name]['spec']['domain']
        if domain_tuple not in current_domain:
            current_domain.append(domain_tuple)

        entity_dict[entity_name]['spec']['body'][domain_tuple] = {
            'func': func,
            'repr': meta.repr(func)
        }
