Running Queries
~~~~~~~~~~~~~~~

Querying data
^^^^^^^^^^^^^

Run a query and wait for it to finish:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query]
   :end-before: [END bigquery_query]


Run a dry run query
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_dry_run]
   :end-before: [END bigquery_query_dry_run]


Writing query results to a destination table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See BigQuery documentation for more information on
`writing query results <https://cloud.google.com/bigquery/docs/writing-results>`_.

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_destination_table]
   :end-before: [END bigquery_query_destination_table]


Run a query using a named query parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See BigQuery documentation for more information on
`parameterized queries <https://cloud.google.com/bigquery/docs/parameterized-queries>`_.

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_params_named]
   :end-before: [END bigquery_query_params_named]
