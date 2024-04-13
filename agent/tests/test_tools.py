import platform
from functools import wraps
from importlib import reload
from unittest import TestCase
from unittest.mock import patch

from agent import consent
from agent import tools


class TestCommandLineWindows(TestCase):
    def setUp(self):
        if platform.system() != "Windows":
            self.skipTest(f"Skipping Windows tests on {platform.system()}")

        # How to patch a decorator: https://stackoverflow.com/a/37890916/9857739
        # Do cleanup first so it is ready if an exception is raised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            patch.stopall()  # Stops all patches started with start()
            # Reload our tools module which restores the original decorator
            reload(tools)

        # We want to make sure this is run so we do this in addCleanup instead of tearDown
        self.addCleanup(kill_patches)

        # Now patch the decorator where the decorator is being imported from
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        patch("agent.consent.ask_execution_consent", lambda x: x).start()
        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        reload(tools)  # Reloads the uut.py module which applies our patched decorator

    def test_run_command_line(self):
        result = tools.run_command_line("echo 'Hello World!'")
        self.assertEqual(result, "Hello World!\nProcess exited with code 0")
