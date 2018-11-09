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

