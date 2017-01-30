from groundwork.patterns import GwThreadsPattern


class ThreadPlugin(GwThreadsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super(ThreadPlugin, self).__init__(*args, **kwargs)

    def activate(self):
        self.threads.register("test_thread", self.thread_func, description="Test Thread")

    def thread_func(self, plugin, **kwargs):
        print("Thread executed by %s" % plugin.name)
        return "Done"

    def deactivate(self):
        pass
