.. _reader:

Reading Tables
==============

Suppose you want to load all data from an existing BigQuery table
``test_dataset.test_table`` into a DataFrame using the
:func:`~pandas_gbq.read_gbq` function.

.. code-block:: python

   import pandas_gbq

   # TODO: Set your BigQuery Project ID.
   projectid = "xxxxxxxx"

   data_frame = pandas_gbq.read_gbq(
       'SELECT * FROM `test_dataset.test_table`',
       project_id=projectid)

.. note::

    A project ID is sometimes optional if it can be inferred during
    authentication, but it is required when authenticating with user
    credentials. You can find your project ID in the `Google Cloud console
    <https://console.cloud.google.com>`__.

You can define which column from BigQuery to use as an index in the
destination DataFrame as well as a preferred column order as follows:

.. code-block:: python

   data_frame = pandas_gbq.read_gbq(
       'SELECT * FROM `test_dataset.test_table`',
       project_id=projectid,
       index_col='index_column_name',
       col_order=['col1', 'col2', 'col3'])


You can specify the query config as parameter to use additional options of
your job. For more information about query configuration parameters see `here
<https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query>`__.

.. code-block:: python

   configuration = {
      'query': {
        "useQueryCache": False
      }
   }
   data_frame = read_gbq(
       'SELECT * FROM `test_dataset.test_table`',
       project_id=projectid,
       configuration=configuration)


The ``dialect`` argument can be used to indicate whether to use
BigQuery's ``'legacy'`` SQL or BigQuery's ``'standard'`` SQL (beta). The
default value is ``'standard'`` For more information on BigQuery's standard
SQL, see `BigQuery SQL Reference
<https://cloud.google.com/bigquery/docs/reference/standard-sql/>`__

.. code-block:: python

   data_frame = pandas_gbq.read_gbq(
       'SELECT * FROM [test_dataset.test_table]',
       project_id=projectid,
       dialect='legacy')


.. _reading-dtypes:

Inferring the DataFrame's dtypes
--------------------------------

The :func:`~pandas_gbq.read_gbq` method infers the pandas dtype for each column, based on the BigQuery table schema.

================== =========================
BigQuery Data Type dtype
================== =========================
FLOAT              float
TIMESTAMP          :class:`~pandas.DatetimeTZDtype` with ``unit='ns'`` and ``tz='UTC'``
DATETIME           datetime64[ns]
TIME               datetime64[ns]
DATE               datetime64[ns]
================== =========================

.. _reading-bqstorage-api:

Using the BigQuery Storage API
------------------------------

Use the BigQuery Storage API to download large (>125 MB) query results more
quickly (but at an `increased cost
<https://cloud.google.com/bigquery/pricing#storage-api>`__) by setting
``use_bqstorage_api`` to ``True``.

#. Enable the BigQuery Storage API on the project you are using to run
   queries.

   `Enable the API
   <https://console.cloud.google.com/apis/library/bigquerystorage.googleapis.com>`__.
#. Ensure you have the `bigquery.readsessions.create permission
   <https://cloud.google.com/bigquery/docs/access-control#bq-permissions>`__. to
   create BigQuery Storage API read sessions. This permission is provided by
   the `bigquery.user role
   <https://cloud.google.com/bigquery/docs/access-control#roles>`__.
#. Install the ``google-cloud-bigquery-storage``, ``fastavro``, and
   ``python-snappy`` packages.

   With pip:

   .. code-block:: sh

      pip install --upgrade google-cloud-bigquery-storage fastavro python-snappy

   With conda:

   .. code-block:: sh

      conda install -c conda-forge google-cloud-bigquery-storage fastavro python-snappy
#. Set ``use_bqstorage_api`` to ``True`` when calling the
   :func:`~pandas_gbq.read_gbq` function. As of the ``google-cloud-bigquery``
   package, version 1.11.1 or later,the function will fallback to the
   BigQuery API if the BigQuery Storage API cannot be used, such as with
   small query results.
