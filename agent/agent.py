import json
import platform
import psutil
from agent import tools
from agent.consent import ask_data_send_consent

from llm_api import LlmApi, types_request, types_tools
import settings
from text import print_in_color, Color


class Agent:
    def __init__(self, system_prompt: str = settings.LLM_SYSTEM_PROMPT):
        self.api: LlmApi = settings.LLM_API
        self.chat_history: list[types_request.Message] = []

        self.start_greeting = "Hello! How can I help you today?"

        self.system_prompt = system_prompt
        self.add_to_chat_history(
            content=system_prompt,
            role="system",
        )

        self.system_info: dict = self.gather_system_info()
        if self.system_info:
            self.add_to_chat_history(
                content=f"Here's basic information on the user's system:\n"
                + json.dumps(self.system_info, indent=2),
                role="system",
            )
        self.add_to_chat_history(content=self.start_greeting, role="assistant")

        self.tools = tools.tools

    def get_response(
        self,
        message: str,
        message_role: types_request.MessageRole = "user",
        allow_tools: bool = True,
    ) -> str:
        self.add_to_chat_history(content=message, role=message_role)

        response: str | types_tools.ToolCall = self.api.response_from_messages(
            self.chat_history, tools=self.tools if allow_tools else None
        )

        # Is a tool call
        # TODO: better way of ensuring the type. Can't use "isinstance" with TypedDict.
        if "function" in response and "parameters" in response:
            return self.handle_tool_call(types_tools.ToolCall(**response))  # type: ignore

        return self.handle_string_response(response)

    def add_to_chat_history(self, content: str, role: types_request.MessageRole):
        new_message = types_request.Message(content=content, role=role)
        self._add_or_merge_message(new_message)

    def _add_or_merge_message(self, message: types_request.Message):
        if len(self.chat_history) == 0:
            self.chat_history.append(message)
            return

        roles_to_merge = ("user", "assistant")
        latest_message = self.chat_history[-1]
        if (
            message["role"] in roles_to_merge
            and message["role"] == latest_message["role"]
        ):
            print(
                f"Duplicate roles \"{message['role']}\" detected, merging messages..."
            )
            latest_message["content"] = (
                f"{latest_message['content']}\n{message['content']}"
            )
            return
        self.chat_history.append(message)

    def handle_tool_call(self, tool_call: types_tools.ToolCall) -> str:
        message_content = json.dumps(tool_call, indent=2)
        self.add_to_chat_history(content=message_content, role="assistant")

        tool_result = f"Output and exit code for this tool call:\n---\n{self.run_tool(tool_call)}\n---"
        self.add_to_chat_history(content=tool_result, role="assistant")

        tool_use_response = self.get_response(
            "Please explain your action and the results",
            message_role="user",
            allow_tools=False,
        )
        return tool_use_response

    def handle_string_response(self, response: str) -> str:
        self.add_to_chat_history(content=response, role="assistant")
        return response

    def run_tool(self, tool_call: types_tools.ToolCall) -> str:
        try:
            tool_function = tools.TOOL_FUNCTIONS[tool_call["function"]]
            return tool_function(**tool_call["parameters"])
        except KeyError:
            message = f"Tool {tool_call['function']} not found"
            print_in_color(message, color=Color.YELLOW)
            return message
        except Exception as e:
            message = f"Error running tool {tool_call['function']}: {e}"
            print_in_color(message, color=Color.RED)
            return message

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
