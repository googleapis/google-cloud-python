Templates
---------

This page provides a description of templates: how to write them, what
variables they receive, and so on and so forth.

In many cases, it should be possible to provide alternative Python libraries
based on protocol buffers by only editing templates (or authoring new ones),
with no requirement to alter the primary codebase itself.

Jinja
~~~~~

All templates are implemented in `Jinja`_, Armin Ronacher's excellent
templating library for Python. This document assumes that you are already
familiar with the basics of writing Jinja templates, and does not seek to
cover that here.


Locating Templates
~~~~~~~~~~~~~~~~~~

Templates are included in output simply on the basis that they exist.
**There is no master list of templates**; it is assumed that every template
should be rendered (unless its name begins with a single underscore).

The name of the output file is based on the name of the template, with
the following string replacements applied:

* The ``.j2`` suffix is removed.
* ``$namespace`` is replaced with the namespace specified in the client,
  converted to appropriate Python module case. If there is no namespace,
  this segment is dropped. If the namespace has more than one element,
  this is expanded out in the directory structure. (For example, a namespace
  of ``['Acme', 'Manufacturing']`` will translate into ``acme/manufacturing/``
  directories.)
* ``$name`` is replaced with the client name. This is expected to be
  present.
* ``$version`` is replaced with the client version (the version of the API).
  If there is no specified version, this is dropped.
* ``$service`` is replaced with the service name, converted to appropriate
  Python module case. There may be more than one service in an API; read on
  for more about this.

.. note::

    ``$name_$version`` is a special case: It is replaced with the client
    name, followed by the version. However, if there is no version, both it
    and the underscore are dropped.

Context (Variables)
~~~~~~~~~~~~~~~~~~~

Every template receives **one** variable, spelled ``api``. It is the
:class:`~.schema.api.API` object that was pieced together in the parsing step.

APIs can (and often do) have more than one service. Therefore, templates
with ``$service/`` in their name are a special case. These files are
rendered *once per service*, with the ``$service`` directory name changed to
the name of the service itself (in snake case, because this is Python).
Additionally, these templates receive two variables: the ``api`` variable
discussed above, as well as a variable spelled ``service``, which corresponds
to the :class:`~.schema.wrappers.Service` currently being iterated over.


Filters
~~~~~~~

Additionally, templates receive a limited number of filters useful for
writing properly formatted templates.

These are:

* ``snake_case`` (:meth:`~.utils.case.to_snake_case`): Converts a string in
  any sane case system to snake case.
* ``wrap`` (:meth:`~.utils.lines.wrap`): Wraps arbitrary text. Keyword
  arguments on this method such as ``offset`` and ``indent`` should make it
  relatively easy to take an arbitrary string and make it wrap to 79
  characters appropriately.

.. _Jinja: http://jinja.pocoo.org/docs/2.10/
