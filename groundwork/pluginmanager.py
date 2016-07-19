from pkg_resources import iter_entry_points, working_set, Environment, get_distribution
import logging
import sys

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
    def __init__(self, app):
        """
        """
        self.log = logging.getLogger(__name__)
        self.log.debug("***************************************")
        self.log.debug("Plugins Detection started")
        self.log.debug("***************************************")
        self.app = app
        self.plugins = {}

        entry_points = []
        for entry_point in iter_entry_points(group='groundwork.plugin', name=None):
            entry_points.append(entry_point)

        for entry_point in entry_points:
            try:
                entry_point_object = entry_point.load()
            except Exception as e:
                self.log.warning("Couldn't load entry_point %s. Reason: %s" % (entry_point.name, e))
                if self.app.config.get("PLUGIN_INIT_CHECK", True):
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

    def load(self, plugins=[]):
        if plugins is None or len(plugins) == 0:
            self.log.warn("Get no plugins to load")
            return
        self.__initialise(plugins)
        self.__activate(plugins)

    def __initialise(self, plugins=[]):
        self.log.debug("***************************************")
        self.log.debug("Plugins Initialisation started")
        self.log.debug("***************************************")
        self.log.debug("Plugins to initialise: %s" % ", ".join(plugins))

        plugin_initialised = []

        for plugin_name in plugins:
            plugin_instance = None

            if plugin_name in self.plugins.keys():
                plugin_class = self.plugins[plugin_name]["class"]

                # for base in plugin_class.__bases__:

                if not issubclass(plugin_class, GwPluginPattern):
                    self.log.warn("Can not load %s. Plugin is not based on groundwork.Plugin." % plugin_name)
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

        self.log.debug("Plugins initialised: %s" % ", ".join(plugin_initialised))

    def __activate(self, plugins=[]):
        self.log.debug("***************************************")
        self.log.debug("Plugins Activation started")
        self.log.debug("***************************************")
        self.log.debug("Plugins to activate: %s" % ", ".join(plugins))

        plugins_activated = []
        for plugin_name in plugins:
            if plugin_name in self.plugins.keys():
                self.log.debug("Activating plugin %s" % plugin_name)
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
                self.log.warn("Plugin %s not found" % plugin_name)
        self.log.debug("Plugins activated: %s" % ", ".join(plugins_activated))

