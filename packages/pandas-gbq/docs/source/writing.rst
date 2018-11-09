.. _writer:

Writing DataFrames
==================

Assume we want to write a DataFrame ``df`` into a BigQuery table using
:func:`~pandas_gbq.to_gbq`.

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

   If the ``if_exists`` argument is set to ``'append'``, the destination
   dataframe will be written to the table using the defined table schema and
   column types. The dataframe must contain fields (matching name and type)
   currently in the destination table.

.. note::

   If an error occurs while streaming data to BigQuery, see
   `Troubleshooting BigQuery Errors <https://cloud.google.com/bigquery/troubleshooting-errors>`__.

.. note::

   While BigQuery uses SQL-like syntax, it has some important differences
   from traditional databases both in functionality, API limitations (size
   and quantity of queries or uploads), and how Google charges for use of the
   service. You should refer to `Google BigQuery documentation
   <https://cloud.google.com/bigquery/docs>`__ often as the service is always
   evolving. BiqQuery is best for analyzing large sets of data quickly, but
   it is not a direct replacement for a transactional database.
