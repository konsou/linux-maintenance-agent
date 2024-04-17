from llm_api import OpenRouterAPI

ALWAYS_SEND_SYSTEM_DATA = True
# LLM_MODEL = "google/gemini-pro"
LLM_MODEL = "anthropic/claude-3-haiku:beta"
# LLM_MODEL = "anthropic/claude-3-sonnet:beta"
# LLM_MODEL = "anthropic/claude-3-opus:beta"
# LLM_MODEL = "cohere/command-r-plus"
# LLM_MODEL = "openai/gpt-4-turbo"
LLM_API = OpenRouterAPI(model=LLM_MODEL)
AGENT_WORK_DIR: str | None = None
