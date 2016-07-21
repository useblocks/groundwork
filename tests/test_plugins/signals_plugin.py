from groundwork.patterns import GwSignalsPattern


class SignalPlugin(GwSignalsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.signals.register("test", "test signal")
        self.signals.connect("test receiver", "test", self.action, "receiver for test signal")

    def action(self, plugin, **kwargs):
        return kwargs
