Managing Tables
~~~~~~~~~~~~~~~

Tables exist within datasets. See BigQuery documentation for more information
on `Tables <https://cloud.google.com/bigquery/docs/tables>`_.

Listing Tables
^^^^^^^^^^^^^^

List the tables belonging to a dataset with the
:func:`~google.cloud.bigquery.client.Client.list_tables` method:

.. literalinclude:: ../samples/list_tables.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_tables]
   :end-before: [END bigquery_list_tables]

Getting a Table
^^^^^^^^^^^^^^^

Get a table resource with the
:func:`~google.cloud.bigquery.client.Client.get_table` method:

.. literalinclude:: ../samples/get_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_get_table]
   :end-before: [END bigquery_get_table]

Determine if a table exists with the
:func:`~google.cloud.bigquery.client.Client.get_table` method:

.. literalinclude:: ../samples/table_exists.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_table_exists]
   :end-before: [END bigquery_table_exists]

Browse data rows in a table with the
:func:`~google.cloud.bigquery.client.Client.list_rows` method:

.. literalinclude:: ../samples/browse_table_data.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_browse_table]
   :end-before: [END bigquery_browse_table]

Creating a Table
^^^^^^^^^^^^^^^^

Create an empty table with the
:func:`~google.cloud.bigquery.client.Client.create_table` method:

.. literalinclude:: ../samples/create_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_table]
   :end-before: [END bigquery_create_table]

Load table data from a file with the
:func:`~google.cloud.bigquery.client.Client.load_table_from_file` method:

.. literalinclude:: ../samples/load_table_from_file.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_from_file]
   :end-before: [END bigquery_load_from_file]

Load a CSV file from Cloud Storage with the
:func:`~google.cloud.bigquery.client.Client.load_table_from_uri` method:

.. literalinclude:: ../samples/load_table_from_uri_csv.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_csv]
   :end-before: [END bigquery_load_table_gcs_csv]

See also: `Loading CSV data from Cloud Storage
<https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv>`_.

Load a JSON file from Cloud Storage:

.. literalinclude:: ../samples/load_table_from_uri_json.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_json]
   :end-before: [END bigquery_load_table_gcs_json]

See also: `Loading JSON data from Cloud Storage
<https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json>`_.

Load a Parquet file from Cloud Storage:

.. literalinclude:: ../samples/load_table_from_uri_parquet.py
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

.. literalinclude:: ../samples/update_table_description.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_table_description]
   :end-before: [END bigquery_update_table_description]

Insert rows into a table's data with the
:func:`~google.cloud.bigquery.client.Client.insert_rows` method:

.. literalinclude:: ../samples/table_insert_rows.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_table_insert_rows]
   :end-before: [END bigquery_table_insert_rows]

Adds an empty column to the existing table with the
:func:`~google.cloud.bigquery.update_table` method:

.. literalinclude:: ../samples/add_empty_column.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_add_empty_column]
   :end-before: [END bigquery_add_empty_column]

Copying a Table
^^^^^^^^^^^^^^^

Copy a table with the
:func:`~google.cloud.bigquery.client.Client.copy_table` method:

.. literalinclude:: ../samples/copy_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_copy_table]
   :end-before: [END bigquery_copy_table]

Copy a table with CMEK with the
:func:`~google.cloud.bigquery.client.Client.copy_table` method:

.. literalinclude:: ../samples/copy_table_cmek.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_copy_table_cmek]
   :end-before: [END bigquery_copy_table_cmek]

Copy table data to Google Cloud Storage with the
:func:`~google.cloud.bigquery.client.Client.extract_table` method:

.. literalinclude:: ../samples/extract_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_extract_table]
   :end-before: [END bigquery_extract_table]

Deleting a Table
^^^^^^^^^^^^^^^^

Delete a table with the
:func:`~google.cloud.bigquery.client.Client.delete_table` method:

