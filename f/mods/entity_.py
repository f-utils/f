import inspect
import re
import textwrap
from f.mods.err_    import EntityErr
from f.mods.helper_ import (
    resolve_,
    repr_,
    get_entry_value_
)
from f.mods.methods.update_ import Update
from f.mods.methods.search_ import Search
from f.mods.methods.info_   import Info
from f.mods.methods.get_    import Get

def entity_(at, att=None):
    class Entity:

        @staticmethod
        def export():
            return at
        E = export

        @staticmethod
        def init():
            pass

        class add:
            @staticmethod
            def tag(entity_name, new_tag):
                if entity_name in at:
                    if new_tag not in at[entity_name]['metadata']['tags']:
                        at[entity_name]['metadata']['tags'].append(new_tag)
                else:
                    raise EntityErr(f"Entity '{entity_name}' not found.")
            t = tag

            @staticmethod
            def comment(entity_name, comment_id, comment_text):
                if entity_name in at:
                    at[entity_name]['metadata']['comments'][comment_id] = comment_text
                else:
                    raise EntityErr(f"Entity '{entity_name}' not found.")
            c = comment
        a = add

        class delete:
            @staticmethod
            def tag(entity_name, new_tag):
                if entity_name in at:
                    if new_tag in at[entity_name]['metadata']['tags']:
                        at[entity_name]['metadata']['tags'].remove(new_tag)
                else:
                    raise EntityErr(f"Entity '{entity_name}' not found.")
            t = tag

            @staticmethod
            def comment(entity_name, comment_id):
                if entity_name in at:
                    if comment_id in at[entity_name]['metadata']['comments']:
                        del at[entity_name]['metadata']['comments'][comment_id]
                else:
                    raise EntityErr(f"Entity '{entity_name}' not found.")
            c = comment
        d = delete

        class get:
            @staticmethod
            def name(entity_name):
                entity = at.get(entity_name, {})
                return Get.name(entity)

            @staticmethod
            def desc(entity_name):
                entity = at.get(entity_name, {})
                return Get.desc(entity)

            @staticmethod
            def tags(entity_name):
                entity = at.get(entity_name, {})
                return Get.tags(entity)

            @staticmethod
            def comments(entity_name):
                entity = at.get(entity_name, {})
                return Get.comments(entity)
        g = get

        class update:
            @staticmethod
            def desc(entity_name, new_desc):
                def updater(entity_info):
                    return Update.desc(entity_info, new_desc)
                if entity_name in at:
                    return updater(at[entity_name])
                else:
                    raise EntityErr(f"Entity '{entity_name}' not found in database.")
            d = desc

            @staticmethod
            def tag(entity_name, old_tag, new_tag):
                def updater(entity_info):
                    return Update.tag(entity_info, old_tag, new_tag)
                if entity_name in at:
                    return updater(at[entity_name])
                else:
                    raise EntityErr(f"Entity '{entity_name}' not found in database.")
            t = tag

            @staticmethod
            def comment(entity_name, comment_id, new_text):
                def updater(entity_info):
                    return Update.comment(entity_info, comment_id, new_text)
                if entity_name in at:
                    return updater(at[entity_name])
                else:
                    raise EntityErr(f"Entity '{entity_name}' not found in database.")
            c = comment

        class info:
            @staticmethod
            def name(entity_name):
                for entity in at.keys():
                    if entity == entity_name:
                        return Info.name(entity_name)

            @staticmethod
            def desc(entity_name):
                entity = at.get(entity_name, {})
                return Info.desc(entity)

            @staticmethod
            def tags(entity_name):
                entity = at.get(entity_name, {})
                return Info.tags(entity)

            @staticmethod
            def comments(entity_name):
                entity = at.get(entity_name, {})
                return Info.comments(entity)

            @staticmethod
            def all(entity_name):
                entity = at.get(entity_name, {})
                return "\n".join([
                    Info.name(entity),
                    Info.desc(entity),
                    Info.tags(entity),
                    Info.comments(entity)
                ])
        I = info

        @staticmethod
        def check(*names):
            for name in names:
                if not isinstance(name, str):
                    raise EntityErr(f"'{name}' is not a string.")
                if name not in at:
                    raise EntityErr(f"'{name}' is not an accessible entity.")
            return True
        c = check

        class search:
            @staticmethod
            def name(term):
                return Search.name(term, at)

            @staticmethod
            def desc(term):
                return Search.desc(term, at)

            @staticmethod
            def tag(term):
                return Search.tag(term, at)

            @staticmethod
            def comment(term):
                return Search.comment(term, at)
        s = search
    return Entity
