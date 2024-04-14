import platform
import subprocess

import text

from agent.consent import ask_execution_consent

from text import print_in_color, Color

from llm_api.types_request import Tool

tools = [
    Tool(
        type="function",
        function={
            "name": "runCommandLine",
            "description": (
                "Runs a command line command on the user's system. The user is asked for their consent "
                "before executing the command. RUN ONLY CLI COMMANDS THAT OUTPUT TEXT.\n\n"
                "On Windows this uses PowerShell. On Linux the default shell is used."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to run",
                    },
                },
                "required": ["command"],
            },
        },
    )
]


@ask_execution_consent
def run_command_line(command: str, timeout: float = 30, *args, **kwargs) -> str:
    if platform.system() == "Windows":
        # Command to invoke PowerShell on Windows
        # Also escape double quotes
        command = command.replace('"', '\\"')
        command = f'powershell -Command "{command}"'

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


TOOL_FUNCTIONS = {"runCommandLine": run_command_line}
