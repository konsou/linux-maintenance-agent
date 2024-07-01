from unittest import TestCase
from unittest.mock import MagicMock, call

import message_bus
import tools.send_message


class TestSendMessage(TestCase):
    def test_tool_send_message(self):
        mbus = message_bus.MessageBus()
        message = message_bus.Message(
            message_type=message_bus.MessageType.CHAT_MESSAGE,
            key="test_key",
            source="test_source",
            target="test_target",
            value="test_value",
        )
        send_message_tool = tools.send_message.ToolSendMessage(message_bus=mbus)
        mock_subscriber_handler = MagicMock(__name__="mock_subscriber_handler")
        mbus.subscribe(mock_subscriber_handler)

        send_message_tool(message)

        self.assertEqual(
            mock_subscriber_handler.call_count,
            1,
            msg="Subscriber handler was not called",
        )
        self.assertEqual(mock_subscriber_handler.call_args.args, (message,))
