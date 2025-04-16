import logging

from llm_api import OpenRouterAPI, GroqApi, AnthropicApi, OllamaApi

ALWAYS_SEND_SYSTEM_DATA = True
LLM_MODEL = "deepseek-r1:14b"
# LLM_MODEL = "google/gemini-pro"
# LLM_MODEL = "anthropic/claude-3-haiku:beta"
# LLM_MODEL = "llama3-70b-8192"
# LLM_MODEL = "claude-3-5-sonnet-20240620"
# LLM_MODEL = "anthropic/claude-3-sonnet:beta"
# LLM_MODEL = "anthropic/claude-3-opus:beta"
# LLM_MODEL = "cohere/command-r-plus"
# LLM_MODEL = "openai/gpt-4-turbo"
# LLM_MODEL = "microsoft/wizardlm-2-8x22b"
LLM_API = OllamaApi(model=LLM_MODEL, base_url="http://localhost:8080")
AGENT_WORK_DIR: str | None = None
LOG_LEVEL = logging.DEBUG
