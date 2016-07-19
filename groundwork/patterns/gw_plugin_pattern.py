import logging

from .exceptions import PluginAttributeMissing
from groundwork.sharedobject import SharedObject
from groundwork.sharedobject.exceptions import SharedObjectExists, SharedObjectNotRegistered


class GwPluginPattern(object):
    def __init__(self, app, *args, **kwargs):
        super().__init__()
        self.app = app

        if not hasattr(self, "name"):
            raise PluginAttributeMissing("name attribute not set in Plugin class. Plugin initialisation stops here.")

        # self.log = logging.getLogger(".".join((__package__, self.name)))
        self.log = logging.getLogger(self.name)

        self.log.debug("Initialisation of %s" % self.name)
        self.plugin_commands = []

        self.log.debug("Initialisation done")

        self.plugin_base_initialised = True

    def activate(self):
        self.log.warn("No activation routine in Plugin defined. Define self.activate() in plugin %s" % self.name)

    def deactivate(self):
        self.log.warn("No activation routine in Plugin defined. Define self.deactivate() in plugin %s" % self.name)

    # #####################################################################################################
    # #   COMMANDS                                                                                        #
    # #####################################################################################################
    # def register_command(self, name, help, func, arguments=[]):
    #     """
    #     Registers a new commad for the command line interface.
    #     e.g. python your_app.py new_command
    #
    #     :param name: Name of the new command
    #     :param help: Help text, which gets shown by e.g. "help new_command"
    #     :param func: function-object, which gets executed, if the given command
    #                  gets executed
    #     :param arguments: Arguments, which must be provided by the user
    #     :return: None
    #     """
    #     self.plugin_commands.append({"name": name,
    #                                  "help": help,
    #                                  "func": func,
    #                                  "arguments": arguments})
    #
    # #####################################################################################################
    # #   SHARED OBJECTS                                                                                  #
    # #####################################################################################################
    # def register_shared_object(self, name, shared_object, description=None):
    #     """
    #     Registers a shared object, which will be availabe for all plugins after
    #     activation phase.
    #
    #     A shared object can be everything: string, number, class, function
    #
    #     The requestor of a shared_object must know how to handle it. Therefore
    #     the creator should provide a documentation.
    #
    #     The name of a shared object must be unique. If another plugin has
    #     already registered something using the same name, the next register
    #     request will raise an error
    #
    #     :param name: Name of the shared object
    #     :param shared_object: the object to share
    #     :param description: string, which describes the shared_object for documentation
    #     :return:
    #     """
    #     shared_objects = self.app.shared_objects
    #
    #     obj = SharedObject(name=name,
    #                        shared_object=shared_object,
    #                        description=description,
    #                        plugin_name=self.name)
    #     shared_objects.register(obj)
    #     self.log.debug("Registered shared object %s" % name )
    #
    # def get_shared_object(self, name):
    #     """
    #     Returns a shared object dictionary, if it exists. Otherwise an error is
    #     raised.
    #
    #     :param name: Name of the shared object
    #     :return: Instance of SharedObject with the keys: name, description, shared_object,
    #              plugin.
    #     shared_object type is not defined and can be everything (string,
    #     number, class, function, ...)
    #     """
    #     shared_objects = self.app.shared_objects
    #     return shared_objects.get(name)
