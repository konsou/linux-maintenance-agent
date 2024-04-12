import json
import platform
import psutil
from agent import tools
from agent.consent import ask_data_send_consent

from llm_api import LlmApi, types_request
import settings


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
                    content=f"Here's some information about my system:\n"
                    + json.dumps(self._system_info, indent=2),
                    role="system",
                )
            )

        self.tools = tools.tools

    def get_response(self, message: str) -> str:
        self._chat_history.append(types_request.Message(content=message, role="user"))
        response = self.api.response_from_messages(self._chat_history, tools=self.tools)
        self._chat_history.append(types_request.Message(content=response, role="assistant"))
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
