import logging
import click

from groundwork.patterns.gw_base_pattern import GwBasePattern


class GwCommandsPattern(GwBasePattern):
    """
    Adds a commandline interface to a groundwork app and allows plugins to register own commands.

    The functionality is based on click: http://click.pocoo.org/5/

    To register command parameters, you have to create instances of click.Option or click.Argument manually and
      add them to the register-parameter "params"

    Example ::

        from groundwork import GwCommandsPattern
        from click import Option

        class MyPlugin(GwCommandsPattern)

            def activate(self):
                self.commands.register(command="my_command",
                                       description="Help for my command",
                                       params=[Option(("--test", "-t"), help="Some
                                       dummy text")])

            def my_command(self, my_test):
                    print("Command executed! my_test=%s" % my_test)

    For a complete list of configurable options, please take a look into the related click documentation of
    `Option
    <https://github.com/pallets/click/blob/c8e21105ebeb824c06c929bdd74c41eed776e956/click/core.py#L1419>`_ and
    `Argument <https://github.com/pallets/click/blob/c8e21105ebeb824c06c929bdd74c41eed776e956/click/core.py#L1687>`_

    **Starting the command line interface**

    Groundwork does not start automatically the command line interface. This step must be done by the application
    developer. Example ::

        from groundwork import GwApp

        gw_app = GwApp(plugins=["MyCommandPlugin"])
        gw_app.activate(plugins=["MyCommandPlugin"])
        gw_app.commands.start_cli()
    """

    def __init__(self, *args, **kwargs):
        super(GwCommandsPattern, self).__init__(*args, **kwargs)
        if not hasattr(self.app, "commands"):
            self.app.commands = CommandsListApplication(self.app)

        #: Instance of :class:`~.CommandsListPlugin`.
        #: Provides functions to register and manage commands for a command line interface.
        self.commands = CommandsListPlugin(self)


class CommandsListPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

        # Let's register a receiver, which cares about the deactivation process of commands for this plugin.
        # We do it after the original plugin deactivation, so we can be sure that the registered function is the last
        # one which cares about commands for this plugin.
        self.plugin.signals.connect(receiver="%s_command_deactivation" % self.plugin.name,
                                    signal="plugin_deactivate_post",
                                    function=self.__deactivate_commands,
                                    description="Deactivate commands for %s" % self.plugin.name,
                                    sender=self.plugin)
        self.log.debug("Plugin commands initialised")

    def __deactivate_commands(self, plugin, *args, **kwargs):
        commands = self.get()
        for command in commands.keys():
            self.unregister(command)

    def register(self, command, description, function, params=[]):
        """
        Registers a new command for a plugin.

        :param command: Name of the command
        :param description: Description of the command. Is used as help message on cli
        :param function: function reference, which gets invoked if command gets called.
        :param params: list of click options and arguments
        :return: command object
        """
        return self.app.commands.register(command, description, function, params, self.plugin)

    def unregister(self, command):
        """
        Unregisters an existing command, so that this command is no longer available on the command line interface.
        This function is mainly used during plugin deactivation.

        :param command: Name of the command
        """
        return self.app.commands.unregister(command)

    def get(self, name=None):
        """
        Returns commands, which can be filtered by name.

        :param name: name of the command
        :type name: str
        :return: None, single command or dict of commands
        """
        return self.app.commands.get(name, self.plugin)


class CommandsListApplication():
    def __init__(self, app):
        self.app = app
        self.log = logging.getLogger(__name__)
        self._commands = {}
        self.log.info("Application commands initialised")
        self._click_root_command = click.Group()

    def start_cli(self, *args, **kwargs):
        """
        Start the command line interface for the application.

        :param args: arguments
        :param kwargs: keyword arguments
        :return: none
        """
        return self._click_root_command(*args, **kwargs)

    def get(self, name=None, plugin=None):
        """
        Returns commands, which can be filtered by name or plugin.

        :param name: name of the command
        :type name: str
        :param plugin: plugin object, which registers the commands
        :type plugin: instance of GwBasePattern
        :return: None, single command or dict of commands
        """
        if plugin is not None:
            if name is None:
                command_list = {}
                for key in self._commands.keys():
                    if self._commands[key].plugin == plugin:
                        command_list[key] = self._commands[key]
                return command_list
            else:
                if name in self._commands.keys():
                    if self._commands[name].plugin == plugin:
                        return self._commands[name]
                    else:
                        return None
                else:
                    return None
        else:
            if name is None:
                return self._commands
            else:
                if name in self._commands.keys():
                    return self._commands[name]
                else:
                    return None

    def register(self, command, description, function, params=[], plugin=None):
        """
        Registers a new command, which can be used on a command line interface (cli).

        :param command: Name of the command
        :param description: Description of the command. Is used as help message on cli
        :param function: function reference, which gets invoked if command gets called.
        :param params: list of click options and arguments
        :param plugin: the plugin, which registered this command
        :return: command object
        """
        if command in self._commands.keys():
            raise CommandExistException("Command %s already registered by %s" % (command,
                                                                                 self._commands[command].plugin.name))

        new_command = Command(command, description, params, function, plugin)
        self._commands[command] = new_command
        self._click_root_command.add_command(new_command.click_command)
        self.log.debug("Command registered: %s" % command)
        return new_command

    def unregister(self, command):
        """
        Unregisters an existing command, so that this command is no longer available on the command line interface.

        This function is mainly used during plugin deactivation.

        :param command: Name of the command
        """
        if command not in self._commands.keys():
            self.log.warning("Can not unregister command %s" % command)
        else:
            # Click does not have any kind of a function to unregister/remove/deactivate already added commands.
            # So we need to delete the related objects manually from the click internal commands dictionary for
            # our root command.
            del(self._click_root_command.commands[command])
            # Finally lets delete the command from our internal dictionary too.
            del(self._commands[command])
            self.log.debug("Command %s got unregistered" % command)


class Command:
    def __init__(self, command, description, parameters, function, plugin):
        self.command = command
        self.description = description
        self.parameters = parameters
        self.plugin = plugin
        self.function = function
        self.click_command = click.Command(command, callback=function, help=description, params=parameters)


class CommandExistException(BaseException):
    pass
