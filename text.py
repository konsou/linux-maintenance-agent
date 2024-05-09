def truncate_string(s: str, n: int) -> str:
    if len(s) > n:
        return s[:n] + "..."
    return s
