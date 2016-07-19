import logging
import click

from groundwork.patterns.gw_plugin_pattern import GwPluginPattern
from groundwork.sharedobject import SharedObject
from groundwork.utilities import Singleton


class GwCommandsPattern(GwPluginPattern):
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
                self.commands.register("my_command", "Help for my command", params=[Option(("--test", "-t"), help="Some dummy text")])

            def my_command(self, my_test):
                    print("Command executed! my_test=%s" % my_test)

    For a complete list of configurable options, please take a look into the related click documentation:

    Option: https://github.com/pallets/click/blob/c8e21105ebeb824c06c929bdd74c41eed776e956/click/core.py#L1419

    Argument: https://github.com/pallets/click/blob/c8e21105ebeb824c06c929bdd74c41eed776e956/click/core.py#L1687

    Usage inside your own App
    *************************

    Groundwork does not start automatically the command line interface. This step must be done by the application
    developer. Example ::

        from groundwork import GwApp

        gw_app = GwApp(config_files=["conf/myconf.py"])
        gw_app.load_plugins(gw_app.config.get("PLUGINS"))
        gw_app.commands.start_cli()
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = CommandsListPlugin(self)

    def activate(self):
        pass

    def deactivate(self):
        pass


class CommandsListPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log
        self.app.commands = CommandsListApplication(plugin.app)
        self.log.info("Plugin commands initialised")

    def register(self, name, description, function, params=[]):
        return self.app.commands.register(name, description, function, params, self.plugin)

    def get(self, name=None):
        return self.app.commands.get(name, self.plugin)

    def __getattr__(self, item):
        """
        Catches unknown function/attribute calls and delegates them to CommandsListApplication
        """
        def method(*args, **kwargs):
            func = getattr(self.app.commands, item, None)
            if func is None:
                raise AttributeError("CommandsList does not have an attribute called %s" % item)
            return func(*args, plugin=self.plugin, **kwargs)
        return method


class CommandsListApplication(metaclass=Singleton):
    def __init__(self, app):
        self.app = app
        self.log = logging.getLogger(__name__)
        self._commands = {}
        self.log.info("Application commands initialised")
        self._click_root_command = click.Group()
        self.start_cli = self._click_root_command

    def get(self, name=None, plugin=None):
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

    def register(self, name, description, function, params=[], plugin=None):
        if name in self._commands.keys():
            raise CommandExistException("Command %s already registered by %s" % (name,
                                                                                 self._commands[name].plugin.name))

        new_command = Command(name, description, params, function, plugin)
        self._commands[name] = new_command
        self._click_root_command.add_command(new_command.click_command)
        self.log.debug("Command registered: %s" % name)
        return new_command


class Command:
    def __init__(self, name, description, parameters, function, plugin):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.plugin = plugin
        self.function = function
        self.click_command = click.Command(name, callback=function, help=description, params=parameters)


class CommandExistException(BaseException):
    pass