.. literalinclude:: ../samples/delete_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_delete_table]
   :end-before: [END bigquery_delete_table]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_list_jobs.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_jobs]
   :end-before: [END bigquery_list_jobs]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query]
   :end-before: [END bigquery_query]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_add_column.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_add_column_query_append]
   :end-before: [END bigquery_add_column_query_append]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_batch.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_batch]
   :end-before: [END bigquery_query_batch]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_destination_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_destination_table]
   :end-before: [END bigquery_query_destination_table]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_destination_table_cmek.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_destination_table_cmek]
   :end-before: [END bigquery_query_destination_table_cmek]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_destination_table_legacy.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_legacy_large_results]
   :end-before: [END bigquery_query_legacy_large_results]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_dry_run.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_dry_run]
   :end-before: [END bigquery_query_dry_run]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_relax_column.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_relax_column_query_append]
   :end-before: [END bigquery_relax_column_query_append]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_total_rows.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_total_rows]
   :end-before: [END bigquery_query_total_rows]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_w_array_params.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_params_arrays]
   :end-before: [END bigquery_query_params_arrays]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_w_named_params.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_params_named]
   :end-before: [END bigquery_query_params_named]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_w_positional_params.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_params_positional]
   :end-before: [END bigquery_query_params_positional]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_w_struct_params.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_params_structs]
   :end-before: [END bigquery_query_params_structs]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/client_query_w_timestamp_params.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_params_timestamps]
   :end-before: [END bigquery_query_params_timestamps]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/copy_table_multiple_source.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_copy_table_multiple_source]
   :end-before: [END bigquery_copy_table_multiple_source]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/create_client_default_credentials.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_client_default_credentials]
   :end-before: [END bigquery_client_default_credentials]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/create_partitioned_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_table_partitioned]
   :end-before: [END bigquery_create_table_partitioned]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/create_table_cmek.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_table_cmek]
   :end-before: [END bigquery_create_table_cmek]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/create_table_nested_repeated_schema.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_nested_repeated_schema]
   :end-before: [END bigquery_nested_repeated_schema]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/ddl_create_view.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_ddl_create_view]
   :end-before: [END bigquery_ddl_create_view]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/extract_table_compressed.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_extract_table_compressed]
   :end-before: [END bigquery_extract_table_compressed]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/extract_table_json.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_extract_table_json]
   :end-before: [END bigquery_extract_table_json]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/list_rows_as_dataframe.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_rows_dataframe]
   :end-before: [END bigquery_list_rows_dataframe]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/load_and_query_partitioned_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_partitioned_table]
   :end-before: [END bigquery_query_partitioned_table]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/load_table_add_column.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_add_column_load_append]
   :end-before: [END bigquery_add_column_load_append]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/load_table_from_dataframe.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_dataframe]
   :end-before: [END bigquery_load_table_dataframe]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/load_table_from_uri_autodetect.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_json_autodetect]
   :end-before: [END bigquery_load_table_gcs_json_autodetect]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/load_table_from_uri_avro.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_avro]
   :end-before: [END bigquery_load_table_gcs_avro]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/load_table_from_uri_cmek.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_json_cmek]
   :end-before: [END bigquery_load_table_gcs_json_cmek]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/load_table_from_uri_orc.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_orc]
   :end-before: [END bigquery_load_table_gcs_orc]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/load_table_from_uri_truncate.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_orc_truncate]
   :end-before: [END bigquery_load_table_gcs_orc_truncate]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/load_table_relax_column.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_relax_column_load_append]
   :end-before: [END bigquery_relax_column_load_append]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/manage_job.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_get_job]
   :end-before: [END bigquery_get_job]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/manage_table_labels.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_delete_label_table]
   :end-before: [END bigquery_delete_label_table]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/manage_views.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_grant_view_access]
   :end-before: [END bigquery_grant_view_access]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/query_external_gcs_permanent_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_external_gcs_perm]
   :end-before: [END bigquery_query_external_gcs_perm]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/query_external_gcs_temporary_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_external_gcs_temp]
   :end-before: [END bigquery_query_external_gcs_temp]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/query_external_sheets_permanent_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_external_sheets_perm]
   :end-before: [END bigquery_query_external_sheets_perm]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/query_external_sheets_temporary_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_auth_drive_scope]
   :end-before: [END bigquery_auth_drive_scope]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/query_no_cache.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_no_cache]
   :end-before: [END bigquery_query_no_cache]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/query_results_as_dataframe.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_results_dataframe]
   :end-before: [END bigquery_query_results_dataframe]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/undelete_table.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_undelete_table]
   :end-before: [END bigquery_undelete_table]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/update_table_cmek.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_table_cmek]
   :end-before: [END bigquery_update_table_cmek]

[-REPLACE_COMMENT-]
:func:`~google.cloud.bigquery.[-REPLACE_METHOD-]` method:

.. literalinclude:: ../samples/update_table_expiration.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_table_expiration]
   :end-before: [END bigquery_update_table_expiration]
