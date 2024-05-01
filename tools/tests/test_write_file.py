import os

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
