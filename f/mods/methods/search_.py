import re

class Search:
    @staticmethod
    def name(term, at):
        pattern = re.compile(term, re.IGNORECASE)
        results = [entity_name for entity_name in at if pattern.search(entity_name)]
        return results

    @staticmethod
    def desc(term, at):
        pattern = re.compile(term, re.IGNORECASE)
        results = [
            entity_name for entity_name, info in at.items()
            if pattern.search(info['metadata']['description'])
        ]
        return results

    @staticmethod
    def tag(term, at):
        pattern = re.compile(term, re.IGNORECASE)
        results = [
            entity_name for entity_name, info in at.items()
            if any(pattern.search(tag) for tag in info['metadata']['tags'])
        ]
        return results

    @staticmethod
    def comment(term, at):
        pattern = re.compile(term, re.IGNORECASE)
        results = [
            entity_name for entity_name, info in at.items()
            if any(pattern.search(comment) for comment in info['metadata']['comments'].values())
        ]
        return results
