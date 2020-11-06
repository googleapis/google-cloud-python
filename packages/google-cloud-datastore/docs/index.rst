.. include:: README.rst

.. note::

   Because the Datastore client uses the :mod:`grpcio` library by default
   and uses third-party :mod:`requests` library if the GRPC is disabled,
   clients are safe to share instances across threads.  In multiprocessing
   scenarios, the best practice is to create client instances *after*
   :class:`multiprocessing.Pool` or :class:`multiprocessing.Process` invokes
   :func:`os.fork`.

API Reference
-------------
.. toctree::
  :maxdepth: 2

  client
  entities
  keys
  queries
  transactions
  batches
  helpers
  admin_client

Migration Guide
---------------

See the guide below for instructions on migrating to the 2.x release of this library.

.. toctree::
    :maxdepth: 2

    UPGRADING

Changelog
---------

For a list of all ``google-cloud-datastore`` releases:

.. toctree::
  :maxdepth: 2

  changelog
