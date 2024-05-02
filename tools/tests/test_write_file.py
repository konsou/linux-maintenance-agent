import os
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from test_helpers import patch_decorator
import tools.write_file


class TestWriteFile(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        consent_patcher = patch_decorator(
            module_being_tested=tools.write_file,
            decorator_patch_location="tools.consent.ask_execution_consent",
        )
        consent_patcher.patch()
        self.addCleanup(consent_patcher.kill_patches)

    def test_write_file(self):
        filename = "test-file.txt"
        contents = "Hello World"
        tools.write_file.write_file(filename, contents)
        self.assertTrue(os.path.exists(filename), "File doesn't exist")
        with open(filename, "r") as f:
            file_contents = f.read()
        self.assertEqual(contents, file_contents, "File contents do not match")

    def test_write_file_uses_default_work_dir(self):
        work_dir = "/home/test/workdir"
        test_file_name = "test_file.txt"
        self.fs.create_dir(work_dir)
        with patch("settings.AGENT_WORK_DIR", work_dir):
            tools.write_file.write_file(test_file_name, "Hello World")
        self.assertTrue(self.fs.isfile(os.path.join(work_dir, test_file_name)))

    def test_write_file_uses_argument_work_dir(self):
        work_dir_argument = "/home/test/argument-workdir"
        work_dir_settings = "/home/test/workdir-in-settings"
        test_file_name = "test_file.txt"
        self.fs.create_dir(work_dir_argument)
        self.fs.create_dir(work_dir_settings)
        with patch("settings.AGENT_WORK_DIR", work_dir_settings):
            tools.write_file.write_file(
                test_file_name, "Hello World", work_dir=work_dir_argument
            )
        self.assertTrue(self.fs.isfile(os.path.join(work_dir_argument, test_file_name)))
        self.assertFalse(
            self.fs.isfile(os.path.join(work_dir_settings, test_file_name))
        )
