import fnmatch
import os
import platform
import subprocess
from pathlib import Path
from typing import List

import settings
import text
from agent.consent import ask_execution_consent
from text import print_in_color, Color


@ask_execution_consent
def run_command_line(
    command: str,
    timeout: float = 30,
    work_dir: str | None = None,
    *args,
    **kwargs,
) -> str:
    if work_dir is None:
        work_dir = settings.AGENT_WORK_DIR

    if platform.system() == "Windows":
        # Command to invoke PowerShell on Windows
        # Also escape double quotes
        command = command.replace('"', '\\"')
        if work_dir is not None:
            command = f"Set-Location {work_dir};{command}"
        command = f'powershell -Command "{command}"'
    if platform.system() == "Linux":
        if work_dir is not None:
            command = f"cd {work_dir};{command}"

    print(f'Running command "{command}"...')

    def _format_and_print_output(
        output: str, exit_code: int, color: str = text.Fore.WHITE
    ) -> str:
        output = output.strip() if output.strip() else "(no output)"
        text_ = f"{output}\nProcess exited with code {exit_code}"
        print_in_color(text_, color=color)
        return text_

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )

        return _format_and_print_output(
            output=result.stdout, exit_code=result.returncode, color=Color.GREEN
        )

    except subprocess.CalledProcessError as e:
        return _format_and_print_output(
            output=e.stdout, exit_code=e.returncode, color=Color.RED
        )
    except subprocess.TimeoutExpired as e:
        return _format_and_print_output(output=str(e), exit_code=1, color=Color.RED)


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
