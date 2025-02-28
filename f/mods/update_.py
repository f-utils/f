from f.mods.err_ import UpdateErr

class Update:
    def std(spec_info, new_std):
        if not callable(new_std):
            raise UpdateErr("The new standard must be callable.")
        spec_info['spec']['std'] = {'func': new_std, 'repr': repr(new_std)}

    def body(spec_info, domain, new_func):
        if not callable(new_func):
            raise UpdateErr("The new body function must be callable.")
        spec_info['spec']['body'][domain] = {'func': new_func, 'repr': repr(new_func)}

    def desc(spec_info, new_value):
        if not isinstance(new_value, str):
            raise UpdateErr("The new value must be a string.")
        spec_info['metadata']['description'] = new_value

    def tag(spec_info, old_tag, new_tag):
        tags = spec_info['metadata']['tags']
        if old_tag not in tags:
            raise UpdateErr(f"Old tag '{old_tag}' not found.")
        if new_tag in tags:
            raise UpdateErr(f"New tag '{new_tag}' already exists.")
        tags[tags.index(old_tag)] = new_tag

    def comment(spec_info, comment_id, new_comment_value):
        comments = spec_info['metadata']['comments']
        if comment_id not in comments:
            raise UpdateErr(f"Comment ID '{comment_id}' not found.")
        comments[comment_id] = new_comment_value
