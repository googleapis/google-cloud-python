Introduction
============

Supported Data Types
++++++++++++++++++++

Pandas supports all these `BigQuery data types <https://cloud.google.com/bigquery/data-types>`__:
``STRING``, ``INTEGER`` (64bit), ``FLOAT`` (64 bit), ``BOOLEAN`` and
``TIMESTAMP`` (microsecond precision). Data types ``BYTES`` and ``RECORD``
are not supported.

Integer and boolean ``NA`` handling
+++++++++++++++++++++++++++++++++++

Since all columns in BigQuery queries are nullable, and NumPy lacks of ``NA``
support for integer and boolean types, this module will store ``INTEGER`` or
``BOOLEAN`` columns with at least one ``NULL`` value as ``dtype=object``.
Otherwise those columns will be stored as ``dtype=int64`` or ``dtype=bool``
respectively.

This is opposite to default pandas behaviour which will promote integer
type to float in order to store NAs.
`See here for how this works in pandas <https://pandas.pydata.org/pandas-docs/stable/gotchas.html#nan-integer-na-values-and-na-type-promotions>`__

While this trade-off works well for most cases, it breaks down for storing
values greater than 2**53. Such values in BigQuery can represent identifiers
and unnoticed precision lost for identifier is what we want to avoid.

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
