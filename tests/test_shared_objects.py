import pytest
from groundwork.patterns.gw_shared_objects_pattern import SharedObjectExistException


def test_shared_object_plugin_activation(basicApp):
    plugin = basicApp.plugins.get("SharedObjectPlugin")
    assert plugin is not None
    assert plugin.active is True


def test_shared_object_registration(basicApp):
    test_object = {"test": "this"}
    plugin = basicApp.plugins.get("SharedObjectPlugin")
    with pytest.raises(SharedObjectExistException):
        plugin.shared_objects.register("test_object", "doc", test_object)

    plugin.shared_objects.register("test_object2", "doc", test_object)
    assert len(basicApp.shared_objects.get()) == 2
    assert len(plugin.shared_objects.get()) == 2
    assert plugin.shared_objects.get("test_object2").obj == test_object
    assert plugin.shared_objects.get("test_object2").obj is test_object


def test_shared_object_deactivation(basicApp, EmptySharedObjectPlugin):
    test_object = {"test": "this"}
    plugin = basicApp.plugins.get("SharedObjectPlugin")
    assert len(basicApp.shared_objects.get()) == 1
    assert len(plugin.shared_objects.get()) == 1

    plugin2 = EmptySharedObjectPlugin(basicApp, "SharedObjectPlugin2")
    plugin2.activate()
    with pytest.raises(SharedObjectExistException):
        plugin.shared_objects.register("test_object", "doc", test_object)

    plugin2.shared_objects.register("test_object2", "doc", test_object)
    assert len(basicApp.shared_objects.get()) == 2
    assert len(plugin.shared_objects.get()) == 1
    assert len(plugin2.shared_objects.get()) == 1

    plugin.deactivate()
    assert len(basicApp.shared_objects.get()) == 1
    assert len(plugin2.shared_objects.get()) == 1
