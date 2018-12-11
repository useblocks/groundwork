"""
    gw_base_pattern provides all basic classes and functions, which are needed by any kind of groundwork plugin or
    pattern.

    It mostly cares about the correct activation and deactivation. Including sending signals to inform
    other patterns or plugins about status changes of a plugin.

"""
import sys
import os
import logging

from groundwork.patterns.exceptions import PluginAttributeMissing, PluginActivateMissing, PluginDeactivateMissing, \
    PluginDependencyLoop


class GwBasePattern(object):
    """
    Base pattern class for all plugins and patterns.

    Usage::

        from groundwork.patterns import GwBasePattern

        class MyPlugin(GwBasePattern):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def activate():
                self.signals.register("MySignal", "My description about signal)

            def deactivate():
                self.signals.unregister("MySignal")

    :param app: groundwork application object, for which the plugin shall be initialised.
    :type app: :class:`groundwork.App`.
    :param name: Unique name. Normally set by plugin.
    """
    def __init__(self, app, name=None, *args, **kwargs):
        #: groundwork application instance. Access it inside a plugin via ``self.app``.
        self.app = app

        # There must be a name for this plugin. Otherwise it is not detectable and manageable on application level
        if not hasattr(self, "name") and name is None:
            raise PluginAttributeMissing("Name not set for plugin")
        elif not hasattr(self, "name") and name is not None:
            # Set the given name, if the plugin itself does not have set one
            self.name = name

        # Be sure we have a set version number. Can be overwritten by the plugin itself.
        if not hasattr(self, "version"):
            self.version = "0.0.1"

        # Let's be sure active is false, even if a child class set something different
        if not hasattr(self, "active"):
            self.active = False

        # Even if this plugin has no dependencies to other plugins, we should set an empty tuple.
        if not hasattr(self, "needed_plugins"):
            #: Variable for storing dependencies to other plugins.
            #: Tuple must contains needed plugin names.
            #: needed_plugins = ("MyPlugin", "MyPlugin2)
            self.needed_plugins = ()

        self.path = sys.modules[self.__module__].__file__
        self.file = os.path.basename(self.path)
        self.dir = os.path.dirname(self.path)

        #: A logger, especially created for this plugin. Usage inside a plugin: ``self.log.warn("WARNING!!")``.
        #:
        #: The logger name is the same as the plugin name. Therefor it is possible to configure the application logging
        #: to show log messages of a specif plugin only. See :ref:`plugin_logging`
        self.log = logging.getLogger(self.name)

        #: Instance of :class:`.SignalsPlugin`.
        #: Provides functions to register and manage signals and retrievers.
        #:
        #: All action takes place in the context of this plugin. For instance a ``self.signals.get()`` will return
        #: signals of this plugin only. To get all signals of an application, please use ``self.app.signals.get()``.
        self.signals = SignalsPlugin(self)

        # This is used as flag for the pluginManager to be sure, that an initiated class has called the __init__()
        # routine of GwPluginPatter
        self._plugin_base_initialised = True

        # Let's tell the pluginManager that this plugin got initialised, so that it gets tracked on app level.
        # This is needed if this class gets initiated by hand and the function self.app.plugins._load() was not used
        # for doing this job.
        self.app.plugins._register_initialisation(self)

    # def __getattribute__(self, name):
    def __getattribute__(self, name):
        """
        Catches all calls on class attributes, but cares only for activate() and deactivate().

        If the plugin gets activated or deactivated, the base class can perform extra work.
        So there is no need for a plugin developer to call something like super().activate() for
        his/her plugin. This gets done automatically.
        """

        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            if hasattr(attr, "__name__"):
                if attr.__name__ == "activate":
                    def newfunc(*args, **kwargs):
                        self._pre_activate_injection()
                        result = attr(*args, **kwargs)
                        self._post_activate_injection()
                        return result
                    return newfunc
                elif attr.__name__ == "deactivate":
                    def newfunc(*args, **kwargs):
                        self._pre_deactivate_injection()
                        result = attr(*args, **kwargs)
                        self._post_deactivate_injection()
                        return result
                    return newfunc

        return attr

    def activate(self):
        """
        Must be overwritten by the plugin class itself.
        """
        self.log.warning("No activation routine in Plugin defined. Define self.activate() in plugin %s" % self.name)
        raise PluginActivateMissing("plugin must provide an activation routine by itself.")

    def deactivate(self):
        """
        Must be overwritten by the plugin class itself.
        """
        self.log.warning("No activation routine in Plugin defined. Define self.deactivate() in plugin %s" % self.name)
        raise PluginDeactivateMissing("plugin must provide an deactivation routine by itself.")

    def _pre_activate_injection(self):
        """
        Injects functions before the activation routine of child classes gets called
        """
        # Let's be sure that this plugins class is registered and available on application level under
        # application.plugins.classes. This allows to reuse this class for *new* plugins.
        if not self.app.plugins.classes.exist(self.__class__.__name__):
            self.app.plugins.classes.register([self.__class__])

        self._load_needed_plugins()

        self.app.signals.send("plugin_activate_pre", self)

    def _post_activate_injection(self):
        """
        Injects functions after the activation routine of child classes got called
        :return: None
        """
        self.active = True
        self.app.signals.send("plugin_activate_post", self)

    def _pre_deactivate_injection(self):
        """
        Injects functions before the deactivation routine of child classes gets called
        :return: None
        """
        self.app.signals.send("plugin_deactivate_pre", self)

    def _post_deactivate_injection(self):
        """
        Injects functions after the deactivation routine of child classes got called
        :return: None
        """
        # Lets be sure that active is really set to false.
        self.active = False
        self.app.signals.send("plugin_deactivate_post", self)
        # After all receivers are handled. We start to clean up signals and receivers of this plugin
        # Attention: This signal clean must not be called via a signal (like in other patterns),
        # because the call order of receivers is not clear and a signal/receiver clean up would prohibit the call
        # of all "later" receivers.
        self.signals.deactivate_plugin_signals()

    def _load_needed_plugins(self):
        """
        Checks if this plugins needs other plugins to work and tries to activate them
        :return: True, if all needed plugins are or got activated. Otherwise False
        """
        global plugin_recursive_store
        if "plugin_recursive_store" not in globals():
            plugin_recursive_store = []

        if self.name in plugin_recursive_store:
            self.log.warning("Plugin dependency loop detected: %s already checked and dependencies got activated" %
                             self.name)
            if self.app.strict:
                raise PluginDependencyLoop("Plugin dependency loop detected: %s already checked and dependencies "
                                           "got activated" % self.name)
            return False
        else:
            plugin_recursive_store.append(self.name)

        if not hasattr(self, "needed_plugins"):
            pass
        elif not isinstance(self.needed_plugins, tuple) and not isinstance(self.needed_plugins, list):
            raise TypeError("needed_plugins must be a tuple or a list")
        elif len(self.needed_plugins) > 0:
            try:
                for needed_plugin in self.needed_plugins:
                    if not isinstance(needed_plugin, str):
                        raise TypeError("Plugin name must be a string, got %s" % type(needed_plugin).__name__)
                    # Check, if a plugin with this name got already activated
                    plugin = self.app.plugins.get(needed_plugin)
                    if plugin is not None and not plugin.active:
                        plugin.activate()
                    # If not, check if a plugin_class with this name is available and activate it
                    plugin_class = self.app.plugins.classes.get(needed_plugin)
                    if plugin_class is not None:
                        plugin_class(self.app, needed_plugin)
            except Exception:
                plugin_recursive_store.remove(self.name)
                return False

        plugin_recursive_store.remove(self.name)
        return True


