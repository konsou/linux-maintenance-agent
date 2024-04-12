from abc import ABC, abstractmethod
from . import types_request



class LlmApi(ABC):
    def __init__(
        self,
        model: str,
        timeout: int = 5,
    ):
        self.model = model
        self.timeout = timeout

    @abstractmethod
    def response_from_messages(self, messages: list[types_request.Message], tools: list[types_request.Tool] | None = None) -> str:
        pass

    def response_from_prompt(self, prompt: str) -> str:
        return self.response_from_messages([{"role": "user", "content": prompt}])
