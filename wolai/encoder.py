from enum import Enum
from json import JSONEncoder, dumps, loads


class WolaiEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            if isinstance(obj.value, str):
                return str(obj.value).replace('__', '-')
            else:
                return obj.value

        # fix static field
        if 'type' not in obj.__dict__:
            try:
                obj.__dict__['type'] = getattr(obj, 'type')
            except AttributeError:
                pass

        return obj.__dict__


def to_json(obj: object) -> str:
    return loads(dumps(obj, cls=WolaiEncoder))