class SignalsPlugin:
    """
    Signal and Receiver management class on plugin level.
    This class gets initiated once per plugin.

    Mostly delegates function calls to the :class:`groundwork.signals.SignalListApplication` instance on application
    level.

    :param plugin: The plugin, which wants to use signals
    :type plugin: GwBasePattern
    """

    def __init__(self, plugin):
        self._plugin = plugin
        self.__app = plugin.app
        self.__log = plugin.log
        self.__log.debug("Plugin messages initialised")

    def deactivate_plugin_signals(self):
        receivers = self.get_receiver()
        for receiver in receivers.keys():
            self.disconnect(receiver)

        signals = self.get()
        for signal in signals:
            self.unregister(signal)

    def register(self, signal, description):
        """
        Registers a new signal.
        Only registered signals are allowed to be send.

        :param signal: Unique name of the signal
        :param description: Description of the reason or use case, why this signal is needed.
                            Used for documentation.
        """
        return self.__app.signals.register(signal, self._plugin, description)

    def unregister(self, signal):
        return self.__app.signals.unregister(signal)

    def connect(self, receiver, signal, function, description, sender=None):
        """
        Connect a receiver to a signal

        :param receiver: Name of the receiver
        :type receiver: str
        :param signal: Name of the signal. Must already be registered!
        :type signal: str
        :param function: Callable functions, which shall be executed, of signal is send.
        :param description: Description of the reason or use case, why this connection is needed.
                            Used for documentation.
        """
        return self.__app.signals.connect(receiver, signal, function, self._plugin, description, sender)

    def disconnect(self, receiver):
        """
        Disconnect a receiver from a signal.
        Receiver must exist, otherwise an exception is thrown.

        :param receiver: Name of the receiver
        """
        return self.__app.signals.disconnect(receiver)

    def send(self, signal, **kwargs):
        """
        Sends a signal for the given plugin.

        :param signal: Name of the signal
        :type signal: str
        """
        return self.__app.signals.send(signal, plugin=self._plugin, **kwargs)

    def get(self, signal=None):
        """
        Returns a single signal or a dictionary of signals for this plugin.
        """
        return self.__app.signals.get(signal, self._plugin)

    def get_receiver(self, receiver=None):
        """
        Returns a single receiver or a dictionary of receivers for this plugin.
        """
        return self.__app.signals.get_receiver(receiver, self._plugin)
