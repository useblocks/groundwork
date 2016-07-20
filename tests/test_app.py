import os
import pytest

import groundwork


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


def test_app_initialisation_with_plugins(test_plugins):
    # Tries to import, but doesn't stop on problems
    app = groundwork.App(plugins=["TestPluginA", "TestPluginB", "NoPlugin"])

    # Tries to import and stops on problems
    with pytest.raises(AttributeError):
        app = groundwork.App(plugins=["TestPluginA", "TestPluginB", "NoPlugin"], strict=True)

    from plugins import BasicPlugin

    app = groundwork.App(plugins=[BasicPlugin])
    app.plugins.activate(["BasicPlugin"])


def test_app_plugin(test_plugins):
    from plugins import BasicPlugin

    app = groundwork.App(plugins=[BasicPlugin], strict=True)
    plugin = app.plugins.get("BasicPlugin")
    assert plugin is not None
    assert plugin["active"] is None

    app.plugins.activate(["BasicPlugin"])
    plugin = app.plugins.get("BasicPlugin")
    assert plugin is not None
    assert plugin["active"] == True




