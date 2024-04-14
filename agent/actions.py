from enum import Enum, auto

ACTIONS_PROMPT = """You have these actions available to you: PLAN, RUN_FUNCTION, COMMUNICATE

Your response must contain only one action. Your response must be JSON.

Action explanations:

# PLAN
## Create or update a plan on how you can accomplish your main goal
## IMPORTANT! You should PLAN after each other action.
Attributes:
  - "main_goal" (string) (required) - a short description of your main goal
  - "steps" (string) (required) - a short list of steps needed to reach the goal. NOTE: For each step, you must indicate if it's [DONE], [IN PROGRESS], or [TODO].  
Example response:
{
  "action": "PLAN",
  "main_goal": "Free disk space on the user's computer",
  "steps": "- [DONE] Check disk space usage (2 GB free of 240 GB total)\n- [IN PROGRESS] Delete temporary files\n- [TODO] Check if cleaning temporary files freed enough space",
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

Your response must contain only one action. Your response MUST be JSON.
"""


class Actions(Enum):
    PLAN = auto()
    RUN_FUNCTION = auto()
    COMMUNICATE = auto()
