.. include:: README.rst

.. note::

   Because this client uses :mod:`grpcio` library, it is safe to
   share instances across threads. In multiprocessing scenarios, the best
   practice is to create client instances *after* the invocation of
   :func:`os.fork` by :class:`multiprocessing.Pool` or
   :class:`multiprocessing.Process`.

Using the API
-------------
.. toctree::
   :maxdepth: 2

   usage


API Reference
-------------
.. toctree::
   :maxdepth: 2

   instance-api
   table-api
   data-api


Changelog
---------

For a list of all ``google-cloud-datastore`` releases:

.. toctree::
  :maxdepth: 2

  changelog
