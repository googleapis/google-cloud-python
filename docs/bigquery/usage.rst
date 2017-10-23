BigQuery
========

.. toctree::
  :maxdepth: 2
  :hidden:

  client
  dataset
  job
  query
  schema
  table

Authentication / Configuration
------------------------------

- Use :class:`Client <google.cloud.bigquery.client.Client>` objects to configure
  your applications.

- :class:`Client <google.cloud.bigquery.client.Client>` objects hold both a ``project``
  and an authenticated connection to the BigQuery service.

- The authentication credentials can be implicitly determined from the
  environment or directly via
  :meth:`from_service_account_json <google.cloud.bigquery.client.Client.from_service_account_json>`
  and
  :meth:`from_service_account_p12 <google.cloud.bigquery.client.Client.from_service_account_p12>`.

- After setting :envvar:`GOOGLE_APPLICATION_CREDENTIALS` and
  :envvar:`GOOGLE_CLOUD_PROJECT` environment variables, create an instance of
  :class:`Client <google.cloud.bigquery.client.Client>`.

  .. code-block:: python

     >>> from google.cloud import bigquery
     >>> client = bigquery.Client()


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

   >>> from google.cloud import bigquery
   >>> client = bigquery.Client(project='PROJECT_ID')


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
   :start-after: [START client_list_datasets]
   :end-before: [END client_list_datasets]

Create a new dataset for the client's project:

.. literalinclude:: snippets.py
   :start-after: [START create_dataset]
   :end-before: [END create_dataset]

Refresh metadata for a dataset (to pick up changes made by another client):

.. literalinclude:: snippets.py
   :start-after: [START get_dataset]
   :end-before: [END get_dataset]

Update a property in a dataset's metadata:

.. literalinclude:: snippets.py
   :start-after: [START update_dataset_simple]
   :end-before: [END update_dataset_simple]

Update multiple properties in a dataset's metadata:

.. literalinclude:: snippets.py
   :start-after: [START update_dataset_multiple_properties]
   :end-before: [END update_dataset_multiple_properties]

Delete a dataset:

.. literalinclude:: snippets.py
   :start-after: [START delete_dataset]
   :end-before: [END delete_dataset]


Tables
------

Tables exist within datasets. See BigQuery documentation for more information
on `Tables <https://cloud.google.com/bigquery/docs/tables>`_.

Table operations
~~~~~~~~~~~~~~~~~~
List tables for the dataset:

.. literalinclude:: snippets.py
   :start-after: [START list_dataset_tables]
   :end-before: [END list_dataset_tables]

Create a table:

.. literalinclude:: snippets.py
   :start-after: [START create_table]
   :end-before: [END create_table]

Get a table:

.. literalinclude:: snippets.py
   :start-after: [START get_table]
   :end-before: [END get_table]

Update a property in a table's metadata:

.. literalinclude:: snippets.py
   :start-after: [START update_table_simple]
   :end-before: [END update_table_simple]

Update multiple properties in a table's metadata:

.. literalinclude:: snippets.py
   :start-after: [START update_table_multiple_properties]
   :end-before: [END update_table_multiple_properties]

Get rows from a table's data:

.. literalinclude:: snippets.py
   :start-after: [START table_list_rows]
   :end-before: [END table_list_rows]

Utilize iterator properties returned with row data:

.. literalinclude:: snippets.py
   :start-after: [START table_list_rows_iterator_properties]
   :end-before: [END table_list_rows_iterator_properties]

Insert rows into a table's data:

.. literalinclude:: snippets.py
   :start-after: [START table_create_rows]
   :end-before: [END table_create_rows]

Upload table data from a file:

.. literalinclude:: snippets.py
   :start-after: [START load_table_from_file]
   :end-before: [END load_table_from_file]

Load table data from Google Cloud Storage:

.. literalinclude:: snippets.py
   :start-after: [START load_table_from_uri]
   :end-before: [END load_table_from_uri]

Copy a table:

.. literalinclude:: snippets.py
   :start-after: [START copy_table]
   :end-before: [END copy_table]

Extract a table to Google Cloud Storage:

.. literalinclude:: snippets.py
   :start-after: [START extract_table]
   :end-before: [END extract_table]

Delete a table:

.. literalinclude:: snippets.py
   :start-after: [START delete_table]
   :end-before: [END delete_table]


Queries
-------

Querying data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: snippets.py
   :start-after: [START client_query]
   :end-before: [END client_query]

.. note::

  - Use of the ``timeout`` parameter is optional. The query will continue to
    run in the background even if it takes longer the timeout allowed.


Run a query using a named query parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See BigQuery documentation for more information on
`parameterized queries <https://cloud.google.com/bigquery/docs/parameterized-queries>`_.

.. literalinclude:: snippets.py
  :start-after: [START client_query_w_param]
  :end-before: [END client_query_w_param]


Querying Table Rows
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run a query and wait for it to finish:

.. literalinclude:: snippets.py
   :start-after: [START client_query_rows]
   :end-before: [END client_query_rows]

.. note::

  - Use of the ``timeout`` parameter is optional. The query will continue to
    run in the background even if it takes longer the timeout allowed. The job
    may be retrieved using the job ID via
    :meth:`~google.cloud.bigquery.client.Client.get_job`


List jobs for a project
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jobs describe actions performed on data in BigQuery tables:

- Load data into a table
- Run a query against data in one or more tables
- Extract data from a table
- Copy a table

.. literalinclude:: snippets.py
   :start-after: [START client_list_jobs]
   :end-before: [END client_list_jobs]
