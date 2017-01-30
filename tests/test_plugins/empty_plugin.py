from groundwork.patterns import GwBasePattern


class EmptyPlugin(GwBasePattern):
    def __init__(self, app, name=None, *args, **kwargs):
        self.name = name or self.__class__.__name__
        super(EmptyPlugin, self).__init__(app, *args, **kwargs)

    def activate(self):
        pass

    def deactivate(self):
        pass
