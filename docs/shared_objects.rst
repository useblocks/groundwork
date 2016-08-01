.. _shared_objects:

Shared Objects
==============

Shared objects are used to provide or access objects to or from other plugins.

As example, a plugin may be responsible for creating and updating users by setting up a database and make some tests
before any change happens. It could provide a shared object, which functions allow other plugins to create
users quite easily without the need to know all the details (database, tests, ...).

There are no restrictions for a shared object, it can be any python object.

.. note::

    As a shared object can be anything, you should be sure that this object is really good documented for other
    plugin developers.

    And if you access a shared object, you should also make some tests to guarantee that the shared object behaves
    like expected.

Registration
------------

Like for commands or signals, there is also a
:func:`~groundwork.patterns.gw_shared_objects_pattern.SharedObjectsListPlugin.register` function for shared objects::

    from groundwork.patterns import GwSharedObjectsPattern

    class MyPlugin(GwSharedObjectsPattern):
        def __init__(self, app, **kwargs)
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

            self.my_shared_object = {"name": "shared"
                                     "name2": "object"}

        def activate(self):
            self.shared_objects.register(name="my_shared_object",
                                         description="A shared object of My Plugin",
                                         obj=self.my_shared_object)


Get/Access a shared object
--------------------------

There are 2 functions, to access a shared object:
 * :func:`~groundwork.patterns.gw_shared_objects_pattern.SharedObjectsListPlugin.get`
 * :func:`~groundwork.patterns.gw_shared_objects_pattern.SharedObjectsListPlugin.access`

``get()`` returns the complete shared object including registered meta data like name, description and plugin.
It may also return a dictionary of shared objects, if no name was given.
The search is performed on plugin level only, so there is no possibility to access shared objects of other plugins
via ``get()``

``access()`` returns the object only, without any meta data. It can be used to access a single shared object only.
A **name** must be given and the search is performed on application level.::

    from groundwork.patterns import GwSharedObjectsPattern

    class MyPlugin(GwSharedObjectsPattern):
        ...

        def activate(self):
            self.shared_objects.register(name="my_shared_object",
                                         description="A shared object of My Plugin",
                                         obj=self.my_shared_object)

    class MyPlugin2(GwSharedObjectsPattern):
        ...

        def some_function(self):
            # Will work
            obj = self.shared_objects.access("my_shared_object")

            # The following will not work as "my_shared_object" was not registered by this plugin
            # get() only works on plugin level!
            shared_object = self.shared_objects.get("my_shared_object")

            # But if access to shared object meta data is needed, you can use the application to get it.
            shared_object = self.app.shared_objects.get(name="my_shared_object")
            obj = shared_object.obj

Unregister
----------
Use :func:`~groundwork.patterns.gw_shared_objects_pattern.SharedObjectsListPlugin.unregister` to unregister a
shared object::

    ...
    def deactivate(self):
        self.shared_objects.unregister("my_shared_object")

.. warning::
    Unregistration of a shared object may be tricky, as other plugins may have already stored a reference to this
    object. Therefore as a plugin developer do not store an external shared object in your own plugin class. Try to
    safely request it via :func:`~groundwork.patterns.gw_shared_objects_pattern.SharedObjectsListPlugin.access`
    every time you need access on it.
