from functools import wraps
import json
import pprint


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
