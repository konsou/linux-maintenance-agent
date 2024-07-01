import os
import re

import settings
from tools.consent_decorators import ask_execution_consent


@ask_execution_consent
def replace_in_file(
    pattern, repl, filename: str, count=0, flags=0, work_dir: str | None = None
):
    work_dir = work_dir or settings.AGENT_WORK_DIR
    if work_dir is None:
        raise ValueError(
            f"No work_dir supplied as an argument or AGENT_WORK_DIR in settings"
        )

    filename = os.path.join(work_dir, filename)

    with open(filename, "r", encoding="utf-8") as f:
        file_contents = f.read()
    new_contents = re.sub(pattern, repl, file_contents, count=count, flags=flags)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_contents)
    return "Text replaced"
