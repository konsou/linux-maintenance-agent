import logging

from agent.agent import Agent
from agent.human_agent import HumanAgent
from message_bus import MessageBus, Message, MessageType

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self):
        self.message_bus = MessageBus()
        self.agents: list[Agent] = [
            HumanAgent(name="konso", message_bus=self.message_bus),
            Agent(name="Alice", message_bus=self.message_bus),
        ]
        self.message_bus.publish(
            Message(
                message_type=MessageType.CHAT_MESSAGE,
                key="",
                source="Alice",
                target="konso",
                value="How can I help you today?",
            )
        )

    def start(self):
        logger.info("AI Helper Chat Session. Type 'exit' to end the session.")

        while True:
            for agent in self.agents:
                agent.update()
                input(f"---------------- Press ENTER to continue ----------------")
