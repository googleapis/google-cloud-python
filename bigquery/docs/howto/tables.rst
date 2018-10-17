Tables
~~~~~~

Tables exist within datasets. See BigQuery documentation for more information
on `Tables <https://cloud.google.com/bigquery/docs/tables>`_.

Table operations
^^^^^^^^^^^^^^^^
List tables for the dataset:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_tables]
   :end-before: [END bigquery_list_tables]

Create a table:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_table]
   :end-before: [END bigquery_create_table]

Get a table:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_get_table]
   :end-before: [END bigquery_get_table]

Update a property in a table's metadata:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_table_description]
   :end-before: [END bigquery_update_table_description]

Browse selected rows in a table:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_browse_table]
   :end-before: [END bigquery_browse_table]

Insert rows into a table's data:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_table_insert_rows]
   :end-before: [END bigquery_table_insert_rows]

Copy a table:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_copy_table]
   :end-before: [END bigquery_copy_table]

Extract a table to Google Cloud Storage:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_extract_table]
   :end-before: [END bigquery_extract_table]

Delete a table:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_delete_table]
   :end-before: [END bigquery_delete_table]

Upload table data from a file:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_from_file]
   :end-before: [END bigquery_load_from_file]

Load table data from Google Cloud Storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See also: `Loading JSON data from Cloud Storage
<https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json>`_.

Load a CSV file from Cloud Storage:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_csv]
   :end-before: [END bigquery_load_table_gcs_csv]

Load a JSON file from Cloud Storage:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_json]
   :end-before: [END bigquery_load_table_gcs_json]

Load a Parquet file from Cloud Storage:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_parquet]
   :end-before: [END bigquery_load_table_gcs_parquet]

Customer Managed Encryption Keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Table data is always encrypted at rest, but BigQuery also provides a way for
you to control what keys it uses to encrypt they data. See `Protecting data
with Cloud KMS keys
<https://cloud-dot-devsite.googleplex.com/bigquery/docs/customer-managed-encryption>`_
in the BigQuery documentation for more details.

Create a new table, using a customer-managed encryption key from
Cloud KMS to encrypt it.

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_table_cmek]
   :end-before: [END bigquery_create_table_cmek]

Change the key used to encrypt a table.

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_table_cmek]
   :end-before: [END bigquery_update_table_cmek]

Load a file from Cloud Storage, using a customer-managed encryption key from
Cloud KMS for the destination table.

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_json_cmek]
   :end-before: [END bigquery_load_table_gcs_json_cmek]

Copy a table, using a customer-managed encryption key from Cloud KMS for the
destination table.

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_copy_table_cmek]
   :end-before: [END bigquery_copy_table_cmek]

Write query results to a table, using a customer-managed encryption key from
Cloud KMS for the destination table.

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_destination_table_cmek]
   :end-before: [END bigquery_query_destination_table_cmek]
