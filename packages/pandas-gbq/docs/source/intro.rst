Introduction
============

Supported Data Types
++++++++++++++++++++

Pandas supports all these `BigQuery data types <https://cloud.google.com/bigquery/data-types>`__:
``STRING``, ``INTEGER`` (64bit), ``FLOAT`` (64 bit), ``BOOLEAN`` and
``TIMESTAMP`` (microsecond precision). Data types ``BYTES`` and ``RECORD``
are not supported.

Logging
+++++++

Because some requests take some time, this library will log its progress of
longer queries. IPython & Jupyter by default attach a handler to the logger.
If you're running in another process and want to see logs, or you want to see
more verbose logs, you can do something like:

.. code-block:: ipython

   import logging
   import sys
   logger = logging.getLogger('pandas_gbq')
   logger.setLevel(logging.DEBUG)
   logger.addHandler(logging.StreamHandler(stream=sys.stdout))
