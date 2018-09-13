.. include:: /../bigquery/README.rst

Using the Library
=================

Projects
--------

A project is the top-level container in the ``BigQuery`` API:  it is tied
closely to billing, and can provide default access control across all its
datasets.  If no ``project`` is passed to the client container, the library
attempts to infer a project using the environment (including explicit
environment variables, GAE, and GCE).

To override the project inferred from the environment, pass an explicit
``project`` to the constructor, or to either of the alternative
``classmethod`` factories:

.. code-block:: python

   from google.cloud import bigquery
   client = bigquery.Client(project='PROJECT_ID')


Project ACLs
~~~~~~~~~~~~

Each project has an access control list granting reader / writer / owner
permission to one or more entities.  This list cannot be queried or set
via the API; it must be managed using the Google Developer Console.


Datasets
--------

A dataset represents a collection of tables, and applies several default
policies to tables as they are created:

- An access control list (ACL).  When created, a dataset has an ACL
  which maps to the ACL inherited from its project.

- A default table expiration period.  If set, tables created within the
  dataset will have the value as their expiration period.

See BigQuery documentation for more information on
`Datasets <https://cloud.google.com/bigquery/docs/datasets>`_.


Dataset operations
~~~~~~~~~~~~~~~~~~

List datasets for the client's project:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_datasets]
   :end-before: [END bigquery_list_datasets]

Create a new dataset for the client's project:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_dataset]
   :end-before: [END bigquery_create_dataset]

Refresh metadata for a dataset (to pick up changes made by another client):

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_get_dataset]
   :end-before: [END bigquery_get_dataset]

Update a property in a dataset's metadata:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_dataset_description]
   :end-before: [END bigquery_update_dataset_description]

Modify user permissions on a dataset:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_dataset_access]
   :end-before: [END bigquery_update_dataset_access]

Delete a dataset:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_delete_dataset]
   :end-before: [END bigquery_delete_dataset]


Tables
------

Tables exist within datasets. See BigQuery documentation for more information
on `Tables <https://cloud.google.com/bigquery/docs/tables>`_.

Table operations
~~~~~~~~~~~~~~~~
List tables for the dataset:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_tables]
   :end-before: [END bigquery_list_tables]

Create a table:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_table]
   :end-before: [END bigquery_create_table]

Get a table:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_get_table]
   :end-before: [END bigquery_get_table]

Update a property in a table's metadata:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_table_description]
   :end-before: [END bigquery_update_table_description]

Browse selected rows in a table:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_browse_table]
   :end-before: [END bigquery_browse_table]

Insert rows into a table's data:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_table_insert_rows]
   :end-before: [END bigquery_table_insert_rows]

Copy a table:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_copy_table]
   :end-before: [END bigquery_copy_table]

Extract a table to Google Cloud Storage:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_extract_table]
   :end-before: [END bigquery_extract_table]

Delete a table:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_delete_table]
   :end-before: [END bigquery_delete_table]

Upload table data from a file:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_from_file]
   :end-before: [END bigquery_load_from_file]

Load table data from Google Cloud Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See also: `Loading JSON data from Cloud Storage
<https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json>`_.

Load a CSV file from Cloud Storage:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_csv]
   :end-before: [END bigquery_load_table_gcs_csv]

Load a JSON file from Cloud Storage:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_json]
   :end-before: [END bigquery_load_table_gcs_json]

Load a Parquet file from Cloud Storage:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_parquet]
   :end-before: [END bigquery_load_table_gcs_parquet]

Customer Managed Encryption Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Table data is always encrypted at rest, but BigQuery also provides a way for
you to control what keys it uses to encrypt they data. See `Protecting data
with Cloud KMS keys
<https://cloud-dot-devsite.googleplex.com/bigquery/docs/customer-managed-encryption>`_
in the BigQuery documentation for more details.

Create a new table, using a customer-managed encryption key from
Cloud KMS to encrypt it.

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_table_cmek]
   :end-before: [END bigquery_create_table_cmek]

Change the key used to encrypt a table.

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_table_cmek]
   :end-before: [END bigquery_update_table_cmek]

Load a file from Cloud Storage, using a customer-managed encryption key from
Cloud KMS for the destination table.

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_gcs_json_cmek]
   :end-before: [END bigquery_load_table_gcs_json_cmek]

Copy a table, using a customer-managed encryption key from Cloud KMS for the
destination table.

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_copy_table_cmek]
   :end-before: [END bigquery_copy_table_cmek]

Write query results to a table, using a customer-managed encryption key from
Cloud KMS for the destination table.

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_destination_table_cmek]
   :end-before: [END bigquery_query_destination_table_cmek]

Queries
-------


Querying data
~~~~~~~~~~~~~

Run a query and wait for it to finish:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query]
   :end-before: [END bigquery_query]


Run a dry run query
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_dry_run]
   :end-before: [END bigquery_query_dry_run]


Writing query results to a destination table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See BigQuery documentation for more information on
`writing query results <https://cloud.google.com/bigquery/docs/writing-results>`_.

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_destination_table]
   :end-before: [END bigquery_query_destination_table]


Run a query using a named query parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See BigQuery documentation for more information on
`parameterized queries <https://cloud.google.com/bigquery/docs/parameterized-queries>`_.

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_params_named]
   :end-before: [END bigquery_query_params_named]


Jobs
----

List jobs for a project
~~~~~~~~~~~~~~~~~~~~~~~

Jobs describe actions performed on data in BigQuery tables:

- Load data into a table
- Run a query against data in one or more tables
- Extract data from a table
- Copy a table

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_jobs]
   :end-before: [END bigquery_list_jobs]


Using BigQuery with Pandas
--------------------------

Retrieve BigQuery data as a Pandas DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_query_results_dataframe]
   :end-before: [END bigquery_query_results_dataframe]

To retrieve table rows as a :class:`pandas.DataFrame`:

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_rows_dataframe]
   :end-before: [END bigquery_list_rows_dataframe]

Load a Pandas DataFrame to a BigQuery Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. literalinclude:: snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_load_table_dataframe]
   :end-before: [END bigquery_load_table_dataframe]

API Reference
=============

.. toctree::
  :maxdepth: 2

  reference
  dbapi

Changelog
=========

For a list of all ``google-cloud-bigquery`` releases:

.. toctree::
  :maxdepth: 2

  changelog

