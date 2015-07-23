.. toctree::
  :maxdepth: 0
  :hidden:

BigQuery
========

Authorization / Configuration
-----------------------------

- Use :class:`Client <gcloud.bigquery.client.Client>` objects to configure
  your applications.

- :class:`Client <gcloud.bigquery.client.Client>` objects hold both a ``project``
  and an authenticated connection to the PubSub service.

- The authentication credentials can be implicitly determined from the
  environment or directly via
  :meth:`from_service_account_json <gcloud.bigquery.client.Client.from_service_account_json>`
  and
  :meth:`from_service_account_p12 <gcloud.bigquery.client.Client.from_service_account_p12>`.

- After setting ``GOOGLE_APPLICATION_CREDENTIALS`` and ``GCLOUD_PROJECT``
  environment variables, create an instance of
  :class:`Client <gcloud.bigquery.client.Client>`.

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client()

- Override the credentials inferred from the environment by passing explicit
  ``credentials`` to one of the alternative ``classmethod`` factories,
  `:meth:gcloud.bigquery.client.Client.from_service_account_json`:

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client.from_service_account_json('/path/to/creds.json')

  or `:meth:gcloud.bigquery.client.Client.from_service_account_p12`:

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client.from_service_account_p12('/path/to/creds.p12', 'jrandom@example.com')


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

  .. doctest::

     >>> from gcloud import bigquery
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

Create a new dataset for the client's project:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.create()  # API request

Check for the existence of a dataset:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.exists()  # API request
   True

List datasets for the client's project:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> datasets, next_page_token = client.list_datasets()  # API request
   >>> [dataset.name for dataset in datasets]
   ['dataset_name']

Refresh metadata for a dataset (to pick up changes made by another client):

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.reload()  # API request

Patch metadata for a dataset:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> one_day_ms = 24 * 60 * 60 * 1000
   >>> dataset.patch(description='Description goes here',
   ...               default_table_expiration_ms=one_day_ms)  # API request

Replace the ACL for a dataset, and update all writeable fields:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.get()  # API request
   >>> acl = list(dataset.acl)
   >>> acl.append(bigquery.Access(role='READER', entity_type='domain', entity='example.com'))
   >>> dataset.acl = acl
   >>> dataset.update()  # API request

Delete a dataset:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.delete()  # API request


Tables
------

Tables exist within datasets.  List tables for the dataset:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> tables, next_page_token = dataset.list_tables()  # API request
   >>> [table.name for table in tables]
   ['table_name']

Create a table:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.create()  # API request

Check for the existence of a table:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.exists()  # API request
   True

Refresh metadata for a table (to pick up changes made by another client):

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.reload()  # API request

Patch specific properties for a table:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.patch(friendly_name='Person Ages',
   ...             description='Ages of persons')  # API request

Update all writable metadata for a table

