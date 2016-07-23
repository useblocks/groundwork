import sys
import os
import pytest

@pytest.fixture
def test_apps(monkeypatch):
    monkeypatch.syspath_prepend(
        os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'test_apps'))
    )

@pytest.fixture
def test_plugins(monkeypatch):
    monkeypatch.syspath_prepend(
        os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'test_plugins'))
    )


@pytest.fixture
def basicApp():
    """
    Loads a basic groundwork application and returns it.

    See tests/test_apps/basic_app for implementation details
    :return: app
    """
    from groundwork import App
    from tests.test_plugins import BasicPlugin, CommandPlugin, DocumentPlugin

    app = App(plugins=[BasicPlugin, CommandPlugin, DocumentPlugin], strict=True)
    app.plugins.activate(["BasicPlugin", "CommandPlugin", "DocumentPlugin"])
    return app


@pytest.fixture
def BasicPlugin():
    """
    :return: basic plugin class
    """
    from tests.test_plugins.basic_plugin import BasicPlugin
    return BasicPlugin

@pytest.fixture
def CommandPlugin():
    """
    :return: command plugin class
    """
    from tests.test_plugins.commands_plugin import CommandPlugin
    return CommandPlugin

@pytest.fixture
def DocumentPlugin():
    """
    :return: document plugin class
    """
    from tests.test_plugins.documentations_plugin import DocumentPlugin
    return DocumentPlugin


@pytest.fixture
def SignalPlugin():
    """
    :return: signal plugin class
    """
    from tests.test_plugins.signals_plugin import SignalPlugin
    return SignalPlugin

# See http://docs.pytest.org/en/latest/example/simple.html#incremental-testing-test-steps
def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


# See http://docs.pytest.org/en/latest/example/simple.html#incremental-testing-test-steps
def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" %previousfailed.name)