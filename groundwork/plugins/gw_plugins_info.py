import inspect

from groundwork.patterns import GwDocumentsPattern, GwCommandsPattern


plugins_content = """
Plugins overview
=================

Registered plugins: {{app.plugins.get()|count}}

List of plugins
---------------

 {% for name, plugin in app.plugins.get().items() %}
 * {{plugin.name-}}
 {% endfor %}

{% for name, plugin in app.plugins.get().items() %}
{{plugin.name}}
{{"-" * plugin.name|length}}
Name: {{plugin.name}}
Description: {{plugin.description}}
{% endfor %}
"""

plugin_classes_content = """
Plugin Classes overview
========================

This is an overview about all plugin classes, which are registered.

Found plugin classes: {{app.plugins.classes.get()|count}}

List of plugin classes
----------------------

 {% for name, class in app.plugins.classes.get().items() %}
 * {{class.name-}}
 {% endfor %}

{% for name, class in app.plugins.classes.get().items() %}
{{class.name}}
{{"-" * class.name|length}}
Name: {{class.name}}
Path: {{class.path}}
Distribution: {{class.distribution.key}} - {{class.distribution.version}}
{% endfor %}
"""


class GwPluginsInfo(GwCommandsPattern, GwDocumentsPattern):
    """
    Collects information about plugins, which are registered at the current application.

    Collected information are accessible via command line or via a generated document during
    documentation generation (Additional plugin needed)
    """

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(GwPluginsInfo, self).__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("plugin_list", "List all plugins", self._list_plugins)
        self.documents.register(name="plugins_overview",
                                content=plugins_content,
                                description="Gives an overview about all registered plugins")

        self.documents.register(name="plugins_classes",
                                content=plugin_classes_content,
                                description="Gives an overview about all available plugin classes"
                                            "")

    def deactivate(self):
        pass

    def _list_plugins(self):
        for key, plugin in self.app.plugins.classes.get().items():
            print("*" * (len(plugin.name) + 4))
            print("* %s *" % plugin.name)
            print("*" * (len(plugin.name) + 4))
            print("")
            print("  Package: %s (%s)" % (plugin.distribution["key"], plugin.distribution["version"]))
            print("  Path: %s" % plugin.distribution["path"])

            if plugin.clazz is not None:
                print("\n  Description:")
                print(plugin.clazz.__doc__)

                print("\n  MRO:")
                for mro in plugin.clazz.__mro__:
                    print("  ", mro.__name__)

            # if "instance" in plugin.keys() and plugin["instance"] is not None:
            plugin_instance = self.app.plugins.get(plugin.name)
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
