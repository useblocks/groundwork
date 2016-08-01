import os
from jinja2 import Environment
from click import echo, prompt
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
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        """
        Activates GwDocumentsInfo by registering:

        * 2 commands (doc, doc_list)
        * 1 document (documents_overview)
        """
        self.commands.register("doc_list", "List all documents", self._list_documents)
        self.commands.register("doc", "Shows the documentation", self._show_documentation)

        self.documents.register(name="documents_overview",
                                content=documents_content,
                                description="Gives an overview about all registered documents")

    def _list_documents(self):
        for key, document in self.app.documents.get().items():
            print("Documents:")
            print("  %s" % document.name)

    def _show_documentation(self):
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
            if index > len(documents)-1:
                index = len(documents)-1
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










