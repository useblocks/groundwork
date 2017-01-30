"""
Groundwork documentation support module.
"""

import logging

from groundwork.patterns.gw_base_pattern import GwBasePattern


class GwDocumentsPattern(GwBasePattern):
    """
    Documents can be collected by other Plugins to present their content inside user documentation, online help,
    console output or whatever.

    Please see :ref:`documents` for more details.
    """

    def __init__(self, *args, **kwargs):
        super(GwDocumentsPattern, self).__init__(*args, **kwargs)

        if not hasattr(self.app, "documents"):
            self.app.documents = DocumentsListApplication(self.app)

        #: Stores an instance of :class:`~groundwork.patterns.gw_documents_pattern.DocumentsListPlugin`
        self.documents = DocumentsListPlugin(self)


class DocumentsListPlugin:
    """
    Stores and handles documents.

    These documents are used for real-time and offline documentation of a groundwork application.

    The content of a document must be string, which is can contain jinja and rst syntax.

    Plugins, which want to generate a documentation out of all documents, must render this content
    (jinja render_template) and transform the rst by the own (e.g. by using rst2html).

    Please see :ref:`documents` for more details.
    """

    def __init__(self, plugin):
        """
        :param plugin: The plugin, which wants to use documents
        :type plugin: GwBasePattern
        """
        self._plugin = plugin
        self.__app = plugin.app
        self.__log = plugin.log

        # Let's register a receiver, which cares about the deactivation process of documents for this plugin.
        # We do it after the original plugin deactivation, so we can be sure that the registered function is the last
        # one which cares about documents for this plugin.
        self._plugin.signals.connect(receiver="%s_documents_deactivation" % self._plugin.name,
                                     signal="plugin_deactivate_post",
                                     function=self.__deactivate_documents,
                                     description="Deactivate documents for %s" % self._plugin.name,
                                     sender=self._plugin)
        self.__log.debug("Plugin documents initialised")

    def __deactivate_documents(self, plugin, *args, **kwargs):
        documents = self.get()
        for document in documents.keys():
            self.unregister(document)

    def register(self, name, content, description=None):
        """
        Register a new document.

        :param content: Content of this document. Jinja and rst are supported.
        :type content: str
        :param name: Unique name of the document for documentation purposes.
        :param description: Short description of this document
        """
        return self.__app.documents.register(name, content, self._plugin, description)

    def unregister(self, document):
        return self.__app.documents.unregister(document)

    def get(self, name=None):
        return self.__app.documents.get(name, self._plugin)


class DocumentsListApplication:
    """

    """

    def __init__(self, app):
        self.__app = app
        self.__log = logging.getLogger(__name__)
        self.documents = {}
        self.__log.info("Application documents initialised")

    def register(self, name, content, plugin, description=None):
        """
        Registers a new document.

        .. warning: You can not use any relative links inside a given document.
                    For instance, sphinx's toctree, image, figure or include statements do not work.

        :param content: Content of the document
        :type content: str
        :param name: Unique name of the document for documentation purposes.
        :param plugin: Plugin object, under which the documents where registered
        :type plugin: GwBasePattern
        """
        if name in self.documents.keys():
            raise DocumentExistsException("Document %s was already registered by %s" %
                                          (name, self.documents[name].plugin.name))

        self.documents[name] = Document(name, content, plugin, description)
        self.__log.debug("Document %s registered by %s" % (name, plugin.name))
        return self.documents[name]

    def unregister(self, document):
        """
        Unregisters an existing document, so that this document is no longer available.

        This function is mainly used during plugin deactivation.

        :param document: Name of the document
        """
        if document not in self.documents.keys():
            self.log.warning("Can not unregister document %s" % document)
        else:
            del (self.documents[document])
            self.__log.debug("Document %s got unregistered" % document)

    def get(self, document=None, plugin=None):
        """
        Get one or more documents.

        :param document: Name of the document
        :type document: str
        :param plugin: Plugin object, under which the document was registered
        :type plugin: GwBasePattern
        """
        if plugin is not None:
            if document is None:
                documents_list = {}
                for key in self.documents.keys():
                    if self.documents[key].plugin == plugin:
                        documents_list[key] = self.documents[key]
                return documents_list
            else:
                if document in self.documents.keys():
                    if self.documents[document].plugin == plugin:
                        return self.documents[document]
                    else:
                        return None
                else:
                    return None
        else:
            if document is None:
                return self.documents
            else:
                if document in self.documents.keys():
                    return self.documents[document]
                else:
                    return None


class Document:
    """
    Groundwork document class. Used to store name, file_path, alias and plugin.

    This information is mostly used to generated overviews about registered documents.

    :param name: Name of the document
    :type name: str
    :param content: Content of the document, which is used for documentation building
    :type content: str (jinja + rst)
    :param plugin: The plugin, which registered this document
    :type plugin: GwBasePattern
    :param description: short description of document
    """
    def __init__(self, name, content, plugin, description=None):
        self.name = name
        self.content = content
        self.plugin = plugin
        self.description = description


class NoAbsolutePathException(BaseException):
    pass


class DocumentExistsException(BaseException):
    pass
