"""
For ideas how to test commands based on clicks, see http://click.pocoo.org/5/testing/#basic-testing
"""

import os
import pytest
from click import Option
from click.testing import CliRunner

from groundwork.patterns import GwCommandsPattern

import groundwork


class TestCommandPlugin(GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("test", "my test command", self._test_command, params=[Option(("--arg", "-a"))])

    def _test_command(self, arg):
        print(arg)


def test_command_plugin_activation():
    app = groundwork.App(plugins=[TestCommandPlugin])
    app.plugins.activate(["TestCommandPlugin"])
    plugin = app.plugins.get("TestCommandPlugin")
    assert plugin is not None
    assert plugin["initialised"] == True
    assert plugin["active"] == True


def test_command_plugin_execution():
    app = groundwork.App(plugins=[TestCommandPlugin])
    app.plugins.activate(["TestCommandPlugin"])
    runner = CliRunner()
    result = runner.invoke(app.commands._commands["test"].click_command, ["--invalid"])
    assert "no such option" in result.output
    assert result.exit_code == 2

    result = runner.invoke(app.commands._commands["test"].click_command, ["--arg", "12345"])
    assert "12345" in result.output
    assert result.exit_code == 0

    command = app.commands.get("test")
    assert command is not None