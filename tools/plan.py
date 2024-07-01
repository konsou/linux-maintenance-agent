import json

from tools.base import Tool, ToolProperty


class ToolPlan(Tool):
    def __init__(self):
        super().__init__(
            name="update_plan",
            description="Create or update your plan on accomplishing your main goal.\nIMPORTANT! You should update your plan every time you've taken another action.",
            properties={
                "main_goal": ToolProperty(
                    type="string",
                    description="Short description of your main goal",
                ),
                "steps": ToolProperty(
                    type="string",
                    description="The steps needed to reach the goal. NOTE: For each step, you must indicate if it's [DONE], [IN PROGRESS], or [TODO]. List each step on its own line.",
                ),
            },
            required=["main_goal", "content"],
            callable=plan,
        )


def plan(main_goal: str, steps: str, *args, **kwargs) -> str:
    return json.dumps({"main_goal": main_goal, "steps": steps})
