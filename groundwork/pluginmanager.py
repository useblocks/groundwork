from pkg_resources import iter_entry_points
import logging
import sys
import inspect

from groundwork.patterns.gw_plugin_pattern import GwPluginPattern
from groundwork.exceptions import PluginNotActivatable, PluginNotInitialisable


class PluginManager:
    """
    PluginManager for searching, initialising, activating and deactivating groundwork plugins.

    groundwork plugins are heavily based on classes and multi-inheritances.

    The implemented class handling is based on solutions/hints/tips of the following online sources:

     * https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
     * https://www.python.org/download/releases/2.3/mro/
     * http://stackoverflow.com/questions/5033903/python-super-method-and-calling-alternatives
     * https://fuhm.org/super-harmful/
    """

    def __init__(self, app, plugins=[], strict=False):
        """
        Initialises the plugin manager and registers plugins, which are in sys.path and have an entry_point called
        'groundwork.plugin'.

        Additional plugins can be registered by adding their class via the plugins argument.

        :param app: groundwork application object
        :param plugins: List of plugin classes to registration
        :param strict: If True, problems during plugin registration/initialisation or activation will throw an exception
        """
        self.log = logging.getLogger(__name__)
        self.log.debug("***************************************")
        self.log.debug("Plugins Detection started")
        self.log.debug("***************************************")
        self.app = app
        self.plugins = {}
        self.strict = strict

        #######################
        # PLUGIN Registration #
        #######################

        # Let's find and register every plugin, which is in sys.path and has defined a entry_point 'groundwork.plugin'
        # in it's setup.py
        entry_points = []
        for entry_point in iter_entry_points(group='groundwork.plugin', name=None):
            entry_points.append(entry_point)

        for entry_point in entry_points:
            try:
                entry_point_object = entry_point.load()
            except Exception as e:
                self.log.warning("Couldn't load entry_point %s. Reason: %s" % (entry_point.name, e))
                if self.app.config.get("PLUGIN_INIT_CHECK", False) or strict:
                    raise Exception from e
                continue

            if not issubclass(entry_point_object, GwPluginPattern):
                self.log.warning("entry_point  %s is not a subclass of groundworkPlugin" % entry_point.name)
                continue
            plugin_name = entry_point_object.__name__

            self.plugins[plugin_name] = {
                "name": plugin_name,
                "entry_point": entry_point.name,
                "path": entry_point.dist.location,
                "class": entry_point.load(),
                "distribution": {
                    "key": entry_point.dist.key,
                    "version": entry_point.dist.version
                },
                "initialised": None,
                "active": None,
            }
            self.log.debug("Found plugin: %s at entry_point %s of package %s (%s)" % (plugin_name, entry_point.name,
                                                                                      entry_point.dist.key,
                                                                                      entry_point.dist.version))

        if len(plugins) > 0:
            self.register(plugins)

    def load(self, plugins=[]):
        if plugins is None or len(plugins) == 0:
            self.log.warn("Get no plugins to load")
            return
        self.initialise(plugins)
        self.activate(plugins)

    def register(self, plugins=[]):
        """
        Registers new plugins.

        The registration only creates a new entry for a plugin inside the plugin dictionary.
        It does not activate or even initialise the plugin.

        A plugin must be a class, which inherits directly or indirectly from GwPluginPattern.

        :param plugins: List of plugins
        :type plugins: lit of classes
        """
        if not isinstance(plugins, list):
            raise AttributeError("plugins must be a list, not %s." % type(plugins))

        plugin_registered = []

        for plugin in plugins:
            if not inspect.isclass(plugin) or not issubclass(plugin, GwPluginPattern):
                self.log.error("Given plugin is not a subclass of groundworkPlugin.")
                if not self.strict:
                    continue
                else:
                    raise AttributeError("Given plugin is not a subclass of groundworkPlugin.")

            if isinstance(plugin, GwPluginPattern):
                self.log.error("Given plugin %s is already initialised. Please provide a class not an instance.")
                if not self.strict:
                    continue
                else:
                    raise Exception("Given plugin %s is already initialised. Please provide a class not an instance.")

            plugin_name = plugin.__name__
            self.plugins[plugin_name] = {
                "name": plugin_name,
                "entry_point": None,
                "path": None,
                "class": plugin,
                "distribution": None,
                "initialised": None,
                "active": None,
            }
            self.log.debug("Plugin %s registered" % plugin_name)
            plugin_registered.append(plugin_name)

        self.log.info("Plugins registered: %s" % ", ".join(plugin_registered))

    def initialise(self, plugins=[]):
        """
        Initialises given plugins, but does not activate them.

        This is needed to import and configure libraries, which are imported by used patterns, like GwFlask.

        After this action, all needed python modules are imported and configured.
        Also the groundwork application object is ready and contains functions and objects, which were added
        by patterns, like app.commands from GwCommandsPattern.

        Given plugins must already be registered.

        :param plugins: List of plugin names
        :type plugins: list of strings
        """
        self.log.debug("***************************************")
        self.log.debug("Plugins Initialisation started")
        self.log.debug("***************************************")

        if not isinstance(plugins, list):
            raise AttributeError("plugins must be a list, not %s" % type(plugins))

        self.log.debug("Plugins to initialise: %s" % ", ".join(plugins))

        plugin_initialised = []

        for plugin_name in plugins:
            if not isinstance(plugin_name, str):
                raise AttributeError("plugin name must be a str, not %s" % type(plugin_name))

            plugin_instance = None

            if plugin_name in self.plugins.keys():
                plugin_class = self.plugins[plugin_name]["class"]

                # for base in plugin_class.__bases__:

                if not issubclass(plugin_class, GwPluginPattern):
                    self.log.warn("Can not load %s. Plugin is not based on groundwork.Plugin." % plugin_name)
                    if self.strict:
                        raise Exception("Can not load %s. Plugin is not based on groundwork.Plugin." % plugin_name)
                else:
                    self.log.debug("Initialising plugin %s" % plugin_name)
                    try:
                        plugin_instance = plugin_class(app=self.app)
                        if not hasattr(plugin_instance, "plugin_base_initialised") or \
                                        plugin_instance.plugin_base_initialised is not True:
                            self.log.error("GwPluginPattern.__init__() was not called during initialisation. "
                                           "Please add 'super(*args, **kwargs).__init__()' to the top of all involved "
                                           "plugin/pattern init routines."
                                           "Activate logging debug-output to see all involved classes.")
                            for mro_class in plugin_class.__mro__:
                                self.log.debug(mro_class)
                            raise Exception("GwPluginPattern.__init()__ was not called during initialisation.")
                        plugin_instance.path = self.plugins[plugin_name]["path"]
                    except Exception as e:
                        self.plugins[plugin_name]["initialised"] = False
                        raise PluginNotInitialisable("Plugin %s could not be initialised" % plugin_name) from e
                    else:
                        self.plugins[plugin_name]["initialised"] = True
                        self.plugins[plugin_name]["instance"] = plugin_instance
                        plugin_initialised.append(plugin_name)
                        self.log.debug("Plugin %s initialised" % plugin_name)
            else:
                self.log.warn("Plugin %s not found" % plugin_name)

        self.log.info("Plugins initialised: %s" % ", ".join(plugin_initialised))

    def activate(self, plugins=[]):
        """
        Activates given plugins.

        This calls mainly plugin.activate() and plugins register needed resources like commands, signals or
        documents.

        Given plugins must already be initialised.

        :param plugins: List of plugin names
        :type plugins: list of strings
        """
        self.log.debug("***************************************")
        self.log.debug("Plugins Activation started")
        self.log.debug("***************************************")

        if not isinstance(plugins, list):
            raise AttributeError("plugins must be a list, not %s" % type(plugins))

        self.log.debug("Plugins to activate: %s" % ", ".join(plugins))

        plugins_activated = []
        for plugin_name in plugins:
            if not isinstance(plugin_name, str):
                raise AttributeError("plugin name must be a str, not %s" % type(plugin_name))

            if plugin_name in self.plugins.keys():
                self.log.debug("Activating plugin %s" % plugin_name)
                if self.plugins[plugin_name]["initialised"] == False:
                    try:
                        self.initialise([plugin_name])
                    except Exception:
                        self.log.error("Couldn't initialise plugin %s" % plugin_name)
                        if self.strict:
                            raise Exception("Couldn't initialise plugin %s" % plugin_name)
                        else:
                            continue
                if self.plugins[plugin_name]["initialised"] == True and \
                                self.plugins[plugin_name]["active"] == False:
                    try:
                        self.plugins[plugin_name]["instance"].activate()
                    except Exception as e:
                        self.plugins[plugin_name]["active"] = False
                        raise PluginNotActivatable("Plugin %s could not be activated" % plugin_name) from e
                    else:
                        self.plugins[plugin_name]["active"] = True
                        self.log.debug("Plugin %s activated" % plugin_name)
                        plugins_activated.append(plugin_name)
                else:
                    self.log.warning("Plugin %s got already activated." % plugin_name)
            else:
                self.log.warn("Plugin %s not found" % plugin_name)
        self.log.info("Plugins activated: %s" % ", ".join(plugins_activated))

    def deactivate(self, plugins=[]):
        pass

    def get(self, name=None):
        """
        Returns the plugin object with the given name.
        Or if a name is not given, the complete plugin dictionary is returned.

        :param name: Name of a plugin
        :return: None, single plugin or dictionary of plugins
        """
        if name is None:
            return self.plugins
        else:
            if name not in self.plugins.keys():
                return None
            else:
                return self.plugins[name]

