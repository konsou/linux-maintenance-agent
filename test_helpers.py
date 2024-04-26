import importlib
import unittest.mock
from types import ModuleType


class __PatchDecorator:
    """Patching a decorator is a pain in the ass. This class does that.
    All credit to user2859458 https://stackoverflow.com/a/37890916/9857739

    Usage: as a context manager

        with patch_decorator(
            module_being_tested=tools,
            decorator_patch_location="agent.consent.ask_execution_consent",
        ):
            result = tools.run_command_line("echo 'Hello World!'")

    """

    def __init__(self, module_being_tested: ModuleType, decorator_patch_location: str):
        self.module_being_tested = module_being_tested
        self.decorator_patch_location = decorator_patch_location

    def patch(self):
        unittest.mock.patch(self.decorator_patch_location, lambda x: x).start()
        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        importlib.reload(self.module_being_tested)

    def kill_patches(self):
        unittest.mock.patch.stopall()
        importlib.reload(self.module_being_tested)

    def __enter__(self):
        self.patch()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kill_patches()


patch_decorator = __PatchDecorator
