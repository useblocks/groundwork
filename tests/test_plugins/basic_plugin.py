from groundwork.patterns import GwBasePattern


class BasicPlugin(GwBasePattern):
    def __init__(self, app, name=None, *args, **kwargs):
        self.name = name or self.__class__.__name__
        super(BasicPlugin, self).__init__(app, *args, **kwargs)

    def activate(self):
        self.signals.register("test", "test signal")
        self.signals.connect("test receiver", "test", self.action, "receiver for test signal")

    def action(self, plugin, **kwargs):
        return kwargs

    def deactivate(self):
        pass
