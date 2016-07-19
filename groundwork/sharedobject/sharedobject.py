class SharedObject:
    def __init__(self, name, shared_object, plugin_name, description=None):
        self.name = name
        self.description = description
        self.shared_object = shared_object
        self.plugin_name = plugin_name

