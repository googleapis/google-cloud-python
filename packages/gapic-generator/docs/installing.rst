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
``protoc`` is also quirky about how it handles well-known protos; you probably
also want to copy them into ``/usr/local/include``

To ensure it is installed propertly:

.. code-block:: shell

  $ protoc --version
  libprotoc 3.6.0


pandoc
~~~~~~

This generator relies on `pandoc`_ to convert from Markdown (the *lingua
franca* for documentation in protocol buffers) into ReStructured Text (the
*lingua franca* for documentation in Python).

Install this using an appropriate mechanism for your operating system.
Multiple installation paths are documented on the `pandoc installation page`_.

.. _pandoc: https://pandoc.org/
.. _pandoc installation page: https://pandoc.org/installing.html


API Generator for Python
~~~~~~~~~~~~~~~~~~~~~~~~

This package is provided as a standard Python library, and can be installed
the usual ways. It fundamentally provides a CLI command,
``protoc-gen-pyclient``, so you will want to install using a mechanism
that is conducive to making CLI commands available.

Additionally, this program currently only runs against Python 3.6 or
Python 3.7, so you will need that installed. (Most Linux distributions ship
with earlier versions.) Use `pyenv`_ to get Python 3.7 installed in a
friendly way.

As for this library itself, the recommended installation approach is
`pipsi`_.

.. code-block:: shell

    # Due to its experimental state, this tool is not published to a
    # package manager; you should clone it.
    # (You can pip install it from GitHub, not not if you want to tinker.)
    git clone git@github.com:googleapis/gapic-generator-python.git
    cd gapic-generator-python/

    # Install the tool. This will handle the virtualenv for you, and
    # make an appropriately-aliased executable.
    # The `--editable` flag is only necessary if you want to work on the
    # tool (as opposed to just use it).
    pipsi install --editable --python=`which python3.7` .

To ensure the tool is installed properly:

.. code-block:: shell

  $ which protoc-gen-pyclient
  /path/to/protoc-gen-pyclient

.. _pyenv: https://github.com/pyenv/pyenv
.. _pipsi: https://github.com/mitsuhiko/pipsi
