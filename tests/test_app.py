import os
import pytest

import groundwork
from groundwork.exceptions import PluginRegistrationException
from groundwork.patterns import GwBasePattern
from groundwork.patterns.gw_base_pattern import PluginAttributeMissing, PluginActivateMissing, PluginDeactivateMissing
from groundwork.patterns.exceptions import PluginDependencyLoop


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


def test_app_strict():

    class MyBadPlugin():
        pass

    my_app = groundwork.App(strict=True)
    with pytest.raises(AttributeError):
        my_app.plugins.classes.register([MyBadPlugin])     # will throw an exception

    my_app.strict = False
    my_app.plugins.classes.register([MyBadPlugin])     # will log a warning only

    assert len(my_app.plugins.get()) == 0


# def test_app_initialisation_with_plugins(BasicPlugin):
#     # Tries to import, but doesn't stop on problems
#     # app = groundwork.App(plugins=["TestPluginA", "TestPluginB", "NoPlugin"])
#
#     # Tries to import and stops on problems
#     with pytest.raises(AttributeError):
#         app = groundwork.App(plugins=["TestPluginA", "TestPluginB", "NoPlugin"], strict=True)
#
#     app = groundwork.App(plugins=[BasicPlugin])
#     app.plugins.activate(["BasicPlugin"])


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


def test_plugin_missing_name(basicApp):

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            super().__init__(app, **kwargs)

    with pytest.raises(PluginAttributeMissing):
        MyPlugin(basicApp)


def test_plugin_missing_activate(basicApp):

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "my_plugin"
            super().__init__(app, **kwargs)

    my_plugin = MyPlugin(basicApp)
    with pytest.raises(PluginActivateMissing):
        my_plugin.activate()


def test_plugin_missing_deactivate(basicApp):

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "my_plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            pass

    my_plugin = MyPlugin(basicApp)
    my_plugin.activate()
    with pytest.raises(PluginDeactivateMissing):
        my_plugin.deactivate()


def test_plugin_unknown_attribute(basicApp):
    plugin = basicApp.plugins.get("CommandPlugin")
    with pytest.raises(AttributeError):
        plugin.nowhere()


def test_plugin_dependency(basicApp):

    class MyPluginA(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "my_plugin_a"
            self.needed_plugins = ("my_plugin_b",)
            super().__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    class MyPluginB(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "my_plugin_b"
            super().__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    my_plugin_a = MyPluginA(basicApp)
    my_plugin_b = MyPluginB(basicApp)

    assert my_plugin_b.active is False
    my_plugin_a.activate()
    assert my_plugin_b.active is True


def test_plugin_dependency_loop(basicApp):

    class MyPluginA(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "my_plugin_a"
            self.needed_plugins = ("my_plugin_b",)
            super().__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    class MyPluginB(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "my_plugin_b"
            self.needed_plugins = ("my_plugin_a",)
            super().__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    my_plugin_a = MyPluginA(basicApp)
    my_plugin_b = MyPluginB(basicApp)

    basicApp.strict = False
    assert my_plugin_b.active is False
    my_plugin_a.activate()
    assert my_plugin_b.active is True

    my_plugin_a.deactivate()
    my_plugin_b.deactivate()

    basicApp.strict = True
    assert my_plugin_b.active is False
    with pytest.raises(PluginDependencyLoop):
        my_plugin_a.activate()
