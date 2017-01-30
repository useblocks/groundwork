from groundwork.patterns import GwCommandsPattern, GwDocumentsPattern

signal_content = """
Signal overview
===============

Registered signals: {{app.signals.get()|count}}

List of signals
---------------

 {% for name, signal in app.signals.get().items() %}
 * {{signal.name-}}
 {% endfor %}

{% for name, signal in app.signals.get().items() %}
{{signal.name}}
{{"-" * signal.name|length}}
Name: {{signal.name}}
Description: {{signal.description}}
Plugin: {{signal.plugin.name}}
{% endfor %}

"""

receiver_content = """
Receiver overview
=================

Registered receivers: {{app.signals.get_receiver()|count}}

List of receivers
-----------------

 {% for name, receiver in app.signals.get_receiver().items() %}
 * {{receiver.name-}}
 {% endfor %}

{% for name, receiver in app.signals.get_receiver().items() %}
{{receiver.name}}
{{"-" * receiver.name|length}}
Name: {{receiver.name}}
Description: {{receiver.description}}
Plugin: {{receiver.plugin.name}}
Signal: {{receiver.signal}}
Sender: {{receiver.sender.name}}
Function: {{receiver.function.__name__}} from {{receiver.function.__self__.__class__.__name__}}
{% endfor %}

"""


class GwSignalsInfo(GwCommandsPattern, GwDocumentsPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(GwSignalsInfo, self).__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("signal_list", "List of all signals", self.list_signals)
        self.commands.register("receiver_list", "List of all signal receivers", self.list_receivers)

        self.documents.register(name="signals_overview",
                                content=signal_content,
                                description="Gives an overview about all registered signals")

        self.documents.register(name="receivers_overview",
                                content=receiver_content,
                                description="Gives an overview about all registered receivers")

    def deactivate(self):
        pass

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
