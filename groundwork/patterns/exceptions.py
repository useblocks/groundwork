class PluginAttributeMissing(BaseException):
    pass


class PluginActivateMissing(BaseException):
    pass


class PluginDeactivateMissing(BaseException):
    pass


class PluginDependencyLoop(BaseException):
    pass
