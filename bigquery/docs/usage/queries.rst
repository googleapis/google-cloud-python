Running Queries
~~~~~~~~~~~~~~~

Querying data
^^^^^^^^^^^^^

Run a query and wait for it to finish with the
:func:`~google.cloud.bigquery.client.Client.query` method:

.. literalinclude:: ../samples/client_query.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query]
   :end-before: [END bigquery_query]


Run a query
^^^^^^^^^^^

Run a dry run query with the 
:func:`~google.cloud.bigquery.client.Client.query` method:
.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_dry_run]
   :end-before: [END bigquery_query_dry_run]

Run a query at a batch priority with the
:func:`~google.cloud.bigquery.client.Client.query` method:

.. literalinclude:: ../samples/client_query_batch.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_batch]
   :end-before: [END bigquery_query_batch]

Write a query results
^^^^^^^^^^^^^^^^^^^^^

See BigQuery documentation for more information on
`writing query results <https://cloud.google.com/bigquery/docs/writing-results>`_.

Write a query results to a destination table with the
:func:`~google.cloud.bigquery.client.Client.query` method:
.. literalinclude:: ../samples/client_query_destination_table.py
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
