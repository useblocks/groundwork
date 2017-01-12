import pytest
from groundwork.patterns.gw_threads_pattern import ThreadExistsException


def test_thread_plugin_activation(basicApp):
    plugin = basicApp.plugins.get("ThreadPlugin")
    assert plugin is not None
    assert plugin.active is True


def test_thread_run(basicApp):
    plugin = basicApp.plugins.get("ThreadPlugin")
    thread = plugin.threads.get("test_thread")
    assert thread is not None
    thread.run()
    while thread.running:
        pass
    assert thread.response == "Done"


def test_thread_exists(basicApp):
    plugin = basicApp.plugins.get("ThreadPlugin")
    with pytest.raises(ThreadExistsException):
        plugin.threads.register("test_thread", None)