.. doctest::

   >>> from gcloud import bigquery
   >>> from gcloud.bigquery import SchemaField
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.schema = [
   ...     SchemaField(name='full_name', type='string', mode='required'),
   ...     SchemaField(name='age', type='int', mode='required)]
   >>> table.update()  # API request

Delete a table:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.delete()  # API request

Jobs
----

Jobs describe actions peformed on data in BigQuery tables:

- Load data into a table
- Run a query against data in one or more tables
- Extract data from a table
- Copy a table

List jobs for a project:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> jobs = client.jobs()  # API request
   >>> [(job.job_id, job.type, job.created, job.state) for job in jobs]
   ['e3344fba-09df-4ae0-8337-fddee34b3840', 'insert', (datetime.datetime(2015, 7, 23, 9, 30, 20, 268260, tzinfo=<UTC>), 'done')]

Querying data (synchronous)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run a query which can be expected to complete within bounded time:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> query = """\
   SELECT count(*) AS age_count FROM dataset_name.person_ages
   """
   >>> results = client.query(query, timeout_ms=1000)
   >>> retry_count = 100
   >>> while retry_count > 0 and not results.job_complete:
   ...     retry_count -= 1
   ...     time.sleep(10)
   ...     results.reload()  # API request
   >>> results.schema
   [{'name': 'age_count', 'type': 'integer', 'mode': 'nullable'}]
   >>> results.rows
   [(15,)]

.. note::
   
   If the query takes longer than the timeout allowed, ``results.job_complete``
   will be ``False``:  we therefore poll until it is completed.

Querying data (asynchronous)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Background a query, loading the results into a table:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> query = """\
   SELECT firstname + ' ' + last_name AS full_name,
          FLOOR(DATEDIFF(CURRENT_DATE(), birth_date) / 365) AS age
    FROM dataset_name.persons
   """
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> job = client.query_async(query,
   ...                          destination=table,
   ...                          write_disposition='truncate')
   >>> job.job_id
   'e3344fba-09df-4ae0-8337-fddee34b3840'
   >>> job.type
   'load'
   >>> job.created
   None
   >>> job.state
   None

.. note::

   - ``gcloud.bigquery`` generates a UUID for each job.
   - The ``created`` and ``state`` fields are not set until the job
     is submitted to the BigQuery back-end.

Then, begin executing the job on the server:

.. doctest::

   >>> job.submit()  # API call
   >>> job.created
   datetime.datetime(2015, 7, 23, 9, 30, 20, 268260, tzinfo=<UTC>)
   >>> job.state
   'running'

Poll until the job is complete:

.. doctest::

   >>> import time
   >>> retry_count = 100
   >>> while retry_count > 0 and job.state == 'running':
   ...     retry_count -= 1
   ...     time.sleep(10)
   ...     job.reload()  # API call
   >>> job.state
   'done'
   >>> job.ended
   datetime.datetime(2015, 7, 23, 9, 30, 21, 334792, tzinfo=<UTC>)

Inserting data (synchronous)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load data synchronously from a local CSV file into a new table.  First,
create the job locally:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> table = dataset.table(name='person_ages')
   >>> with open('/path/to/person_ages.csv', 'rb') as file_obj:
   ...     job = table.load_from_file(
   ...         file_obj,
   ...         source_format='CSV',
   ...         skip_leading_rows=1
   ...         write_disposition='truncate',
   ...         )  # API request
   >>> job.job_id
   'e3344fba-09df-4ae0-8337-fddee34b3840'
   >>> job.type
   'load'
   >>> job.created
   datetime.datetime(2015, 7, 23, 9, 30, 20, 268260, tzinfo=<UTC>)
   >>> job.state
   'done'
   >>> job.ended
   datetime.datetime(2015, 7, 23, 9, 30, 21, 334792, tzinfo=<UTC>)

Inserting data (asynchronous)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start a job loading data asynchronously from a set of CSV files, located on
GCloud Storage, appending rows into an existing table.  First, create the job
locally:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> table = dataset.table(name='person_ages')
   >>> job = table.load_from_storage(bucket_name='bucket-name',
   ...                               object_name='object-prefix*',
   ...                               source_format='CSV',
   ...                               skip_leading_rows=1,
   ...                               write_disposition='truncate')
   >>> job.job_id
   'e3344fba-09df-4ae0-8337-fddee34b3840'
   >>> job.type
   'load'
   >>> job.created
   None
   >>> job.state
   None

.. note::

   - ``gcloud.bigquery`` generates a UUID for each job.
   - The ``created`` and ``state`` fields are not set until the job
     is submitted to the BigQuery back-end.

Then, begin executing the job on the server:

.. doctest::

   >>> job.submit()  # API call
   >>> job.created
   datetime.datetime(2015, 7, 23, 9, 30, 20, 268260, tzinfo=<UTC>)
   >>> job.state
   'running'

Poll until the job is complete:

.. doctest::

   >>> import time
   >>> retry_count = 100
   >>> while retry_count > 0 and job.state == 'running':
   ...     retry_count -= 1
   ...     time.sleep(10)
   ...     job.reload()  # API call
   >>> job.state
   'done'
   >>> job.ended
   datetime.datetime(2015, 7, 23, 9, 30, 21, 334792, tzinfo=<UTC>)
