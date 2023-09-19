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
   * - `AI Platform <https://github.com/googleapis/python-aiplatform>`_
     - |stable|
     - |PyPI-google-cloud-aiplatform|
   * - `App Engine Admin <https://github.com/googleapis/python-appengine-admin>`_
     - |stable|
     - |PyPI-google-cloud-appengine-admin|
   * - `Asset Inventory <https://github.com/googleapis/python-asset>`_
     - |stable|
     - |PyPI-google-cloud-asset|
   * - `AutoML <https://github.com/googleapis/python-automl>`_
     - |stable|
     - |PyPI-google-cloud-automl|
   * - `BigQuery <https://github.com/googleapis/python-bigquery>`_
     - |stable|
     - |PyPI-google-cloud-bigquery|
   * - `BigQuery Connection <https://github.com/googleapis/python-bigquery-connection>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-connection|
   * - `BigQuery Data Transfer <https://github.com/googleapis/python-bigquery-datatransfer>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-datatransfer|
   * - `BigQuery Reservation <https://github.com/googleapis/python-bigquery-reservation>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-reservation|
   * - `BigQuery Storage <https://github.com/googleapis/python-bigquery-storage>`_
     - |stable|
     - |PyPI-google-cloud-bigquery-storage|
   * - `Bigtable <https://github.com/googleapis/python-bigtable>`_
     - |stable|
     - |PyPI-google-cloud-bigtable|
   * - `Binary Authorization <https://github.com/googleapis/python-binary-authorization>`_
     - |stable|
     - |PyPI-google-cloud-binary-authorization|
   * - `Build <https://github.com/googleapis/python-cloudbuild>`_
     - |stable|
     - |PyPI-google-cloud-build|
   * - `Common <https://github.com/googleapis/python-cloud-common>`_
     - |stable|
     - |PyPI-google-cloud-common|
   * - `Compute Engine <https://github.com/googleapis/python-compute>`_
     - |stable|
     - |PyPI-google-cloud-compute|
   * - `Container Analysis <https://github.com/googleapis/python-containeranalysis>`_
     - |stable|
     - |PyPI-google-cloud-containeranalysis|
   * - `Data Loss Prevention <https://github.com/googleapis/python-dlp>`_
     - |stable|
     - |PyPI-google-cloud-dlp|
   * - `Dataproc <https://github.com/googleapis/python-dataproc>`_
     - |stable|
     - |PyPI-google-cloud-dataproc|
   * - `Datastore <https://github.com/googleapis/python-datastore>`_
     - |stable|
     - |PyPI-google-cloud-datastore|
   * - `Dialogflow <https://github.com/googleapis/python-dialogflow>`_
     - |stable|
     - |PyPI-google-cloud-dialogflow|
   * - `Filestore <https://github.com/googleapis/python-filestore>`_
     - |stable|
     - |PyPI-google-cloud-filestore|
   * - `Firestore <https://github.com/googleapis/python-firestore>`_
     - |stable|
     - |PyPI-google-cloud-firestore|
   * - `GKE Hub <https://github.com/googleapis/python-gke-hub>`_
     - |stable|
     - |PyPI-google-cloud-gke-hub|
   * - `Grafeas <https://github.com/googleapis/python-grafeas>`_
     - |stable|
     - |PyPI-grafeas|
   * - `Identity and Access Management <https://github.com/googleapis/python-grpc-google-iam-v1>`_
     - |stable|
     - |PyPI-grpc-google-iam-v1|
   * - `Key Management Service <https://github.com/googleapis/python-kms>`_
     - |stable|
     - |PyPI-google-cloud-kms|
   * - `Kubernetes Engine <https://github.com/googleapis/python-container>`_
     - |stable|
     - |PyPI-google-cloud-container|
   * - `Live Stream <https://github.com/googleapis/python-video-live-stream>`_
     - |stable|
     - |PyPI-google-cloud-video-live-stream|
   * - `Logging <https://github.com/googleapis/python-logging>`_
     - |stable|
     - |PyPI-google-cloud-logging|
   * - `Monitoring Dashboards <https://github.com/googleapis/python-monitoring-dashboards>`_
     - |stable|
     - |PyPI-google-cloud-monitoring-dashboards|
   * - `NDB Client Library for Datastore <https://github.com/googleapis/python-ndb>`_
     - |stable|
     - |PyPI-google-cloud-ndb|
   * - `OS Login <https://github.com/googleapis/python-oslogin>`_
     - |stable|
     - |PyPI-google-cloud-os-login|
   * - `Pandas Data Types for SQL systems (BigQuery, Spanner) <https://github.com/googleapis/python-db-dtypes-pandas>`_
     - |stable|
     - |PyPI-db-dtypes|
   * - `Pub/Sub <https://github.com/googleapis/python-pubsub>`_
     - |stable|
     - |PyPI-google-cloud-pubsub|
   * - `Pub/Sub Lite <https://github.com/googleapis/python-pubsublite>`_
     - |stable|
     - |PyPI-google-cloud-pubsublite|
   * - `Retail <https://github.com/googleapis/python-retail>`_
     - |stable|
     - |PyPI-google-cloud-retail|
   * - `Scheduler <https://github.com/googleapis/python-scheduler>`_
     - |stable|
     - |PyPI-google-cloud-scheduler|
   * - `Service Management <https://github.com/googleapis/python-service-management>`_
     - |stable|
     - |PyPI-google-cloud-service-management|
   * - `Spanner <https://github.com/googleapis/python-spanner>`_
     - |stable|
     - |PyPI-google-cloud-spanner|
   * - `Spanner Django <https://github.com/googleapis/python-spanner-django>`_
     - |stable|
     - |PyPI-django-google-spanner|
   * - `Speech <https://github.com/googleapis/python-speech>`_
     - |stable|
     - |PyPI-google-cloud-speech|
   * - `Stackdriver Monitoring <https://github.com/googleapis/python-monitoring>`_
     - |stable|
     - |PyPI-google-cloud-monitoring|
   * - `Storage <https://github.com/googleapis/python-storage>`_
     - |stable|
     - |PyPI-google-cloud-storage|
   * - `Storage Transfer Service <https://github.com/googleapis/python-storage-transfer>`_
     - |stable|
     - |PyPI-google-cloud-storage-transfer|
   * - `Tasks <https://github.com/googleapis/python-tasks>`_
     - |stable|
     - |PyPI-google-cloud-tasks|
   * - `Text-to-Speech <https://github.com/googleapis/python-texttospeech>`_
     - |stable|
     - |PyPI-google-cloud-texttospeech|
   * - `Trace <https://github.com/googleapis/python-trace>`_
     - |stable|
     - |PyPI-google-cloud-trace|
   * - `Transcoder <https://github.com/googleapis/python-video-transcoder>`_
     - |stable|
     - |PyPI-google-cloud-video-transcoder|
   * - `Translation <https://github.com/googleapis/python-translate>`_
     - |stable|
     - |PyPI-google-cloud-translate|
   * - `Video Intelligence <https://github.com/googleapis/python-videointelligence>`_
     - |stable|
     - |PyPI-google-cloud-videointelligence|
   * - `Vision <https://github.com/googleapis/python-vision>`_
     - |stable|
     - |PyPI-google-cloud-vision|
   * - `A unified Python API in BigQuery <https://github.com/googleapis/python-bigquery-dataframes>`_
     - |preview|
     - |PyPI-bigframes|
   * - `Analytics Admin <https://github.com/googleapis/python-analytics-admin>`_
     - |preview|
     - |PyPI-google-analytics-admin|
   * - `Analytics Data <https://github.com/googleapis/python-analytics-data>`_
     - |preview|
     - |PyPI-google-analytics-data|
   * - `Audit Log <https://github.com/googleapis/python-audit-log>`_
     - |preview|
     - |PyPI-google-cloud-audit-log|
   * - `BigQuery connector for pandas <https://github.com/googleapis/python-bigquery-pandas>`_
     - |preview|
     - |PyPI-pandas-gbq|
   * - `DNS <https://github.com/googleapis/python-dns>`_
     - |preview|
     - |PyPI-google-cloud-dns|
   * - `Dataflow <https://github.com/googleapis/python-dataflow-client>`_
     - |preview|
     - |PyPI-google-cloud-dataflow-client|
   * - `Document AI Toolbox <https://github.com/googleapis/python-documentai-toolbox>`_
     - |preview|
     - |PyPI-google-cloud-documentai-toolbox|
   * - `Error Reporting <https://github.com/googleapis/python-error-reporting>`_
     - |preview|
     - |PyPI-google-cloud-error-reporting|
   * - `Run <https://github.com/googleapis/python-run>`_
     - |preview|
     - |PyPI-google-cloud-run|
   * - `Runtime Configurator <https://github.com/googleapis/python-runtimeconfig>`_
     - |preview|
     - |PyPI-google-cloud-runtimeconfig|
   * - `SQLAlchemy dialect for BigQuery <https://github.com/googleapis/python-bigquery-sqlalchemy>`_
     - |preview|
     - |PyPI-sqlalchemy-bigquery|
   * - `Video Stitcher <https://github.com/googleapis/python-video-stitcher>`_
     - |preview|
     - |PyPI-google-cloud-video-stitcher|
   * - `Workspace Add-ons API <https://github.com/googleapis/python-gsuiteaddons>`_
     - |preview|
     - |PyPI-google-cloud-gsuiteaddons|

