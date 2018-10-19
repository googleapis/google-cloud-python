Managing Tables
~~~~~~~~~~~~~~~

Tables exist within datasets. See BigQuery documentation for more information
on `Tables <https://cloud.google.com/bigquery/docs/tables>`_.

Listing Tables
^^^^^^^^^^^^^^

List the tables belonging to a dataset with the
:func:`~google.cloud.bigquery.client.Client.list_tables` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_tables]
   :end-before: [END bigquery_list_tables]

Getting a Table
^^^^^^^^^^^^^^^

Get a table resource with the
:func:`~google.cloud.bigquery.client.Client.get_table` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_get_table]
   :end-before: [END bigquery_get_table]

Browse data rows in a table with the
:func:`~google.cloud.bigquery.client.Client.list_rows` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_browse_table]
   :end-before: [END bigquery_browse_table]

Creating a Table
^^^^^^^^^^^^^^^^

Create an empty table with the
:func:`~google.cloud.bigquery.client.Client.create_table` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_table]
   :end-before: [END bigquery_create_table]

Load table data from a file with the
:func:`~google.cloud.bigquery.client.Client.load_table_from_file` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_from_file]
   :end-before: [END bigquery_load_from_file]

Load a CSV file from Cloud Storage with the
:func:`~google.cloud.bigquery.client.Client.load_table_from_uri` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_csv]
   :end-before: [END bigquery_load_table_gcs_csv]

See also: `Loading CSV data from Cloud Storage
<https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv>`_.

Load a JSON file from Cloud Storage:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_json]
   :end-before: [END bigquery_load_table_gcs_json]

See also: `Loading JSON data from Cloud Storage
<https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json>`_.

Load a Parquet file from Cloud Storage:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_parquet]
   :end-before: [END bigquery_load_table_gcs_parquet]

See also: `Loading Parquet data from Cloud Storage
<https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet>`_.

Updating a Table
^^^^^^^^^^^^^^^^

Update a property in a table's metadata with the
:func:`~google.cloud.bigquery.client.Client.update_table` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_table_description]
   :end-before: [END bigquery_update_table_description]

Insert rows into a table's data with the
:func:`~google.cloud.bigquery.client.Client.insert_rows` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_table_insert_rows]
   :end-before: [END bigquery_table_insert_rows]

Copying a Table
^^^^^^^^^^^^^^^

Copy a table with the
:func:`~google.cloud.bigquery.client.Client.copy_table` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_copy_table]
   :end-before: [END bigquery_copy_table]

Copy table data to Google Cloud Storage with the
:func:`~google.cloud.bigquery.client.Client.extract_table` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_extract_table]
   :end-before: [END bigquery_extract_table]

Deleting a Table
^^^^^^^^^^^^^^^^

Delete a table with the
:func:`~google.cloud.bigquery.client.Client.delete_table` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_delete_table]
   :end-before: [END bigquery_delete_table]
