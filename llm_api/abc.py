import json
from abc import ABC, abstractmethod
from typing import TypeVar, NamedTuple, Type, Callable, Protocol


Message = dict[str, str]


class LlmApi(ABC):
    def __init__(
        self,
        model: str,
        timeout: int = 5,
    ):
        self.model = model
        self.timeout = timeout

    @abstractmethod
    def response_from_messages(self, messages: list[Message]) -> str:
        pass

    def response_from_prompt(self, prompt: str) -> str:
        return self.response_from_messages([{"role": "user", "content": prompt}])
