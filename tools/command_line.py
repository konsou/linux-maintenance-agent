import logging
import platform
import subprocess

import colorama

import settings
from tools.consent import ask_execution_consent_explain_command
from tools.tool import Tool, ToolProperty


class ToolCommandLine(Tool):
    def __init__(self):
        super().__init__(
            name="run_command_line",
            description=(
                "Run a command line command in your workspace\n"
                "- Each command is executed in a separate process\n"
                "- Use full paths when accessing files and directories\n"
                "- Will time out after 30 seconds - avoid long-running commands\n"
                "- The user is asked for their consent before executing the command\n"
                "- SUPPORTS ONLY CLI COMMANDS THAT OUTPUT TEXT - NO SUPPORT FOR GRAPHICS\n"
                "- Uses PowerShell on Windows and the default shell on Linux"
            ),
            properties={
                "command": ToolProperty(type="string", description="the command to run")
            },
            required=["command"],
            callable=run_command_line,
        )


@ask_execution_consent_explain_command
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

    logging.info(f'Running command "{command}"...')

    def _format_output(output: str, exit_code: int) -> str:
        output = output.strip() if output.strip() else "(no output)"
        text_ = f"{output}\nProcess exited with code {exit_code}"
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

        formatted_result = _format_output(
            output=result.stdout, exit_code=result.returncode
        )
        logging.info(
            formatted_result,
            extra={"ansi_color": colorama.Fore.GREEN},
        )
        return formatted_result

    except subprocess.CalledProcessError as e:
        formatted_result = _format_output(output=e.stdout, exit_code=e.returncode)
        logging.error(formatted_result)
        return formatted_result
    except subprocess.TimeoutExpired as e:
        formatted_result = _format_output(output=str(e), exit_code=1)
        logging.error(formatted_result)
        return formatted_result
