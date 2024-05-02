import json
import platform
import re

import psutil
from llm_api import LlmApi, types_request

import agent.actions
import settings
import tools
import tools.write_file
from agent.actions.parser import handle_action_from_response
from agent.actions.prompts import BASE_ACTIONS_PROMPT, PLANNER_ACTIONS_PROMPT
from agent.actions.types import ActionResponse, Actions
from agent.confirmer import confirm_child_agent_done
from agent.prompts import CLARIFICATION_PROMPT
from text import print_in_color, Color, truncate_string
from tools import run_command_line, list_directory_contents
from tools.consent import ask_data_send_consent


class Agent:
    def __init__(self, name: str, system_prompt, is_planner: bool = False):
        self.api: LlmApi = settings.LLM_API
        self.chat_history: list[types_request.Message] = []
        self.name = name

        self.is_planner = is_planner
        actions_prompt = PLANNER_ACTIONS_PROMPT if is_planner else BASE_ACTIONS_PROMPT
        work_dir_contents = list_directory_contents(settings.AGENT_WORK_DIR)
        work_dir_contents = "(empty)" if not work_dir_contents else work_dir_contents
        self.add_initial_prompts(
            [
                system_prompt,
                CLARIFICATION_PROMPT,
                actions_prompt,
                f"Your work dir contents:\n{work_dir_contents}",
            ]
        )

        self.start_greeting = "Hello! How can I help you today?"
        self.add_action_to_chat_history(
            action={"action": "COMMUNICATE", "content": self.start_greeting},
            role="assistant",
            name=self.name,
        )

        self.action_handlers = {
            Actions.PLAN.name: self.action_plan,
            Actions.RUN_COMMAND_LINE.name: self.action_command_line,
            Actions.WRITE_FILE.name: self.action_write_file,
            Actions.SPAWN_AND_EXECUTE.name: self.action_spawn_and_execute,
            Actions.COMMUNICATE.name: self.action_communicate,
        }

    def get_response(
        self,
        content: str,
        role: types_request.MessageRole = "user",
        asker_name: str = "User",
        tag: str | None = "AGENT",
    ) -> str:
        self.add_to_chat_history(content=content, role=role, name=asker_name)

        while True:

            response: str = self.api.response_from_messages(self.chat_history, tag=tag)

            response_stripped = self.strip_text_outside_curly_braces(response)
            if response != response_stripped:
                print_in_color("Had to strip extra content outside {}", Color.YELLOW)
                self.add_to_chat_history(
                    "Your response contained text that wasn't valid JSON. I stripped the extra text for now."
                    " In the future, please respond ONLY JSON.",
                    role="user",
                    name="Response parser",
                )

            try:
                response_parsed: ActionResponse = json.loads(
                    response_stripped, strict=False
                )
            except json.decoder.JSONDecodeError as e:
                print_in_color(f"Error parsing response:\n{response}\n{e}", Color.RED)
                self.add_to_chat_history(
                    content="Your response threw a JSONDecodeError - please try again",
                    role="user",
                    name="Response parser",
                )
                continue

            self.add_to_chat_history(content=response, role="assistant", name=self.name)

            action_result: str = handle_action_from_response(
                response=response_parsed, handlers=self.action_handlers
            )
            # Empty string -> not COMMUNICATE, continue looping
            # Non-empty string -> COMMUNICATE result, return
            if action_result:
                return action_result

        return self.handle_string_response(response)

    def action_plan(self, response: ActionResponse) -> str:
        print(f"Main goal: {response.get('main_goal')}")
        print(f"Steps:\n{response.get('steps')}")
        self.delete_old_plans()
        self.add_to_chat_history(
            content="You've updated your plan, good! What's next?",
            role="user",
            name="Response parser",
        )
        return ""

    def action_communicate(self, response: ActionResponse) -> str:
        return response.get("content", "(NO CONTENT)")

    def action_command_line(self, response: ActionResponse) -> str:
        command = response.get("command")
        result = (
            f"COMMAND LINE: Output and exit code for your command:\n"
            f"---\n"
            f"{run_command_line(command)}\n"
            f"---"
        )
        self.add_to_chat_history(
            content=result, role="user", name="Command line runner"
        )
        self.add_to_chat_history(
            content="You've ran a command. You should PLAN next.",
            role="user",
            name="Response parser",
        )
        return ""

    def action_invalid(self, response: ActionResponse) -> str:
        response_action = response.get("action")
        print_in_color(f"INVALID ACTION: {response_action}", Color.RED)
        self.add_to_chat_history(
            content=f"INVALID ACTION: {response_action}",
            role="user",
            name="Response parser",
        )
        return ""

    def action_write_file(self, response: ActionResponse) -> str:
        result = tools.write_file.write_file(response["filename"], response["content"])
        self.add_to_chat_history(content=result, role="user", name="Write file runner")
        self.add_to_chat_history(
            content="You've written to a file. You should PLAN next.",
            role="user",
            name="Response parser",
        )
        return ""

    def action_spawn_and_execute(self, response: ActionResponse) -> str:
        """Spawn an agent to fulfill a task. Exits this function when the task is complete."""
        name = response["name"]
        instructions = response["instructions"]

        child = Agent(name=name, system_prompt=instructions, is_planner=False)
        self.add_to_chat_history(
            f"Spawned a temporary child agent named {name}",
            role="user",
            name="Response parser",
        )
        self.add_to_chat_history(
            f"CHILD AGENT COMMUNICATION SESSION ACTIVE. DURING THIS SESSION, "
            f"ALL [COMMUNICATE] CALLS WILL BE DIRECTED TO THE CHILD AGENT.",
            role="system",
        )
        parent_communication = 'Please execute your task. COMMUNICATE "My task is done." to me when you are finished.'
        while True:
            child_communication = child.get_response(
                parent_communication, asker_name=self.name, tag="CHILD"
            )
            print(f"{name}: {child_communication}")
            if "task is done" in child_communication.lower():

                task_confirmed = confirm_child_agent_done(instructions)
                if not task_confirmed:
                    child.add_to_chat_history(
                        "I checked and you did not actually execute your task. I am disappointed. "
                        "You must be truthful. Use your actions to execute your task. "
                        "Do not lie. Do not hallucinate.\n\n"
                        "Reason:\n"
                        f"{task_confirmed.reason}",
                        name="Result checker",
                        role="user",
                    )
                    continue

                # Task confirmed
                self.add_to_chat_history(child_communication, role="user", name=name)
                break

            parent_communication = self.get_response(
                child_communication, asker_name=name
            )
            print(f"{self.name}: {parent_communication}")
            input("Press ENTER to continue")

        self.add_to_chat_history(
            f"CHILD AGENT COMMUNICATION SESSION ENDED. CHILD AGENT TERMINATED. "
            f"[COMMUNICATE] CALLS ARE ONCE MORE DIRECTED TO THE USER.",
            role="system",
        )
        return ""

    def strip_text_outside_curly_braces(self, text: str) -> str:
        # Matches everything from the first { to the last } including nested ones
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0)
        return ""  # Return an empty string if no outermost braces are found

    def add_action_to_chat_history(
        self,
        action: dict[agent.actions.types.Actions.__members__, str | dict],
        role: types_request.MessageRole,
        name: str | None = None,
    ):
        content = json.dumps(action, indent=2)
        self.add_to_chat_history(content=content, role=role, name=name)

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

    def delete_old_plans(self):
        first = True
        for message in reversed(self.chat_history):
            content = message["content"]
            try:
                content_parsed = json.loads(content, strict=False)
            except json.JSONDecodeError:
                # Not an action - maybe just a string
                continue

            if first and content_parsed.get("action") == Actions.PLAN.name:
                first = False
                continue

            if content_parsed.get("action") == Actions.PLAN.name:
                self.chat_history.remove(message)

    def _add_or_merge_message(self, message: types_request.Message):
        content_truncated = truncate_string(
            message.get("content").replace("\n", " "), 100
        )
        print_in_color(
            f"[{self.name}] {message.get('name', '')} ({message.get('role')}): {content_truncated}",
            Color.LIGHTBLACK_EX,
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
            print_in_color(f"[Merging disabled for now]", Color.LIGHTBLACK_EX)
            self.chat_history.append(message)
            return

            print(
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

    def add_initial_prompts(self, prompts: list[str]):
        for prompt in prompts:
            self.add_to_chat_history(content=prompt, role="system")
