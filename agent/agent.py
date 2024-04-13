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
        self.system_message: types_request.Message = types_request.Message(
            content=system_prompt,
            role="system",
        )
        self._chat_history: list[types_request.Message] = [self.system_message]

        self._system_info: dict = self.gather_system_info()
        if self._system_info:
            self._chat_history.append(
                types_request.Message(
                    content=f"Here's basic information on the user's system:\n"
                    + json.dumps(self._system_info, indent=2),
                    role="system",
                )
            )

        self.tools = tools.tools

    def get_response(
        self,
        message: str,
        message_role: types_request.MessageRole = "user",
        allow_tools: bool = True,
    ) -> str:
        self._chat_history.append(
            types_request.Message(content=message, role=message_role)
        )
        response: str | types_tools.ToolCall = self.api.response_from_messages(
            self._chat_history, tools=self.tools if allow_tools else None
        )

        # Is a tool call
        # TODO: better way of ensuring the type. Can't use "isinstance" with TypedDict.
        if "function" in response and "parameters" in response:
            return self.handle_tool_call(types_tools.ToolCall(**response))  # type: ignore

        return self.handle_string_response(response)

    def handle_tool_call(self, tool_call: types_tools.ToolCall) -> str:
        message_content = json.dumps(tool_call, indent=2)
        self._chat_history.append(
            types_request.Message(content=message_content, role="assistant")
        )
        tool_result = f"Tool use result:\n{self.run_tool(tool_call)}"
        tool_use_response = self.get_response(tool_result, message_role="system")
        return tool_use_response

    def handle_string_response(self, response: str) -> str:
        self._chat_history.append(
            types_request.Message(content=response, role="assistant")
        )
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
