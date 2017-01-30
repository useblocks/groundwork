from groundwork.patterns import GwDocumentsPattern, GwCommandsPattern

commands_content = """
Commands overview
=================

Registered commands: {{app.commands.get()|count}}

List of commands
----------------

 {% for name, command in app.commands.get().items() %}
 * {{command.command-}}
 {% endfor %}

{% for name, command in app.commands.get().items() %}
{{command.command}}
{{"-" * command.command|length}}
Name: {{command.command}}
Description: {{command.description}}
Plugin: {{command.plugin.name}}
{% endfor %}

"""


class GwCommandsInfo(GwDocumentsPattern, GwCommandsPattern):
    """
    Provides documents for giving an overview about registered commands.
    """
    # GwCommandsPatterns is not really needed for this plugin as parent class, because we do not register any command.
    # However, if no plugin does inherit from GwCommandsPattern the needed argument app.commands would not exist.
    # So this is the way to make sure that command-functionality was set up when this plugins gets used.
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(GwCommandsInfo, self).__init__(*args, **kwargs)

    def activate(self):
        self.documents.register(name="commands_overview",
                                content=commands_content,
                                description="Gives an overview about all registered commands")
