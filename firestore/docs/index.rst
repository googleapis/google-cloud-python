.. include:: README.rst

.. note::

   Because the firestore client uses :mod:`grpc` library and the third-party
   :mod:`requests` library, it is safe to share instances across threads.
   In multiprocessing scenarios, best practice is to create client instances *after*
   :class:`multiprocessing.Pool` or :class:`multiprocessing.Process` invokes
   :func:`os.fork`.

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
