Storage
=======

.. toctree::
  :maxdepth: 2
  :hidden:

  blobs
  buckets
  acl
  batch
  changelog

Installation
------------

Install the ``google-cloud-storage`` library using ``pip``:

.. code-block:: console

    $ pip install google-cloud-storage

Usage
-----

.. note::

   Becuase the :class:`~google.cloud.storage.client.Client` uses the
   third-party :mod:`requests` library by default, it should be safe to
   share instances across threads.  In multiprocessing scenarious, best
   practice is to create client instances *after*
   :class:`multiprocessing.Pool` or :class:`multiprocessing.Process` invokes
   :func:`os.fork`.

.. automodule:: google.cloud.storage.client
  :members:
  :show-inheritance:
