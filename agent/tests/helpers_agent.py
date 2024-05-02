import json

from llm_api import types_request
from llm_api.types_request import MessageRole

from agent.actions import types
from agent.agent import Agent


def message_factory(
    content: str, role: types_request.MessageRole
) -> types_request.Message:
    return types_request.Message(content=content, role=role)


def action_message_factory(
    action_data: dict[types.Actions.__members__, str | dict]
) -> types_request.Message:
    return message_factory(content=json.dumps(action_data, indent=2), role="assistant")


def count_messages_by_action(
    messages: list[types_request.Message], action: types.Actions.__members__
) -> int:
    count = 0
    for message in messages:
        content = message["content"]
        try:
            content_parsed = json.loads(content, strict=False)
        except json.JSONDecodeError:
            # Not an action - maybe just a string
            continue
        if content_parsed.get("action", "") == action:
            count += 1
    return count


def agent_has_message_containing(
    agent: Agent, string: str, role: MessageRole | None = None
) -> bool:
    for m in agent.chat_history:
        if role and m.get("role") != role:
            continue
        if string in m.get("content", ""):
            return True
    return False
