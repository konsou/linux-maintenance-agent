from unittest import TestCase
from unittest.mock import MagicMock

from message_bus.message import Message, MessageType
from message_bus.message_bus import MessageBus


class TestMessageBus(TestCase):
    def test_subscribe(self):
        mb = MessageBus()
        mock_subscriber = MagicMock(__name__="mock_subscriber")
        mb.subscribe(mock_subscriber)
        self.assertIn(mock_subscriber, mb.get_subscribers())

    def test_unsubscribe(self):
        mb = MessageBus()
        mock_subscriber = MagicMock(__name__="mock_subscriber")
        mb.subscribe(mock_subscriber)
        mb.unsubscribe(mock_subscriber)
        self.assertNotIn(mock_subscriber, mb.get_subscribers())

    def test_publish(self):
        mb = MessageBus()
        message = Message(
            message_type=MessageType.TEST,
            key="test_key",
            source="test_source",
            target="test_target",
            value="test_value",
        )
        mock_subscriber = MagicMock(__name__="mock_subscriber")
        mb.subscribe(mock_subscriber)
        mb.publish(message)
        mock_subscriber.assert_called_once_with(message)
