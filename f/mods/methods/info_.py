class Info:
    @staticmethod
    def name(entity):
        return f"Entity '{entity}':"

    @staticmethod
    def desc(entity):
        return f"Desc: {entity['metadata'].get('description', 'N/A')}"

    @staticmethod
    def tags(entity):
        tags = entity['metadata'].get('tags', [])
        return f"Tags: {', '.join(tags) if tags else 'None'}"

    @staticmethod
    def comments(entity):
        comments = entity['metadata'].get('comments', {})
        comments_str = "Comments:\n" + "".join(f"    {k}: {v}\n" for k, v in comments.items())
        return comments_str if comments else "Comments: None"

    @staticmethod
    def domain(entity):
        domain = entity['spec'].get('domain', []) if 'spec' in entity else []
        domain_str = "\n    ".join(f"{i+1}. {typ.__name__}" for i, typ in enumerate(domain))
        return f"Domain:\n  {domain_str}" if domain_str else f"Domain: ()"

    @staticmethod
    def body(entity):
        body = entity['spec'].get('body', {}) if 'spec' in entity else {}
        body_str = "\n    ".join(
            f"{i+1}. {key[0].__name__} -> {val['repr']}" 
            for i, (key, val) in enumerate(body.items())
        )
        return f"Body:\n    {body_str if body else ''}\n"

    @staticmethod
    def func(entity):
        return f"Function: {entity['op']['repr'] if 'op' in entity else 'None'}\n"
