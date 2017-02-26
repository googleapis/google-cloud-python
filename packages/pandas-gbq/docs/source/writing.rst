.. _writer:

Writing DataFrames
==================

Assume we want to write a DataFrame ``df`` into a BigQuery table using :func:`~to_gbq`.

.. ipython:: python

   import pandas as pd
   df = pd.DataFrame({'my_string': list('abc'),
                      'my_int64': list(range(1, 4)),
                      'my_float64': np.arange(4.0, 7.0),
                      'my_bool1': [True, False, True],
                      'my_bool2': [False, True, False],
                      'my_dates': pd.date_range('now', periods=3)})

   df
   df.dtypes

.. code-block:: python

   to_gbq(df, 'my_dataset.my_table', projectid)

.. note::

   The destination table and destination dataset will automatically be created if they do not already exist.

The ``if_exists`` argument can be used to dictate whether to ``'fail'``, ``'replace'``
or ``'append'`` if the destination table already exists. The default value is ``'fail'``.

For example, assume that ``if_exists`` is set to ``'fail'``. The following snippet will raise
a ``TableCreationError`` if the destination table already exists.

.. code-block:: python

   to_gbq(df, 'my_dataset.my_table', projectid, if_exists='fail')

.. note::

   If the ``if_exists`` argument is set to ``'append'``, the destination dataframe will
   be written to the table using the defined table schema and column types. The
   dataframe must match the destination table in structure and data types.
   If the ``if_exists`` argument is set to ``'replace'``, and the existing table has a
   different schema, a delay of 2 minutes will be forced to ensure that the new schema
   has propagated in the Google environment. See
   `Google BigQuery issue 191 <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__.

Writing large DataFrames can result in errors due to size limitations being exceeded.
This can be avoided by setting the ``chunksize`` argument when calling :func:`~to_gbq`.
For example, the following writes ``df`` to a BigQuery table in batches of 10000 rows at a time:

.. code-block:: python

   to_gbq(df, 'my_dataset.my_table', projectid, chunksize=10000)

You can also see the progress of your post via the ``verbose`` flag which defaults to ``True``.
For example:

.. code-block:: python

   In [8]: to_gbq(df, 'my_dataset.my_table', projectid, chunksize=10000, verbose=True)

           Streaming Insert is 10% Complete
           Streaming Insert is 20% Complete
           Streaming Insert is 30% Complete
           Streaming Insert is 40% Complete
           Streaming Insert is 50% Complete
           Streaming Insert is 60% Complete
           Streaming Insert is 70% Complete
           Streaming Insert is 80% Complete
           Streaming Insert is 90% Complete
           Streaming Insert is 100% Complete

.. note::

   If an error occurs while streaming data to BigQuery, see
   `Troubleshooting BigQuery Errors <https://cloud.google.com/bigquery/troubleshooting-errors>`__.

.. note::

   The BigQuery SQL query language has some oddities, see the
   `BigQuery Query Reference Documentation <https://cloud.google.com/bigquery/query-reference>`__.

.. note::

   While BigQuery uses SQL-like syntax, it has some important differences from traditional
   databases both in functionality, API limitations (size and quantity of queries or uploads),
   and how Google charges for use of the service. You should refer to `Google BigQuery documentation <https://cloud.google.com/bigquery/what-is-bigquery>`__
   often as the service seems to be changing and evolving. BiqQuery is best for analyzing large
   sets of data quickly, but it is not a direct replacement for a transactional database.
