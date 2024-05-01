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
            print(f"Sending this data because ALWAYS_SEND_SYSTEM_DATA is True:")
            print(result_string)
            return result

        print(f"The assistant would like to have this information:")
        print(result_string)
        consent = input("Is it ok to send this data to the assistant? (y/N): ").lower()
        if consent != "y":
            print(f"Ok, not sending data")
            return {}
        print(f"Sending data to assistant...")
        return result

    return wrapper


def ask_execution_consent(explain_command: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"The assistant would like to execute this function:")
            args_and_kwargs = args + tuple(
                (f"{k}={json.dumps(v)}" for k, v in kwargs.items())
            )
            func_call_str = f"{func.__name__}({', '.join(args_and_kwargs)})"
            print(func_call_str)
            if explain_command:
                print(f"Explanation: {_explain_command(func_call_str)}")
            consent = input("Execute? (y/N): ").lower()
            if consent != "y":
                print(f"Ok, not executing")
                return "User denied execution"
            print(f"Executing...")
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def _explain_command(command: str, api: llm_api.LlmApi = settings.LLM_API) -> str:
    return api.response_from_prompt(
        f"Please explain this command with one sentence: `{command}`. Include only your explanation.",
        tag="EXPLAIN_COMMAND",
    )
