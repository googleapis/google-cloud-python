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
via the API:  it must be managed using the Google Developer Console.


Datasets
--------

A dataset represents a collection of tables, and applies several default
policies to tables as they are created:

- An access control list (ACL).  When created, a dataset has an ACL
  which maps to the ACL inherited from its project.

- A default table expiration period.  If set, tables created within the
  dataset will have the value as their expiration period.


Dataset operations
~~~~~~~~~~~~~~~~~~

List datasets for the client's project:

.. literalinclude:: snippets.py
   :start-after: [START client_list_datasets]
   :end-before: [END client_list_datasets]

Create a new dataset for the client's project:

.. literalinclude:: snippets.py
   :start-after: [START dataset_create]
   :end-before: [END dataset_create]

Check for the existence of a dataset:

.. literalinclude:: snippets.py
   :start-after: [START dataset_exists]
   :end-before: [END dataset_exists]

Refresh metadata for a dataset (to pick up changes made by another client):

.. literalinclude:: snippets.py
   :start-after: [START dataset_reload]
   :end-before: [END dataset_reload]

Patch metadata for a dataset:

.. literalinclude:: snippets.py
   :start-after: [START dataset_patch]
   :end-before: [END dataset_patch]

Replace the ACL for a dataset, and update all writeable fields:

.. code-block:: python

   >>> from google.cloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.get()  # API request
   >>> acl = list(dataset.acl)
   >>> acl.append(bigquery.Access(role='READER', entity_type='domain', entity='example.com'))
   >>> dataset.acl = acl
   >>> dataset.update()  # API request

Delete a dataset:

.. literalinclude:: snippets.py
   :start-after: [START dataset_delete]
   :end-before: [END dataset_delete]


Tables
------

Tables exist within datasets.  List tables for the dataset:

.. literalinclude:: snippets.py
   :start-after: [START dataset_list_tables]
   :end-before: [END dataset_list_tables]

Create a table:

.. literalinclude:: snippets.py
   :start-after: [START table_create]
   :end-before: [END table_create]

Check for the existence of a table:

.. literalinclude:: snippets.py
   :start-after: [START table_exists]
   :end-before: [END table_exists]

Refresh metadata for a table (to pick up changes made by another client):

.. literalinclude:: snippets.py
   :start-after: [START table_reload]
   :end-before: [END table_reload]

Patch specific properties for a table:

.. literalinclude:: snippets.py
   :start-after: [START table_patch]
   :end-before: [END table_patch]

Update all writable metadata for a table

.. literalinclude:: snippets.py
   :start-after: [START table_update]
   :end-before: [END table_update]

Get rows from a table's data:

.. literalinclude:: snippets.py
   :start-after: [START table_fetch_data]
   :end-before: [END table_fetch_data]

Insert rows into a table's data:

.. literalinclude:: snippets.py
   :start-after: [START table_insert_data]
   :end-before: [END table_insert_data]

Upload table data from a file:

.. literalinclude:: snippets.py
   :start-after: [START table_upload_from_file]
   :end-before: [END table_upload_from_file]

Delete a table:

.. literalinclude:: snippets.py
   :start-after: [START table_delete]
   :end-before: [END table_delete]


Jobs
----

Jobs describe actions peformed on data in BigQuery tables:

- Load data into a table
- Run a query against data in one or more tables
- Extract data from a table
- Copy a table

List jobs for a project:

.. literalinclude:: snippets.py
   :start-after: [START client_list_jobs]
   :end-before: [END client_list_jobs]


Querying data (synchronous)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run a query which can be expected to complete within bounded time:

.. literalinclude:: snippets.py
   :start-after: [START client_run_sync_query]
   :end-before: [END client_run_sync_query]

Run a query using a named query parameter:

.. literalinclude:: snippets.py
   :start-after: [START client_run_sync_query_w_param]
   :end-before: [END client_run_sync_query_w_param]

If the rows returned by the query do not fit into the initial response,
then we need to fetch the remaining rows via
:meth:`~google.cloud.bigquery.query.QueryResults.fetch_data`:

.. literalinclude:: snippets.py
   :start-after: [START client_run_sync_query_paged]
   :end-before: [END client_run_sync_query_paged]

If the query takes longer than the timeout allowed, ``query.complete``
will be ``False``.  In that case, we need to poll the associated job until
it is done, and then fetch the results:

.. literalinclude:: snippets.py
   :start-after: [START client_run_sync_query_timeout]
   :end-before: [END client_run_sync_query_timeout]


Querying data (asynchronous)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Background a query, loading the results into a table:

.. code-block:: python

   >>> from google.cloud import bigquery
   >>> client = bigquery.Client()
   >>> query = """\
   SELECT firstname + ' ' + last_name AS full_name,
          FLOOR(DATEDIFF(CURRENT_DATE(), birth_date) / 365) AS age
    FROM dataset_name.persons
   """
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> job = client.run_async_query('fullname-age-query-job', query)
   >>> job.destination = table
   >>> job.write_disposition= 'WRITE_TRUNCATE'
   >>> job.name
   'fullname-age-query-job'
   >>> job.job_type
   'query'
   >>> job.created
   None
   >>> job.state
   None

.. note::

   - The ``created`` and ``state`` fields are not set until the job
     is submitted to the BigQuery back-end.

Then, begin executing the job on the server:

.. code-block:: python

   >>> job.begin()  # API call
   >>> job.created
   datetime.datetime(2015, 7, 23, 9, 30, 20, 268260, tzinfo=<UTC>)
   >>> job.state
   'RUNNING'

Poll until the job is complete:

