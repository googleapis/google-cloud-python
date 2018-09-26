SQLAlchemy dialect and API client for BigQuery.


Usage
=====


SQLAchemy
_________

.. code-block:: python

    from sqlalchemy import *
    from sqlalchemy.engine import create_engine
    from sqlalchemy.schema import *
    engine = create_engine('bigquery://project')
    table = Table('dataset.table', MetaData(bind=engine), autoload=True)
    print(select([func.count('*')], from_obj=table).scalar())

API Client
__________

.. code-block:: python

    from pybigquery.api import ApiClient
    api_client = ApiClient()
    print(api_client.dry_run_query(query=sqlstr).total_bytes_processed)

Project
_______

``project`` in ``bigquery://project`` is used to instantiate BigQuery client with the specific project ID. To infer project from the environment, use ``bigquery://`` – without ``project``

Authentication
______________

Follow the `Google Cloud library guide <https://google-cloud-python.readthedocs.io/en/latest/core/auth.html>`_ for authentication. Alternatively, you can provide the path to a service account JSON file in ``create_engine()``:

.. code-block:: python

    engine = create_engine('bigquery://', credentials_path='/path/to/keyfile.json')


Location
________

To specify location of your datasets pass ``location`` to ``create_engine()``:

.. code-block:: python

    engine = create_engine('bigquery://project', location="asia-northeast1")


Table names
___________

To query tables from non-default projects, use the following format for the table name: ``project.dataset.table``, e.g.:

.. code-block:: python

    sample_table = Table('bigquery-public-data.samples.natality')

Batch size
__________

By default, ``arraysize`` is set to ``5000``. ``arraysize`` is used to set the batch size for fetching results. To change it, pass ``arraysize`` to ``create_engine()``:

.. code-block:: python

    engine = create_engine('bigquery://project', arraysize=1000)


Adding a Default Dataset
________________________

If you want to have the ``Client`` use a default dataset, specify it as the "database" portion of the connection string.

.. code-block:: python

    engine = create_engine('bigquery://project/dataset')


Connection String Parameters
____________________________


There are many situations where you can't call ``create_engine`` directly, such as when using tools like `Flask SQLAlchemy <http://flask-sqlalchemy.pocoo.org/2.3/>`_. For situations like these, or for situations where you want the ``Client`` to have a ```default_query_job_config`` <https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client>`_, you can pass many arguments in the query of the connection string.

The ``credentials_path``, ``location``, and ``arraysize`` parameters are used by this library, and the rest are used to create a ```QueryJobConfig`` <https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.QueryJobConfig.html#google.cloud.bigquery.job.QueryJobConfig>`_

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


Requirements
============

Install using

- ``pip install pybigquery``


Testing
============

Load sample tables::

    ./scripts/load_test_data.sh

This will create a dataset ``test_pybigquery`` with tables named ``sample_one_row`` and ``sample``.

Set up an environment and run tests::

    pyvenv .env
    source .env/bin/activate
    pip install -r dev_requirements.txt
    pytest
