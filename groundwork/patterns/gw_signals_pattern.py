"""
Groudnwork signal support module.

Provides a pattern to allow plugins to register and send signals and to connect their own functions to signals.

Functionality is based on the library `blinker <http://pythonhosted.org/blinker/>`_
"""

import logging
from blinker import signal as blinker_signal

from groundwork.patterns.gw_plugin_pattern import GwPluginPattern
from groundwork.utilities import Singleton


class GwSignalsPattern(GwPluginPattern):
    """
    Pattern for activating signals and receivers inside a plugin.

    To register a signal::

        self.signals.register("my_signal", "Just a test signal")

    To connect to a signal::

        def test_func(plugin, **kwargs)
            self.log.debug("My connected signal was called by %s" % plugin.name)

        self.signals.connect("My_test_Connection", "my_signal", test_func, "Just a test connection to my_test")

    To send a signal::

        self.signals.send("my_signal", argument="test", additional_argument="test_2")

    To disconnect from a signal::

        self.signals.disconnect("My_test_Connection")

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signals = SignalListPlugin(self)

    def activate(self):
        pass

    def deactivate(self):
        pass


class SignalListPlugin:
    """
    Signal and Receiver management class on plugin level.
    This class gets initiated once per plugin.

    Mostly delegates function calls to the SingnalListApplication instance on application level.

    :param plugin: The plugin, which wants to use signals
    :type plugin: GwPluginPattern
    """

    def __init__(self, plugin):
        self._plugin = plugin
        self.__app = plugin.app
        self.__log = plugin.log
        self.__app.signals = SignalsListApplication(plugin.app)
        self.__log.info("Plugin messages initialised")

    def register(self, signal, description):
        """
        Registers a new signal.
        Only registered signals are allowed to be send.

        :param signal: Unique name of the signal
        :param description: Description of the reason or use case, why this signal is needed.
                            Used for documentation.
        """
        return self.__app.signals.register(signal, self._plugin, description)

    def connect(self, receiver, signal, function, description):
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
        return self.__app.signals.connect(receiver, signal, function, self._plugin, description)

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
        return self.__app.signals.get(signal, self.__plugin)

    def __getattr__(self, item):
        """
        Catches unknown function/attribute calls and delegates them to SignalsListApplication
        """

        def method(*args, **kwargs):
            func = getattr(self.__app.signals, item, None)
            if func is None:
                raise AttributeError("SignalsListApplication does not have an attribute called %s" % item)
            return func(*args, plugin=self.__plugin, **kwargs)

        return method


class SignalsListApplication(metaclass=Singleton):
    """
    Signal and Receiver management class on application level.
    This class can only be instantiated once (Singleton)

    Provides functions to register and send signals. And to connect receivers to signals.

    :param app: The groundwork application object
    :type app: GwApp
    """
    def __init__(self, app):
        self.__app = app
        # self.__log = app.log
        self.__log = logging.getLogger(__name__)
        self.signals = {}
        self.receivers = {}

        self.__log.info("Application signals initialised")

    def register(self, signal, plugin, description=""):
        """
        Registers a new signal.

        :param signal: Unique name of the signal
        :param plugin: Plugin, which registers the new signal
        :param description: Description of the reason or use case, why this signal is needed.
                            Used for documentation.
        """
        if signal in self.signals.keys():
            raise Exception("Signal %s was already registered by %s" % (signal, self.signals[signal].plugin.name))

        self.signals[signal] = Signal(signal, plugin, description)
        self.__log.debug("Signal %s registered by %s" % (signal, plugin.name))
        return self.signals[signal]

    def connect(self, receiver, signal, function, plugin, description=""):
        """
        Connect a receiver to a signal

        :param receiver: Name of the receiver
        :type receiver: str
        :param signal: Name of the signal. Must already be registered!
        :type signal: str
        :param function: Callable functions, which shall be executed, of signal is send.
        :param plugin: The plugin objects, which connects one of its functions to a signal.
        :param description: Description of the reason or use case, why this connection is needed.
                            Used for documentation.

        """
        if receiver in self.receivers.keys():
            raise Exception("Receiver %s was already registered by %s" % (receiver, self.receiver[receiver].plugin.name))
        self.receivers[receiver] = Receiver(receiver, signal, function, plugin, description)
        self.__log.debug("Receiver %s registered for signal %s" % (receiver, signal))
        return self.receivers[receiver]

    def disconnect(self, receiver):
        """
        Disconnect a receiver from a signal.
        Signal and receiver must exist, otherwise an exception is thrown.

        :param receiver: Name of the receiver
        """
        if receiver not in self.receivers.keys():
            raise Exception("No receiver %s was registered" % receiver)
        self.receivers[receiver].disconnect()
        self.__log.debug("Receiver %s disconnected" % receiver)

    def send(self, signal, plugin, **kwargs):
        """
        Sends a signal for the given plugin.

        :param signal: Name of the signal
        :type signal: str
        :param plugin: Plugin object, under which the signals where registered
        :type plugin: GwPluginPattern
        """
        if signal not in self.signals.keys():
            raise Exception("Unknown signal %s" % signal)
        self.__log.debug("Sending signal %s for %s" % (signal, plugin.name))
        self.signals[signal].send(plugin, **kwargs)

    def get(self, signal=None, plugin=None):
        """
        Get one or more signals.

        :param signal: Name of the signal
        :type signal: str
        :param plugin: Plugin object, under which the signals where registered
        :type plugin: GwPluginPattern
        """
        if plugin is not None:
            if signal is None:
                signals_list = {}
                for key in self.signals.keys():
                    if self.signals[key].plugin == plugin:
                        signals_list[key] = self.signals[key]
                return signals_list
            else:
                if signal in self.signals.keys():
                    if self.signals[signal].plugin == plugin:
                        return self.signals[signal]
                    else:
                        return None
                else:
                    return None
        else:
            if signal is None:
                return self.signals
            else:
                if signal in self.signals.keys():
                    return self.signals[signal]
                else:
                    return None


class Signal:
    """
    Groundwork signal class. Used to store name, description and plugin.

    This information is mostly used to generated overviews about registered signals and their send history.

    :param name: Name of the signal
    :type name: str
    :param description: Additional description for the signal
    :type description: str
    :param plugin: The plugin, which registered this signal
    :type plugin: GwPluginPattern
    """
    def __init__(self, name, plugin, description=""):
        self.name = name
        self.description = description
        self.plugin = plugin
        self._signal = blinker_signal(name, doc=description)
        self.__log = logging.getLogger(__name__)

    def send(self, plugin, **kwargs):
        return self._signal.send(plugin, **kwargs)


class Receiver:
    """
    Subscriber class, which stores information for documentation purposes.

    :param name: Name of the Subscriber
    :type name: str
    :param signal: Signal name(s)
    :type signal: str
    :param function: Callable function, which gets executed, if signal is sent.
    :param plugin: Plugin object, which registered the subscriber
    :type plugin: GwPluginPattern
    :param description: Additional description about the subscriber.
    :type description: str
    """
    def __init__(self, name, signal, function, plugin, description=""):
        self.name = name
        self.plugin = plugin
        self.function = function
        self.description = description
        self.signal = signal
        self.__log = logging.getLogger(__name__)
        self.connect()

    def connect(self):
        if not hasattr(self.function, '__call__'):
            self.__log.error("Given function object for signal %s is not a function" % self.signal)
        else:
            if isinstance(self.signal, str):
                blinker_signal(self.signal).connect(self.function)
            else:
                self.__log.error("Given signal object is not a string.")

    def disconnect(self):
        blinker_signal(self.signal).disconnect(self.function)
