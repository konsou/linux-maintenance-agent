import unittest
from unittest.mock import mock_open, patch, Mock

import gitignorant

from tools.directory_listing import (
    read_gitignore,
    should_ignore,
    list_directory_contents,
)


class TestDirectoryListing(unittest.TestCase):
    def test_read_gitignore_exists(self):
        mock_data = "tmp\n*.log\n"
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=mock_data)),
        ):
            result = read_gitignore(".")
            self.assertIsInstance(result[0], gitignorant.Rule)
            self.assertIsInstance(result[1], gitignorant.Rule)
            self.assertEqual("tmp", result[0].content)
            self.assertEqual("*.log", result[1].content)
            self.assertFalse(result[0].negative)
            self.assertFalse(result[1].negative)

    def test_read_gitignore_not_exists(self):
        with patch("pathlib.Path.exists", return_value=False):
            result = read_gitignore(".")
            self.assertEqual(result, [])

    def test_should_ignore_true(self):
        patterns = [
            gitignorant.Rule(negative=False, content="tmp"),
            gitignorant.Rule(negative=False, content="*.log"),
        ]
        self.assertTrue(should_ignore("tmp/123", patterns))
        self.assertTrue(should_ignore("error.log", patterns))
        self.assertTrue(should_ignore(".git/", patterns))

    def test_should_ignore_false(self):
        patterns = [
            gitignorant.Rule(negative=False, content="tmp"),
            gitignorant.Rule(negative=False, content="*.log"),
        ]
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
                "tools.directory_listing.read_gitignore",
                Mock(return_value=[gitignorant.Rule(negative=False, content="*.log")]),
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
