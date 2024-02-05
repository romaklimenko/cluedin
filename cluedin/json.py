import json
from typing import Any


def dump(file: str, obj: Any) -> None:
    """Serialize obj as a JSON formatted stream to file.

    Args:
        file (str): File path.
        obj (Any): Object to be serialized.
    """
    with open(file, 'w', encoding='utf-8') as file:
        json.dump(obj, file, ensure_ascii=False,
                  indent=2, sort_keys=False)


def load(file: str) -> Any:
    """Deserialize file to a Python object.

    Args:
        file (str): File path.

    Returns:
        Any: Python object.
    """
    with open(file, 'r', encoding='utf-8') as file:
        return json.load(file)
