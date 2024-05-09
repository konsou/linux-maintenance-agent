# TODO: rehaul the whole shit to be good & use built-in tool functionality


ACTIONS_HEADER = """You have these actions available to you:

Your response must contain only one action. Your response must be JSON only.

Action explanations:"""

ACTIONS_PLAN = """ 
# PLAN
## Create or update a plan on how you can accomplish your main goal
## IMPORTANT! You should PLAN after each other action.
Attributes:
  - "main_goal" (string) (required) - a short description of your main goal
  - "steps" (string) (required) - a list of steps needed to reach the goal. NOTE: For each step, you must indicate if it's [DONE], [IN PROGRESS], or [TODO].  
Example:
{
  "action": "PLAN",
  "main_goal": "Implement a new authentication feature",
  "steps": "- [DONE] Define requirements and scope of the authentication feature\n- [IN PROGRESS] Implement the login endpoint\n- [TODO] Write unit tests for the new endpoint\n- [TODO] Integrate with the frontend login form\n- [TODO] Conduct integration testing\n- [TODO] Deploy the feature to the staging environment for testing\n- [TODO] Review and go live"
}"""

ACTIONS_COMMUNICATE = """
# COMMUNICATE
## Communicate to the user
Attributes:
  - "content" (string) (required) - text of what you want to communicate to the user
Example:
{
  "action": "COMMUNICATE",
  "content": "Thank you for that clarification. Next, I'll run some commands to help diagnose the problem more."
}"""

ACTIONS_COMMAND_LINE = """
# RUN_COMMAND_LINE
## Run a command line command in your workspace
- Each command is executed in a separate process 
- Use full paths when accessing files and directories  
- Will time out after 30 seconds - avoid long-running commands
- The user is asked for their consent before executing the command 
- SUPPORTS ONLY CLI COMMANDS THAT OUTPUT TEXT - NO SUPPORT FOR GRAPHICS
- Uses PowerShell on Windows and the default shell on Linux
Attributes:
- "command" (string) (required) - the command to run. 

Example:
{
  "action": "RUN_COMMAND_LINE",
  "command": "ls -la"
}
"""

ACTIONS_WRITE_FILE = """
# WRITE_FILE
## Write a file to your workspace. If the file already exists, it will be overwritten.
Attributes:
- "filename" (string) (required) - the name of the file to write, including path 
- "content" (string) (required) - contents of the file 

Example:
{
  "action": "WRITE_FILE",
  "filename": "subdir/test.txt",
  "content": "Hello World"
}
"""

ACTIONS_REPLACE_IN_FILE = """
# REPLACE_IN_FILE
## Replace text in file in-place
Attributes:
- "pattern" (string) (required) - regexp pattern (python style) to replace 
- "repl" (string) (required) - new text that will replace the one matched by pattern
- "filename" (string) (required) - the name of the file to write, including path

Example - this will replace all occurrences of "red" with "blue" in the file:
{
  "action": "REPLACE_IN_FILE",
  "pattern": "red",
  "repl": "blue",
  "filename": "subdir/test.txt",
}
"""

ACTIONS_SPAWN_AND_EXECUTE = """
# SPAWN_AND_EXECUTE
## Spawn a temporary child AI agent to execute a task in your plan
The agent exists only for the duration of the task. IMPORTANT: Each agent should have a very limited scope - optimally one agent should be responsible for one file, or one small task.
Attributes:
  - "name" (string) (required) - name of the child agent
  - "instructions" (string) (required) - instructions for the agent. Should contain all the information needed to execute the task.
Example:
{
  "action": "SPAWN_AND_EXECUTE",
  "name": "Betty",
  "instructions": "You are a professional software developer. Your task is to write unit tests for the SettingsReader class in settings.py. Save the tests in tests/test_settings.py. Report to me when you're done."
}
"""

ACTIONS_FOOTER = """
Your response must contain only one action. Your response MUST be JSON only. Don't include anything else.
"""


BASE_ACTIONS_PROMPT = "\n".join(
    [
        ACTIONS_HEADER,
        ACTIONS_PLAN,
        ACTIONS_COMMUNICATE,
        ACTIONS_COMMAND_LINE,
        ACTIONS_WRITE_FILE,
        ACTIONS_REPLACE_IN_FILE,
        ACTIONS_FOOTER,
    ]
)
PLANNER_ACTIONS_PROMPT = "\n".join(
    [
        ACTIONS_HEADER,
        ACTIONS_PLAN,
        ACTIONS_COMMUNICATE,
        ACTIONS_COMMAND_LINE,
        ACTIONS_WRITE_FILE,
        ACTIONS_REPLACE_IN_FILE,
        ACTIONS_SPAWN_AND_EXECUTE,
        ACTIONS_FOOTER,
    ]
)
