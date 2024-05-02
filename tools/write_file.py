import os.path

import settings
from text import print_in_color, Color
from .consent import ask_execution_consent


@ask_execution_consent
def write_file(filename: str, content: str, work_dir: str | None = None) -> str:
    if work_dir is None:
        work_dir = settings.AGENT_WORK_DIR

    full_path = os.path.join(work_dir, filename)
    print_in_color(f"Writing file {full_path}", Color.LIGHTBLACK_EX)
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        return f"Cannot write file {filename}: {e}"
    return f"File {filename} has been written successfully."
