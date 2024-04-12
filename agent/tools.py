import subprocess
from agent.consent import ask_execution_consent

from text import print_in_color, Color

from llm_api.types_request import Tool

tools = [
    Tool(
        type="function",
        function={
            "name": "runCommandLine",
            "description": "Runs a command line command on the user's system. The user is asked for their consent before executing the command.",
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
def run_command_line(command: str, *args, **kwargs) -> str:
    try:
        # Run the command and capture the output
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        print_in_color(
            f"{result.stdout}\nExit code: {result.returncode}",
            Color.GREEN,
        )
        return f"{result.stdout}\nProcess exited with code {result.returncode}"
    except subprocess.CalledProcessError as e:
        print_in_color(f"{e.stdout}\nExit code: {e.returncode}", Color.RED)
        return f"{e.stdout}\nProcess exited with code {e.returncode}"


TOOL_FUNCTIONS = {"runCommandLine": run_command_line}
