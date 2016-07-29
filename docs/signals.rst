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
new user was created.

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
        def __init__(app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate():
            self.signals.register("my_signal", "this is my first signal")

You are able to get all signals, which were registered by you plugin by
using :func:`~groundwork.patterns.gw_base_pattern.SignalsPlugin.get`::

    ...
    def activate():
        self.signals.register("my_signal", "this is my first signal")
        my_signals = self.signals.get()                             # Returns a dictionary
        my_single_signal = self.signals.get(signal="my_signal")     # Return Signal or None

Send a signal
~~~~~~~~~~~~~
Sending a signal can be done by every plugin, even if it has not registered any signals or receivers.

However, a signal, which shall be send, must already be registered. Otherwise an exception is thrown.::

    ...
    def activate():
        self.signals.register(signal ="my_signal",
                              description="this is my first signal")

        self.signals.send("my_signal")  # Will work
        self.signals.send("not_registered__signal")  # Will throw an exception

.. note::
    Also the application can send signals by using :func:`class groundwork.signals.SignalsApplication.send`, like
    ``my_app.signals.send("my_signal", plugin=self)``.

Signals installed by groundwork
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Working with receivers
----------------------

Register a receiver
~~~~~~~~~~~~~~~~~~~

Unregister a receiver
~~~~~~~~~~~~~~~~~~~~~

Signals and receivers on application level
------------------------------------------
