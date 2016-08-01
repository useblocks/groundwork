import os
import pytest
from groundwork.patterns.gw_documents_pattern import NoAbsolutePathException, DocumentExistsException


def test_document_plugin_activation(basicApp):
    plugin = basicApp.plugins.get("DocumentPlugin")
    assert plugin is not None
    assert plugin.active is True


def test_document_registration(basicApp):
    plugin = basicApp.plugins.get("DocumentPlugin")
    plugin.documents.register("new_document", os.path.abspath("static/document.txt"))

    docs = plugin.documents.get()
    assert len(docs.keys()) == 2
    assert "new_document" in docs.keys()

    doc = plugin.documents.get("new_document")
    assert doc.name == "new_document"


def test_document_deactivation(basicApp, EmptyDocumentPlugin):
    plugin = basicApp.plugins.get("DocumentPlugin")
    with pytest.raises(DocumentExistsException):
        plugin.documents.register("test_document", "test_content")

    doc_content = os.path.abspath("test_content")

    assert len(plugin.documents.get().keys()) == 1
    assert len(basicApp.documents.get().keys()) == 1

    plugin.documents.unregister("test_document")
    assert len(plugin.documents.get().keys()) == 0
    assert len(basicApp.documents.get().keys()) == 0

    plugin.documents.register("test_document", doc_content)
    assert len(plugin.documents.get().keys()) == 1
    assert len(basicApp.documents.get().keys()) == 1

    plugin2 = EmptyDocumentPlugin(basicApp, "DocumentPlugin2")
    plugin2.activate()
    plugin2.documents.register("test_document2", doc_content)
    assert len(plugin.documents.get().keys()) == 1
    assert len(plugin2.documents.get().keys()) == 1
    assert len(basicApp.documents.get().keys()) == 2

    plugin.deactivate()
    assert len(plugin.documents.get().keys()) == 0
    assert len(plugin2.documents.get().keys()) == 1
    assert len(basicApp.documents.get().keys()) == 1
