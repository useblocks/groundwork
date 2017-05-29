"""
The pluginmanager module cares about the management of plugin status and their changes between status.

There are two manager classes for managing plugin related objects.

 * PluginManager: Cares about initialised Plugins, which can be activated and deactivated.
 * PluginClassManager: Cares about plugin classes, which are used to create plugins.

A plugin class can be reused for several plugins. The only thing to care about is the naming of a plugin.
This plugin name must be unique inside a groundwork app and can be set during plugin initialisation/activation.
"""
from __future__ import absolute_import
from future.utils import raise_from
from pkg_resources import iter_entry_points
import logging
import inspect
import sys

from groundwork.patterns import GwBasePattern
from groundwork.exceptions import PluginNotActivatableException, PluginNotInitialisableException, \
    PluginRegistrationException, PluginNotDeactivatableException


class PluginManager:
    """
    PluginManager for searching, initialising, activating and deactivating groundwork plugins.
    """

    def __init__(self, app):
        """
        Initialises the plugin manager.

        Additional plugins can be registered by adding their class via the plugins argument.

        :param app: groundwork application object
        :param strict: If True, problems during plugin registration/initialisation or activation will throw an exception
        """
        self._log = logging.getLogger(__name__)
        self._app = app
        self._plugins = {}

        #: Instance of :class:`~groundwork.pluginmanager.PluginClassManager`.
        #: Handles the registration of plugin classes, which can be used to create new plugins during runtime.
        self.classes = PluginClassManager(self._app)

    def initialise_by_names(self, plugins=None):
        """
        Initialises given plugins, but does not activate them.

        This is needed to import and configure libraries, which are imported by used patterns, like GwFlask.

        After this action, all needed python modules are imported and configured.
        Also the groundwork application object is ready and contains functions and objects, which were added
        by patterns, like app.commands from GwCommandsPattern.

        The class of a given plugin must already be registered in the :class:`.PluginClassManager`.

        :param plugins: List of plugin names
        :type plugins: list of strings
        """

        if plugins is None:
            plugins = []

        self._log.debug("Plugins Initialisation started")
        if not isinstance(plugins, list):
            raise AttributeError("plugins must be a list, not %s" % type(plugins))

        self._log.debug("Plugins to initialise: %s" % ", ".join(plugins))
        plugin_initialised = []
        for plugin_name in plugins:
            if not isinstance(plugin_name, str):
                raise AttributeError("plugin name must be a str, not %s" % type(plugin_name))

            plugin_class = self.classes.get(plugin_name)
            self.initialise(plugin_class.clazz, plugin_name)
            plugin_initialised.append(plugin_name)

        self._log.info("Plugins initialised: %s" % ", ".join(plugin_initialised))

    def initialise(self, clazz, name=None):
        if clazz is not None and issubclass(clazz, GwBasePattern):
            if name is None:
                name = clazz.__name__
            try:
                # Plugin Initialisation
                plugin_instance = clazz(app=self._app, name=name)
                # Let's be sure the correct name was set. Even if the init_routine of
                # the plugin does not support the name parameter.
                if plugin_instance.name != name:
                    plugin_instance.name = name
            except Exception as e:
                self._log.warning("Plugin class %s could not be initialised. Reason %s" % (clazz.__name__, e))
                error = "Plugin class %s could not be initialised: %s" % (clazz.__name__, e)
                if sys.version_info[0] < 3:
                    error += "Reason: %s" % e
                raise_from(PluginNotInitialisableException(error), e)

            # Let's be sure, that GwBasePattern got called
            if not hasattr(plugin_instance, "_plugin_base_initialised") \
                    or plugin_instance._plugin_base_initialised is not True:
                self._log.error("GwBasePattern.__init__() was not called during initialisation. "
                                "Please add 'super(*args, **kwargs).__init__()' to the top of all involved "
                                "plugin/pattern init routines."
                                "Activate logging debug-output to see all involved classes.")
                for mro_class in clazz.__mro__:
                    self._log.debug(mro_class)
                raise Exception("GwBasePattern.__init()__ was not called during initialisation.")
            self._register_initialisation(plugin_instance)
            self._log.debug("Plugin %s initialised" % name)
            return plugin_instance

        if clazz is None:
            self._log.warn("Plugin class %s not found" % clazz.__name__)
            return None

        if not issubclass(clazz, GwBasePattern):
            self._log.warn("Can not load %s. Plugin is not based on groundwork.Plugin." % clazz.__name__)
            if self._app.strict:
                raise Exception("Can not load %s. Plugin is not based on groundwork.Plugin." % clazz.__name__)
        return None

    def _register_initialisation(self, plugin_instance):
        """
        Internal functions to perform registration actions after plugin load was successful.
        """
        self._plugins[plugin_instance.name] = plugin_instance

    def activate(self, plugins=[]):
        """
        Activates given plugins.

        This calls mainly plugin.activate() and plugins register needed resources like commands, signals or
        documents.

        If given plugins have not been initialised, this is also done via :func:`_load`.

        :param plugins: List of plugin names
        :type plugins: list of strings
        """
        self._log.debug("Plugins Activation started")

        if not isinstance(plugins, list):
            raise AttributeError("plugins must be a list, not %s" % type(plugins))

        self._log.debug("Plugins to activate: %s" % ", ".join(plugins))

        plugins_activated = []
        for plugin_name in plugins:
            if not isinstance(plugin_name, str):
                raise AttributeError("plugin name must be a str, not %s" % type(plugin_name))

            if plugin_name not in self._plugins.keys() and plugin_name in self.classes._classes.keys():
                self._log.debug("Initialisation needed before activation.")
                try:
                    self.initialise_by_names([plugin_name])
                except Exception as e:
                    self._log.error("Couldn't initialise plugin %s. Reason %s" % (plugin_name, e))
                    if self._app.strict:
                        error = "Couldn't initialise plugin %s" % plugin_name
                        if sys.version_info[0] < 3:
                            error += "Reason: %s" % e
                        raise_from(Exception(error), e)
                    else:
                        continue
            if plugin_name in self._plugins.keys():
                self._log.debug("Activating plugin %s" % plugin_name)
                if not self._plugins[plugin_name].active:
                    try:
                        self._plugins[plugin_name].activate()
                    except Exception as e:
                        raise_from(
                            PluginNotActivatableException("Plugin %s could not be activated: %s" % (plugin_name,
                                                                                                    e)), e)
                    else:
                        self._log.debug("Plugin %s activated" % plugin_name)
                        plugins_activated.append(plugin_name)
                else:
                    self._log.warning("Plugin %s got already activated." % plugin_name)
                    if self._app.strict:
                        raise PluginNotInitialisableException()

        self._log.info("Plugins activated: %s" % ", ".join(plugins_activated))

    def deactivate(self, plugins=[]):
        """
        Deactivates given plugins.

        A given plugin must be activated, otherwise it is ignored and no action takes place (no signals are fired,
        no deactivate functions are called.)

        A deactivated plugin is still loaded and initialised and can be reactivated by calling :func:`activate` again.
        It is also still registered in the :class:`.PluginManager` and can be requested via :func:`get`.

        :param plugins: List of plugin names
        :type plugins: list of strings
        """
        self._log.debug("Plugins Deactivation started")

        if not isinstance(plugins, list):
            raise AttributeError("plugins must be a list, not %s" % type(plugins))

        self._log.debug("Plugins to deactivate: %s" % ", ".join(plugins))

        plugins_deactivated = []
        for plugin_name in plugins:
            if not isinstance(plugin_name, str):
                raise AttributeError("plugin name must be a str, not %s" % type(plugin_name))

            if plugin_name not in self._plugins.keys():
                self._log.info("Unknown activated plugin %s" % plugin_name)
                continue
            else:
                self._log.debug("Deactivating plugin %s" % plugin_name)
                if not self._plugins[plugin_name].active:
                    self._log.warning("Plugin %s seems to be already deactivated" % plugin_name)
                else:
                    try:
                        self._plugins[plugin_name].deactivate()
                    except Exception as e:
                        raise_from(
                            PluginNotDeactivatableException("Plugin %s could not be deactivated" % plugin_name), e)
                    else:
                        self._log.debug("Plugin %s deactivated" % plugin_name)
                        plugins_deactivated.append(plugin_name)

        self._log.info("Plugins deactivated: %s" % ", ".join(plugins_deactivated))

    def get(self, name=None):
        """
        Returns the plugin object with the given name.
        Or if a name is not given, the complete plugin dictionary is returned.

        :param name: Name of a plugin
        :return: None, single plugin or dictionary of plugins
        """
        if name is None:
            return self._plugins
        else:
            if name not in self._plugins.keys():
                return None
            else:
                return self._plugins[name]

    def exist(self, name):
        """
        Returns True if plugin exists.
        :param name: plugin name
        :return: boolean
        """
        if name in self._plugins.keys():
            return True
        return False

    def is_active(self, name):
        """
        Returns True if plugin exists and is active.
        If plugin does not exist, it returns None

        :param name: plugin name
        :return: boolean or None
        """
        if name in self._plugins.keys():
            return self._plugins["name"].active
        return None


