import os
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

import tools.replace_in_file


class TestReplaceInFile(TestCase):
    def setUp(self):
        os.environ["_PROGRAMMER_AGENT_TESTING_SKIP_CONSENT"] = "1"
        self.setUpPyfakefs()

    def test_replace_in_file(self):
        filename = "/home/test/testfile"
        self.fs.create_file(filename, contents="Roses are red, violets are blue")
        tools.replace_in_file.replace_in_file("red", "blue", filename, work_dir="/test")
        with open(filename, "r", encoding="utf-8") as f:
            file_contents = f.read()
        self.assertEqual("Roses are blue, violets are blue", file_contents)

    def test_replace_in_file_uses_default_work_dir(self):
        work_dir = "/home/test/workdir"
        test_file_name = "test_file.txt"
        test_file_path = os.path.join(work_dir, test_file_name)
        self.fs.create_dir(work_dir)
        self.fs.create_file(test_file_path, contents="Roses are red, violets are blue")
        with patch("settings.AGENT_WORK_DIR", work_dir):
            tools.replace_in_file.replace_in_file("red", "blue", test_file_name)
        with open(test_file_path, "r", encoding="utf-8") as f:
            file_contents = f.read()
        self.assertEqual("Roses are blue, violets are blue", file_contents)

    def test_replace_in_file_raises_error_if_work_dir_none(self):
        with patch("settings.AGENT_WORK_DIR", None):
            with self.assertRaises(
                ValueError,
                msg="Must raise an error if settings.AGENT_WORK_DIR is None and no work_dir argument supplied",
            ):
                tools.replace_in_file.replace_in_file("red", "blue", ".")
            with self.assertRaises(
                ValueError,
                msg="Must raise an error if settings.AGENT_WORK_DIR is None and work_dir argument is None",
            ):
                tools.replace_in_file.replace_in_file("red", "blue", ".", work_dir=None)

    def test_write_file_uses_argument_work_dir(self):
        work_dir_argument = "/home/test/argument-workdir"
        work_dir_settings = "/home/test/workdir-in-settings"
        test_file_name = "test_file.txt"
        test_file_path = os.path.join(work_dir_argument, test_file_name)
        self.fs.create_dir(work_dir_argument)
        self.fs.create_dir(work_dir_settings)
        self.fs.create_file(test_file_path, contents="Roses are red, violets are blue")

        with patch("settings.AGENT_WORK_DIR", work_dir_settings):
            tools.replace_in_file.replace_in_file(
                "red", "blue", test_file_name, work_dir=work_dir_argument
            )
        with open(test_file_path, "r", encoding="utf-8") as f:
            file_contents = f.read()
        self.assertEqual("Roses are blue, violets are blue", file_contents)
