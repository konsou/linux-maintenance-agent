import message_bus
from .base import Tool, ToolProperty


class ToolSendMessage(Tool):
    def __init__(self, sender_name: str, message_bus: message_bus.MessageBus):
        self.sender_name = sender_name
        self.message_bus = message_bus

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
            callable=self.send_message,
        )

    def send_message(self, recipient: str, content: str, *args, **kwargs) -> str:
        message = message_bus.Message(
            message_type=message_bus.MessageType.CHAT_MESSAGE,
            key="",
            source=self.sender_name,
            target=recipient,
            value=content,
        )
        self.message_bus.publish(message)
        return "Message sent successfully."
