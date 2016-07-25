import os
import inspect

from groundwork.patterns import GwCommandsPattern, GwDocumentsPattern


class GwCommandsInfo(GwDocumentsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.signals.connect(receiver="command_documentation",
                             signal="doc_fetch",
                             description="Used to generate a rst files for documenting all registered "
                                         "commands.",
                             function=self.document_command_list)

        self.documents.register("CommandList",
                                "/".join([os.path.dirname(__file__), "../../doc/plugins/command_list.rst"]))

    def document_command_list(self, plugin, **kwargs):
        command_list_file = open("/".join([os.path.dirname(__file__), "../../doc/plugins/command_list.rst"]), "w")
        command_list_file.write("Registered Commands\n")
        command_list_file.write("-------------------\n\n")
        command_list_file.write(".. contents:: \n\n")
        for key, command in self.app.commands.get().items():
            command_list_file.write("%s\n" % command.name)
            command_list_file.write("~" * len(command.name) + "\n")
            command_list_file.write("| **Command name**: %s\n" % command.name)
            command_list_file.write("| **Command plugin**: %s\n" % command.plugin.name)
            command_list_file.write("\n| **Command description**:\n")
            command_list_file.write("| %s\n\n" % command.description)
            if len(command.parameters) > 0:
                command_list_file.write("**Command parameters**:\n\n")
                for parameter in command.parameters:
                    command_list_file.write("* **%s** : %s " % (", ".join(parameter.opts), parameter.help))
                    flags = []
                    if parameter.required:
                        flags.append("Required")
                    if parameter.is_flag:
                            flags.append("Flag")
                    if len(flags) > 0:
                        command_list_file.write("(**%s**)" % ",".join(flags))
                    command_list_file.write("\n")
        command_list_file.close()
