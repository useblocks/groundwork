from groundwork.patterns import GwSharedObjectsPattern


class SharedObjectPlugin(GwSharedObjectsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super(SharedObjectPlugin, self).__init__(*args, **kwargs)

    def activate(self):
        test_object = {"test": "this"}

        self.shared_objects.register("test_object", "test_object description", test_object)

    def deactivate(self):
        pass
