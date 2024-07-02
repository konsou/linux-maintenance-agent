from abc import ABC, abstractmethod
import message_bus


class AgentABC(ABC):
    def __init__(
        self,
        name: str,
        message_bus: message_bus.MessageBus,
        system_prompt: str | None = None,
    ):
        self.name = name
        self.message_bus = message_bus
        self.system_prompt = system_prompt
        self.tag = "AGENT"

        message_bus.subscribe(self.receive)

    @abstractmethod
    def receive(self, message: message_bus.Message):
        pass

    @abstractmethod
    def update(self):
        pass
