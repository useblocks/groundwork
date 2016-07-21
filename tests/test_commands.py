"""
For ideas how to test commands based on clicks, see http://click.pocoo.org/5/testing/#basic-testing
"""
from click.testing import CliRunner


def test_command_plugin_activation(basicApp):
    plugin = basicApp.plugins.get("CommandPlugin")
    assert plugin is not None
    assert plugin["initialised"] == True
    assert plugin["active"] == True


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