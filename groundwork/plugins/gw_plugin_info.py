import inspect

from groundwork.patterns import GwBasePattern, GwCommandsPattern


class GwPluginInfo(GwCommandsPattern):

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
        for key, plugin in self.app.pluginManager.plugins.items():
            print("**** %s ****" % plugin["name"])
            print("  Initialised: %s" % ("True" if plugin["initialised"] else "False"))
            print("  Active: %s" % ("True" if plugin["active"] else "False"))
            print("  Package: %s (%s)" % (plugin["distribution"]["key"], plugin["distribution"]["version"]))
            print("  Path: %s" % plugin["path"])

            if plugin["class"] is not None:
                print("\n  Description:")
                print(plugin["class"].__doc__)

                print("\n  MRO:")
                for mro in plugin["class"].__mro__:
                    print("  ", mro.__name__)

            if "instance" in plugin.keys() and plugin["instance"] is not None:
                print("\n  Functions:")
                for instance_cls in inspect.getmro(plugin["instance"].__class__):
                    print("  ", instance_cls.__name__)
                    for func in inspect.getmembers(instance_cls, predicate=inspect.isfunction):
                        print("    ", func[0])

                print("\n  Accessible Objects:")
                # for instance_cls in inspect.getmro(plugin["instance"].__class__):
                #     print("  ", instance_cls.__name__)
                attributes = inspect.getmembers(plugin["instance"], lambda a: not(inspect.isroutine(a)))
                attributes = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
                for attribute in attributes:
                    print("   ", attribute[0])
            print("**************************\n\n")

    def _doc_build(self, plugin, **kwargs):
        self.log.debug("_doc_build of PluginInfo got called by signal from %s" % plugin.name)

