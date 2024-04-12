import json
import platform
import psutil
from agent.consent import requires_user_consent

from llm_api import LlmApi, Message
import settings


class Agent:
    def __init__(self, system_prompt: str = settings.LLM_SYSTEM_PROMPT):
        self.api: LlmApi = settings.LLM_API
        self.system_message: Message = Message(
            content=system_prompt,
            role="system",
        )
        self._chat_history: list[Message] = [self.system_message]

        self._system_info: dict = self.gather_system_info()
        if self._system_info:
            self._chat_history.append(
                Message(content=f"Here's some information about my system:\n" + 
                        json.dumps(self._system_info, indent=2), role="system")
            )

    def get_response(self, message: str) -> str:
        self._chat_history.append(Message(content=message, role="user"))
        response = self.api.response_from_messages(self._chat_history)
        self._chat_history.append(Message(content=response, role="assistant"))
        return response

    @requires_user_consent
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
