import logging

import agent
import message_bus

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self):
        self.message_bus = message_bus.MessageBus()
        self.agents: list["agent.AgentABC"] = []
        self.add_agent(agent.HumanAgent(name="konso", message_bus=self.message_bus))
        self.add_agent(
            agent.ArchitectAgent(
                name="Alice", controller=self, message_bus=self.message_bus
            )
        )

        self.message_bus.publish(
            message_bus.Message(
                message_type=message_bus.MessageType.CHAT_MESSAGE,
                key="",
                source="Alice",
                target="konso",
                value="How can I help you today?",
            )
        )

    def add_agent(self, agent: "agent.AgentABC"):
        self.agents.append(agent)
        logger.info(f"Agent added: {agent.name}")

    def start(self):
        logger.info("AI Helper Chat Session. Type 'exit' to end the session.")

        while True:
            for a in self.agents:
                a.update()
                input(f"---------------- Press ENTER to continue ----------------")
