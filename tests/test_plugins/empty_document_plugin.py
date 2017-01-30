from groundwork.patterns import GwDocumentsPattern


class EmptyDocumentPlugin(GwDocumentsPattern):
    def __init__(self, app, name=None, *args, **kwargs):
        self.name = name or self.__class__.__name__
        super(EmptyDocumentPlugin, self).__init__(app, *args, **kwargs)

    def activate(self):
        pass

    def deactivate(self):
        pass
