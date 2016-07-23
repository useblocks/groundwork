import os
import pytest
from groundwork.patterns.gw_documents_pattern import NoAbsolutePathException
from groundwork.exceptions import PluginRegistrationException


def test_document_plugin_activation(basicApp):
    plugin = basicApp.plugins.get("DocumentPlugin")
    assert plugin is not None
    assert plugin.active == True


def test_document_registration(basicApp):
    plugin = basicApp.plugins.get("DocumentPlugin")
    with pytest.raises(NoAbsolutePathException):
        plugin.documents.register("new_document", "static/document.txt")
    plugin.documents.register("new_document", os.path.abspath("static/document.txt"))

    docs = plugin.documents.get()
    assert len(docs.keys()) == 2
    assert "new_document" in docs.keys()

    doc = plugin.documents.get("new_document")
    assert doc.name == "new_document"




