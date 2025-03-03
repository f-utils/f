from f.mods.err_ import UpdateErr
from f.mods.helper_ import repr_

class Update:
    def desc(entity_info, new_value):
        if not isinstance(new_value, str):
            raise UpdateErr("The new value must be a string.")
        entity_info['metadata']['description'] = new_value

    def tag(entity_info, old_tag, new_tag):
        tags = entity_info['metadata']['tags']
        if old_tag not in tags:
            raise UpdateErr(f"Old tag '{old_tag}' not found.")
        if new_tag in tags:
            raise UpdateErr(f"New tag '{new_tag}' already exists.")
        tags[tags.index(old_tag)] = new_tag

    def comment(entity_info, comment_id, new_comment_value):
        comments = entity_info['metadata']['comments']
        if comment_id not in comments:
            raise UpdateErr(f"Comment ID '{comment_id}' not found.")
        comments[comment_id] = new_comment_value

    def std(spec_info, new_std):
        if not callable(new_std):
            raise UpdateErr("The new standard must be callable.")
        spec_info['spec']['std'] = {'func': new_std, 'repr': repr_(new_std)}

    def body(spec_info, domain, new_func):
        if not callable(new_func):
            raise UpdateErr("The new body function must be callable.")
        domain_key = (domain,) if not isinstance(domain, tuple) else domain
        if domain_key not in spec_info['spec']['body']:
            raise UpdateErr(f"Domain '{domain_key}' not found in specification.")
        spec_info['spec']['body'][domain_key] = {
            'func': new_func,
            'repr': repr_(new_func)
        }

    def dbody(dspec_info, arg_types, new_func):
        if not callable(new_func):
            raise UpdateErr("The new dynamic body function must be callable.")

        expanded_arg_types = []
        if isinstance(arg_types, tuple):
            for typ in arg_types:
                expanded_arg_types.append(expand_types_(typ))
            fixed_part = tuple(typ for typ in arg_types if not isinstance(typ, list))
        else:
            expanded_arg_types.append(expand_types_(arg_types))
            fixed_part = ()

        type_combinations = product(*expanded_arg_types)

        for combo in type_combinations:
            combo_key = tuple(combo)
            dynamic_part_sorted = tuple(sorted(combo_key[len(fixed_part):], key=lambda x: x.__name__))
            dynamic_part_key = combo_key[:len(fixed_part)] + dynamic_part_sorted

            if dynamic_part_key in dspec_info['spec']['body']:
                dspec_info['spec']['body'][dynamic_part_key] = {
                    'func': new_func,
                    'repr': repr_(new_func)
                }
                return
            else:
                raise UpdateErr(f"Domain '{dynamic_part_key}' not found for dynamic specification.")

    def func(op_info, new_func):
        if not callable(new_func):
            raise UpdateErr("The new operation function must be callable.")
        op_info['op']['func'] = new_func
        op_info['op']['repr'] = repr_(new_func)

