import json
from collections import namedtuple


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    try:
        obj = json.loads(data, object_hook=_json_object_hook)
        return  obj
    except Exception as err:
        print(f'Exception during json parsing:\n{data}\n{err}')
        raise err
