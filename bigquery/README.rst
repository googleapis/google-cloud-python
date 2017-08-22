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

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: https://google-cloud-python.readthedocs.io/en/latest/core/auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/gcloud-common/tree/master/authentication

Using the API
-------------

Querying massive datasets can be time consuming and expensive without the
right hardware and infrastructure. Google `BigQuery`_ (`BigQuery API docs`_)
solves this problem by enabling super-fast, SQL-like queries against
append-only tables, using the processing power of Google's infrastructure.

.. _BigQuery: https://cloud.google.com/bigquery/what-is-bigquery
.. _BigQuery API docs: https://cloud.google.com/bigquery/docs/reference/v2/

Load data from CSV
~~~~~~~~~~~~~~~~~~

.. code:: python

    import csv

    from google.cloud import bigquery
    from google.cloud.bigquery import SchemaField

    client = bigquery.Client()

    dataset = client.dataset('dataset_name')
    dataset.create()  # API request

    SCHEMA = [
        SchemaField('full_name', 'STRING', mode='required'),
        SchemaField('age', 'INTEGER', mode='required'),
    ]
    table = dataset.table('table_name', SCHEMA)
    table.create()

    with open('csv_file', 'rb') as readable:
        table.upload_from_file(
            readable, source_format='CSV', skip_leading_rows=1)

Perform a synchronous query
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # Perform a synchronous query.
    QUERY = (
        'SELECT name FROM [bigquery-public-data:usa_names.usa_1910_2013] '
        'WHERE state = "TX"')
    query = client.run_sync_query('%s LIMIT 100' % QUERY)
    query.timeout_ms = TIMEOUT_MS
    query.run()

    for row in query.rows:
        print(row)


See the ``google-cloud-python`` API `BigQuery documentation`_ to learn how
to connect to BigQuery using this Client Library.

.. _BigQuery documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/usage.html

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-bigquery.svg
   :target: https://pypi.org/project/google-cloud-bigquery/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-bigquery.svg
   :target: https://pypi.org/project/google-cloud-bigquery/
