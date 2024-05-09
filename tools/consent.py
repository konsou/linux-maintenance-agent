import logging
import os
from functools import wraps
import json

import llm_api
import settings


def ask_data_send_consent(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result_string = json.dumps(result, indent=2)

        if getattr(settings, "ALWAYS_SEND_SYSTEM_DATA") is True:
            logging.info(f"Sending this data because ALWAYS_SEND_SYSTEM_DATA is True:")
            logging.info(result_string)
            return result

        logging.info(f"The assistant would like to have this information:")
        logging.info(result_string)
        if os.getenv("_PROGRAMMER_AGENT_TESTING_SKIP_CONSENT") == "1":
            logging.warning(f"TESTING MODE - SKIPPING CONSENT QUERY")
            consent = "y"
        else:
            consent = input(
                "Is it ok to send this data to the assistant? (y/N): "
            ).lower()
        if consent != "y":
            logging.info(f"Ok, not sending data")
            return {}
        logging.info(f"Sending data to assistant...")
        return result

    return wrapper


# TODO: fix duplication
def ask_execution_consent(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"The assistant would like to execute this function:")
        args_and_kwargs = args + tuple(
            (f"{k}={json.dumps(v)}" for k, v in kwargs.items())
        )
        func_call_str = f"{func.__name__}({', '.join(args_and_kwargs)})"
        logging.info(func_call_str)
        if os.getenv("_PROGRAMMER_AGENT_TESTING_SKIP_CONSENT") == "1":
            logging.warning(f"TESTING MODE - SKIPPING CONSENT QUERY")
            consent = "y"
        else:
            consent = input("Execute? (y/N): ").lower()
        if consent != "y":
            logging.info(f"Ok, not executing")
            return "User denied execution"
        logging.info(f"Executing...")
        result = func(*args, **kwargs)
        return result

    return wrapper


def ask_execution_consent_explain_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"The assistant would like to execute this function:")
        args_and_kwargs = args + tuple(
            (f"{k}={json.dumps(v)}" for k, v in kwargs.items())
        )
        func_call_str = f"{func.__name__}({', '.join(args_and_kwargs)})"
        logging.info(func_call_str)
        logging.info(f"Explanation: {_explain_command(func_call_str)}")
        if os.getenv("_PROGRAMMER_AGENT_TESTING_SKIP_CONSENT") == "1":
            logging.warning(f"TESTING MODE - SKIPPING CONSENT QUERY")
            consent = "y"
        else:
            consent = input("Execute? (y/N): ").lower()
        if consent != "y":
            logging.info(f"Ok, not executing")
            return "User denied execution"
        logging.info(f"Executing...")
        result = func(*args, **kwargs)
        return result

    return wrapper


def _explain_command(command: str, api: llm_api.LlmApi = settings.LLM_API) -> str:
    return api.response_from_prompt(
        f"Please explain this command with one sentence: `{command}`. Include only your explanation.",
        tag="EXPLAIN_COMMAND",
    )
