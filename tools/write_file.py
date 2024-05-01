from .consent import ask_execution_consent_explain_command, ask_execution_consent


@ask_execution_consent
def write_file(filename: str, content: str) -> str:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        return f"Cannot write file {filename}: {e}"
    return f"File {filename} has been written successfully."
