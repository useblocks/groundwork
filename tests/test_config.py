import pytest
from groundwork.configuration.config import Config


def test_config():
    config = Config()

    config.set("test", 1)
    assert config.get("test") == 1

    with pytest.raises(Exception):
        config.set("test", 1)

    config.set("test", 2, overwrite=True)
    assert config.get("test") == 2
