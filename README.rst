Google Cloud Python Client
==========================

Python idiomatic clients for `Google Cloud Platform`_ services.

.. _Google Cloud Platform: https://cloud.google.com/


Stability levels
*******************

The `development status classifier`_ on PyPI indicates the current stability
of a package.

.. _development status classifier: https://pypi.org/classifiers/

General Availability
--------------------

**GA** (general availability) indicates that the client library for a
particular service is stable, and that the code surface will not change in
backwards-incompatible ways unless either absolutely necessary (e.g. because
of critical security issues) or with an extensive deprecation period.
Issues and requests against GA libraries are addressed with the highest
priority.

GA libraries have development status classifier ``Development Status :: 5 - Production/Stable``.

.. note::

    Sub-components of GA libraries explicitly marked as beta in the
    import path (e.g. ``google.cloud.language_v1beta2``) should be considered
    to be beta.

Beta Support
------------

**Beta** indicates that the client library for a particular service is
mostly stable and is being prepared for release. Issues and requests
against beta libraries are addressed with a higher priority.

Beta libraries have development status classifier ``Development Status :: 4 - Beta``.

Alpha Support
-------------

**Alpha** indicates that the client library for a particular service is
still a work-in-progress and is more likely to get backwards-incompatible
updates. See `versioning`_ for more details.


Alpha libraries have development status classifier ``Development Status :: 3 - Alpha``.

If you need support for other Google APIs, check out the
`Google APIs Python Client library`_.

.. _Google APIs Python Client library: https://github.com/google/google-api-python-client


Libraries
*********

.. This table is generated, see synth.py for details.

.. API_TABLE_START

.. list-table::
   :header-rows: 1

   * - Client
     - Release Level
     - Version
   * - `A python wrapper of the C library 'CRC32C' <https://github.com/googleapis/python-crc32c>`_
     - |stable|
     - |PyPI-google-crc32c|
   * - `AI Platform <https://github.com/googleapis/python-aiplatform>`_
     - |stable|
     - |PyPI-google-cloud-aiplatform|
   * - `BigQuery <https://github.com/googleapis/python-bigquery>`_
     - |stable|
     - |PyPI-google-cloud-bigquery|
   * - `BigQuery Storage <https://github.com/googleapis/python-bigquery-storage>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-storage|
   * - `BigQuery connector for Jupyter and IPython <https://github.com/googleapis/python-bigquery-magics>`_
     - |stable|
     - |PyPI-bigquery-magics|
   * - `Bigtable <https://github.com/googleapis/python-bigtable>`_
     - |stable|
     - |PyPI-google-cloud-bigtable|
   * - `Datastore <https://github.com/googleapis/python-datastore>`_
     - |stable|
     - |PyPI-google-cloud-datastore|
   * - `Firestore <https://github.com/googleapis/python-firestore>`_
     - |stable|
     - |PyPI-google-cloud-firestore|
   * - `Identity and Access Management <https://github.com/googleapis/python-grpc-google-iam-v1>`_
     - |stable|
     - |PyPI-grpc-google-iam-v1|
   * - `Logging <https://github.com/googleapis/python-logging>`_
     - |stable|
     - |PyPI-google-cloud-logging|
   * - `NDB Client Library for Datastore <https://github.com/googleapis/python-ndb>`_
     - |stable|
     - |PyPI-google-cloud-ndb|
   * - `Pandas Data Types for SQL systems (BigQuery, Spanner) <https://github.com/googleapis/python-db-dtypes-pandas>`_
     - |stable|
     - |PyPI-db-dtypes|
   * - `Pub/Sub <https://github.com/googleapis/python-pubsub>`_
     - |stable|
     - |PyPI-google-cloud-pubsub|
   * - `Pub/Sub Lite <https://github.com/googleapis/python-pubsublite>`_
     - |stable|
     - |PyPI-google-cloud-pubsublite|
   * - `Spanner <https://github.com/googleapis/python-spanner>`_
     - |stable|
     - |PyPI-google-cloud-spanner|
   * - `Spanner Django <https://github.com/googleapis/python-spanner-django>`_
     - |stable|
     - |PyPI-django-google-spanner|
   * - `Storage <https://github.com/googleapis/python-storage>`_
     - |stable|
     - |PyPI-google-cloud-storage|
   * - `A unified Python API in BigQuery <https://github.com/googleapis/python-bigquery-dataframes>`_
     - |preview|
     - |PyPI-bigframes|
   * - `Audit Log <https://github.com/googleapis/python-audit-log>`_
     - |preview|
     - |PyPI-google-cloud-audit-log|
   * - `BigQuery connector for pandas <https://github.com/googleapis/python-bigquery-pandas>`_
     - |preview|
     - |PyPI-pandas-gbq|
   * - `DNS <https://github.com/googleapis/python-dns>`_
     - |preview|
     - |PyPI-google-cloud-dns|
   * - `Document AI Toolbox <https://github.com/googleapis/python-documentai-toolbox>`_
     - |preview|
     - |PyPI-google-cloud-documentai-toolbox|
   * - `Error Reporting <https://github.com/googleapis/python-error-reporting>`_
     - |preview|
     - |PyPI-google-cloud-error-reporting|
   * - `Runtime Configurator <https://github.com/googleapis/python-runtimeconfig>`_
     - |preview|
     - |PyPI-google-cloud-runtimeconfig|
   * - `SQLAlchemy dialect for BigQuery <https://github.com/googleapis/python-bigquery-sqlalchemy>`_
     - |preview|
     - |PyPI-sqlalchemy-bigquery|

.. |PyPI-google-crc32c| image:: https://img.shields.io/pypi/v/google-crc32c.svg
     :target: https://pypi.org/project/google-crc32c
