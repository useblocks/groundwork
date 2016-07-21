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


def test_app_plugin(BasicPlugin):
    app = groundwork.App(plugins=[BasicPlugin], strict=True)
    plugin = app.plugins.get("BasicPlugin")
    assert plugin is not None
    assert plugin["active"] is None

    app.plugins.activate(["BasicPlugin"])
    plugin = app.plugins.get("BasicPlugin")
    assert plugin is not None
    assert plugin["active"] == True


def test_app_multi_repeating_registration(BasicPlugin, basicApp):
    with pytest.raises(PluginRegistrationException):
        basicApp.plugins.register([BasicPlugin])


def test_multi_app(BasicPlugin):
    app = groundwork.App(plugins=[BasicPlugin], strict=True)
    plugin = app.plugins.get("BasicPlugin")

    app2 = groundwork.App(plugins=[BasicPlugin], strict=True)
    plugin2 = app2.plugins.get("BasicPlugin")

    assert app is not app2
    assert plugin == plugin2  # Checks, if content is the same
    assert plugin is not plugin2  # Checks, if reference is not the same

    app.plugins.activate(["BasicPlugin"])
    app2.plugins.activate(["BasicPlugin"])
    assert plugin != plugin2  # Content should be different, because plugin instance was added.
