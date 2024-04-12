import json
import os

import requests
from dotenv import load_dotenv

from llm_api.abc import LlmApi, Message
from text import print_in_color, Color

AVAILABLE_MODELS = [
    "anthropic/claude-3-haiku:beta",
]


class OpenRouterAPI(LlmApi):
    def __init__(
        self,
        model: str,
    ):
        super().__init__(model=model)

        load_dotenv()
        self._api_key = os.getenv("OPENROUTER_API_KEY")

    def response_from_messages(self, messages: list[Message]) -> str:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self._api_key}",
            },
            data=json.dumps(
                {
                    "model": self.model,
                    "messages": messages,
                }
            ),
        )
        response.raise_for_status()
        response_json = response.json()
        response_message = response_json["choices"][0]["message"]
        print_in_color(
            f'token usage: prompt {response_json["usage"]["prompt_tokens"]} tokens, '
            f'completion {response_json["usage"]["completion_tokens"]}, total {response_json["usage"]["total_tokens"]}',
            color=Color.YELLOW,
        )
        return response_message["content"]