.. |PyPI-google-cloud-aiplatform| image:: https://img.shields.io/pypi/v/google-cloud-aiplatform.svg
     :target: https://pypi.org/project/google-cloud-aiplatform
.. |PyPI-google-cloud-bigquery| image:: https://img.shields.io/pypi/v/google-cloud-bigquery.svg
     :target: https://pypi.org/project/google-cloud-bigquery
.. |PyPI-google-cloud-bigquery-storage| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-storage.svg
     :target: https://pypi.org/project/google-cloud-bigquery-storage
.. |PyPI-bigquery-magics| image:: https://img.shields.io/pypi/v/bigquery-magics.svg
     :target: https://pypi.org/project/bigquery-magics
.. |PyPI-google-cloud-bigtable| image:: https://img.shields.io/pypi/v/google-cloud-bigtable.svg
     :target: https://pypi.org/project/google-cloud-bigtable
.. |PyPI-google-cloud-datastore| image:: https://img.shields.io/pypi/v/google-cloud-datastore.svg
     :target: https://pypi.org/project/google-cloud-datastore
.. |PyPI-google-cloud-firestore| image:: https://img.shields.io/pypi/v/google-cloud-firestore.svg
     :target: https://pypi.org/project/google-cloud-firestore
.. |PyPI-grpc-google-iam-v1| image:: https://img.shields.io/pypi/v/grpc-google-iam-v1.svg
     :target: https://pypi.org/project/grpc-google-iam-v1
.. |PyPI-google-cloud-logging| image:: https://img.shields.io/pypi/v/google-cloud-logging.svg
     :target: https://pypi.org/project/google-cloud-logging
.. |PyPI-google-cloud-ndb| image:: https://img.shields.io/pypi/v/google-cloud-ndb.svg
     :target: https://pypi.org/project/google-cloud-ndb
.. |PyPI-db-dtypes| image:: https://img.shields.io/pypi/v/db-dtypes.svg
     :target: https://pypi.org/project/db-dtypes
.. |PyPI-google-cloud-pubsub| image:: https://img.shields.io/pypi/v/google-cloud-pubsub.svg
     :target: https://pypi.org/project/google-cloud-pubsub
.. |PyPI-google-cloud-pubsublite| image:: https://img.shields.io/pypi/v/google-cloud-pubsublite.svg
     :target: https://pypi.org/project/google-cloud-pubsublite
.. |PyPI-google-cloud-spanner| image:: https://img.shields.io/pypi/v/google-cloud-spanner.svg
     :target: https://pypi.org/project/google-cloud-spanner
.. |PyPI-django-google-spanner| image:: https://img.shields.io/pypi/v/django-google-spanner.svg
     :target: https://pypi.org/project/django-google-spanner
.. |PyPI-google-cloud-storage| image:: https://img.shields.io/pypi/v/google-cloud-storage.svg
     :target: https://pypi.org/project/google-cloud-storage
.. |PyPI-bigframes| image:: https://img.shields.io/pypi/v/bigframes.svg
     :target: https://pypi.org/project/bigframes
.. |PyPI-google-cloud-audit-log| image:: https://img.shields.io/pypi/v/google-cloud-audit-log.svg
     :target: https://pypi.org/project/google-cloud-audit-log
.. |PyPI-pandas-gbq| image:: https://img.shields.io/pypi/v/pandas-gbq.svg
     :target: https://pypi.org/project/pandas-gbq
.. |PyPI-google-cloud-dns| image:: https://img.shields.io/pypi/v/google-cloud-dns.svg
     :target: https://pypi.org/project/google-cloud-dns
.. |PyPI-google-cloud-documentai-toolbox| image:: https://img.shields.io/pypi/v/google-cloud-documentai-toolbox.svg
     :target: https://pypi.org/project/google-cloud-documentai-toolbox
.. |PyPI-google-cloud-error-reporting| image:: https://img.shields.io/pypi/v/google-cloud-error-reporting.svg
     :target: https://pypi.org/project/google-cloud-error-reporting
.. |PyPI-google-cloud-runtimeconfig| image:: https://img.shields.io/pypi/v/google-cloud-runtimeconfig.svg
     :target: https://pypi.org/project/google-cloud-runtimeconfig
.. |PyPI-sqlalchemy-bigquery| image:: https://img.shields.io/pypi/v/sqlalchemy-bigquery.svg
     :target: https://pypi.org/project/sqlalchemy-bigquery

.. API_TABLE_END

.. |ga| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability

.. |beta| image:: https://img.shields.io/badge/support-beta-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#beta-support


.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#alpha-support


Example Applications
********************

-  `getting-started-python`_ - A sample and `tutorial`_ that demonstrates how to build a complete web application using Cloud Datastore, Cloud Storage, and Cloud Pub/Sub and deploy it to Google App Engine or Google Compute Engine.
-  `google-cloud-python-expenses-demo`_ - A sample expenses demo using Cloud Datastore and Cloud Storage.

.. _getting-started-python: https://github.com/GoogleCloudPlatform/getting-started-python
.. _tutorial: https://cloud.google.com/python
.. _google-cloud-python-expenses-demo: https://github.com/GoogleCloudPlatform/google-cloud-python-expenses-demo


Authentication
********************


With ``google-cloud-python`` we try to make authentication as painless as possible.
Check out the `Getting started with authentication`_ in our documentation to learn more.

.. _Getting started with authentication: https://cloud.google.com/docs/authentication/getting-started



License
********************


Apache 2.0 - See `the LICENSE`_ for more information.

.. _the LICENSE: https://github.com/googleapis/google-cloud-python/blob/main/LICENSE
