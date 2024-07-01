# TODO: rehaul the whole shit to be good & use built-in tool functionality


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
