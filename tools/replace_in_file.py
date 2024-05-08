import os
import re

import settings


def replace_in_file(
    pattern, repl, file_path: str, count=0, flags=0, work_dir: str | None = None
):
    work_dir = work_dir or settings.AGENT_WORK_DIR
    if work_dir is None:
        raise ValueError(
            f"No work_dir supplied as an argument or AGENT_WORK_DIR in settings"
        )

    file_path = os.path.join(work_dir, file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        file_contents = f.read()
    new_contents = re.sub(pattern, repl, file_contents, count=count, flags=flags)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_contents)
