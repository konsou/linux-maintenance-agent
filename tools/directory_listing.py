import logging
import os
from pathlib import Path
from typing import List

import gitignorant

import settings
from tools.base import Tool, ToolProperty
from tools.errors import NoWorkDirSetError


class ToolDirectoryListing(Tool):
    def __init__(self):
        super().__init__(
            name="list_directory_contents",
            description="Lists the contents of a directory.\n",
            properties={
                "directory": ToolProperty(
                    type="string",
                    description="The directory to list. Defaults to your working directory if not given.",
                )
            },
            required=[],
            callable=list_directory_contents,
        )


def read_gitignore(directory: str) -> List[gitignorant.Rule]:
    gitignore_path = Path(directory) / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, "r", encoding="utf-8") as file:
            return list(gitignorant.parse_gitignore_file(file))
    return []


def should_ignore(path: str, patterns: List[gitignorant.Rule]) -> bool:
    # .git dir should always be ignored
    patterns.append(gitignorant.Rule(negative=False, content=".git/"))
    return gitignorant.check_path_match(rules=patterns, path=path)


def list_directory_contents(directory: str | None = None) -> str:
    if not directory:
        directory = settings.AGENT_WORK_DIR

    if directory == ".":
        directory = settings.AGENT_WORK_DIR

    if not directory:
        raise NoWorkDirSetError(
            "No directory given and no default work directory set in settings"
        )

    ignore_patterns = read_gitignore(directory)
    result = []

    walk_result = os.walk(directory)
    for root, dirs, files in walk_result:
        relative_root = os.path.relpath(root, directory).replace(os.sep, "/")
        # Remove leading './' from the path
        if relative_root == ".":
            relative_root = ""
        else:
            relative_root += "/"

        if should_ignore(relative_root, ignore_patterns):
            dirs[:] = []  # Prevent diving into ignored dirs
            continue

        for name in files:
            file_path = (relative_root + name).replace(os.sep, "/")
            if not should_ignore(file_path, ignore_patterns):
                result.append(file_path)

        for name in dirs:
            dir_path = (relative_root + name + "/").replace(os.sep, "/")
            if not should_ignore(dir_path, ignore_patterns):
                result.append(dir_path)

    return "\n".join(sorted(result))
