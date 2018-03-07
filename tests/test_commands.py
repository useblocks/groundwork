"""
For ideas how to test commands based on clicks, see http://click.pocoo.org/5/testing/#basic-testing
"""
import click
import pytest
from click import Argument, Option
from click.testing import CliRunner

from groundwork.patterns.gw_commands_pattern import CommandExistException


def test_command_plugin_activation(basicApp):
    plugin = basicApp.plugins.get("CommandPlugin")
    assert plugin is not None
    assert plugin.active is True


# def test_command_cli_activation(basicApp):
#     test = basicApp.commands.start_cli(standalone_mode=True, args=[])
#     print(test)


def test_command_plugin_execution(basicApp):
    runner = CliRunner()
    result = runner.invoke(basicApp.commands._commands["test"].click_command, ["--invalid"])
    assert "no such option" in result.output
    assert result.exit_code == 2

    result = runner.invoke(basicApp.commands._commands["test"].click_command, ["--arg", "12345"])
    assert "12345" in result.output
    assert result.exit_code == 0

    command = basicApp.commands.get("test")
    assert command is not None


def test_command_multi_registration(basicApp):
    def _test_command(arg):
        print(arg)

    plugin = basicApp.plugins.get("CommandPlugin")
    with pytest.raises(CommandExistException):
        plugin.commands.register("test", "my test command", _test_command, params=[Option(("--arg", "-a"))])

    plugin.commands.unregister("test")
    plugin.commands.register("test", "my test command", _test_command, params=[Option(("--arg", "-a"))])
    assert len(basicApp.commands.get()) == 1

    plugin.commands.register("test2", "my test2 command", _test_command, params=[Option(("--arg", "-a"))])
    assert len(basicApp.commands.get()) == 2

    basicApp.plugins.deactivate(["CommandPlugin"])
    print(basicApp.commands.get().keys())
    assert len(basicApp.commands.get().keys()) == 0


def test_command_multi_plugin_registration(basicApp, EmptyCommandPlugin):
    def _test_command(arg):
        print(arg)

    plugin = basicApp.plugins.get("CommandPlugin")
    plugin2 = EmptyCommandPlugin(app=basicApp, name="CommandPlugin2")
    plugin2.activate()
    plugin2.commands.register("test2", "my test2 command", _test_command, params=[Option(("--arg", "-a"))])
    assert len(basicApp.commands.get()) == 2
    assert len(plugin.commands.get()) == 1
    assert len(plugin2.commands.get()) == 1

    basicApp.plugins.deactivate(["CommandPlugin2"])
    assert len(basicApp.commands.get()) == 1
    assert len(plugin.commands.get()) == 1
    assert len(plugin2.commands.get()) == 0


def test_command_mandatory_argument(basicApp):
    def _test_command(*args, **kwargs):
        print(args)
        print(kwargs)

    plugin = basicApp.plugins.get("CommandPlugin")
    plugin.commands.unregister("test")
    # register a command with a mandatory argument
    plugin.commands.register("test", "my test command", _test_command, params=[Argument(("man_arg",), required=True)])
    # call command with argument -> expect ok
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ["arg"])
    assert result.exit_code == 0

    # call command with no argument -> expect error
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, [])
    assert result.exit_code == 2


def test_command_optional_argument(basicApp):
    def _test_command(*args, **kwargs):
        print(args)
        print(kwargs)

    plugin = basicApp.plugins.get("CommandPlugin")
    plugin.commands.unregister("test")
    # register a command with an optional argument
    plugin.commands.register("test", "my test command", _test_command, params=[Argument(("opt_arg",), required=False)])
    # call command with argument -> expect ok
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ["arg"])
    assert result.exit_code == 0

    # call command with no argument -> expect ok
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, [])
    assert result.exit_code == 0


def test_command_mandatory_option(basicApp):
    def _test_command(*args, **kwargs):
        print(args)
        print(kwargs)

    plugin = basicApp.plugins.get("CommandPlugin")
    plugin.commands.unregister("test")
    # register a command with a mandatory option
    plugin.commands.register("test", "my test command", _test_command, params=[Option(["--man-opt"], required=True)])
    # call command with option --man-opt -> expect ok
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ["--man-opt", 123])
    assert result.exit_code == 0

    # call command with no option -> expect error
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, [])
    assert result.exit_code == 2


def test_command_optional_option(basicApp):
    def _test_command(*args, **kwargs):
        print(args)
        print(kwargs)

    plugin = basicApp.plugins.get("CommandPlugin")
    plugin.commands.unregister("test")
    # register a command with a mandatory option
    plugin.commands.register("test", "my test command", _test_command, params=[Option(["--opt-opt"], required=False)])
    # call command with option --opt-opt -> expect ok
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ["--opt-opt", 123])
    assert result.exit_code == 0

    # call command with no option -> expect ok
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, [])
    assert result.exit_code == 0


def test_command_path_argument(basicApp):
    def _test_command(*args, **kwargs):
        print(args)
        print(kwargs)

    plugin = basicApp.plugins.get("CommandPlugin")
    plugin.commands.unregister("test")
    # register a command with a path argument, that must exist
    plugin.commands.register("test", "my test command", _test_command, params=[Argument(("man_arg",),
                                                                                        type=click.Path(exists=True))])
    # call command with existing path as argument -> expect ok
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, [__file__])
    assert result.exit_code == 0

    # call command with non-existing path as argument -> expect error
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ['no such path'])
    assert result.exit_code == 2


def test_command_path_option(basicApp):
    def _test_command(*args, **kwargs):
        print(args)
        print(kwargs)

    plugin = basicApp.plugins.get("CommandPlugin")
    plugin.commands.unregister("test")
    # register a command with a path option, that must exist
    plugin.commands.register("test", "my test command", _test_command, params=[Option(["--path"],
                                                                                      type=click.Path(exists=True))])
    # call command with existing path as option -> expect ok
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ['--path', __file__])
    assert result.exit_code == 0

    # call command with non-existing path as option -> expect error
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ['--path', 'no such path'])
    assert result.exit_code == 2


def test_command_flag_on_off(basicApp):
    def _test_command(*args, **kwargs):
        print(args)
        print(kwargs)
        if not kwargs['flag_on']:
            raise Exception

    plugin = basicApp.plugins.get("CommandPlugin")
    plugin.commands.unregister("test")
    # register a command with an on/off flag; command throws exception if flag is off
    plugin.commands.register("test", "my test command", _test_command, params=[Option(["--flag-on/--flag-off"])])

    # call command with --flag-on (True) -> expect ok
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ['--flag-on'])
    assert result.exit_code == 0

    # call command with --flag-off (False)  -> expect error
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ['--flag-off'])
    assert result.exit_code == -1


def test_command_flag_count(basicApp):
    def _test_command(*args, **kwargs):
        print(args)
        print(kwargs)
        assert kwargs['flag'] == 3

    plugin = basicApp.plugins.get("CommandPlugin")
    plugin.commands.unregister("test")
    # register a command with a countable flag
    plugin.commands.register("test", "my test command", _test_command, params=[Option(["-f", "--flag"], count=True)])

    # call command with --fff -> count == 3 is asserted in the command handler
    result = CliRunner().invoke(basicApp.commands.get("test").click_command, ['-fff'])
    assert result.exit_code == 0
