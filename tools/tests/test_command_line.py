import platform
import tempfile
import unittest
from unittest import TestCase
from unittest.mock import patch

from tools import command_line
from test_helpers import patch_decorator


class TestCommandLineCommon(TestCase):
    def setUp(self):
        consent_patcher = patch_decorator(
            module_being_tested=command_line,
            decorator_patch_location="tools.consent_decorators.ask_execution_consent_explain_command",
        )
        consent_patcher.patch()
        self.addCleanup(consent_patcher.kill_patches)

    def test_run_command_line(self):
        result = command_line.run_command_line("echo 'Hello World!'")
        self.assertEqual("Hello World!\nProcess exited with code 0", result)

    def test_run_command_line_failure(self):
        result = command_line.run_command_line("exit 1")
        self.assertEqual("(no output)\nProcess exited with code 1", result)

    def test_run_command_line_invalid_command(self):
        result = command_line.run_command_line("invalidcommandasdf6ats6")
        self.assertIn("Process exited with code 1", result)

    def test_run_command_line_long_running(self):
        result = command_line.run_command_line("sleep 1", timeout=0.01)
        self.assertIn("Process exited with code 1", result)
        self.assertIn("timed out", result)

    def test_run_command_single_quotes(self):
        command = "echo 'Hello World!'"
        result = command_line.run_command_line(command)
        self.assertEqual("Hello World!\nProcess exited with code 0", result)

    def test_run_command_double_quotes(self):
        command = 'echo "Hello World!"'
        result = command_line.run_command_line(command)
        self.assertEqual("Hello World!\nProcess exited with code 0", result)

    def test_run_command_empty_output(self):
        result = command_line.run_command_line("echo ''")
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
            module_being_tested=command_line,
            decorator_patch_location="tools.consent_decorators.ask_execution_consent_explain_command",
        )
        consent_patcher.patch()
        self.addCleanup(consent_patcher.kill_patches)

    def test_run_command_multiple(self):
        command = 'Write-Output "Hello line 1"; Write-Output "Hello line 2"'
        result = command_line.run_command_line(command)
        self.assertEqual(
            "Hello line 1\nHello line 2\nProcess exited with code 0", result
        )

    def test_run_command_set_work_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = command_line.run_command_line("Get-Location", work_dir=temp_dir)
            self.assertIn(temp_dir, result)
            self.assertIn("Process exited with code 0", result)

    def test_default_work_dir_read_from_settings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("settings.AGENT_WORK_DIR", temp_dir):
                result = command_line.run_command_line("Get-Location")
                self.assertIn(temp_dir, result)
                self.assertIn("Process exited with code 0", result)


class TestCommandLineLinux(TestCase):
    def setUp(self):
        if platform.system() != "Linux":
            self.skipTest(f"Skipping Linux tests on {platform.system()}")

        consent_patcher = patch_decorator(
            module_being_tested=command_line,
            decorator_patch_location="tools.consent_decorators.ask_execution_consent_explain_command",
        )
        consent_patcher.patch()
        self.addCleanup(consent_patcher.kill_patches)

    def test_run_command_set_work_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = command_line.run_command_line("pwd", work_dir=temp_dir)
            self.assertIn(temp_dir, result)
            self.assertIn("Process exited with code 0", result)

    def test_default_work_dir_read_from_settings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("settings.AGENT_WORK_DIR", temp_dir):
                result = command_line.run_command_line("pwd")
                self.assertIn(temp_dir, result)
                self.assertIn("Process exited with code 0", result)


if __name__ == "__main__":
    unittest.main()
