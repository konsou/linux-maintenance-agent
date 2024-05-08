import os.path

import settings
from text import print_in_color, Color
from .consent import ask_execution_consent


# TODO: add consent query? Problem: patching for tests is a pain in the ass >_>
def write_file(filename: str, content: str, work_dir: str | None = None) -> str:
    work_dir = work_dir or settings.AGENT_WORK_DIR
    if work_dir is None:
        raise ValueError(
            f"No work_dir supplied as an argument or AGENT_WORK_DIR in settings"
        )

    full_path = os.path.join(work_dir, filename)
    print_in_color(f"Writing file {full_path}", Color.LIGHTBLACK_EX)
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        return f"Cannot write file {filename}: {e}"
    return f"File {filename} has been written successfully."
