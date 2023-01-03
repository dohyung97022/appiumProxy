from enum import Enum


def object_to_dict(obj):
    if obj is None:
        return None
    elif isinstance(obj, list):
        data = []
        for element in obj:
            data.append(object_to_dict(element))
    elif isinstance(obj, dict):
        data = {}
        for key, value in obj.items():
            data[key] = object_to_dict(value)
    elif isinstance(obj, str):
        data = obj
    elif isinstance(obj, int):
        data = obj
    elif isinstance(obj, Enum):
        data = obj.value
    else:
        data = {}
        for key, value in obj.__dict__.items():
            data[key] = object_to_dict(value)

    return data
