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

.. _plugin.proto: https://github.com/google/protobuf/blob/master/src/google/protobuf/compiler/plugin.proto
.. _descriptor.proto: https://github.com/google/protobuf/blob/master/src/google/protobuf/descriptor.proto

Parse
~~~~~

As mentioned, this plugin is divided into two steps. The first step is
parsing. The guts of this is handled by the :class:`~.schema.api.API` object,
which is this plugin's internal representation of the full API client.

In particular, this class has a :meth:`~.schema.api.API.load` method which
accepts a `FileDescriptor`_ (remember, this is ``protoc``'s internal
representation of each proto file). The method is called once for each proto
file you send to be compiled as well as each dependency. (``protoc`` itself
is smart enough to de-duplicate and send everything in the right order.)

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
  documentation).

Translation
~~~~~~~~~~~

The translation step follows a straightfoward process to write the contents
of client library files.

First, it loads every template in the ``generator/templates/`` directory.
These are `Jinja`_ templates. There is no master list of templates;
it is assumed that every template in this directory should be rendered
(unless its name begins with an underscore), and that the name of the
resulting file should be the same as the template's file name with the
``.j2`` suffix truncated.

Every template receives **one** variable, spelled ``api``. It is the
:class:`~.schema.api.API` object that was pieced together in the parsing step.

There is one caveat to the above, which is that an API can have more than
one service. Therefore, the ``generator/templates/service/`` directory
is a special case. These files are rendered *once per service*, with the
``service`` directory name changed to the name of the service itself
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
