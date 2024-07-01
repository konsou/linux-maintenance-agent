import os.path

from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import patch, MagicMock

import llm_api.abc

import settings
from agent import agent
from agent.tests.helpers_agent import (
    action_message_factory,
    count_messages_by_action,
    agent_has_message_containing,
)


class TestAgent(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        mock_api = MagicMock(spec=llm_api.abc.LlmApi)
        mock_api.response_from_messages = MagicMock(return_value="test")
        settings.ALWAYS_SEND_SYSTEM_DATA = True
        settings.AGENT_WORK_DIR = "/home/agent/workdir"
        self.fs.create_dir(settings.AGENT_WORK_DIR)
        with patch("settings.LLM_API", mock_api):
            self.agent = agent.Agent(
                name="Test Agent", system_prompt="You are a test agent"
            )

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

    def test_correct_work_dir_used(self):
        parent_dir = "/home/test/parent"
        work_dir = "/home/test/parent/workdir"
        parent_file = "very_secret"
        test_file_1 = "test1.txt"
        test_file_2 = "test2.py"
        self.fs.create_dir(work_dir)
        self.fs.create_file(os.path.join(parent_dir, parent_file))
        self.fs.create_file(os.path.join(work_dir, test_file_1))
        self.fs.create_file(os.path.join(work_dir, test_file_2))

        with patch("settings.AGENT_WORK_DIR", work_dir):
            a = agent.Agent("test name", "test prompt")
            self.assertFalse(agent_has_message_containing(a, parent_file))
            self.assertTrue(agent_has_message_containing(a, test_file_1, role="system"))
            self.assertTrue(agent_has_message_containing(a, test_file_2, role="system"))
