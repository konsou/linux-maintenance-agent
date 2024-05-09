from typing import Any, Tuple


def tuple_get(tup: Tuple[Any, ...], index: int, default: Any = None) -> Any:
    try:
        return tup[index]
    except IndexError:
        return default
