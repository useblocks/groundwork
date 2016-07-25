"""
Groundwork documentation support module.
"""

import os
import logging

from groundwork.patterns.gw_base_pattern import GwBasePattern


class GwDocumentsPattern(GwBasePattern):
    """
    Documents can be collected by other Plugins to present their content inside user documentation, online help,
    console output or whatever.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self.app, "documents"):
            self.app.documents = DocumentsListApplication(self.app)
        self.documents = DocumentsListPlugin(self)

    def activate(self):
        pass

    def deactivate(self):
        pass


class DocumentsListPlugin:
    """
    """

    def __init__(self, plugin):
        """
        :param plugin: The plugin, which wants to use signals
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

    def register(self, name, file_path, alias=None):
        """
        Register a new document.

        :param file_path: Absolute path of the document location
        :param name: Unique name of the document for documentation purposes.
        :param alias: Alias of the document. May be used as file name, if documents are copied or restructured.
               (Optional)
        """
        return self.__app.documents.register(name, file_path, alias, self._plugin)

    def unregister(self, document):
        return self.__app.documents.unregister(document)

    def get(self, name=None):
        return self.__app.documents.get(name, self._plugin)

    def __getattr__(self, item):
        """
        Catches unknown function/attribute calls and delegates them to DocumentsListApplication
        """

        def method(*args, **kwargs):
            func = getattr(self.__app.documents, item, None)
            if func is None:
                raise AttributeError("DocumentsListApplication does not have an attribute called %s" % item)
            return func(*args, plugin=self._plugin, **kwargs)

        return method


class DocumentsListApplication:
    """

    """

    def __init__(self, app):
        self.__app = app
        self.__log = logging.getLogger(__name__)
        self.documents = {}
        self.__log.info("Application documents initialised")

    def register(self, name, file_path, alias, plugin):
        """
        Registers a new signal.

        .. warning: You can not use any relative links inside a given document.
                    For instance, sphinx's toctree, image, figure or include statements do not work.

        :param file_path: Absolute path of the document location
        :param name: Unique name of the document for documentation purposes.
        :param alias: Alias of the document. May be used as file name, if documents are copied or restructured.
               (Optional)
        :param plugin: Plugin object, under which the signals where registered
        :type plugin: GwBasePattern
        """
        if name in self.documents.keys():
            raise DocumentExistsException("Document %s was already registered by %s" %
                                          (name, self.documents[name].plugin.name))

        if not os.path.isabs(file_path):
            raise NoAbsolutePathException("file_path %s is not absolute" % file_path)
        self.documents[name] = Document(name, file_path, alias, plugin)
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

        :param document: Name of the signal
        :type document: str
        :param plugin: Plugin object, under which the signals where registered
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
    :param file_path: Absolute path to the document file
    :type file_path: str (path)
    :param alias: Alias of the document. May be used as file name, if documents are copied or restructured.
    :type alias: str
    :param plugin: The plugin, which registered this document
    :type plugin: GwBasePattern
    """

    def __init__(self, name, file_path, alias, plugin, ):
        self.name = name
        self.file_path = file_path
        self.alias = alias
        self.plugin = plugin
        self.__log = logging.getLogger(__name__)


class NoAbsolutePathException(BaseException):
    pass


class DocumentExistsException(BaseException):
    pass

