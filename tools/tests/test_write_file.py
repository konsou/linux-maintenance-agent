import os
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from test_helpers import patch_decorator
import tools.write_file


class TestWriteFile(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_write_file_raises_error_if_work_dir_none(self):
        with patch("settings.AGENT_WORK_DIR", None):
            with self.assertRaises(
                ValueError,
                msg="Must raise an error if settings.AGENT_WORK_DIR is None and no work_dir argument supplied",
            ):
                tools.write_file.write_file("testfile", "contents")
            with self.assertRaises(
                ValueError,
                msg="Must raise an error if settings.AGENT_WORK_DIR is None and work_dir argument is None",
            ):
                tools.write_file.write_file("testfile", "contents", work_dir=None)

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
