"""
For ideas how to test commands based on clicks, see http://click.pocoo.org/5/testing/#basic-testing
"""
import pytest
from click.testing import CliRunner
from click import Option
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
