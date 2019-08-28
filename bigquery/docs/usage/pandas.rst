Using BigQuery with Pandas
~~~~~~~~~~~~~~~~~~~~~~~~~~

Retrieve BigQuery data as a Pandas DataFrame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As of version 0.29.0, you can use the
:func:`~google.cloud.bigquery.table.RowIterator.to_dataframe` function to
retrieve query results or table rows as a :class:`pandas.DataFrame`.

First, ensure that the :mod:`pandas` library is installed by running:

.. code-block:: bash

   pip install --upgrade pandas

Alternatively, you can install the BigQuery python client library with
:mod:`pandas` by running:

.. code-block:: bash

   pip install --upgrade google-cloud-bigquery[pandas]

To retrieve query results as a :class:`pandas.DataFrame`:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_results_dataframe]
   :end-before: [END bigquery_query_results_dataframe]

To retrieve table rows as a :class:`pandas.DataFrame`:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_rows_dataframe]
   :end-before: [END bigquery_list_rows_dataframe]

Load a Pandas DataFrame to a BigQuery Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As of version 1.3.0, you can use the
:func:`~google.cloud.bigquery.client.Client.load_table_from_dataframe` function
to load data from a :class:`pandas.DataFrame` to a
:class:`~google.cloud.bigquery.table.Table`. To use this function, in addition
to :mod:`pandas`, you will need to install the :mod:`pyarrow` library. You can
install the BigQuery python client library with :mod:`pandas` and
:mod:`pyarrow` by running:

.. code-block:: bash

   pip install --upgrade google-cloud-bigquery[pandas,pyarrow]

The following example demonstrates how to create a :class:`pandas.DataFrame`
and load it into a new table:

.. literalinclude:: ../samples/load_table_dataframe.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_dataframe]
   :end-before: [END bigquery_load_table_dataframe]
