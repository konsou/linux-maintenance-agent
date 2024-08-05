from typing import TYPE_CHECKING

import agent
from .base import Tool, ToolProperty

if TYPE_CHECKING:
    import message_bus
    import controller


class ToolSpawnAgent(Tool):
    def __init__(
        self, controller: "controller.Controller", message_bus: "message_bus.MessageBus"
    ):
        self.controller = controller
        self.message_bus = message_bus

        super().__init__(
            name="spawn_agent",
            description="Spawn a new AI agent. The agent should have a very narrow area of responsibility.",
            properties={
                "name": ToolProperty(
                    type="string",
                    description="Name of the new agent.",
                ),
                "system_prompt": ToolProperty(
                    type="string",
                    description="System prompt for the new agent. It should explicitly explain the agent's role and responsibilities. Example: 'You are a software developer agent, helping develop a WhatsApp-like communications web app. The project is implemented in Python. Your responsibility is making fixes and improvements to the 'src/services/services.py' file. Communicate with other agents when needed.'",
                ),
            },
            required=["name", "system_prompt"],
            callable=self.spawn_agent,
        )

    def spawn_agent(self, name: str, system_prompt: str, *args, **kwargs) -> str:
        a = agent.Agent(
            name=name, system_prompt=system_prompt, message_bus=self.message_bus
        )
        self.controller.add_agent(a)
        return f"Agent {name} spawned successfully."
