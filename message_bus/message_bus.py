from typing import Callable

from message_bus.message import Message

import logging

logger = logging.getLogger(__name__)


class MessageBus:
    def __init__(self):
        self._subscribers: set[Callable[[Message], None]] = set()

    def publish(self, message: Message):
        for handler in self._subscribers:
            handler(message)

    def subscribe(self, handler: Callable[[Message], None]):
        self._subscribers.add(handler)
        logger.info(f"{handler.__name__} subscribed to message bus")

    def unsubscribe(self, handler: Callable[[Message], None]):
        self._subscribers.remove(handler)
        logger.info(f"{handler.__name__} unsubscribed from message bus")

    def get_subscribers(self) -> list[Callable[[Message], None]]:
        return list(self._subscribers)
