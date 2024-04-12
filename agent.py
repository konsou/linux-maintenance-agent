from llm_api.abc import Message
import settings
from llm_api import LlmApi


class Agent:
    def __init__(self):
        self.api: LlmApi = settings.LLM_API
        self._chat_history: list[Message] = []

    def get_response(self, message: str) -> str:
        self._chat_history.append(Message(content=message, role="user"))
        response = self.api.response_from_messages(self._chat_history)
        self._chat_history.append(Message(content=response, role="assistant"))
        return response
