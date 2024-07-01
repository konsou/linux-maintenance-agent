import re


def truncate_string(s: str, n: int) -> str:
    if len(s) > n:
        return s[:n] + "..."
    return s


def strip_text_outside_curly_braces(text: str) -> str:
    # Matches everything from the first { to the last } including nested ones
    match = re.search(r"\{.*}", text, re.DOTALL)
    if match:
        return match.group(0)
    return ""  # Return an empty string if no outermost braces are found
