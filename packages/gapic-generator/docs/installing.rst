Installing
----------

protoc
~~~~~~

This tool is implemented as a plugin to the `protocol buffers`_ compiler, so
in order to use it, you will need to have the ``protoc`` command available.

The `release page`_ on GitHub contains the download you need.

.. note::

  You may notice both packages that designate languages (e.g.
  ``protobuf-python-X.Y.Z.tar.gz``) as well as packages that
  designate architectures (e.g. ``protoc-X.Y.Z-linux-x86_64.zip``). You want
  the one that designates an architecture; your goal here is to have a CLI
  command.

.. _protocol buffers: https://developers.google.com/protocol-buffers/
.. _release page: https://github.com/google/protobuf/releases

It is likely preferable to install ``protoc`` somewhere on your shell's path,
but this is not a strict requirement (as you will be invoking it directly).

To ensure it is installed propertly:

.. code-block:: shell

  $ protoc --version
  libprotoc 3.5.1


API Generator for Python
~~~~~~~~~~~~~~~~~~~~~~~~

This package is provided as a standard Python library, and can be installed
the usual ways. It fundamentally provides a CLI command,
``protoc-gen-pyclient``, so you will want to install using a mechanism
that is conducive to making CLI commands available.

Additionally, this program currently only runs against Python 3.6, so you
will need that installed. (Most Linux distributions ship with earlier
versions.) Use `pyenv`_ to get Python 3.6 installed in a friendly way.

As for this library itself, the recommended installation approach is
`pipsi`_.

.. code-block:: shell

    # Due to its experimental state, this tool is not published to a
    # package manager, and pip can not install from git-on-borg;
    # you should clone it.
    git clone sso://team/apiclient-eng/python-client-generator
    cd python-client-generator/

    # Install the tool. This will handle the virtualenv for you, and
    # make an appropriately-aliased executable.
    # The `--editable` flag is only necessary if you want to work on the
    # tool (as opposed to just use it).
    pipsi install --editable --python=`which python3.6` .

To ensure the tool is installed properly:

.. code-block:: shell

  $ which protoc-gen-pyclient
  /path/to/protoc-gen-pyclient

.. _pyenv: https://github.com/pyenv/pyenv
.. _pipsi: https://github.com/mitsuhiko/pipsi
