"""
Groundwork threads support module.
"""

import logging
import threading
import datetime

from groundwork.patterns.gw_base_pattern import GwBasePattern


class GwThreadsPattern(GwBasePattern):
    """
    Threads can be created and started to perform tasks in the background and in parallel to the main application.

    Please see :ref:`threads` for more details.
    """

    def __init__(self, *args, **kwargs):
        super(GwThreadsPattern, self).__init__(*args, **kwargs)

        if not hasattr(self.app, "threads"):
            self.app.threads = ThreadsListApplication(self.app)

        #: Stores an instance of :class:`~groundwork.patterns.gw_threads_pattern.ThreadsListPlugin`
        self.threads = ThreadsListPlugin(self)


class ThreadsListPlugin:
    """
    Stores and handles threads.

    Please see :ref:`threads` for more details.
    """

    def __init__(self, plugin):
        """
        :param plugin: The plugin, which wants to use threads
        :type plugin: GwBasePattern
        """
        self._plugin = plugin
        self.__app = plugin.app
        self.__log = plugin.log

        # Let's register a receiver, which cares about the deactivation process of threads for this plugin.
        # We do it after the original plugin deactivation, so we can be sure that the registered function is the last
        # one which cares about threads for this plugin.
        self._plugin.signals.connect(receiver="%s_threads_deactivation" % self._plugin.name,
                                     signal="plugin_deactivate_post",
                                     function=self.__deactivate_threads,
                                     description="Deactivate threads for %s" % self._plugin.name,
                                     sender=self._plugin)
        self.__log.debug("Plugin threads initialised")

    def __deactivate_threads(self, plugin, *args, **kwargs):
        threads = self.get()
        for thread in threads.keys():
            self.unregister(thread)

    def register(self, name, function, description=None):
        """
        Register a new thread.

        :param function: Function, which gets called for the new thread
        :type function: function
        :param name: Unique name of the thread for documentation purposes.
        :param description: Short description of the thread
        """
        return self.__app.threads.register(name, function, self._plugin, description)

    def unregister(self, thread):
        return self.__app.threads.unregister(thread)

    def get(self, name=None):
        return self.__app.threads.get(name, self._plugin)


class ThreadsListApplication:
    """

    """

    def __init__(self, app):
        self.__app = app
        self.__log = logging.getLogger(__name__)
        self.threads = {}
        self.__log.info("Application threads initialised")

    def register(self, name, function, plugin, description=None):
        """
        Registers a new document.

        .. warning: You can not use any relative links inside a given document.
                    For instance, sphinx's toctree, image, figure or include statements do not work.

        :param function: Function, which gets called for the new thread
        :type function: function
        :param name: Unique name of the thread for documentation purposes.
        :param plugin: Plugin object, under which the threads where registered
        :type plugin: GwBasePattern
        :param description: Short description of the thread
        """
        if name in self.threads.keys():
            raise ThreadExistsException("Thread %s was already registered by %s" %
                                        (name, self.threads[name].plugin.name))

        self.threads[name] = Thread(name, function, plugin, description)
        self.__log.debug("Thread %s registered by %s" % (name, plugin.name))
        return self.threads[name]

    def unregister(self, thread):
        """
        Unregisters an existing thread, so that this thread is no longer available.

        This function is mainly used during plugin deactivation.

        :param thread: Name of the thread
        """
        if thread not in self.threads.keys():
            self.log.warning("Can not unregister thread %s" % thread)
        else:
            del (self.threads[thread])
            self.__log.debug("Thread %s got unregistered" % thread)

    def get(self, thread=None, plugin=None):
        """
        Get one or more threads.

        :param thread: Name of the thread
        :type thread: str
        :param plugin: Plugin object, under which the thread was registered
        :type plugin: GwBasePattern
        """
        if plugin is not None:
            if thread is None:
                threads_list = {}
                for key in self.threads.keys():
                    if self.threads[key].plugin == plugin:
                        threads_list[key] = self.threads[key]
                return threads_list
            else:
                if thread in self.threads.keys():
                    if self.threads[thread].plugin == plugin:
                        return self.threads[thread]
                    else:
                        return None
                else:
                    return None
        else:
            if thread is None:
                return self.threads
            else:
                if thread in self.threads.keys():
                    return self.threads[thread]
                else:
                    return None


class Thread:
    """
    Groundwork thread class. Used to store name, function and plugin.

    This information is mostly used to generated overviews about registered threads.

    :param name: Name of the thread
    :type name: str
    :param function: Function, which gets called inside the thread
    :type function: function
    :param plugin: The plugin, which registered this thread
    :type plugin: GwBasePattern
    :param description: short description of this thread
    """
    def __init__(self, name, function, plugin, description=None):
        self.name = name
        self.function = function
        self.plugin = plugin
        self.description = description

        #: Thread base class. Type is threading.Thread
        self.thread = ThreadWrapper(self)

        #: Stores the function return value, if thread has finished
        self.response = None

        #: datetime object of the starting moment
        self.time_start = None

        #: datetime object of the ending moment
        self.time_end = None

        #: True, if thread is running. Otherwise its False.
        self.running = False

    def run(self, **kwargs):
        """
        Runs the thread

        :param kwargs: dictionary of keyword arguments
        :return:
        """
        self.thread.start()


class ThreadWrapper(threading.Thread):
    """
    Wrapper class, which inherits from threading.Thread and performs some useful tasks
    before and after the provided functions gets executed.

    """
    def __init__(self, thread):
        super(ThreadWrapper, self).__init__()
        self.thread = thread
        self.plugin = thread.plugin
        self.app = thread.plugin.app

    def run(self, **kwargs):
        self.thread.running = True
        self.thread.time_start = datetime.datetime.now()
        self.thread.response = self.thread.function(self.plugin, **kwargs)
        self.thread.time_end = datetime.datetime.now()
        self.thread.running = False


class ThreadExistsException(BaseException):
    pass
