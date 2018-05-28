import logging

# from blinker import Namespace

# Used in groundwork <= 0.1.11
# Used WeakNamespace could also be Namespace.
# But doc says, Weaknamespace gets clean up, if no reference exists anymore.
# from blinker import WeakNamespace as Namespace  # Do not use, seems to Clean up still needed parts!
from blinker import Namespace as Namespace


class SignalsApplication:
    """
    Signal and Receiver management class on application level.
    This class is initialised once per groundwork application object.

    Provides functions to register and send signals. And to connect receivers to signals.

    :param app: The groundwork application object
    :type app: GwApp
    """
    def __init__(self, app):
        self.__app = app
        # self.__log = app.log
        self.__log = logging.getLogger(__name__)

        #: Dictionary of registered signals. Dictionary key is the registered signal name.
        #: Value is an instance of :class:`~groundwork.signals.Signal`.
        self.signals = {}

        #: Dictionary of registered receivers. Dictionary key is the registered receiver name.
        #: Value is an instance of :class:`~groundwork.signals.Receiver`.
        self.receivers = {}

        # We must use an unique namespace for our signals. Otherwise we get problems with multiple applications or
        # application recreation, because blinker throws every signal to a "singleton container", which stays
        # the same for the whole runtime of the python interpreter. No cleanup or anything else.
        # So registered signals and receivers keep registered, whatever you do with the app.
        # How to use namespace in blinker? See:
        # http://flask.pocoo.org/docs/0.11/signals/#creating-signals for blinker namespace usage
        # https://github.com/jek/blinker/blob/master/blinker/base.py#L432
        #: Used blinker namespace object to register signals only for the context of a single groundwork application
        #: instance
        self._namespace = Namespace()

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

        self.signals[signal] = Signal(signal, plugin, self._namespace, description)
        self.__log.debug("Signal %s registered by %s" % (signal, plugin.name))
        return self.signals[signal]

    def unregister(self, signal):
        """
        Unregisters an existing signal

        :param signal: Name of the signal
        """
        if signal in self.signals.keys():
            del(self.signals[signal])
            self.__log.debug("Signal %s unregisterd" % signal)
        else:
            self.__log.debug("Signal %s does not exist and could not be unregistered.")

    def connect(self, receiver, signal, function, plugin, description="", sender=None):
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
        :param sender: If set, only signals from this sender will be send to ths receiver.

        """
        if receiver in self.receivers.keys():
            raise Exception("Receiver %s was already registered by %s" % (receiver,
                                                                          self.receivers[receiver].plugin.name))
        self.receivers[receiver] = Receiver(receiver, signal, function, plugin, self._namespace, description, sender)
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
        del(self.receivers[receiver])
        self.__log.debug("Receiver %s disconnected" % receiver)

    def send(self, signal, plugin, **kwargs):
        """
        Sends a signal for the given plugin.

        :param signal: Name of the signal
        :type signal: str
        :param plugin: Plugin object, under which the signals where registered
        :type plugin: GwBasePattern
        """
        if signal not in self.signals.keys():
            raise UnknownSignal("Unknown signal %s" % signal)
        self.__log.debug("Sending signal %s for %s" % (signal, plugin.name))
        rv = self.signals[signal].send(plugin, **kwargs)
        return rv

    def get(self, signal=None, plugin=None):
        """
        Get one or more signals.

        :param signal: Name of the signal
        :type signal: str
        :param plugin: Plugin object, under which the signals where registered
        :type plugin: GwBasePattern
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

    def get_receiver(self, receiver=None, plugin=None):
        """
        Get one or more receivers.

        :param receiver: Name of the signal
        :type receiver: str
        :param plugin: Plugin object, under which the signals where registered
        :type plugin: GwBasePattern
        """
        if plugin is not None:
            if receiver is None:
                receiver_list = {}
                for key in self.receivers.keys():
                    if self.receivers[key].plugin == plugin:
                        receiver_list[key] = self.receivers[key]
                return receiver_list
            else:
                if receiver in self.receivers.keys():
                    if self.receivers[receiver].plugin == plugin:
                        return self.receivers[receiver]
                    else:
                        return None
                else:
                    return None
        else:
            if receiver is None:
                return self.receivers
            else:
                if receiver in self.receivers.keys():
                    return self.receivers[receiver]
                else:
                    return None


class Signal:
    """
    Groundwork signal class. Used to store name, description and plugin.

    This information is mostly used to generated overviews about registered signals and their send history.

    :param name: Name of the signal
    :type name: str
    :param namespace: Namespace of the signal. There is one per groundwork app.
    :param description: Additional description for the signal
    :type description: str
    :param plugin: The plugin, which registered this signal
    :type plugin: GwBasePattern
    """
    def __init__(self, name, plugin, namespace, description=""):
        self.name = name
        self.description = description
        self.plugin = plugin
        self._signal = namespace.signal(name, doc=description)

    def send(self, plugin, **kwargs):
        return self._signal.send(plugin, **kwargs)


class Receiver:
    """
    Subscriber class, which stores information for documentation purposes.

    :param name: Name of the Subscriber
    :type name: str
    :param signal: Signal name(s)
    :type signal: str
    :param namespace: Namespace of the signal. There is one per groundwork app.
    :param function: Callable function, which gets executed, if signal is sent.
    :param plugin: Plugin object, which registered the subscriber
    :type plugin: GwBasePattern
    :param description: Additional description about the subscriber.
    :type description: str
    """
    def __init__(self, name, signal, function, plugin, namespace, description="", sender=None):
        self.name = name
        self.plugin = plugin
        self.function = function
        self.description = description
        self.signal = signal
        self.__log = logging.getLogger(__name__)
        self.namespace = namespace
        self.sender = sender
        self.connect()

    def connect(self):
        if not hasattr(self.function, '__call__'):
            self.__log.error("Given function object for signal %s is not a function" % self.signal)
        else:
            if isinstance(self.signal, str):
                if self.sender is None:
                    self.namespace.signal(self.signal).connect(self.function)
                else:
                    self.namespace.signal(self.signal).connect(self.function, sender=self.sender)
            else:
                self.__log.error("Given signal object is not a string.")

    def disconnect(self):
        self.namespace.signal(self.signal).disconnect(self.function)


class UnknownSignal(Exception):
    pass
