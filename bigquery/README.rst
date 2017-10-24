Python Client for Google BigQuery
=================================

    Python idiomatic client for `Google BigQuery`_

.. _Google BigQuery: https://cloud.google.com/bigquery/what-is-bigquery

|pypi| |versions|

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/usage.html

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-bigquery

Fore more information on setting up your Python development environment, such as installing ``pip`` and on your system, please refer to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: https://google-cloud-python.readthedocs.io/en/latest/core/auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/google-cloud-common/tree/master/authentication

Using the API
-------------

Querying massive datasets can be time consuming and expensive without the
right hardware and infrastructure. Google `BigQuery`_ (`BigQuery API docs`_)
solves this problem by enabling super-fast, SQL queries against
append-mostly tables, using the processing power of Google's infrastructure.

.. _BigQuery: https://cloud.google.com/bigquery/what-is-bigquery
.. _BigQuery API docs: https://cloud.google.com/bigquery/docs/reference/v2/

Create a dataset
~~~~~~~~~~~~~~~~

.. code:: python

    from google.cloud import bigquery
    from google.cloud.bigquery import Dataset

    client = bigquery.Client()

    dataset_ref = client.dataset('dataset_name')
    dataset = Dataset(dataset_ref)
    dataset.description = 'my dataset'
    dataset = client.create_dataset(dataset)  # API request

Load data from CSV
~~~~~~~~~~~~~~~~~~

.. code:: python

    import csv

    from google.cloud import bigquery
    from google.cloud.bigquery import LoadJobConfig
    from google.cloud.bigquery import SchemaField

    client = bigquery.Client()

    SCHEMA = [
        SchemaField('full_name', 'STRING', mode='required'),
        SchemaField('age', 'INTEGER', mode='required'),
    ]
    table_ref = client.dataset('dataset_name').table('table_name')

    load_config = LoadJobConfig()
    load_config.skip_leading_rows = 1
    load_config.schema = SCHEMA

    # Contents of csv_file.csv:
    #     Name,Age
    #     Tim,99
    with open('csv_file.csv', 'rb') as readable:
        client.load_table_from_file(
            readable, table_ref, job_config=load_config)  # API request

Perform a query
~~~~~~~~~~~~~~~

.. code:: python

    # Perform a query.
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print(row.name)


See the ``google-cloud-python`` API `BigQuery documentation`_ to learn how
to connect to BigQuery using this Client Library.

.. _BigQuery documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/usage.html

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-bigquery.svg
   :target: https://pypi.org/project/google-cloud-bigquery/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-bigquery.svg
   :target: https://pypi.org/project/google-cloud-bigquery/
