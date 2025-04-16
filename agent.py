import logging

import ollama

import settings
from custom_types import Role

CLIENT = ollama.Client(host=settings.LLM_HOST)


class Agent:
    def __init__(self):
        self._client = CLIENT
        self.model = settings.LLM_MODEL
        self.messages: list[ollama.Message] = []
        self.greeting = "How can I help you?"
        self.logger = logging.getLogger(self.__class__.__name__)

    def respond(self, query: str, query_role: Role = "user") -> str:
        self.logger.debug(f"{query_role}: {query}")
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
        self.logger.debug(f"{response.message.role}: {response.message.content}")
        return response.message.content
