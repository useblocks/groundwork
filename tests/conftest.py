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