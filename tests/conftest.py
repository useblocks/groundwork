import os
import pytest
import sys

# The following addition to sys.path is needed to find imports
# like 'from test.test_plugins import BasicPlugin'
# Normally the test path is not part of sys.path
sys.path.append("/".join([os.path.dirname(os.path.abspath(__file__)), ".."]))


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
    from tests.test_plugins import BasicPlugin, CommandPlugin, DocumentPlugin, SharedObjectPlugin

    app = App(plugins=[BasicPlugin, CommandPlugin, DocumentPlugin, SharedObjectPlugin], strict=True)
    app.plugins.activate(["BasicPlugin", "CommandPlugin", "DocumentPlugin", "SharedObjectPlugin"])
    return app


@pytest.fixture
def EmptyPlugin():
    """
    :return: empty plugin class
    """
    from tests.test_plugins.empty_plugin import EmptyPlugin
    return EmptyPlugin


@pytest.fixture
def EmptyCommandPlugin():
    """
    :return: empty command plugin class
    """
    from tests.test_plugins.empty_command_plugin import EmptyCommandPlugin
    return EmptyCommandPlugin


@pytest.fixture
def EmptyDocumentPlugin():
    """
    :return: empty document plugin class
    """
    from tests.test_plugins.empty_document_plugin import EmptyDocumentPlugin
    return EmptyDocumentPlugin


@pytest.fixture
def EmptySharedObjectPlugin():
    """
    :return: empty shared object plugin class
    """
    from tests.test_plugins.empty_shared_object_plugin import EmptySharedObjectPlugin
    return EmptySharedObjectPlugin


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
            pytest.xfail("previous test failed (%s)" % previousfailed.name)
