import logging

from message_bus.message import MessageType
from message_bus import Message as MessageBusMessage
from message_bus import MessageBus
from agent.abc import AgentABC


class HumanAgent(AgentABC):
    def __init__(
        self,
        name: str,
        message_bus: MessageBus,
        system_prompt: str | None = None,
    ):
        super().__init__(
            name=name, message_bus=message_bus, system_prompt=system_prompt
        )
        self.received_messages: list[MessageBusMessage] = []
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{self.name}")

    def receive(self, message: MessageBusMessage):
        if message.target.lower().strip() == self.name.lower().strip():
            self.logger.debug(f"Received message: {message}")
            self.received_messages.append(message)

    def update(self):
        print(f"Showing all received messages for {self.name}")
        for _ in range(len(self.received_messages)):
            message = self.received_messages.pop(0)
            print(f"{message.source}: {message.value}")
            reply = input(
                f"Respond? Empty response skips, any text will be sent as a response: "
            )
            if reply:
                print(f"Sending...")
                self.message_bus.publish(
                    MessageBusMessage(
                        message_type=MessageType.CHAT_MESSAGE,
                        key="",
                        source=self.name,
                        target=message.source,
                        value=reply,
                    )
                )