.. |PyPI-google-cloud-aiplatform| image:: https://img.shields.io/pypi/v/google-cloud-aiplatform.svg
     :target: https://pypi.org/project/google-cloud-aiplatform
.. |PyPI-google-cloud-appengine-admin| image:: https://img.shields.io/pypi/v/google-cloud-appengine-admin.svg
     :target: https://pypi.org/project/google-cloud-appengine-admin
.. |PyPI-google-cloud-asset| image:: https://img.shields.io/pypi/v/google-cloud-asset.svg
     :target: https://pypi.org/project/google-cloud-asset
.. |PyPI-google-cloud-automl| image:: https://img.shields.io/pypi/v/google-cloud-automl.svg
     :target: https://pypi.org/project/google-cloud-automl
.. |PyPI-google-cloud-bigquery| image:: https://img.shields.io/pypi/v/google-cloud-bigquery.svg
     :target: https://pypi.org/project/google-cloud-bigquery
.. |PyPI-google-cloud-bigquery-connection| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-connection.svg
     :target: https://pypi.org/project/google-cloud-bigquery-connection
.. |PyPI-google-cloud-bigquery-datatransfer| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-datatransfer.svg
     :target: https://pypi.org/project/google-cloud-bigquery-datatransfer
.. |PyPI-google-cloud-bigquery-reservation| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-reservation.svg
     :target: https://pypi.org/project/google-cloud-bigquery-reservation
