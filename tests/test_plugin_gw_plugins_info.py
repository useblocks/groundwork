from click.testing import CliRunner
from groundwork.plugins import GwPluginsInfo


def test_plugin_activation(basicApp):
    app = basicApp
    plugin = GwPluginsInfo(app)
    plugin.activate()


def test_plugin_deactivation(basicApp):
    app = basicApp
    plugin = GwPluginsInfo(app)
    plugin.activate()
    plugin.deactivate()


def test_plugin_list_plugins(emptyApp):
    app = emptyApp
    plugin = GwPluginsInfo(app)
    plugin.activate()
    runner = CliRunner()
    runner.invoke(app.commands.get("plugin_list").click_command)
