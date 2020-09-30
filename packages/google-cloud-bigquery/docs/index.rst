.. include:: README.rst

.. note::

   Because the BigQuery client uses the third-party :mod:`requests` library
   by default and the BigQuery-Storage client uses :mod:`grpcio` library,
   both are safe to share instances across threads.  In multiprocessing
   scenarios, the best practice is to create client instances *after*
   :class:`multiprocessing.Pool` or :class:`multiprocessing.Process` invokes
   :func:`os.fork`.

More Examples
~~~~~~~~~~~~~

.. toctree::
  :maxdepth: 2

  usage/index
  Official Google BigQuery How-to Guides <https://cloud.google.com/bigquery/docs/how-to>

API Reference
-------------

.. toctree::
  :maxdepth: 2

  reference
  dbapi

Migration Guide
---------------

See the guide below for instructions on migrating to the 2.x release of this library.

.. toctree::
    :maxdepth: 2

    UPGRADING

Changelog
---------

For a list of all ``google-cloud-bigquery`` releases:

.. toctree::
  :maxdepth: 2

  changelog
