import os
import re

import settings
from tools.abc import Tool, ToolProperty
from tools.consent_decorators import ask_execution_consent
from tools.errors import NoWorkDirSetError


class ToolReplaceInFile(Tool):
    def __init__(self):
        super().__init__(
            name="replace_in_file",
            description="Replaces all the occurrences of matching text in a file.",
            properties={
                "pattern": ToolProperty(
                    type="string",
                    description="A regexp pattern matching the text to replace. Python-style.",
                ),
                "repl": ToolProperty(
                    type="string",
                    description="The text to replace the match(es) with.",
                ),
                "filename": ToolProperty(
                    type="string",
                    description="Path to the file to do the replacing in. NOTE: this will always be relative to your work dir! Absolute paths are not supported for security reasons.",
                ),
                "count": ToolProperty(
                    type="number",
                    description="The maximum number of pattern occurrences to be replaced. Must be a positive integer if given.",
                ),
            },
            required=["pattern", "repl", "filename"],
            callable=replace_in_file,
        )


@ask_execution_consent
def replace_in_file(
    pattern,
    repl,
    filename: str,
    count=0,
    flags=0,
    work_dir: str | None = None,
    *args,
    **kwargs,
) -> str:
    work_dir = work_dir or settings.AGENT_WORK_DIR
    if work_dir is None:
        raise NoWorkDirSetError(
            f"No work_dir supplied as an argument or AGENT_WORK_DIR in settings"
        )

    filename = os.path.join(work_dir, filename)

    with open(filename, "r", encoding="utf-8") as f:
        file_contents = f.read()
    new_contents = re.sub(pattern, repl, file_contents, count=count, flags=flags)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_contents)
    return "Text replaced"
