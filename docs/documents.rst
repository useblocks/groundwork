.. _documents:

Documents
=========

Documents are used to describe functions and usage of a plugin to an end-user.

Their output is independent, so that plugins can collect them and create documentations in different formats, like
console output, html pages or whatever is needed.

groundwork documents support `Jinja <http://jinja.pocoo.org/>`_ and `rst <http://docutils.sourceforge.net/rst.html>`_.
Based on this, they are not static and can be easily used to document
dynamic behaviors of an application. For instance to provide a list of available commands.

Live example
------------

groundwork provides an easy console viewer for its basic_app. It is part of the
:class:`~groundwork.plugins.gw_documents_info.GwDocumentsInfo` plugin.

After installation of groundwork, simply type the following in a console window::

    groundwork doc

Use **N** and **P** to navigate. **X** to quit.

Registration
------------

To register a document, a plugin must inherit from :class:`~groundwork.patterns.gw_documents_pattern.GwDocumentsPattern`
and call the :func:`~groundwork.patterns.gw_documents_pattern.DocumentsListPlugin.register` function::

    from groundwork.patterns import GwDocumentsPattern

    class My_Plugin(GwDocumentsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            my_content = """
            My Plugin
            =========

            Application name: {{app.name}}
            Plugin name: {{plugin.name}}
            """
            self.documents.register(name="my_document",
                                    content=my_content,
                                    description="Provides information about 'My Plugin'")

Unregister document
-------------------

To unregister a document, you must use
:func:`~groundwork.patterns.gw_documents_pattern.DocumentsListPlugin.unregister`::

    ...
    def deactivate(self):
        self.documents.unregister("my_document")

Using Jinja and RST
-------------------
`Jinja <http://jinja.pocoo.org/>`_ and `rst <http://docutils.sourceforge.net/rst.html>`_ are really powerful, wide used
and well documented. Therefore it is a big benefit use these techniques inside a documents content.

Jinja
~~~~~
`Jinja <http://jinja.pocoo.org/>`_ is template engine and allows a developer to use variables and loops inside
a text document (besides a lot of more awesome stuff).

groundwork provides the application object as ``app`` and the plugin object, which has registered the document, as
``plugin`` to each template::

    # JINJA template

    Application name: {{ app.name }}

    {% if app.plugins.get()|count > 5 %}
        Wohooow, we have a lot of plugins!
    {% else %}
        Ok, we have some plugins.
    {% endif %}

    {# get() provides a dict, so we use items() to iterate over it #}
    {% for key, plugin in app.plugins.get().items() %}
        name: plugin.name
    {% endfor %}

The template engine must be executed by the plugin, which provides a viewer to these documents. And the execution
should be done directly before the document gets presented to the user.

RST
~~~
`Restructured Text <http://docutils.sourceforge.net/rst.html>`_ is used to give your document some sort of a layout.
For instance add titles and chapters, make some words strong and add some links.

rst so so generic, that it can be used to build pdf documents, html webpages, epub (an ebook format) and much more.

A famous rst based documentation framework is `Sphinx <http://www.sphinx-doc.org/>`_

For a quick introduction, please read
`Quick reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_.