.. |PyPI-google-cloud-bigquery-storage| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-storage.svg
     :target: https://pypi.org/project/google-cloud-bigquery-storage
.. |PyPI-google-cloud-bigtable| image:: https://img.shields.io/pypi/v/google-cloud-bigtable.svg
     :target: https://pypi.org/project/google-cloud-bigtable
.. |PyPI-google-cloud-binary-authorization| image:: https://img.shields.io/pypi/v/google-cloud-binary-authorization.svg
     :target: https://pypi.org/project/google-cloud-binary-authorization
.. |PyPI-google-cloud-build| image:: https://img.shields.io/pypi/v/google-cloud-build.svg
     :target: https://pypi.org/project/google-cloud-build
.. |PyPI-google-cloud-common| image:: https://img.shields.io/pypi/v/google-cloud-common.svg
     :target: https://pypi.org/project/google-cloud-common
.. |PyPI-google-cloud-compute| image:: https://img.shields.io/pypi/v/google-cloud-compute.svg
     :target: https://pypi.org/project/google-cloud-compute
.. |PyPI-google-cloud-containeranalysis| image:: https://img.shields.io/pypi/v/google-cloud-containeranalysis.svg
     :target: https://pypi.org/project/google-cloud-containeranalysis
.. |PyPI-google-cloud-dlp| image:: https://img.shields.io/pypi/v/google-cloud-dlp.svg
     :target: https://pypi.org/project/google-cloud-dlp
.. |PyPI-google-cloud-dataproc| image:: https://img.shields.io/pypi/v/google-cloud-dataproc.svg
     :target: https://pypi.org/project/google-cloud-dataproc
.. |PyPI-google-cloud-datastore| image:: https://img.shields.io/pypi/v/google-cloud-datastore.svg
     :target: https://pypi.org/project/google-cloud-datastore
