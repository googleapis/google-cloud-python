Getting Started
---------------

This code generator is implemented as a plugin to ``protoc``, the compiler
for `protocol buffers`_, and will run in any environment that Python 3.6+ and
protocol buffers do.

Because dependency management and such can be a significant undertaking, we
offer a Docker image and interface which requires you only to have Docker
installed and provide the protos for your API. Alternatively, the generator is
also invocable via bazel rules.

It is also possible to install the tool locally and run it through ``protoc``,
and this approach is fully supported.

.. note::

    The Docker approach is recommended for users new to this ecosystem, or
    those which do not have a robust Python environment available. If you want
    to experiment with generating client libraries but do not want to make
    changes to the generator itself, try the Docker image first.

    The bazel approach is recommended for established pipelines. It is more
    lightweight than the Docker image but may take some more effort to set up.

.. _protocol buffers: https://developers.google.com/protocol-buffers/

.. toctree::
   :maxdepth: 4

   docker
   local
   bazel
