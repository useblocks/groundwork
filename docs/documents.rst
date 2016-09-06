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
`Jinja <http://jinja.pocoo.org/>`_ and `rst <http://docutils.sourceforge.net/rst.html>`_ are powerful, wide used
and well documented libraries for creating intelligent and beautiful documents.

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

rst
~~~
`Restructured Text <http://docutils.sourceforge.net/rst.html>`_ is used to give your document some sort of a layout.
For instance add titles and chapters, make some words strong and add some links.

rst is so generic, that it can be used to build pdf documents, html webpages, epub (an ebook format) and much more.

A famous rst based documentation framework is `Sphinx <http://www.sphinx-doc.org/>`_

For a quick introduction, please read
`Quick reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_.


Developing a document viewer
----------------------------

A viewer for the groundwork documents must care about the following functions:

    1. Render the `Jinja <http://jinja.pocoo.org/>`_ template string.
    2. Transform rst-content to the needed output.

Step 1: Render Jinja
~~~~~~~~~~~~~~~~~~~~

Step 1 can be done using the Jinja template and its
`from_string() <http://jinja.pocoo.org/docs/dev/api/#jinja2.Environment.from_string>`_ command::

    from jinja2 import Environment

    ...  # App initialisation, plugin activation, ...

    document = my_app.documents.get("my example document")
    rendered_doc = Environment().from_string(document.content).render(app=my_app, plugin=document.plugin))

It is important to provide 2 parameters to the jinja template:

    * **app**: the current application object
    * **plugin**: the plugin, which has registered the current document

Step 2: Transform rst
~~~~~~~~~~~~~~~~~~~~~

The second step depends on the needed output format. You will find a wide range of rst supports for different
programming languages. A good starting point is a list of rst supporting libraries and tools in this
`stackoverflow answer <http://stackoverflow.com/questions/2746692/restructuredtext-tool-support>`_.

However, the following example will make *html* from an already rendered, rst structured document content::

    from docutils.core import publish_parts

    ...  # App initialisation, plugin activation, jinja rendering, ...

    output = publish_parts(rendered_doc, writer_name="html")['html_body']

``publish_parts()`` renders the rst string and provides several groups of html areas.
Based on this it is very easy to get the complete html tree or the body content only. Which would be really helpful,
if a document should be integrated into an already existing html frame.

Supported areas are: body_prefix, fragment, html_subtitle, header, version, meta, stylesheet, subtitle,
html_head, body_pre_docinfo, head, html_body, body, html_prolog, title, docinfo, html_title,
whole, body_suffix, head_prefix, footer, encoding.

For details of ``publish_parts()`` and its supported part names, please take a look into the
`official documentation <http://docutils.sourceforge.net/docs/api/publisher.html#publish-parts-details>`_.


Sphinx support
--------------

`Sphinx <http://www.sphinx-doc.org/>`_ is a documentation builder, which takes static, rst based files and generates
websites, PDFs and more out of it. For instance, this documentation is using sphinx.

As sphinx supports physical files on a hard disk only, it can not integrate with groundwork documents directly.

Luckily the groundwork plugin :class:`~groundwork.plugins.gw_documents_info.GwDocumentsInfo` provides the
command ``doc_write`` to store the content of all registered documents of an application in a directory.

Before it writes the files, the command will give you an overview about what will happen and asks for a final
confirmation.

Examples::

    # On a command line

    groundwork doc_write ../temp            # Writes rst documents to given, relative path.

    groundwork doc_write /home/user/temp    # Writes rst documents to the given, absolute path.

    groundwork doc_write ./temp -h          # Writes HTML documents.

    groundwork doc_write ./temp -o          # Does not exit, if given directory is not empty.

    groundwork doc_write ./temp -q          # Does not ask for final confirmation. Most needed by automation scripts.

    groundwork doc_write ./temp -o -q -h    # All options together...

After export, you can use the generated rst files as normal input files for sphinx. For instance you can add them
to a ``.. toctree::`` of your index.rst.

.. note::

    The output filename of a document is the document name in lowercase. Also all whitespaces are removed.
    For instance: "My Great Document" becomes "mygreatdocument.rst"



