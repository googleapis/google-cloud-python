.. _create_tables:

Creating Tables
===============

.. code-block:: ipython

   In [10]: gbq.generate_bq_schema(df, default_type='STRING')

   Out[10]: {'fields': [{'name': 'my_bool1', 'type': 'BOOLEAN'},
            {'name': 'my_bool2', 'type': 'BOOLEAN'},
            {'name': 'my_dates', 'type': 'TIMESTAMP'},
            {'name': 'my_float64', 'type': 'FLOAT'},
            {'name': 'my_int64', 'type': 'INTEGER'},
            {'name': 'my_string', 'type': 'STRING'}]}

.. note::

   If you delete and re-create a BigQuery table with the same name, but different table schema,
   you must wait 2 minutes before streaming data into the table. As a workaround, consider creating
   the new table with a different name. Refer to
   `Google BigQuery issue 191 <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__.
