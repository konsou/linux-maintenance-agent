import logging
import os.path

import settings
from .abc import Tool, ToolProperty
from .consent_decorators import ask_execution_consent


class ToolWriteFile(Tool):
    def __init__(self):
        super().__init__(
            name="write_file",
            description="Write text to a file, overwriting if it already exists.",
            properties={
                "filename": ToolProperty(
                    type="string",
                    description="Path to the file to write. NOTE: this will always be relative to your work dir! Absolute paths are not supported for security reasons.",
                ),
                "content": ToolProperty(
                    type="string",
                    description="Contents to write.",
                ),
            },
            required=["filename", "content"],
            callable=write_file,
        )


@ask_execution_consent
# TODO: don't ask consent for files created by agent
def write_file(filename: str, content: str, work_dir: str | None = None) -> str:
    work_dir = work_dir or settings.AGENT_WORK_DIR
    if work_dir is None:
        raise ValueError(
            f"No work_dir supplied as an argument or AGENT_WORK_DIR in settings"
        )

    full_path = os.path.join(work_dir, filename)
    logging.debug(f"Writing file {full_path}")
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            bytes_written = f.tell()
    except OSError as e:
        return f"Cannot write file {filename}: {e}"
    return f"{bytes_written} bytes written to file {filename}."
