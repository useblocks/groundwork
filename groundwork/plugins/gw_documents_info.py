import os
import sys
from jinja2 import Environment
from click import echo, prompt, Option, Argument
from docutils.core import publish_parts
from groundwork.patterns import GwDocumentsPattern, GwCommandsPattern

documents_content = """
Documents overview
==================

Registered documents: {{app.documents.get()|count}}

List of documents
------------------

 {% for name, document in app.documents.get().items() -%}
 * {{document.name}}
 {% endfor %}

{% for name, document in app.documents.get().items() %}
{{document.name}}
{{"-" * document.name|length}}
Name: {{document.name}}
Description: {{document.description}}
Plugin: {{document.plugin.name}}
{% endfor %}

"""


class GwDocumentsInfo(GwCommandsPattern, GwDocumentsPattern):
    """
    Provides a little documentation viewer for all registered documents.
    Accessible via **app doc**.

    Presents also an overview about all registered documents of an application.
    Accessible via **app doc_list**.
    """

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(GwDocumentsInfo, self).__init__(*args, **kwargs)

    def activate(self):
        """
        Activates GwDocumentsInfo by registering:

        * 2 commands (doc, doc_list)
        * 1 document (documents_overview)
        """
        self.commands.register("doc_list", "List all documents", self._list_documents)
        self.commands.register("doc", "Shows the documentation", self._show_documentation)
        self.commands.register("doc_write", "Stores documents as files ", self._store_documentation,
                               params=[Argument(("path",),
                                                required=True),
                                       Option(("--html", "-h"),
                                              required=False,
                                              help="Will output html instead of rst",
                                              default=False,
                                              is_flag=True),
                                       Option(("--overwrite", "-o"),
                                              required=False,
                                              help="Will overwrite existing files",
                                              default=False,
                                              is_flag=True),
                                       Option(("--quiet", "-q"),
                                              required=False,
                                              help="Will suppress any user interaction",
                                              default=False,
                                              is_flag=True)
                                       ])

        self.documents.register(name="documents_overview",
                                content=documents_content,
                                description="Gives an overview about all registered documents")

    def deactivate(self):
        pass

    def _list_documents(self):
        print("Documents:")
        for key, document in self.app.documents.get().items():
            print("  %s" % document.name)

    def _store_documentation(self, path, html, overwrite, quiet):
        """
        Stores all documents on the file system.

        Target location is **path**. File name is the lowercase name of the document + .rst.
        """

        echo("Storing groundwork application documents\n")
        echo("Application: %s" % self.app.name)
        echo("Number of documents: %s\n" % len(self.app.documents.get()))

        if not os.path.isabs(path):
            path = os.path.abspath(path)

        if not os.path.isdir(path):
            echo("Path %s is not a directory!" % path)
            sys.exit(1)

        if not os.path.exists(path):
            echo("Path %s does not exist" % path)
            sys.exit(1)

        for dirpath, dirnames, files in os.walk(path):
            if files:
                echo("Path %s is not empty!\n" % path)
                if not overwrite:
                    sys.exit(1)

        documents = []
        for key, document in self.app.documents.get().items():
            file_extension = ".html" if html else ".rst"

            # lowers the name, removes all whitespaces and adds the file extension
            file_name_parts = key.lower().split()
            file_name = "".join(file_name_parts)
            file_name += file_extension
            documents.append((file_name, document))

        echo("Going to write to following files:")
        for document in documents:
            echo("  %s" % document[0])

        echo("\nTarget directory: %s" % path)
        answer = None
        while answer not in ["N", "Y"] and not quiet:
            answer = prompt("Shall we go on? [Y]es, [N]o: ").upper()

        if answer == "N":
            sys.exit(0)

        for document in documents:
            try:
                with open(os.path.join(path, document[0]), "w") as doc_file:
                    doc_rendered = Environment().from_string(document[1].content).render(app=self.app,
                                                                                         plugin=document[1].plugin)
                    if html:
                        output = publish_parts(doc_rendered, writer_name="html")['whole']
                    else:
                        output = doc_rendered

                    doc_file.write(output)
            except Exception as e:
                echo("%s error occurred: %s" % (document[0], e))
            else:
                echo("%s stored." % document[0])

    def _show_documentation(self):
        """
        Shows all documents of the current groundwork app in the console.

        Documents are sorted bei its names, except "main", which gets set to the beginning.
        """
        documents = []
        for key, document in self.app.documents.get().items():
            if key != "main":
                documents.append((key, document))
        documents = sorted(documents, key=lambda x: x[0])
        main = self.app.documents.get("main")
        if main is not None:
            documents.insert(0, (main.name, main))

        user_answer = ""
        index = 0
        while user_answer != "X":
            if index < 0:
                index = 0
            if index > len(documents) - 1:
                index = len(documents) - 1
            document = documents[index][1]

            os.system('cls' if os.name == 'nt' else 'clear')
            echo(Environment().from_string(document.content).render(app=self.app, plugin=document.plugin))

            source = "This document is registered by '%s' under the name '%s'" % (document.plugin.name, document.name)
            echo("-" * len(source))
            echo(source)
            echo("-" * len(source))
            commands = "Actions: "
            if index < len(documents) - 1:
                commands += "[N]ext, "
            if index > 0:
                commands += "[P]revious, "
            commands += "E[x]it"
            echo(commands)

            if index < len(documents) - 1:
                default = "N"
            elif index > 0:
                default = "P"
            else:
                default = "X"
            user_answer = prompt("Select your action", default=default).upper()

            if user_answer == "N":
                index += 1
            elif user_answer == "P":
                index -= 1