.. |PyPI-google-cloud-dialogflow| image:: https://img.shields.io/pypi/v/google-cloud-dialogflow.svg
     :target: https://pypi.org/project/google-cloud-dialogflow
.. |PyPI-google-cloud-filestore| image:: https://img.shields.io/pypi/v/google-cloud-filestore.svg
     :target: https://pypi.org/project/google-cloud-filestore
.. |PyPI-google-cloud-firestore| image:: https://img.shields.io/pypi/v/google-cloud-firestore.svg
     :target: https://pypi.org/project/google-cloud-firestore
.. |PyPI-google-cloud-gke-hub| image:: https://img.shields.io/pypi/v/google-cloud-gke-hub.svg
     :target: https://pypi.org/project/google-cloud-gke-hub
.. |PyPI-grafeas| image:: https://img.shields.io/pypi/v/grafeas.svg
     :target: https://pypi.org/project/grafeas
.. |PyPI-grpc-google-iam-v1| image:: https://img.shields.io/pypi/v/grpc-google-iam-v1.svg
     :target: https://pypi.org/project/grpc-google-iam-v1
.. |PyPI-google-cloud-kms| image:: https://img.shields.io/pypi/v/google-cloud-kms.svg
     :target: https://pypi.org/project/google-cloud-kms
.. |PyPI-google-cloud-container| image:: https://img.shields.io/pypi/v/google-cloud-container.svg
     :target: https://pypi.org/project/google-cloud-container
.. |PyPI-google-cloud-video-live-stream| image:: https://img.shields.io/pypi/v/google-cloud-video-live-stream.svg
     :target: https://pypi.org/project/google-cloud-video-live-stream
.. |PyPI-google-cloud-logging| image:: https://img.shields.io/pypi/v/google-cloud-logging.svg
     :target: https://pypi.org/project/google-cloud-logging
.. |PyPI-google-cloud-monitoring-dashboards| image:: https://img.shields.io/pypi/v/google-cloud-monitoring-dashboards.svg
     :target: https://pypi.org/project/google-cloud-monitoring-dashboards
.. |PyPI-google-cloud-ndb| image:: https://img.shields.io/pypi/v/google-cloud-ndb.svg
     :target: https://pypi.org/project/google-cloud-ndb
.. |PyPI-google-cloud-os-login| image:: https://img.shields.io/pypi/v/google-cloud-os-login.svg
     :target: https://pypi.org/project/google-cloud-os-login
.. |PyPI-db-dtypes| image:: https://img.shields.io/pypi/v/db-dtypes.svg
     :target: https://pypi.org/project/db-dtypes
.. |PyPI-google-cloud-pubsub| image:: https://img.shields.io/pypi/v/google-cloud-pubsub.svg
     :target: https://pypi.org/project/google-cloud-pubsub
.. |PyPI-google-cloud-pubsublite| image:: https://img.shields.io/pypi/v/google-cloud-pubsublite.svg
     :target: https://pypi.org/project/google-cloud-pubsublite
.. |PyPI-google-cloud-retail| image:: https://img.shields.io/pypi/v/google-cloud-retail.svg
     :target: https://pypi.org/project/google-cloud-retail
.. |PyPI-google-cloud-scheduler| image:: https://img.shields.io/pypi/v/google-cloud-scheduler.svg
     :target: https://pypi.org/project/google-cloud-scheduler
.. |PyPI-google-cloud-service-management| image:: https://img.shields.io/pypi/v/google-cloud-service-management.svg
     :target: https://pypi.org/project/google-cloud-service-management
.. |PyPI-google-cloud-spanner| image:: https://img.shields.io/pypi/v/google-cloud-spanner.svg
     :target: https://pypi.org/project/google-cloud-spanner
.. |PyPI-django-google-spanner| image:: https://img.shields.io/pypi/v/django-google-spanner.svg
     :target: https://pypi.org/project/django-google-spanner
.. |PyPI-google-cloud-speech| image:: https://img.shields.io/pypi/v/google-cloud-speech.svg
     :target: https://pypi.org/project/google-cloud-speech
.. |PyPI-google-cloud-monitoring| image:: https://img.shields.io/pypi/v/google-cloud-monitoring.svg
     :target: https://pypi.org/project/google-cloud-monitoring
.. |PyPI-google-cloud-storage| image:: https://img.shields.io/pypi/v/google-cloud-storage.svg
     :target: https://pypi.org/project/google-cloud-storage
