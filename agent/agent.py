import json
import logging
import platform

import llm_api.types_request
import psutil
from llm_api import LlmApi, types_request

import message_bus
import settings
import tools.base
from agent.prompts import SYSTEM_PROMPT_ADDITION, PLANNER_SYSTEM_PROMPT
from tools import list_directory_contents
from tools.consent_decorators import ask_data_send_consent


class Agent:
    def __init__(
        self, name: str, system_prompt: str | None = None, is_planner: bool = False
    ):
        # TODO: define message bus higher up
        self.message_bus = message_bus.MessageBus()

        self.api: LlmApi = settings.LLM_API
        self.chat_history: list[types_request.Message] = []
        self.name = name
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{self.name}")

        self.is_planner = is_planner
        self.start_greeting = "Hello! How can I help you today?"
        self.system_prompt = system_prompt
        self.add_initial_prompts()

        self.tools: list[tools.Tool] = self._add_tools()

    def get_response(
        self,
        content: str,
        role: types_request.MessageRole = "user",
        asker_name: str = "User",
        tag: str | None = "AGENT",
    ) -> str:
        self.add_to_chat_history(content=content, role=role, name=asker_name)

        while True:
            response: str = self.api.response_from_messages(
                self.chat_history,
                tag=tag,
                tool_choice="required",
                tools=self._tools_as_dicts(),
                response_format="json",
            )

            try:
                response_parsed = json.loads(response, strict=False)
            except json.decoder.JSONDecodeError as e:
                self.logger.error(f"Error parsing response:\n{response}\n{e}")
                self.add_to_chat_history(
                    content="Your response threw a JSONDecodeError - please try again",
                    role="user",
                    name="Response parser",
                )
                continue

            self.add_to_chat_history(content=response, role="assistant", name=self.name)

            self.handle_tools(response_parsed)

        return self.handle_string_response(response)

    def handle_tools(self, parsed_response):
        # TODO
        pass

    # def action_spawn_and_execute(self, response: ActionResponse) -> str:
    #     """Spawn an agent to fulfill a task. Exits this function when the task is complete."""
    #     name = response["name"]
    #     instructions = response["instructions"]
    #
    #     child = Agent(name=name, system_prompt=instructions, is_planner=False)
    #     self.add_to_chat_history(
    #         f"Spawned a temporary child agent named {name}",
    #         role="user",
    #         name="Response parser",
    #     )
    #     self.add_to_chat_history(
    #         f"CHILD AGENT COMMUNICATION SESSION ACTIVE. DURING THIS SESSION, "
    #         f"ALL [COMMUNICATE] CALLS WILL BE DIRECTED TO THE CHILD AGENT.",
    #         role="system",
    #     )
    #     parent_communication = 'Please execute your task. COMMUNICATE "My task is done." to me when you are finished.'
    #     while True:
    #         child_communication = child.get_response(
    #             parent_communication, asker_name=self.name, tag="CHILD"
    #         )
    #         self.logger.info(f"{name}: {child_communication}")
    #         if "task is done" in child_communication.lower():
    #
    #             task_confirmed = confirm_child_agent_done(instructions)
    #             if not task_confirmed:
    #                 child.add_to_chat_history(
    #                     "I checked and you did not actually execute your task. I am disappointed. "
    #                     "You must be truthful. Use your actions to execute your task. "
    #                     "Do not lie. Do not hallucinate.\n\n"
    #                     "Reason:\n"
    #                     f"{task_confirmed.reason}",
    #                     name="Result checker",
    #                     role="user",
    #                 )
    #                 continue
    #
    #             # Task confirmed
    #             self.add_to_chat_history(child_communication, role="user", name=name)
    #             break
    #
    #         parent_communication = self.get_response(
    #             child_communication, asker_name=name
    #         )
    #         self.logger.info(f"{self.name}: {parent_communication}")
    #         input("Press ENTER to continue")
    #
    #     self.add_to_chat_history(
    #         f"CHILD AGENT COMMUNICATION SESSION ENDED. CHILD AGENT TERMINATED. "
    #         f"[COMMUNICATE] CALLS ARE ONCE MORE DIRECTED TO THE USER.",
    #         role="system",
    #     )
    #     return ""

    def add_to_chat_history(
        self,
        content: str | None = None,
        name: str | None = None,
        role: types_request.MessageRole | None = None,
        message: types_request.Message | None = None,
    ):
        if (content is None or role is None) and message is None:
            raise ValueError("Either content and role or message must be provided")

        if message is None:
            message = self._create_message(content=content, role=role, name=name)

        self._add_or_merge_message(message)

    # def delete_old_plans(self):
    #     first = True
    #     for message in reversed(self.chat_history):
    #         content = message["content"]
    #         try:
    #             content_parsed = json.loads(content, strict=False)
    #         except json.JSONDecodeError:
    #             # Not an action - maybe just a string
    #             continue
    #
    #         if first and content_parsed.get("action") == Actions.PLAN.name:
    #             first = False
    #             continue
    #
    #         if content_parsed.get("action") == Actions.PLAN.name:
    #             self.chat_history.remove(message)

    def _add_or_merge_message(self, message: types_request.Message):
        content = message.get("content")
        self.logger.debug(
            f"Added message: {message.get('name', '')} ({message.get('role')}): {content}",
        )

        if len(self.chat_history) == 0:
            self.chat_history.append(message)
            return

        roles_to_merge = ("user",)
        latest_message = self.chat_history[-1]
        if (
            message["role"] in roles_to_merge
            and message["role"] == latest_message["role"]
        ):
            self.logger.debug(f"[Merging messages disabled for now]")
            self.chat_history.append(message)
            return

            self.logger.debug(
                f"Duplicate roles \"{message['role']}\" detected, merging messages..."
            )
            latest_message["content"] = (
                f"{latest_message['content']}\n{message['content']}"
            )
            return
        self.chat_history.append(message)

    def handle_string_response(self, response: str) -> str:
        self.add_to_chat_history(content=response, role="assistant", name=self.name)
        return response

    @ask_data_send_consent
    def gather_system_info(self) -> dict:
        system_info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "ram": str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB",
        }
        return system_info

    def _create_message(
        self, content: str, role: types_request.MessageRole, name: str | None = None
    ) -> types_request.Message:
        message = types_request.Message(content=content, role=role)
        if name is not None:
            message["name"] = name
        return message

    def add_initial_prompts(self):
        if self.system_prompt is None and not self.is_planner:
            self.system_prompt = "You are a helpful assistant."
        if self.system_prompt is None and self.is_planner:
            self.system_prompt = PLANNER_SYSTEM_PROMPT
        self.system_prompt = (
            f"Your name is {self.name}. {self.system_prompt}\n{SYSTEM_PROMPT_ADDITION}"
        )
        self.add_to_chat_history(
            content=self.system_prompt,
            role="system",
        )

        work_dir_contents = list_directory_contents(settings.AGENT_WORK_DIR)
        work_dir_contents = "(empty)" if not work_dir_contents else work_dir_contents
        self.add_to_chat_history(
            content=f"Your work dir contents:\n{work_dir_contents}",
            role="user",
            name="System",
        )
        self.add_to_chat_history(
            content=self.start_greeting,
            role="assistant",
            name=self.name,
        )

    def _add_tools(self) -> list[type(tools.Tool)]:
        return [
            tools.ToolCommandLine(),
            tools.ToolDirectoryListing(),
            tools.ToolPlan(),
            tools.ToolReplaceInFile(),
            tools.ToolSendMessage(message_bus=self.message_bus),
            tools.ToolWriteFile(),
        ]

    def _tools_as_dicts(self) -> list[llm_api.types_request.Tool]:
        return [t.dict for t in self.tools]
