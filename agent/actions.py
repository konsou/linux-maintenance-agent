from enum import Enum, auto

ACTIONS_PROMPT = """You have these actions available to you: PLAN, RUN_FUNCTION, COMMUNICATE

Your response must contain only one action. Your response must be JSON only.

Action explanations:

# PLAN
## Create or update a plan on how you can accomplish your main goal
## IMPORTANT! You should PLAN after each other action.
Attributes:
  - "main_goal" (string) (required) - a short description of your main goal
  - "steps" (string) (required) - a list of steps needed to reach the goal. NOTE: For each step, you must indicate if it's [DONE], [IN PROGRESS], or [TODO].  
Example response:
{
  "action": "PLAN",
  "main_goal": "Implement a new authentication feature",
  "steps": "- [DONE] Define requirements and scope of the authentication feature\n- [IN PROGRESS] Implement the login endpoint\n- [TODO] Write unit tests for the new endpoint\n- [TODO] Integrate with the frontend login form\n- [TODO] Conduct integration testing\n- [TODO] Deploy the feature to the staging environment for testing\n- [TODO] Review and go live"
}

# RUN_FUNCTION
## Run a function available to you
Available functions are provided to you. If not, this action cannot be used.
Attributes:
  - "function" (string) (required) - name of the function
  - "parameters" (dict) (optional) - parameters to pass to the function
Example response:
{
  "action": "RUN_FUNCTION",
  "function": "example_function",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  }
}

# COMMUNICATE
## Communicate to the user
Attributes:
  - "content" (string) (required) - text of what you want to communicate to the user
Example response:
{
  "action": "COMMUNICATE",
  "content": "Thank you for that clarification. Next, I'll run some commands to help diagnose the problem more."
}

Your response must contain only one action. Your response MUST be JSON only. Don't include anything else.
"""

EXECUTE_ACTION = """
In addition, as you are the planner, you have this action available to you:

# EXECUTE
## Spawn an AI agent to execute a task in your plan
Attributes:
  - "name" (string) (required) - name of the agent
  - "instructions" (string) (required) - instructions for the agent. Should contain all the information needed to execute the task.
Example response:
{
  "action": "EXECUTE",
  "name": "Betty",
  "instructions": "You are a professional software developer. Your task is to write unit tests for the SettingsReader class in settings.py. Save the tests in tests/test_settings.py. Report to me when you're done."
}
"""


class Actions(Enum):
    PLAN = auto()
    RUN_FUNCTION = auto()
    COMMUNICATE = auto()
    EXECUTE = auto()
