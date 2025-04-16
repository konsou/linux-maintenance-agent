import logging
import os

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

LLM_MODEL = "deepseek-r1:14b"
LLM_HOST = "http://localhost:11434"

AGENT_WORK_DIR: str | None = None
LOG_LEVEL = logging.DEBUG
