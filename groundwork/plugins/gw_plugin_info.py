import inspect

from groundwork.patterns import GwBasePattern, GwCommandsPattern


class GwPluginInfo(GwCommandsPattern):
    """
    Collects information about plugins, which are registered at the current application.

    Collected information are accessible via command line or via a generated document during
    documentation generation (Additional plugin needed)
    """

    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("plugin_list", "List all plugins", self._list_plugins)
        self.signals.connect(receiver="plugin_info_doc_build_receiver",
                             signal="doc_build",
                             function=self._doc_build,
                             description="Does nothing in the moment")

    def _list_plugins(self):
        for key, plugin in self.app.plugins.classes.get().items():
            print("*" * (len(plugin["name"]) + 4))
            print("* %s *" % plugin["name"])
            print("*" * (len(plugin["name"]) + 4))
            print("")
            print("  Package: %s (%s)" % (plugin["distribution"]["key"], plugin["distribution"]["version"]))
            print("  Path: %s" % plugin["path"])

            if plugin["class"] is not None:
                print("\n  Description:")
                print(plugin["class"].__doc__)

                print("\n  MRO:")
                for mro in plugin["class"].__mro__:
                    print("  ", mro.__name__)

            # if "instance" in plugin.keys() and plugin["instance"] is not None:
            plugin_instance = self.app.plugins.get(plugin["name"])
            if plugin_instance is not None:
                print("\n  Functions:")
                for instance_cls in inspect.getmro(plugin_instance.__class__):
                    print("  ", instance_cls.__name__)
                    for func in inspect.getmembers(instance_cls, predicate=inspect.isfunction):
                        if not func[0].startswith("_"):
                            print("    ", func[0])

                print("\n  Accessible Objects:")
                # for instance_cls in inspect.getmro(plugin["instance"].__class__):
                #     print("  ", instance_cls.__name__)
                attributes = inspect.getmembers(plugin_instance, lambda a: not(inspect.isroutine(a)))
                attributes = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
                for attribute in attributes:
                    if not attribute[0].startswith("_"):
                        print("   ", attribute[0])
            print("\n\n")

    def _doc_build(self, plugin, **kwargs):
        self.log.debug("_doc_build of PluginInfo got called by signal from %s" % plugin.name)

