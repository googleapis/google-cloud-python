IPython Magics for BigQuery
===========================

To use these magics, you must first register them. Run the ``%load_ext`` magic
in a Jupyter notebook cell.

.. code::

    %load_ext bigquery_magics

This makes the ``%%bigquery`` and ``%%bqsql`` magics available.

Code Samples
------------

Running a query:

.. literalinclude:: ../samples/snippets/query.py
   :dedent: 4
   :start-after: [START bigquery_jupyter_query]
   :end-before: [END bigquery_jupyter_query]

Running a parameterized query:

.. literalinclude:: ../samples/snippets/query_params_scalars.py
   :dedent: 4
   :start-after: [START bigquery_jupyter_query_params_scalars]
   :end-before: [END bigquery_jupyter_query_params_scalars]

API Reference
-------------

.. automodule:: bigquery_magics.bigquery
    :members:

Configuration
~~~~~~~~~~~~~

.. automodule:: bigquery_magics.config
    :members:
