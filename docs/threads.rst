.. _threads:

Threads
=======

Threads are used to allow functions to run in background and in parallel to the application, so that these functions
do not block the execution of the app.

This is very helpful when you have long-running tasks (e.g. file operations) but your app must still be able to response
to user input very quickly (like a running webserver).

Registering threads
-------------------

To register threads, a plugin must inherit from :class:`~groundwork.patterns.gw_threads_pattern.GwThreadsPattern`
and use the function :func:`~groundwork.patterns.gw_threads_pattern.ThreadsListPlugin.register`. ::

    from groundwork.patterns import GwThreadsPattern

    class MyPlugin(GwThreadsPattern):
        def __init__(self, app, **kwargs)
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            my_thread = self.threads.register(name="my_thread",
                                              description="run something",
                                              function=self.my_thread)

            my_thread.run()

        def my_thread(self, plugin, **kwargs):
            print("Yehaaa")

The registered function must have two arguments: ``self`` and ``plugin``.

As the function gets not executed in the context of the plugin class, but in the context of a threading class,
``self`` can not help to get access to your plugin.

Therefore we need the argument ``plugin``, which contains the plugin, which has registered the thread.


Thread status and response
--------------------------

Because threads are running in parallel to the normal execution, you can not simply catch the response value of
``my_thread.run()``. Following code does **not** work::

    response = my_thread.run()   # response will be None, because my_thread is still running

Instead you have to wait and monitor the thread by your own::

    while my_thread.running:
        pass  # Do nothing
    response = my_thread.response

But again, this code would block your application.

Another approach would be to let your thread-function send a :ref:`signal <signals>` as last action.
Now you are able to define a :ref:`receiver <receivers>`, which can catch the response.



