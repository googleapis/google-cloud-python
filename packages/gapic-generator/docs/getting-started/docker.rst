.. _getting-started/docker:

Docker Image
============

If you are just getting started with code generation for protobuf-based APIs,
or if you do not have a robust Python environment already available, we
recommend using our `Docker`_ image to build client libraries.

However, this tool offers first-class support for local execution using
protoc: :ref:`getting-started/local`. It is still reasonably easy, but
initial setup will take a bit longer.

.. note::

    If you are interested in contributing, using a local installation
    is recommended.

.. _Docker: https://docker.com/


Installing
----------

Docker
~~~~~~

In order to use a Docker image, you must have `Docker`_ installed.
Docker is a container management service, and is available on Linux, Mac,
and Windows (although most of these instructions will be biased toward
Linux and Mac).

Install Docker according to their `installation instructions`_.

.. note::

    This image requires Docker 17.05 or later.

.. _installation instructions: https://docs.docker.com/install/

Pull the Docker Image
~~~~~~~~~~~~~~~~~~~~~

Once Docker is installed, simply pull the Docker image for this tool:

.. parsed-literal::

    $ docker pull gcr.io/gapic-images/gapic-generator-python:\ |version|\


Usage
-----

.. include:: _usage_intro.rst

Example
~~~~~~~

.. include:: _example.rst


Compiling an API
~~~~~~~~~~~~~~~~

.. note::

    If you are running code generation repeatedly, executing the
    long ``docker run`` command may be cumbersome. While you should ensure
    you understand this section, a :ref:`shortcut script<docker-shortcut>`
    is available to make iterative work easier.

Compile the API into a client library by invoking the Docker image.

It is worth noting that the image must interact with the host machine
(your local machine) for two things: reading in the protos you wish to compile,
and writing the output. This means that when you run the image, two mount
points are required in order for anything useful to happen.

In particular, the input protos are expected to be mounted into ``/in/``,
and the desired output location is expected to be mounted into ``/out/``.
The output directory must also be writable.

.. note::

    The ``/in/`` and ``/out/`` directories inside the image are
    hard-coded; they can not be altered where they appear in the command
    below.

Perform that step with ``docker run``:

.. code-block:: shell

    # This is assumed to be run from the `googleapis` project root.
    $ docker run \
      --mount type=bind,source=google/cloud/vision/v1/,destination=/in/google/cloud/vision/v1/,readonly \
      --mount type=bind,source=dest/,destination=/out/ \
      --rm \
      --user $UID \
      gcr.io/gapic-images/gapic-generator-python

.. warning::

    ``protoc`` is *very* picky about paths, and the exact construction here
    matters a lot. The source is ``google/cloud/vision/v1/``, and then
    the destination is that full directory path after the ``/in/`` root;
    therefore: ``/in/google/cloud/vision/v1/``.

    This matters because of how proto imports are resolved. The ``import``
    statement imports a *file*, relative to a base directory or set of
    base directories, called the ``proto_path``. This is assumed
    (and hard-coded) to ``/in/`` in the Docker image, and so any directory
    structure present in the imports of the proto files must be preserved
    beneath this for compilation to succeed.


.. include:: _verifying.rst
