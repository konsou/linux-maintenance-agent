import ollama

import settings
from types import Role

CLIENT = ollama.Client(host=settings.LLM_HOST)


class Agent:
    def __init__(self):
        self._client = CLIENT
        self.model = settings.LLM_MODEL
        self.messages: list[ollama.Message] = []

    def respond(self, query: str, query_role: Role) -> str:
        msg = ollama.Message(
            role=query_role,
            content=query,
        )
        self.messages.append(msg)
        response = self._client.chat(
            model=self.model,
            messages=self.messages,
        )
        self.messages.append(response.message)
        return response.message.content
