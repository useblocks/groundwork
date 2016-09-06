from click.testing import CliRunner
from groundwork.plugins import GwSignalsInfo


def test_plugin_activation(basicApp):
    app = basicApp
    plugin = GwSignalsInfo(app)
    plugin.activate()


def test_plugin_deactivation(basicApp):
    app = basicApp
    plugin = GwSignalsInfo(app)
    plugin.activate()
    plugin.deactivate()


def test_plugin_list_signals(emptyApp):
    app = emptyApp
    plugin = GwSignalsInfo(app)
    plugin.activate()
    runner = CliRunner()
    runner.invoke(app.commands.get("signal_list").click_command)


def test_plugin_list_receivers(emptyApp):
    app = emptyApp
    plugin = GwSignalsInfo(app)
    plugin.activate()
    runner = CliRunner()
    runner.invoke(app.commands.get("receiver_list").click_command)
