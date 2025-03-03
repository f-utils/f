class Get:
    @staticmethod
    def name(entity):
        return entity.get('name', '')

    @staticmethod
    def desc(entity):
        return entity['metadata'].get('description', '')

    @staticmethod
    def tags(entity):
        return entity['metadata'].get('tags', [])

    @staticmethod
    def comments(entity):
        return entity['metadata'].get('comments', {})

    @staticmethod
    def std(entity):
        return entity['spec']['std']['func'] if 'spec' in entity else None

    @staticmethod
    def domain(entity):
        return entity['spec'].get('domain', []) if 'spec' in entity else []

    @staticmethod
    def body(entity):
        return entity['spec'].get('body', {}) if 'spec' in entity else {}

    @staticmethod
    def func(entity):
        return entity['op']['func'] if 'op' in entity else None
