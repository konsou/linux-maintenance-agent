import os
from pathlib import Path
from typing import List

import gitignorant

from text import print_in_color, Color


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
        print_in_color(
            f'list_directory_contents called with "{directory}", returning empty string',
            Color.YELLOW,
        )
        return ""

    directory_path = Path(directory)
    ignore_patterns = read_gitignore(directory)
    result = []

    for root, dirs, files in os.walk(directory):
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
