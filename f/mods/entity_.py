import inspect
import re
import textwrap
from f.mods.err_ import EntityErr
from f.mods.helper_ import resolve_, repr_
from f.mods.update_ import Update

class Entity:
    default_alias_map = {
        'description': ['d', 'desc', 'description'],
        'tags': ['t', 'tag', 'tags'],
        'comments': ['c', 'comment', 'comments']
    }

    @staticmethod
    def database(db, *args):
        if len(args) == 1:
            db = args[0]
        elif len(args) == 0:
            db = {}
        else:
            raise EntityErr(f"Provided '{len(args)}' arguments. Expecting at most one argument.")

    @staticmethod
    def add(attribute, at, type_dict):
        attribute = resolve_(attribute, type_dict)
        entity_dict = at

        if entity in entity_dict:
            spec = entity_dict[entity]['metadata']
        else:
            raise EntityErr(f"Entity '{entity}' not found.")

        if attribute == 'tags':
            def _add_tags_(tag):
                if tag not in spec['tags']:
                    spec['tags'].append(tag)
            return _add_tags_

        if attribute == 'comments':
            def _add_comments_(comment_id, comment_text):
                spec['comments'][comment_id] = comment_text
            return _add_comments_

        raise EntityErr(f"Unsupported attribute: '{attribute}'.")

    @staticmethod
    def delete(attribute, at, type_dict):
        attribute = resolve_(attribute, type_dict)
        entity_dict = at
        if entity in entity_dict:
            spec = entity_dict[entity]['metadata']
        else:
            raise EntityErr(f"Entity '{entity}' not found.")

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

        raise EntityErr(f"Unsupported attribute: '{attribute}'.")

    @staticmethod
    def update(entity, attribute, at, custom_updaters=None, additional_alias_map=None):
        if entity not in at:
            raise EntityErr(f"Entity '{entity}' is not registered.")

        alias_map = {**Entity.default_alias_map, **(additional_alias_map or {})}
        resolved_attribute = resolve_(attribute, alias_map)
        spec_info = at[entity]

        common_updaters = {
            'description': lambda desc: Update.desc(spec_info, desc),
            'tags': lambda old_tag, new_tag: Update.tag(spec_info, old_tag, new_tag),
            'comments': lambda comment_id, new_value: Update.comment(spec_info, comment_id, new_value)
        }

        all_updaters = {**common_updaters, **(custom_updaters or {})}

        if resolved_attribute not in all_updaters:
            raise EntityErr(f"Attribute '{resolved_attribute}' is not supported for entity '{entity}'.")

        return all_updaters[resolved_attribute]

    @staticmethod
    def info(entity_name, at, aliases):
        entity_dict = at
        if entity_name not in entity_dict:
            raise EntityErr(entity_name.split('.')[0], f"Entity '{entity_name}' not found.")

        entity_info = entity_dict[entity_name]
        info_string = f"Entity '{entity_name}':\n"

        for attribute, alias_list in aliases.items():
            resolved_attr = Entity.resolve(attribute, aliases)
            entry = Entity.get_entry_value(entity_info, resolved_attr)

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
    def export(at):
        return at

    @staticmethod
    def check(names, at):
        for name in names:
            if not isinstance(name, str):
                raise EntityErr(f"'{name}' is not a string.")
            if name not in at:
                raise EntityErr(f"'{name}' is not an accessible entity.")
        return True

    @staticmethod
    def search(term, where, at, aliases):
        where_key = Entity.resolve(where, aliases)
        results = []
        pattern = re.compile(term, re.IGNORECASE)

        for entity_name, info in at.items():
            entry_value = Entity.get_entry_value(info, where_key)
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
            raise EntityErr("Entry must be a string, type or None.")
        if not isinstance(description, str):
            raise EntityErr("The description must be a string.")
        if std is not None and not callable(std):
            raise EntityErr("The std must be a function or a lambda.")

        entity_dict = at
        if entity_name in entity_dict:
            raise EntityErr(f"Entity '{entity_name}' is already registered.")

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
                    'repr': repr_(std)
                },
                'domain': [],
                'body': {}
            }

    @staticmethod
    def extend(entity_name, arg_types, func, at, att, any_cls=None):
        if not callable(func):
            raise EntityErr("The function must be callable.")
        entity_dict = at
        type_dict = att
        if entity_name not in entity_dict:
            raise EntityErr(f"Entity '{entity_name}' is not registered.")

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
            raise EntityErr("All arg types must be accessible types.")

        current_domain = entity_dict[entity_name]['spec']['domain']
        if domain_tuple not in current_domain:
            current_domain.append(domain_tuple)

        entity_dict[entity_name]['spec']['body'][domain_tuple] = {
            'func': func,
            'repr': repr_(func)
        }
