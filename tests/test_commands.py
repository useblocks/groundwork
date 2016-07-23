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
    assert plugin.active == True


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
    def _test_command(self, arg):
        print(arg)

    plugin = basicApp.plugins.get("CommandPlugin")
    with pytest.raises(CommandExistException):
        plugin.commands.register("test", "my test command", _test_command, params=[Option(("--arg", "-a"))])

    plugin.commands.unregister("test")
    plugin.commands.register("test", "my test command", _test_command, params=[Option(("--arg", "-a"))])
    assert len(basicApp.commands.get()) == 1

    basicApp.plugins.deactivate(["CommandPlugin"])
    print(basicApp.commands.get().keys())
    assert len(basicApp.commands.get().keys()) == 0
