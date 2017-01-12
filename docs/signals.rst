.. _signals:

Signals and Receivers
=====================

Signals and receivers are used to loosely connect plugins. Every plugin can register and send signals.
And every plugin can register a receiver for a specific signal.

A signal is defined by its unique name and should have a meaningful description.

A receiver is connected to a specific signal and is defined additionally by an unique name, a function
and a description.

groundwork also stores the plugin, which has registered a signal or a receiver.

.. note::
    groundwork is internally using the library `Blinker <https://pythonhosted.org/blinker/>`_ and made most
    of its functions available.


Use case: User creation
-----------------------

Let's imagine we have 3 active plugins:

 * **GwUserManager** - For creating users in database
 * **GwEMail** - For sending e-mails
 * **GwChat** - For sending chat messages

If a user gets created, the GwUSerManager sends the signal "User created" and adds the created user object.

Both, GwEMail and GwChat, have registered receivers to the signal "User created". So GwEMail gets called, it fetches
the e-mail address from the attached user object and sends a "Welcome" message to the user.
GwChat gets also called and send a chat message to the chat room of the development team and informs them, that a
new user has been created.

Working with signals
--------------------

Signals and receivers can be used inside plugins, without the need of using any specific pattern.
As groundwork itself uses signals for some internal processes, signals and receivers are already part of
:class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`.

Register a signal
~~~~~~~~~~~~~~~~~

To register a signal, simply use the :func:`~groundwork.patterns.gw_base_pattern.SignalsPlugin.register` function
of self.signals::

    from grundwork.patters import GwBasePattern

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            self.signals.register("my_signal", "this is my first signal")

You are able to get all signals, which were registered by you plugin by
using :func:`~groundwork.patterns.gw_base_pattern.SignalsPlugin.get`::

    ...
    def activate(self):
        self.signals.register("my_signal", "this is my first signal")
        my_signals = self.signals.get()                             # Returns a dictionary
        my_single_signal = self.signals.get(signal="my_signal")     # Return Signal or None

Send a signal
~~~~~~~~~~~~~
Sending a signal can be done by every plugin, even if it has not registered any signals or receivers.

However, a signal, which shall be send, must already be registered. Otherwise an exception is thrown.::

    ...
    def activate(self):
        self.signals.register(signal ="my_signal",
                              description="this is my first signal")

        self.signals.send("my_signal")  # Will work
        self.signals.send("not_registered__signal")  # Will throw an exception

.. note::
    Also the application can send signals by using :func:`~groundwork.signals.SignalsApplication.send`, like
    ``my_app.signals.send("my_signal", plugin=self)``.

Signals installed by groundwork
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
groundwork installs 4 signals during start up:

 * plugin_activate_pre
 * plugin_activate_post
 * plugin_deactivate_pre
 * plugin_activate_post

This signals are called automatically if a plugin gets activated or deactivated.

The difference between **pre** and **post** is that **pre** is called before any action is done by the plugin.
And **post** is called after the plugin did some action for de/activation.

.. _receivers:

Working with receivers
----------------------
Any plugin can register a receiver for any signal. Even if the signal itself will never be send or even registered.

Register a receiver
~~~~~~~~~~~~~~~~~~~

To register a receiver, a callback function is needed, which gets executed, if the receiver gets called.

Registration of receiver is done by the function :func:`~groundwork.patterns.gw_base_pattern.SignalsPlugin.connect`::

    from grundwork.patters import GwBasePattern

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            self.signals.connect(receiver="My signal receiver",
                                 signal="My signal",
                                 function=self.fancy_stuff,
                                 description="Doing some fancy")

        def fancy_stuff(plugin, **kwargs):
            print("FANCY STUFF!!! " * 50)


The used function must accept as first parameter the sender/plugin, which send the signal.
After this multiple, optional keyword arguments must be accepted as well.

The parameter **sender** can be used during registration, do receive signals only from specific senders/plugins.

Best practice: Pattern clean up
'''''''''''''''''''''''''''''''

Lets say, a pattern provides a function to register web-routes. During activation, the plugin registers some of them.
But during deactivation is forgets to unregister them, so that they are still registered and available.

The pattern should register to **plugin_deactivate_post** and make sure, that everything gets unregistered.

Example::

    class GwWebPattern(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.signals.connect(receiver="%s_web_route_deactivation" % self.name,
                                 signal="plugin_deactivate_post",
                                 function=self.__deactivate_commands,
                                 description="Deactivate commands for %s" % self.name,
                                 sender=self)    # We only need signals from this plugin

        def __deactivate_web_routes(self, plugin, *args, **kwargs):
            web_routes = self.web_routes.get()
            for web_route in web_routes.keys():
                self.web_routes.unregister(web_route)

Unregister a receiver
~~~~~~~~~~~~~~~~~~~~~
To disconnect a receiver from a signal, use the :func:`~groundwork.patterns.gw_base_pattern.SignalsPlugin.disconnect`
function::

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            self.signals.connect(receiver="%s_my_deactivation" % self.name, ... )

        def deactivate(self):
            self.signals.disconnect("%s_my_deactivation" % self.name)


Signals and receivers on application level
------------------------------------------

All signals and receivers can be accessed on application level via
:func:`~groundwork.signals.SignalsApplication.get`::

    from groundwork import App

    my_app = App()
    my_app.signals.register("app_signal", "signal from application", plugin=app)
    signals = my_app.signals.get()

It is also possible to register new signals and receivers. But inside the application an additional parameter
called **plugin** is necessary.
This parameter gets set automatically inside plugins. However on application level this must be set by
the developer.
