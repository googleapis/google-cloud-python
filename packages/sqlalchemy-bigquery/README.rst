SQLAlchemy Dialect for BigQuery
===============================

|beta| |pypi| |versions|

`SQLALchemy Dialects`_

- `Dialect Documentation`_
- `Product Documentation`_

.. |beta| image:: https://img.shields.io/badge/support-beta-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#beta-support
.. |pypi| image:: https://img.shields.io/pypi/v/pybigquery.svg
   :target: https://pypi.org/project/pybigquery/
.. |versions| image:: https://img.shields.io/pypi/pyversions/pybigquery.svg
   :target: https://pypi.org/project/pybigquery/
.. _SQLAlchemy Dialects: https://docs.sqlalchemy.org/en/14/dialects/
.. _Dialect Documentation: https://googleapis.dev/python/pybigquery/latest
.. _Product Documentation: https://cloud.google.com/bigquery/docs/


Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. [Optional] `Enable billing for your project.`_
3. `Enable the BigQuery Storage API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the BigQuery Storage API.: https://console.cloud.google.com/apis/library/bigquery.googleapis.com
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
------------

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.6

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python <= 3.5.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install pybigquery


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install pybigquery

Usage
-----

SQLAlchemy
^^^^^^^^^^

.. code-block:: python

    from sqlalchemy import *
    from sqlalchemy.engine import create_engine
    from sqlalchemy.schema import *
    engine = create_engine('bigquery://project')
    table = Table('dataset.table', MetaData(bind=engine), autoload=True)
    print(select([func.count('*')], from_obj=table).scalar())

API Client
^^^^^^^^^^

.. code-block:: python

    from pybigquery.api import ApiClient
    api_client = ApiClient()
    print(api_client.dry_run_query(query=sqlstr).total_bytes_processed)

Project
^^^^^^^

``project`` in ``bigquery://project`` is used to instantiate BigQuery client with the specific project ID. To infer project from the environment, use ``bigquery://`` – without ``project``

Authentication
^^^^^^^^^^^^^^

Follow the `Google Cloud library guide <https://google-cloud-python.readthedocs.io/en/latest/core/auth.html>`_ for authentication. Alternatively, you can provide the path to a service account JSON file in ``create_engine()``:

.. code-block:: python

    engine = create_engine('bigquery://', credentials_path='/path/to/keyfile.json')


Location
^^^^^^^^

To specify location of your datasets pass ``location`` to ``create_engine()``:

.. code-block:: python

    engine = create_engine('bigquery://project', location="asia-northeast1")


Table names
^^^^^^^^^^^

To query tables from non-default projects or datasets, use the following format for the SQLAlchemy schema name: ``[project.]dataset``, e.g.:

.. code-block:: python

    # If neither dataset nor project are the default
    sample_table_1 = Table('natality', schema='bigquery-public-data.samples')
    # If just dataset is not the default
    sample_table_2 = Table('natality', schema='bigquery-public-data')

Batch size
^^^^^^^^^^

By default, ``arraysize`` is set to ``5000``. ``arraysize`` is used to set the batch size for fetching results. To change it, pass ``arraysize`` to ``create_engine()``:

.. code-block:: python

    engine = create_engine('bigquery://project', arraysize=1000)


Adding a Default Dataset
^^^^^^^^^^^^^^^^^^^^^^^^

If you want to have the ``Client`` use a default dataset, specify it as the "database" portion of the connection string.

.. code-block:: python

    engine = create_engine('bigquery://project/dataset')

When using a default dataset, don't include the dataset name in the table name, e.g.:

.. code-block:: python

    table = Table('table_name')

Note that specifying a default dataset doesn't restrict execution of queries to that particular dataset when using raw queries, e.g.:

.. code-block:: python

    # Set default dataset to dataset_a
    engine = create_engine('bigquery://project/dataset_a')

    # This will still execute and return rows from dataset_b
    engine.execute('SELECT * FROM dataset_b.table').fetchall()


Connection String Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are many situations where you can't call ``create_engine`` directly, such as when using tools like `Flask SQLAlchemy <http://flask-sqlalchemy.pocoo.org/2.3/>`_. For situations like these, or for situations where you want the ``Client`` to have a `default_query_job_config <https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client>`_, you can pass many arguments in the query of the connection string.

The ``credentials_path``, ``credentials_info``, ``location``, and ``arraysize`` parameters are used by this library, and the rest are used to create a `QueryJobConfig <https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.QueryJobConfig.html#google.cloud.bigquery.job.QueryJobConfig>`_

Note that if you want to use query strings, it will be more reliable if you use three slashes, so ``'bigquery:///?a=b'`` will work reliably, but ``'bigquery://?a=b'`` might be interpreted as having a "database" of ``?a=b``, depending on the system being used to parse the connection string.

Here are examples of all the supported arguments. Any not present are either for legacy sql (which isn't supported by this library), or are too complex and are not implemented.

.. code-block:: python

    engine = create_engine(
        'bigquery://some-project/some-dataset' '?'
        'credentials_path=/some/path/to.json' '&'
        'location=some-location' '&'
        'arraysize=1000' '&'
        'clustering_fields=a,b,c' '&'
        'create_disposition=CREATE_IF_NEEDED' '&'
        'destination=different-project.different-dataset.table' '&'
        'destination_encryption_configuration=some-configuration' '&'
        'dry_run=true' '&'
        'labels=a:b,c:d' '&'
        'maximum_bytes_billed=1000' '&'
        'priority=INTERACTIVE' '&'
        'schema_update_options=ALLOW_FIELD_ADDITION,ALLOW_FIELD_RELAXATION' '&'
        'use_query_cache=true' '&'
        'write_disposition=WRITE_APPEND'
    )


Creating tables
^^^^^^^^^^^^^^^

To add metadata to a table:

.. code-block:: python

    table = Table('mytable', ..., bigquery_description='my table description', bigquery_friendly_name='my table friendly name')

To add metadata to a column:

.. code-block:: python

    Column('mycolumn', doc='my column description')
