How Code Generation Works
-------------------------

This page gives a brief decription of how *this* code generator works.
It is not intended to be the final treatise on how to write *any* code
generator. It is meant to be a reference for those who wish to contribute
to this effort, or to use it as a reference implementation.

There are two steps: a **parse** step which essentially involves reorganizing
data to make it more friendly to templates, and a **translation** step which
sends information about the API to templates, which ultimately write the
library.

The protoc contract
~~~~~~~~~~~~~~~~~~~

This code generator is written as a ``protoc`` plugin, which operates on
a defined contract. The contract is straightforward: a plugin must
accept a `CodeGeneratorRequest <plugin.proto>`_ (essentially a sequence of
`FileDescriptor <descriptor.proto>`_ objects) and output a
`CodeGeneratorResponse <plugin.proto>`_.

If you are unfamiliar with ``protoc`` plugins, welcome! That last paragraph
likely sounded not as straightforward as claimed. It may be useful to read
`plugin.proto`_ and `descriptor.proto`_ before continuing on. The former
describes the contract with plugins (such as this one) and is relatively
easy to digest, the latter describes protocol buffer files themselves and is
rather dense. The key point to grasp is that each ``.proto`` *file* compiles
into one of these proto messages (called *descriptors*), and this plugin's
job is to parse those descriptors.

That said, you should not need to know the ins and outs of the ``protoc``
contract model to be able to follow what this library is doing.

.. _plugin.proto: https://github.com/google/protobuf/blob/master/src/google/protobuf/compiler/plugin.proto
.. _descriptor.proto: https://github.com/google/protobuf/blob/master/src/google/protobuf/descriptor.proto


Entry Point
~~~~~~~~~~~

The entry point to this tool is ``api_factory/cli/generate.py``. The function
in this module is responsible for accepting CLI input, building the internal
API schema, and then rendering templates and using them to build a response
object.


Parse
~~~~~

As mentioned, this plugin is divided into two steps. The first step is
parsing. The guts of this is handled by the :class:`~.schema.api.API` object,
which is this plugin's internal representation of the full API client.

In particular, this class has a :meth:`~.schema.api.API.build` method which
accepts a sequence of `FileDescriptor`_ objects (remember, this is ``protoc``'s
internal representation of each proto file). That method iterates over each
file and creates a :class:`~.schema.api.Proto` object for each one.

.. note::

  An :class:`~.schema.api.API` object will not only be given the descriptors
  for the files you specify, but also all of their dependencies.
  ``protoc`` is smart enough to de-duplicate and send everything in the
  correct order.

The :class:`~.schema.api.API` object's primary purpose is to make sure all
the information from the proto files is in one place, and reasonably
accessible by `Jinja`_ templates (which by design are not allowed to call
arbitrary Python code). Mostly, it tries to avoid creating an entirely
duplicate structure, and simply wraps the descriptor representations.
However, some data needs to be moved around to get it into a structure
useful for templates (in particular, descriptors have an unfriendly approach
to sorting protobuf comments, and this parsing step places these back
alongside their referent objects).

The internal data model does use wrapper classes around most of the
descriptors, such as :class:`~.schema.wrappers.Service` and
:class:`~.schema.wrappers.MessageType`. These consistently contain their
original descriptor (which is always spelled with a ``_pb`` suffix, e.g.
the ``Service`` wrapper class has a ``service_pb`` instance variable).
These exist to handle bringing along additional relevant data (such as the
protobuf comments as mentioned above) and handling resolution of references
(for example, allowing a :class:`~.schema.wrappers.Method` to reference its
input and output types, rather than just the strings).

These wrapper classes follow a consistent structure:

* They define a ``__getattr__`` method that defaults to the wrapped
  desctiptor unless the wrapper itself provides something, making the wrappers
  themselves transparent to templates.
* They provide a ``meta`` attribute with metadata (package information and
  documentation). That means templates can consistently access the name
  for the module where an object can be found, or an object's documentation,
  in predictable and consistent places (``thing.meta.doc``, for example,
  prints the comments for ``thing``).

Translation
~~~~~~~~~~~

The translation step follows a straightfoward process to write the contents
of client library files.

First, it loads every template in the ``templates/`` directory.
These are `Jinja`_ templates. **There is no master list of templates**;
it is assumed that every template in this directory should be rendered
(unless its name begins with a single underscore).

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
* ``$name_$version`` is a special case: It is replaced with the client
  name, followed by the version. However, if there is no version, both it
  and the underscore are dropped.
* ``$service`` is replaced with the service name, converted to appropriate
  Python module case. There may be more than one service in an API; read on
  for more about this.

Every template receives **one** variable, spelled ``api``. It is the
:class:`~.schema.api.API` object that was pieced together in the parsing step.

There is one caveat to the above, which is that an API can have more than
one service. Therefore, templates with ``$service/`` in their name
are a special case. These files are rendered *once per service*, with the
``$service`` directory name changed to the name of the service itself
(in snake case, because this is Python). Additionally, these templates
receive two variables: the ``api`` variable discussed above, as well as a
variable spelled ``service``, which corresponds to the
:class:`~/schema.wrappers.Service` currently being iterated over.

.. note::

  The Jinja environment also receives a small number of filters useful
  for writing properly formatted templates (e.g. a ``snake_case`` filter);
  these are defined in :meth:`~.generator.generate` where the environment is
  created.

After all templates are processed, any files in the ``generator/files/``
directory are written. These are not templates, and they are read into
memory and eventually written with no processing whatsoever.

.. _Jinja: http://jinja.pocoo.org/docs/2.10/
