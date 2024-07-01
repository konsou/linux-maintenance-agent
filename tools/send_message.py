import functools

import message_bus
from .base import Tool, ToolProperty


class ToolSendMessage(Tool):
    def __init__(self, message_bus: message_bus.MessageBus):
        super().__init__(
            name="send_message",
            description="Send message to another user in the system.",
            properties={
                "recipient": ToolProperty(
                    type="string",
                    description="Name of the recipient",
                ),
                "content": ToolProperty(
                    type="string",
                    description="Contents of the message.",
                ),
            },
            required=["recipient", "content"],
            callable=functools.partial(send_message, message_bus=message_bus),
        )


def send_message(
    message: message_bus.Message, message_bus: message_bus.MessageBus, *args, **kwargs
) -> str:
    message_bus.publish(message)
    return "Message sent successfully."
