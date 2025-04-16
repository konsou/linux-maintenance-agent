import logging
from typing import Any, Tuple

import settings_logging


def tuple_get(tup: Tuple[Any, ...], index: int, default: Any = None) -> Any:
    try:
        return tup[index]
    except IndexError:
        return default


def print_and_log(
    message: str, logger: logging.Logger, level: int = logging.INFO
) -> None:
    """Print a message and log it, skipping logger's console handler"""
    logger.root.removeHandler(settings_logging.CONSOLE_HANDLER)
    print(message)
    logger.log(level=level, msg=message)
    logger.root.addHandler(settings_logging.CONSOLE_HANDLER)
