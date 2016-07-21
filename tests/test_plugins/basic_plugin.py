from groundwork.patterns import GwPluginPattern


class BasicPlugin(GwPluginPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)