.. code-block:: python

   >>> import time
   >>> retry_count = 100
   >>> while retry_count > 0 and job.state != 'DONE':
   ...     retry_count -= 1
   ...     time.sleep(10)
   ...     job.reload()  # API call
   >>> job.state
   'done'
   >>> job.ended
   datetime.datetime(2015, 7, 23, 9, 30, 21, 334792, tzinfo=<UTC>)

Retrieve the results:

.. code-block:: python

   >>> results = job.results()
   >>> rows, total_count, token = query.fetch_data()  # API request
   >>> while True:
   ...     do_something_with(rows)
   ...     if token is None:
   ...         break
   ...     rows, total_count, token = query.fetch_data(
   ...         page_token=token)       # API request


Inserting data (asynchronous)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start a job loading data asynchronously from a set of CSV files, located on
Google Cloud Storage, appending rows into an existing table.  First, create
the job locally:

.. code-block:: python

   >>> from google.cloud import bigquery
   >>> from google.cloud.bigquery import SchemaField
   >>> client = bigquery.Client()
   >>> table = dataset.table(name='person_ages')
   >>> table.schema = [
   ...     SchemaField('full_name', 'STRING', mode='required'),
   ...     SchemaField('age', 'INTEGER', mode='required')]
   >>> job = client.load_table_from_storage(
   ...     'load-from-storage-job', table, 'gs://bucket-name/object-prefix*')
   >>> job.source_format = 'CSV'
   >>> job.skip_leading_rows = 1  # count of skipped header rows
   >>> job.write_disposition = 'WRITE_TRUNCATE'
   >>> job.name
   'load-from-storage-job'
   >>> job.job_type
   'load'
   >>> job.created
   None
   >>> job.state
   None

.. note::

   - ``google.cloud.bigquery`` generates a UUID for each job.
   - The ``created`` and ``state`` fields are not set until the job
     is submitted to the BigQuery back-end.

Then, begin executing the job on the server:

.. code-block:: python

   >>> job.begin()  # API call
   >>> job.created
   datetime.datetime(2015, 7, 23, 9, 30, 20, 268260, tzinfo=<UTC>)
   >>> job.state
   'RUNNING'

Poll until the job is complete:

.. code-block:: python

   >>> import time
   >>> retry_count = 100
   >>> while retry_count > 0 and job.state != 'DONE':
   ...     retry_count -= 1
   ...     time.sleep(10)
   ...     job.reload()  # API call
   >>> job.state
   'done'
   >>> job.ended
   datetime.datetime(2015, 7, 23, 9, 30, 21, 334792, tzinfo=<UTC>)


Exporting data (async)
~~~~~~~~~~~~~~~~~~~~~~

Start a job exporting a table's data asynchronously to a set of CSV files,
located on Google Cloud Storage.  First, create the job locally:

.. code-block:: python

   >>> from google.cloud import bigquery
   >>> client = bigquery.Client()
   >>> table = dataset.table(name='person_ages')
   >>> job = client.extract_table_to_storage(
   ...     'extract-person-ages-job', table,
   ...     'gs://bucket-name/export-prefix*.csv')
   ... job.destination_format = 'CSV'
   ... job.print_header = True
   ... job.write_disposition = 'WRITE_TRUNCATE'
   >>> job.name
   'extract-person-ages-job'
   >>> job.job_type
   'extract'
   >>> job.created
   None
   >>> job.state
   None

.. note::

   - ``google.cloud.bigquery`` generates a UUID for each job.
   - The ``created`` and ``state`` fields are not set until the job
     is submitted to the BigQuery back-end.

Then, begin executing the job on the server:

.. code-block:: python

   >>> job.begin()  # API call
   >>> job.created
   datetime.datetime(2015, 7, 23, 9, 30, 20, 268260, tzinfo=<UTC>)
   >>> job.state
   'RUNNING'

Poll until the job is complete:

.. code-block:: python

   >>> import time
   >>> retry_count = 100
   >>> while retry_count > 0 and job.state != 'DONE':
   ...     retry_count -= 1
   ...     time.sleep(10)
   ...     job.reload()  # API call
   >>> job.state
   'done'
   >>> job.ended
   datetime.datetime(2015, 7, 23, 9, 30, 21, 334792, tzinfo=<UTC>)


Copy tables (async)
~~~~~~~~~~~~~~~~~~~

First, create the job locally:

.. code-block:: python

   >>> from google.cloud import bigquery
   >>> client = bigquery.Client()
   >>> source_table = dataset.table(name='person_ages')
   >>> destination_table = dataset.table(name='person_ages_copy')
   >>> job = client.copy_table(
   ...     'copy-table-job', destination_table, source_table)
   >>> job.name
   'copy-table-job'
   >>> job.job_type
   'copy'
   >>> job.created
   None
   >>> job.state
   None

.. note::

   - ``google.cloud.bigquery`` generates a UUID for each job.
   - The ``created`` and ``state`` fields are not set until the job
     is submitted to the BigQuery back-end.

Then, begin executing the job on the server:

.. code-block:: python

   >>> job.begin()  # API call
   >>> job.created
   datetime.datetime(2015, 7, 23, 9, 30, 20, 268260, tzinfo=<UTC>)
   >>> job.state
   'RUNNING'

Poll until the job is complete:

.. code-block:: python

   >>> import time
   >>> retry_count = 100
   >>> while retry_count > 0 and job.state != 'DONE':
   ...     retry_count -= 1
   ...     time.sleep(10)
   ...     job.reload()  # API call
   >>> job.state
   'done'
   >>> job.ended
   datetime.datetime(2015, 7, 23, 9, 30, 21, 334792, tzinfo=<UTC>)
