API
===

Application Object
------------------
.. currentmodule:: groundwork

.. autoclass:: App
   :members:
   :inherited-members:
   :undoc-members:


PluginManagers
--------------
There are two manager classes for managing plugin related objects.

 * PluginManager: Cares about initialised Plugins, which can be activate and deactivate.
 * PluginClassManager: Cares about plugin classes, which are used to create plugins.

A plugin class can be reused for several plugins. The only thing to care about is the naming of a plugin.
This plugin name must be unique inside an groundwork app and can be set during plugin initialisation/activation.

.. currentmodule:: groundwork.pluginmanager

PluginManager
~~~~~~~~~~~~~

.. autoclass:: PluginManager
   :members:
   :inherited-members:
   :undoc-members:
   :private-members:

PluginClassManager
~~~~~~~~~~~~~~~~~~

.. autoclass:: PluginClassManager
   :members:
   :inherited-members:
   :undoc-members:
   :private-members:

Plugin Patterns
---------------
.. currentmodule:: groundwork.patterns

GwPluginPattern
~~~~~~~~~~~~~~~

.. autoclass:: GwPluginPattern
   :members:
   :inherited-members:
   :undoc-members:

GwCommandPattern
~~~~~~~~~~~~~~~~~

.. autoclass:: GwCommandsPattern
   :members:
   :inherited-members:
   :undoc-members:

GwExchangePattern
~~~~~~~~~~~~~~~~~

.. autoclass:: GwExchangePattern
   :members:
   :inherited-members:
   :undoc-members:

Plugins
-------
.. currentmodule:: groundwork.plugins

GwPluginInfo
~~~~~~~~~~~~

.. autoclass:: GwPluginInfo
   :members:
   :inherited-members:
   :undoc-members:
