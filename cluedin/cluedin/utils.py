import json


def save(obj, filename, sort_keys=True):
    with open(filename, 'w') as file:
        json.dump(obj, file, ensure_ascii=False, indent=2, sort_keys=sort_keys)


def load(filename):
    with open(filename, 'r') as file:
        return json.load(file)
