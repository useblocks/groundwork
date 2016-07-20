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


def test_app_initialisation_with_plugins(test_apps):
    # Tries to import, but doesn't stop on problems
    app = groundwork.App(plugins=["TestPluginA", "TestPluginB", "NoPlugin"])

    # Tries to import and stops on problems
    with pytest.raises(AttributeError):
        app = groundwork.App(plugins=["TestPluginA", "TestPluginB", "NoPlugin"], strict=True)

    from basicapp.plugins import TestPlugin
    app = groundwork.App(plugins=[TestPlugin])
    app.plugins.activate(["MyPlugin"])


def test_app_plugin(test_apps):
    from basicapp.plugins import TestPlugin
    app = groundwork.App(plugins=[TestPlugin])
    app.plugins.activate(["MyPlugin"])
    plugins = app.plugins.get()



