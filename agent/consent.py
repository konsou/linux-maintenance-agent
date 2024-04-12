from functools import wraps
import json


def ask_data_send_consent(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"The assistant would like to have this information:")
        print(json.dumps(result, indent=2))
        consent = input("Is it ok to send this data to the assistant? (y/N): ").lower()
        if consent != "y":
            print(f"Ok, not sending data")
            return {}
        print(f"Sending data to assistant...")
        return result

    return wrapper


def ask_execution_consent(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"The assistant would like to execute this function:")
        kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        print(f"{func.__name__}({', '.join(args)}, {kwargs_str})")
        consent = input("Execute? (y/N): ").lower()
        if consent != "y":
            print(f"Ok, not executing")
            return "User denied execution"
        print(f"Executing...")
        result = func(*args, **kwargs)

        return result

    return wrapper
