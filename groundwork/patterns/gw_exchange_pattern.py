import logging

from groundwork.patterns.gw_plugin_pattern import GwPluginPattern

from groundwork.sharedobject import SharedObject


class GwExchangePattern(GwPluginPattern):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self.app, "exchange"):
            self.app.exchange = ExchangeListApplication(self.app)
        self.exchange = ExchangeListPlugin(self)

    def activate(self):
        pass

    def deactivate(self):
        pass


class ExchangeListPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log
        self.log.info("Plugin exchange initialised")

    def register(self, name, description, obj):
        return self.app.exchange.register(name, description, obj, self.plugin)

    def get(self, name=None):
        return self.app.exchange.get(name, self.plugin)

    def __getattr__(self, item):
        """
        Catches unknown function/attribute calls and delegates them to ExchangeListApplication
        """

        def method(*args, **kwargs):
            func = getattr(self.app.exchange, item, None)
            if func is None:
                raise AttributeError("ExchangeList does not have an attribute called %s" % item)
            return func(*args, plugin=self.plugin, **kwargs)

        return method


class ExchangeListApplication():
    def __init__(self, app):
        self.app = app
        self.log = app.log
        self._exchange = {}
        self.log.info("Application exchange initialised")

    def get(self, name=None, plugin=None):
        if plugin is not None:
            if name is None:
                exchange_list = {}
                for key in self._exchange.keys():
                    if self._exchange[key].plugin == plugin:
                        exchange_list[key] = self._exchange[key]
                return exchange_list
            else:
                if name in self._exchange.keys():
                    if self._exchange[name].plugin == plugin:
                        return self._exchange[name]
                    else:
                        return None
                else:
                    return None
        else:
            if name is None:
                return self._exchange
            else:
                if name in self._exchange.keys():
                    return self._exchange[name]
                else:
                    return None

    def register(self, name, description, obj, plugin):
        if name in self._exchange.keys():
            raise ExchangeExistException("Exchange %s already registered by %s" % (name,
                                                                                   self._exchange[name].plugin.name))

        new_exchange = Exchange(name, description, obj, plugin)
        self._exchange[name] = new_exchange
        self.log.debug("Exchange registered: %s" % name)
        return new_exchange


class Exchange:
    def __init__(self, name, description, obj, plugin):
        self.name = name
        self.description = description
        self.obj = obj
        self.plugin = plugin


class ExchangeExistException(BaseException):
    pass
