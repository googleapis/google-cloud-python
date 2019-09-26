.. include:: README.rst

.. note::

   Because the firestore client uses :mod:`grpcio` library, it is safe to
   share instances across threads. In multiprocessing scenarios, the best
   practice is to create client instances *after* the invocation of
   :func:`os.fork` by :class:`multiprocessing.Pool` or
   :class:`multiprocessing.Process`.

API Reference
-------------

.. toctree::
  :maxdepth: 2

  client
  collection
  document
  field_path
  query
  batch
  transaction
  transforms
  types


Changelog
---------

For a list of all ``google-cloud-firestore`` releases:

.. toctree::
  :maxdepth: 2

  changelog
