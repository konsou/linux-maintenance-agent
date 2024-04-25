import platform
import tempfile
import unittest
from unittest import TestCase
from unittest.mock import mock_open, patch, Mock

from agent import tools
from agent.tests.helpers import patch_decorator
from agent.tools import read_gitignore, should_ignore, list_directory_contents


class TestCommandLineCommon(TestCase):
    def setUp(self):
        consent_patcher = patch_decorator(
            module_being_tested=tools,
            decorator_patch_location="agent.consent.ask_execution_consent",
        )
        consent_patcher.patch()
        self.addCleanup(consent_patcher.kill_patches)

    def test_run_command_line(self):
        result = tools.run_command_line("echo 'Hello World!'")
        self.assertEqual("Hello World!\nProcess exited with code 0", result)

    def test_run_command_line_failure(self):
        result = tools.run_command_line("exit 1")
        self.assertEqual("(no output)\nProcess exited with code 1", result)

    def test_run_command_line_invalid_command(self):
        result = tools.run_command_line("invalidcommandasdf6ats6")
        self.assertIn("Process exited with code 1", result)

    def test_run_command_line_long_running(self):
        result = tools.run_command_line("sleep 1", timeout=0.01)
        self.assertIn("Process exited with code 1", result)
        self.assertIn("timed out", result)

    def test_run_command_single_quotes(self):
        command = "echo 'Hello World!'"
        result = tools.run_command_line(command)
        self.assertEqual("Hello World!\nProcess exited with code 0", result)

    def test_run_command_double_quotes(self):
        command = 'echo "Hello World!"'
        result = tools.run_command_line(command)
        self.assertEqual("Hello World!\nProcess exited with code 0", result)

    def test_run_command_empty_output(self):
        result = tools.run_command_line("echo ''")
        self.assertEqual("(no output)\nProcess exited with code 0", result)

    def test_json_with_escaped_quotes(self):
        # TODO: THIS
        """Error parsing response:
{
  "action": "RUN_COMMAND_LINE",
  "command": "echo 'def write_file(file_path, content):\n    try:\n        with open(file_path, \'w\') as f:\n            f.write(content)\n    except Exception as e:\n        print(f\"Error: {e}\")' >> tools/write_file.py"
}
Invalid \escape: line 3 column 97 (char 130)"""


class TestCommandLineWindows(TestCase):
    def setUp(self):
        if platform.system() != "Windows":
            self.skipTest(f"Skipping Windows tests on {platform.system()}")

        consent_patcher = patch_decorator(
            module_being_tested=tools,
            decorator_patch_location="agent.consent.ask_execution_consent",
        )
        consent_patcher.patch()
        self.addCleanup(consent_patcher.kill_patches)

    def test_run_command_multiple(self):
        command = 'Write-Output "Hello line 1"; Write-Output "Hello line 2"'
        result = tools.run_command_line(command)
        self.assertEqual(
            "Hello line 1\nHello line 2\nProcess exited with code 0", result
        )

    def test_run_command_set_work_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = tools.run_command_line("Get-Location", work_dir=temp_dir)
            self.assertIn(temp_dir, result)
            self.assertIn("Process exited with code 0", result)

    def test_default_work_dir_read_from_settings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("settings.AGENT_WORK_DIR", temp_dir):
                result = tools.run_command_line("Get-Location")
                self.assertIn(temp_dir, result)
                self.assertIn("Process exited with code 0", result)


class TestCommandLineLinux(TestCase):
    def setUp(self):
        if platform.system() != "Linux":
            self.skipTest(f"Skipping Linux tests on {platform.system()}")

        consent_patcher = patch_decorator(
            module_being_tested=tools,
            decorator_patch_location="agent.consent.ask_execution_consent",
        )
        consent_patcher.patch()
        self.addCleanup(consent_patcher.kill_patches)

    def test_run_command_set_work_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = tools.run_command_line("pwd", work_dir=temp_dir)
            self.assertIn(temp_dir, result)
            self.assertIn("Process exited with code 0", result)

    def test_default_work_dir_read_from_settings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("settings.AGENT_WORK_DIR", temp_dir):
                result = tools.run_command_line("pwd")
                self.assertIn(temp_dir, result)
                self.assertIn("Process exited with code 0", result)


class TestDirectoryListing(unittest.TestCase):
    def test_read_gitignore_exists(self):
        mock_data = "tmp\n*.log\n"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = read_gitignore(".")
            self.assertEqual(result, ["tmp", "*.log"])

    def test_read_gitignore_not_exists(self):
        with patch("pathlib.Path.exists", return_value=False):
            result = read_gitignore(".")
            self.assertEqual(result, [])

    def test_should_ignore_true(self):
        patterns = ["tmp", "*.log"]
        self.assertTrue(should_ignore("tmp/123", patterns))
        self.assertTrue(should_ignore("error.log", patterns))

    def test_should_ignore_false(self):
        patterns = ["tmp", "*.log"]
        self.assertFalse(should_ignore("src/error.txt", patterns))
        self.assertFalse(should_ignore("README.md", patterns))

    def test_list_directory_contents(self):
        test_structure = {
            "root": ("root", ["src", "tmp"], ["README.md", "todo.txt"]),
            "root/src": ("root/src", [], ["main.py", "test.py"]),
            "root/tmp": ("root/tmp", [], ["temp.log"]),
        }

        with (
            patch("os.walk") as mock_walk,
            patch("agent.tools.read_gitignore", Mock(return_value=["*.log"])),
        ):
            mock_walk.side_effect = lambda x: [
                test_structure[dir_] for dir_ in test_structure
            ]
            result = list_directory_contents("root")
            expected_result = (
                "README.md\nsrc/\nsrc/main.py\nsrc/test.py\ntmp/\ntodo.txt"
            )
            self.assertEqual(expected_result, result)


if __name__ == "__main__":
    unittest.main()
