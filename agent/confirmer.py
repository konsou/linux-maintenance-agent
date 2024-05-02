import json
from typing import NamedTuple

import llm_api.types_request

from agent.actions.prompts import (
    ACTIONS_HEADER,
    ACTIONS_COMMUNICATE,
    ACTIONS_COMMAND_LINE,
    ACTIONS_FOOTER,
)
from agent.actions.parser import handle_action_from_response
from agent.actions.types import Actions, ActionResponse
from settings import LLM_API
from tools import run_command_line

CONFIRMER_ACTIONS_PROMPT = (
    ACTIONS_HEADER + ACTIONS_COMMUNICATE + ACTIONS_COMMAND_LINE + ACTIONS_FOOTER
)

# TODO: much duplicate - just make another Agent?


class ConfirmResult(NamedTuple):
    result: bool
    reason: str = ""

    def __bool__(self) -> bool:
        return self.result


def confirm_child_agent_done(instructions: str) -> ConfirmResult:
    confirmer_base_prompt = (
        "An AI agent claims to have completed these instructions:\n\n"
        f'"{instructions}"\n\n'
        f"Please check if the agent has actually done this. Use your tools for this.\n\n"
        f"When you are finished checking, COMMUNICATE:\n"
        f'"CHECK FINISHED - RESULT: [YES or NO]\n'
        f'(reason on the next line if the result is NO)"'
    )
    messages: list[llm_api.types_request.Message] = [
        {"role": "system", "content": CONFIRMER_ACTIONS_PROMPT},
        {"role": "user", "content": confirmer_base_prompt},
    ]

    def action_command_line(response: ActionResponse) -> str:
        nonlocal messages
        command = response.get("command")
        result = (
            f"COMMAND LINE: Output and exit code for your command:\n"
            f"---\n"
            f"{run_command_line(command)}\n"
            f"---"
        )
        messages.append(
            {"role": "user", "name": "Command line runner", "content": result}
        )
        return ""

    def action_communicate(response: ActionResponse) -> str:
        content = response.get("content", "")
        if "check finished" in content.lower():
            return content
        return ""

    action_handlers = {
        Actions.RUN_COMMAND_LINE.name: action_command_line,
        Actions.COMMUNICATE.name: action_communicate,
    }

    while True:
        llm_response: str = LLM_API.response_from_messages(messages, tag="CONFIRMER")
        llm_response_parsed = json.loads(llm_response, strict=False)
        messages.append({"role": "assistant", "content": llm_response})
        action_result: str = handle_action_from_response(
            llm_response_parsed, action_handlers
        )
        if action_result:
            action_result_lines = action_result.split("\n")
            if "yes" in action_result_lines.pop(0):
                return ConfirmResult(True)
            if action_result_lines:
                return ConfirmResult(False, "\n".join(action_result_lines))
            messages.append(
                {
                    "role": "user",
                    "content": "You didn't specify a reason on the next line. "
                    "Please respond according to your instructions.",
                }
            )