.. |PyPI-google-cloud-storage-transfer| image:: https://img.shields.io/pypi/v/google-cloud-storage-transfer.svg
     :target: https://pypi.org/project/google-cloud-storage-transfer
.. |PyPI-google-cloud-tasks| image:: https://img.shields.io/pypi/v/google-cloud-tasks.svg
     :target: https://pypi.org/project/google-cloud-tasks
.. |PyPI-google-cloud-texttospeech| image:: https://img.shields.io/pypi/v/google-cloud-texttospeech.svg
     :target: https://pypi.org/project/google-cloud-texttospeech
.. |PyPI-google-cloud-trace| image:: https://img.shields.io/pypi/v/google-cloud-trace.svg
     :target: https://pypi.org/project/google-cloud-trace
.. |PyPI-google-cloud-video-transcoder| image:: https://img.shields.io/pypi/v/google-cloud-video-transcoder.svg
     :target: https://pypi.org/project/google-cloud-video-transcoder
.. |PyPI-google-cloud-translate| image:: https://img.shields.io/pypi/v/google-cloud-translate.svg
     :target: https://pypi.org/project/google-cloud-translate
.. |PyPI-google-cloud-videointelligence| image:: https://img.shields.io/pypi/v/google-cloud-videointelligence.svg
     :target: https://pypi.org/project/google-cloud-videointelligence
.. |PyPI-google-cloud-vision| image:: https://img.shields.io/pypi/v/google-cloud-vision.svg
     :target: https://pypi.org/project/google-cloud-vision
.. |PyPI-bigframes| image:: https://img.shields.io/pypi/v/bigframes.svg
     :target: https://pypi.org/project/bigframes
.. |PyPI-google-analytics-admin| image:: https://img.shields.io/pypi/v/google-analytics-admin.svg
     :target: https://pypi.org/project/google-analytics-admin
.. |PyPI-google-analytics-data| image:: https://img.shields.io/pypi/v/google-analytics-data.svg
     :target: https://pypi.org/project/google-analytics-data
.. |PyPI-google-cloud-audit-log| image:: https://img.shields.io/pypi/v/google-cloud-audit-log.svg
     :target: https://pypi.org/project/google-cloud-audit-log
.. |PyPI-pandas-gbq| image:: https://img.shields.io/pypi/v/pandas-gbq.svg
     :target: https://pypi.org/project/pandas-gbq
.. |PyPI-google-cloud-dns| image:: https://img.shields.io/pypi/v/google-cloud-dns.svg
     :target: https://pypi.org/project/google-cloud-dns
.. |PyPI-google-cloud-dataflow-client| image:: https://img.shields.io/pypi/v/google-cloud-dataflow-client.svg
     :target: https://pypi.org/project/google-cloud-dataflow-client
.. |PyPI-google-cloud-documentai-toolbox| image:: https://img.shields.io/pypi/v/google-cloud-documentai-toolbox.svg
     :target: https://pypi.org/project/google-cloud-documentai-toolbox
.. |PyPI-google-cloud-error-reporting| image:: https://img.shields.io/pypi/v/google-cloud-error-reporting.svg
     :target: https://pypi.org/project/google-cloud-error-reporting
.. |PyPI-google-cloud-run| image:: https://img.shields.io/pypi/v/google-cloud-run.svg
     :target: https://pypi.org/project/google-cloud-run
.. |PyPI-google-cloud-runtimeconfig| image:: https://img.shields.io/pypi/v/google-cloud-runtimeconfig.svg
     :target: https://pypi.org/project/google-cloud-runtimeconfig
.. |PyPI-sqlalchemy-bigquery| image:: https://img.shields.io/pypi/v/sqlalchemy-bigquery.svg
     :target: https://pypi.org/project/sqlalchemy-bigquery
.. |PyPI-google-cloud-video-stitcher| image:: https://img.shields.io/pypi/v/google-cloud-video-stitcher.svg
     :target: https://pypi.org/project/google-cloud-video-stitcher
.. |PyPI-google-cloud-gsuiteaddons| image:: https://img.shields.io/pypi/v/google-cloud-gsuiteaddons.svg
     :target: https://pypi.org/project/google-cloud-gsuiteaddons

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