class PluginClassManager:
    """
    Manages the plugin classes, which can be used to initialise and activate new plugins.

    Loads all plugin classes from entry_point "groundwork.plugin" automatically during own initialisation.
    Provides functions to register new plugin classes during runtime.
    """

    def __init__(self, app):
        self._log = logging.getLogger(__name__)
        self._app = app
        self._classes = {}
        self._get_plugins_by_entry_points()

    def _get_plugins_by_entry_points(self):
        """
        Registers plugin classes, which are in sys.path and have an entry_point called 'groundwork.plugin'.
        :return: dict of plugin classes
        """
        # Let's find and register every plugin, which is in sys.path and has defined a entry_point 'groundwork.plugin'
        # in it's setup.py
        entry_points = []
        classes = {}
        for entry_point in iter_entry_points(group='groundwork.plugin', name=None):
            entry_points.append(entry_point)

        for entry_point in entry_points:
            try:
                entry_point_object = entry_point.load()
            except Exception as e:
                # We should not throw an exception now, because a package/entry_point can be outdated, using an old
                # api from groundwork, tries to import unavailable packages, what ever...
                # We just do not make it available. That's all we can do.
                self._log.debug("Couldn't load entry_point %s. Reason: %s" % (entry_point.name, e))
                continue

            if not issubclass(entry_point_object, GwBasePattern):
                self._log.warning("entry_point  %s is not a subclass of groundworkPlugin" % entry_point.name)
                continue
            plugin_name = entry_point_object.__name__

            plugin_class = self.register_class(entry_point_object, plugin_name,
                                               entrypoint_name=entry_point.name,
                                               distribution_path=entry_point.dist.location,
                                               distribution_key=entry_point.dist.key,
                                               distribution_version=entry_point.dist.version)

            classes[plugin_name] = plugin_class
            # classes[plugin_name] = {
            #     "name": plugin_name,
            #     "entry_point": entry_point.name,
            #     "path": entry_point.dist.location,
            #     "class": entry_point_object,
            #     "distribution": {
            #         "key": entry_point.dist.key,
            #         "version": entry_point.dist.version
            #     },
            # }
            self._log.debug("Found plugin: %s at entry_point %s of package %s (%s)" % (plugin_name, entry_point.name,
                                                                                       entry_point.dist.key,
                                                                                       entry_point.dist.version))
        return classes

    def register(self, classes=[]):
        """
        Registers new plugins.

        The registration only creates a new entry for a plugin inside the _classes dictionary.
        It does not activate or even initialise the plugin.

        A plugin must be a class, which inherits directly or indirectly from GwBasePattern.

        :param classes: List of plugin classes
        :type classes: list
        """
        if not isinstance(classes, list):
            raise AttributeError("plugins must be a list, not %s." % type(classes))

        plugin_registered = []

        for plugin_class in classes:
            plugin_name = plugin_class.__name__
            self.register_class(plugin_class, plugin_name)
            self._log.debug("Plugin %s registered" % plugin_name)
            plugin_registered.append(plugin_name)

        self._log.info("Plugins registered: %s" % ", ".join(plugin_registered))

    def register_class(self, clazz, name=None, entrypoint_name=None, distribution_path=None,
                       distribution_key=None, distribution_version=None):

        if name is None:
            name = clazz.__name__

        if not inspect.isclass(clazz) or not issubclass(clazz, GwBasePattern):
            self._log.error("Given plugin is not a subclass of groundworkPlugin.")
            if self._app.strict:
                raise AttributeError("Given plugin is not a subclass of groundworkPlugin.")

        if isinstance(clazz, GwBasePattern):
            self._log.error("Given plugin %s is already initialised. Please provide a class not an instance.")
            if self._app.strict:
                raise Exception("Given plugin %s is already initialised. Please provide a class not an instance.")

        if name in self._classes.keys():
            self._log.warning("Plugin %s already registered" % name)
            if self._app.strict:
                raise PluginRegistrationException("Plugin %s already registered" % name)

        self._classes[name] = PluginClass(name, clazz, entrypoint_name, distribution_path,
                                          distribution_key, distribution_version)

        return self._classes[name]

        # self._classes[name] = {
        #     "name": plugin_name,
        #     "entry_point": None,
        #     "path": None,
        #     "class": plugin,
        #     "distribution": None,
        # }

    def get(self, name=None):
        """
        Returns the plugin class object with the given name.
        Or if a name is not given, the complete plugin dictionary is returned.

        :param name: Name of a plugin
        :return: None, single plugin or dictionary of plugins
        """
        if name is None:
            return self._classes
        else:
            if name not in self._classes.keys():
                return None
            else:
                return self._classes[name]

    def exist(self, name):
        """
        Returns True if plugin class exists.
        :param name: plugin name
        :return: boolean
        """
        if name in self._classes.keys():
            return True
        return False


class PluginClass:
    def __init__(self, name, clazz, entrypoint_name, distribution_path, distribution_key, distribution_version):
        self.name = name
        self.entrypoint_name = entrypoint_name
        self.clazz = clazz
        self.distribution = {
            "path": distribution_path,
            "key": distribution_key,
            "version": distribution_version
        }
