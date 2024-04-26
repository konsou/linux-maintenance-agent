import unittest
from unittest.mock import mock_open, patch, Mock

from tools.directory_listing import (
    read_gitignore,
    should_ignore,
    list_directory_contents,
)


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
            patch(
                "tools.directory_listing.read_gitignore", Mock(return_value=["*.log"])
            ),
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
