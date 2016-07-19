"""
Groundwork documentation support module.
"""

import logging

from groundwork.patterns.gw_plugin_pattern import GwPluginPattern
from groundwork.utilities import Singleton


class GwDocumentsPattern(GwPluginPattern):
    """
    Documents can be collected by other Plugins to present their content inside user documentation, online help,
    console output or whatever.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        :type plugin: GwPluginPattern
        """
        self._plugin = plugin
        self.__app = plugin.app
        self.__log = plugin.log
        self.__app.documents = DocumentsListApplication(plugin.app)
        self.__log.info("Plugin messages initialised")

    def register(self, name, file_path, alias=None):
        """
        Register a new document.

        :param file_path: Absolute path of the document location
        :param name: Unique name of the document for documentation purposes.
        :param alias: Alias of the document. May be used as file name, if documents are copied or restructured.
               (Optional)
        """
        return self.__app.documents.register(name, file_path, alias, self._plugin)

    def get(self, name=None):
        return self.__app.documents.get(name, self.__plugin)

    def __getattr__(self, item):
        """
        Catches unknown function/attribute calls and delegates them to DocumentsListApplication
        """

        def method(*args, **kwargs):
            func = getattr(self.__app.documents, item, None)
            if func is None:
                raise AttributeError("DocumentsListApplication does not have an attribute called %s" % item)
            return func(*args, plugin=self.__plugin, **kwargs)

        return method


class DocumentsListApplication(metaclass=Singleton):
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

        :param name:
        :param file_path:
        :param alias:
        :param plugin:
        """
        if name in self.documents.keys():
            raise Exception("Document %s was already registered by %s" % (name, self.documents[name].plugin.name))

        self.documents[name] = Document(name, file_path, alias, plugin)
        self.__log.debug("Document %s registered by %s" % (name, plugin.name))
        return self.documents[name]

    def get(self, document=None, plugin=None):
        """
        Get one or more documents.

        :param document: Name of the signal
        :type document: str
        :param plugin: Plugin object, under which the signals where registered
        :type plugin: GwPluginPattern
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
    :type plugin: GwPluginPattern
    """
    def __init__(self, name, file_path, alias, plugin, ):
        self.name = name
        self.file_path = file_path
        self.alias = alias
        self.plugin = plugin
        self.__log = logging.getLogger(__name__)
