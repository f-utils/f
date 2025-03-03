from f.mods.err_ import InitErr
from f.mods.helper_ import repr_

class Init:
    @staticmethod
    def desc(entity, description):
        if not isinstance(description, str):
            raise InitErr("The description must be a string.")
        entity['metadata']['description'] = description

    @staticmethod
    def std(entity, std):
        if std is not None and not callable(std):
            raise InitErr(f"The '{std}' must be a function or a lambda.")
        entity['spec'] = {
            'std': {
                'func': std,
                'repr': repr_(std)
            },
            'domain': [],
            'body': {}
        }

    @staticmethod
    def func(entity, func):
        if not callable(func):
            raise InitErr(f"The given '{func}' must be callable.")
        entity['op'] = {
            'func': func,
            'repr': repr_(func)
        }
