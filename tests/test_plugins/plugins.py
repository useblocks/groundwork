from groundwork.patterns import GwPluginPattern, GwCommandsPattern
from click import Option


class BasicPlugin(GwPluginPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)


class CommandPlugin(GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("test", "my test command", self._test_command, params=[Option(("--arg", "-a"))])

    def _test_command(self, arg):
        print(arg)
