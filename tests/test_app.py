import os
import pytest

import groundwork
from groundwork.exceptions import PluginRegistrationException


def test_app_initialisation():
    app = groundwork.App()
    assert app.path == os.getcwd()


def test_app_initialisation_with_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = os.path.join(current_dir, "static", "config.py")
    app = groundwork.App([config])

    assert app.path == os.getcwd()
    assert app.config.PLUGINS == ["PluginA", "PluginB", "NoPlugin"]


def test_app_initialisation_with_config2():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = os.path.join(current_dir, "static", "config2.py")
    app = groundwork.App([config])

    assert app.path == os.path.join(current_dir, "static")
    with pytest.raises(AttributeError):
        app.config.PLUGINS != ["PluginA", "PluginB", "NoPlugin"]


def test_app_initialisation_with_plugins(BasicPlugin):
    # Tries to import, but doesn't stop on problems
    app = groundwork.App(plugins=["TestPluginA", "TestPluginB", "NoPlugin"])

    # Tries to import and stops on problems
    with pytest.raises(AttributeError):
        app = groundwork.App(plugins=["TestPluginA", "TestPluginB", "NoPlugin"], strict=True)

    app = groundwork.App(plugins=[BasicPlugin])
    app.plugins.activate(["BasicPlugin"])


def test_app_plugin_registration(BasicPlugin):
    app = groundwork.App(plugins=[BasicPlugin], strict=True)
    plugin_class = app.plugins.classes.get("BasicPlugin")
    assert plugin_class is not None


def test_app_plugin_activation(BasicPlugin):
    app = groundwork.App(plugins=[BasicPlugin], strict=True)
    app.plugins.activate(["BasicPlugin"])
    plugin = app.plugins.get("BasicPlugin")
    assert plugin is not None
    assert plugin.active is True


def test_app_plugin_deactivation(BasicPlugin):
    app = groundwork.App(plugins=[BasicPlugin], strict=True)
    app.plugins.activate(["BasicPlugin"])
    plugin = app.plugins.get("BasicPlugin")
    assert plugin is not None
    assert plugin.active is True
    app.plugins.deactivate(["BasicPlugin"])
    assert plugin.active is False


def test_app_plugin_multi_status_change(BasicPlugin):
    app = groundwork.App(plugins=[BasicPlugin], strict=True)

    # De/Activation via app
    app.plugins.activate(["BasicPlugin"])
    plugin = app.plugins.get("BasicPlugin")
    assert plugin.active is True
    app.plugins.deactivate(["BasicPlugin"])
    assert plugin.active is False
    app.plugins.activate(["BasicPlugin"])
    assert plugin.active is True
    # De/Activation via plugin itself
    plugin = app.plugins.get("BasicPlugin")
    plugin.deactivate()
    assert plugin.active is False


def test_app_multi_repeating_registration(BasicPlugin, basicApp):
    with pytest.raises(PluginRegistrationException):
        basicApp.plugins.classes.register([BasicPlugin])


def test_multi_app(BasicPlugin):
    app = groundwork.App(plugins=[BasicPlugin], strict=True)
    plugin_class = app.plugins.classes.get("BasicPlugin")

    app2 = groundwork.App(plugins=[BasicPlugin], strict=True)
    plugin2_class = app2.plugins.classes.get("BasicPlugin")

    assert app is not app2
    assert plugin_class is not plugin2_class  # Checks, if reference is not the same

    app.plugins.activate(["BasicPlugin"])
    plugin = app.plugins.get("BasicPlugin")

    app2.plugins.activate(["BasicPlugin"])
    plugin2 = app2.plugins.get("BasicPlugin")

    assert plugin is not plugin2
