import fnmatch
import os
from pathlib import Path
from typing import List


def read_gitignore(directory: str) -> List[str]:
    gitignore_path = Path(directory) / ".gitignore"
    patterns = []
    if gitignore_path.exists():
        with open(gitignore_path, "r") as file:
            for line in file.readlines():
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith("#"):
                    patterns.append(stripped_line)
    return patterns


def should_ignore(path: str, patterns: List[str]) -> bool:
    # .git dir should always be ignored
    patterns.append(".git/")
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(
            os.path.basename(path), pattern
        ):
            return True
    return False


def list_directory_contents(directory: str) -> str:
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
