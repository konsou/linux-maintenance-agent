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
