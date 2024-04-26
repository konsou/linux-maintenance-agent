import os

from pyfakefs.fake_filesystem_unittest import TestCase

from tools.write_file import write_file


class TestWriteFile(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_write_file(self):
        filename = "test-file.txt"
        contents = "Hello World"
        write_file(filename, contents)
        self.assertTrue(os.path.exists(filename), "File doesn't exist")
        with open(filename, "r") as f:
            file_contents = f.read()
        self.assertEqual(contents, file_contents, "File contents do not match")
