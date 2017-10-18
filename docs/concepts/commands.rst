.. _commands:

Commands
========

Commands are used to provide access to different function via a command line interface (CLI).

groundwork cares automatically about CLI setup, help messages and  command arguments.

However the command line interface must be started by the application itself.

Starting the CLI
----------------

To start the cli, be sure that at least one plugin gets activated, which is using the pattern
:class:`~groundwork.patterns.gw_commands_pattern.GwCommandsPattern`.

After application initialisation and plugin activations,
:func:`~groundwork.patterns.gw_commands_pattern.CommandsListApplication.start_cli` must be called::

    from groundwork import App
    from groundword.plugins import GwCommandInfo

    my_app = App()
    my_app.plugins.activate(["GwCommandInfo"])
    my_app.commands.start_cli()

Registering commands
--------------------

To register commands, a plugin must inherit from :class:`~groundwork.patterns.gw_commands_pattern.GwCommandsPattern`
and use the function :func:`~groundwork.patterns.gw_commands_pattern.CommandsListPlugin.register`. ::

    from groundwork.patterns import GwCommandsPattern

    class MyPlugin(GwCommandsPattern):
        def __init__(self, app, **kwargs)
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            self.commands.register(command="my_command",
                                   description="executes something",
                                   function=self.my_command,
                                   params=[])

        def my_command(self, plugin, **kwargs):
            print("Yehaaa")

Using arguments and options
---------------------------

groundworks's command line support is based on `click <http://click.pocoo.org/>`_.

For arguments and options, groundwork is using the definition and native classes of click:

    * `Arguments <http://click.pocoo.org/5/api/#click.Argument>`_ are positional parameters to a command
    * `Options <http://click.pocoo.org/5/api/#click.Option>`_ are usually optional value on a command.

To use them, you have to pass instances of them to the ``params`` parameter of the function
:func:`~groundwork.patterns.gw_commands_pattern.CommandsListPlugin.register`. ::

    from groundwork.patterns import GwCommandsPattern
    from click import Argument, Option

    class MyPlugin(GwCommandsPattern):
        def __init__(self, app, **kwargs)
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            self.commands.register(command="my_command",
                                   description="executes something",
                                   function=self.my_command,
                                   params=[Option(("--force", "-f"),
                                                  required=False,
                                                  help="Will force something...",
                                                  default=False,
                                                  is_flag=True)])

        def my_command(self, plugin, force, **kwargs):
            if force:
                print("FORCE Yehaaa")
            else:
                print("Maybe Yehaaa")

For detailed parameter description, please take a look into the documentation of `click <http://click.pocoo.org/>`_ for
`arguments <http://click.pocoo.org/5/api/#click.Argument>`_ and
`options <http://click.pocoo.org/5/api/#click.Option>`_

Unregister a command
--------------------

A command can also be unregistered during runtime.

Simply use :func:`~groundwork.patterns.gw_commands_pattern.CommandsListPlugin.unregister` and pass the name of
the command::

    ...

    def deactivate(self):
        self.commands.unregister("my_command")


