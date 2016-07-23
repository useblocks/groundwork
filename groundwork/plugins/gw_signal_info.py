import os
import inspect

from groundwork.patterns import GwCommandsPattern, GwDocumentsPattern


class GwSignalInfo(GwCommandsPattern, GwDocumentsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("signal_list", "List of all signals", self.list_signals)
        self.commands.register("receiver_list", "List of all signal receivers", self.list_receivers)
        self.signals.connect(receiver="signal_documentation",
                             signal="doc_fetch",
                             description="Used to generate a rst files for documenting all registered "
                                         "signals.",
                             function=self.document_signal_list)

        self.signals.connect(receiver="receiver_documentation",
                             signal="doc_fetch",
                             description="Used to generate a rst file for documenting all registered "
                                         "receivers.",
                             function=self.document_receiver_list)

        self.documents.register("GwSignalInfo doc",
                                "/".join([os.path.dirname(__file__), "../../doc/plugins/signal_info.rst"]))

        self.documents.register("SignalList",
                                "/".join([os.path.dirname(__file__), "../../doc/plugins/signal_list.rst"]))

        self.documents.register("ReceiverList",
                                "/".join([os.path.dirname(__file__), "../../doc/plugins/receiver_list.rst"]))

    def list_signals(self):
        """
        Prints a list of all registered signals. Including description and plugin name.
        """
        print("Signal list")
        print("***********\n")
        for key, signal in self.app.signals.signals.items():
            print("%s (%s)\n  %s\n" % (signal.name, signal.plugin.name, signal.description))

    def list_receivers(self):
        """
        Prints a list of all registered receivers. Including signal, plugin name and description.
        """
        print("Receiver list")
        print("*************\n")
        for key, receiver in self.app.signals.receivers.items():
            print("%s <-- %s (%s):\n  %s\n" % (receiver.name,
                                               receiver.signal,
                                               receiver.plugin.name,
                                               receiver.description))

    def document_receiver_list(self, plugin, **kwargs):
        receiver_list_file = open("/".join([os.path.dirname(__file__), "../../doc/plugins/receiver_list.rst"]), "w")
        receiver_list_file.write("Registered Receivers\n")
        receiver_list_file.write("--------------------\n\n")
        receiver_list_file.write(".. contents:: \n\n")
        for key, receiver in self.app.signals.receivers.items():
            receiver_list_file.write("%s\n" % receiver.name)
            receiver_list_file.write("~" * len(receiver.name) + "\n")
            receiver_list_file.write("| **Receiver name**: %s\n" % receiver.name)
            receiver_list_file.write("| **Used signal**: %s\n" % receiver.signal)
            receiver_list_file.write("| **Receiver plugin**: %s\n" % receiver.plugin.name)
            receiver_list_file.write("\n| **Receiver description**:\n")
            receiver_list_file.write("| %s\n\n" % receiver.description)
        receiver_list_file.close()

    def document_signal_list(self, plugin, **kwargs):
        signals_list_file = open("/".join([os.path.dirname(__file__), "../../doc/plugins/signal_list.rst"]), "w")
        signals_list_file.write("Registered Signals\n")
        signals_list_file.write("--------------------\n\n")
        signals_list_file.write(".. contents:: \n\n")
        for key, signal in self.app.signals.signals.items():
            signals_list_file.write("%s\n" % signal.name)
            signals_list_file.write("~" * len(signal.name) + "\n")
            signals_list_file.write("| **Signal name**: %s\n" % signal.name)
            signals_list_file.write("| **Signal plugin**: %s\n" % signal.plugin.name)
            signals_list_file.write("\n| **Signal description**:\n")
            signals_list_file.write("| %s\n\n" % signal.description)
        signals_list_file.close()
