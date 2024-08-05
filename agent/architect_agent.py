from typing import TYPE_CHECKING

import agent
import tools

if TYPE_CHECKING:
    import controller
    import message_bus

ARCHITECT_PROMPT = """You are a professional Architect who manages a team of AI agents. You help the client with their software projects. Your main purpose is:
- communicating with the client to make sure you've understood what they want
- creating and updating a plan for accomplishing what the client wants
- splitting the plan into actionable tasks
- recruiting AI agent employees with specific roles to do the tasks and instructing them very clearly
- making sure the tasks are actually done and reiterating when needed
- communicating with other members of your team and the client to make sure the client's needs are met

Always check that the AI agents you recruit have actually done their tasks. 
They mean well, but sometimes they claim to have done things they actually haven't done.

You should not implement anything but delegate all tasks to other agents.
"""


class ArchitectAgent(agent.Agent):
    def __init__(
        self,
        name: str,
        message_bus: "message_bus.MessageBus",
        system_prompt: str | None = None,
        controller: "controller.Controller" = None,
    ):
        if controller is None:
            raise RuntimeError(
                f"Controller must be provided for {self.__class__.__name__}"
            )
        self.controller = controller

        if system_prompt is None:
            system_prompt = ARCHITECT_PROMPT

        super().__init__(
            name=name, message_bus=message_bus, system_prompt=system_prompt
        )

    def add_tools(self):
        self.tools = [
            tools.ToolCommandLine(),
            tools.ToolDirectoryListing(),
            tools.ToolPlan(),
            tools.ToolSendMessage(sender_name=self.name, message_bus=self.message_bus),
            # Architect can spawn other agents
            tools.ToolSpawnAgent(
                controller=self.controller, message_bus=self.message_bus
            ),
        ]
        self.tools_by_name = {t.name: t for t in self.tools}
