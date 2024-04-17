import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

import llm_api.abc
from agent import Agent, actions
from llm_api import types_request


def message_factory(
    content: str, role: types_request.MessageRole
) -> types_request.Message:
    return types_request.Message(content=content, role=role)


def action_message_factory(
    action_data: dict[actions.Actions.__members__, str | dict]
) -> types_request.Message:
    return message_factory(content=json.dumps(action_data, indent=2), role="assistant")


def count_messages_by_action(
    messages: list[types_request.Message], action: actions.Actions.__members__
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


class TestAgent(TestCase):
    def setUp(self):
        mock_api = MagicMock(spec=llm_api.abc.LlmApi)
        mock_api.response_from_messages = MagicMock(return_value="test")
        with patch("settings.LLM_API", mock_api):
            self.agent = Agent()

    def test_delete_old_plans(self):
        plan1 = action_message_factory(
            {"action": "PLAN", "main_goal": "Test goal 1", "steps": "Test steps1 "}
        )
        plan2 = action_message_factory(
            {"action": "PLAN", "main_goal": "Test goal 2", "steps": "Test steps 2"}
        )
        self.agent.add_to_chat_history(message=plan1)
        self.agent.add_to_chat_history(message=plan2)
        self.agent.delete_old_plans()

        self.assertEqual(
            1,
            count_messages_by_action(self.agent.chat_history, "PLAN"),
            "Should have only one plan after deleting old",
        )
        self.assertEqual(
            plan2, self.agent.chat_history[-1], "Latest plan should match the last one"
        )
