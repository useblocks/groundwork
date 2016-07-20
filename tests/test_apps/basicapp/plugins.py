from groundwork.patterns import GwPluginPattern


class TestPlugin(GwPluginPattern):
    def __init__(self, *args, **kwargs):
        self.name = "MyPlugin"
        super().__init__(*args, **kwargs)