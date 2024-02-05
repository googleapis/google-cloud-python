:orphan:

.. _docker-shortcut:

Docker Shortcut Script
----------------------

Because code generation requires two mounts from the host machine into
the Docker image, and because the paths are somewhat pedantic, you may
find this shortcut script to be handy:

.. literalinclude:: ../../gapic.sh
    :language: shell

Place it somewhere on your system, marked executable.

Once available, it can be invoked using:

.. code-block:: shell

    # This is assumed to be from the "proto root" directory.
    $ gapic.sh --image gcr.io/gapic-images/gapic-generator-python \
        --in path/to/src/protos/
        --out dest/


It will work not only with the Python code generator, but all of our code
generators that implement this Docker interface.
