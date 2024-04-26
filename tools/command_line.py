import platform
import subprocess

import settings
import text
from tools.consent import ask_execution_consent
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
