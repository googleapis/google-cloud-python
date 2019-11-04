Google Cloud Python Client
==========================

Python idiomatic clients for `Google Cloud Platform`_ services.

.. _Google Cloud Platform: https://cloud.google.com/

**Heads up**! These libraries are supported on App Engine standard's `Python 3 runtime`_ but are *not* supported on App Engine's `Python 2 runtime`_.

.. _Python 3 runtime: https://cloud.google.com/appengine/docs/standard/python3
.. _Python 2 runtime: https://cloud.google.com/appengine/docs/standard/python

General Availability
--------------------

**GA** (general availability) indicates that the client library for a
particular service is stable, and that the code surface will not change in
backwards-incompatible ways unless either absolutely necessary (e.g. because
of critical security issues) or with an extensive deprecation period.
Issues and requests against GA libraries are addressed with the highest
priority.

.. note::

    Sub-components of GA libraries explicitly marked as beta in the
    import path (e.g. ``google.cloud.language_v1beta2``) should be considered
    to be beta.

The following client libraries have **GA** support:

-  `Google BigQuery`_ (`BigQuery README`_, `BigQuery Documentation`_)
-  `Google Cloud Bigtable`_ (`Bigtable README`_, `Bigtable Documentation`_)
-  `Google Cloud Datastore`_ (`Datastore README`_, `Datastore Documentation`_)
-  `Google Cloud KMS`_ (`KMS README`_, `KMS Documentation`_)
-  `Google Cloud Natural Language`_ (`Natural Language README`_, `Natural Language Documentation`_)
-  `Google Cloud Pub/Sub`_ (`Pub/Sub README`_, `Pub/Sub Documentation`_)
-  `Google Cloud Scheduler`_ (`Scheduler README`_, `Scheduler Documentation`_)
-  `Google Cloud Spanner`_ (`Spanner README`_, `Spanner Documentation`_)
-  `Google Cloud Speech to Text`_ (`Speech to Text README`_, `Speech to Text Documentation`_)
-  `Google Cloud Storage`_ (`Storage README`_, `Storage Documentation`_)
-  `Google Cloud Tasks`_ (`Tasks README`_, `Tasks Documentation`_)
-  `Google Cloud Translation`_ (`Translation README`_, `Translation Documentation`_)
-  `Stackdriver Logging`_ (`Logging README`_, `Logging Documentation`_)

.. _Google BigQuery: https://pypi.org/project/google-cloud-bigquery/
.. _BigQuery README: https://github.com/googleapis/google-cloud-python/tree/master/bigquery
.. _BigQuery Documentation: https://googleapis.dev/python/bigquery/latest

.. _Google Cloud Bigtable: https://pypi.org/project/google-cloud-bigtable/
.. _Bigtable README: https://github.com/googleapis/google-cloud-python/tree/master/bigtable
.. _Bigtable Documentation: https://googleapis.dev/python/bigtable/latest

.. _Google Cloud Datastore: https://pypi.org/project/google-cloud-datastore/
.. _Datastore README: https://github.com/googleapis/google-cloud-python/tree/master/datastore
.. _Datastore Documentation: https://googleapis.dev/python/datastore/latest 

.. _Google Cloud KMS: https://pypi.org/project/google-cloud-kms/
.. _KMS README: https://github.com/googleapis/google-cloud-python/tree/master/kms
.. _KMS Documentation: https://googleapis.dev/python/cloudkms/latest

.. _Google Cloud Natural Language: https://pypi.org/project/google-cloud-language/
.. _Natural Language README: https://github.com/googleapis/google-cloud-python/tree/master/language
.. _Natural Language Documentation: https://googleapis.dev/python/language/latest

.. _Google Cloud Pub/Sub: https://pypi.org/project/google-cloud-pubsub/
.. _Pub/Sub README: https://github.com/googleapis/google-cloud-python/tree/master/pubsub
.. _Pub/Sub Documentation: https://googleapis.dev/python/pubsub/latest

.. _Google Cloud Spanner: https://pypi.org/project/google-cloud-spanner
.. _Spanner README: https://github.com/googleapis/google-cloud-python/tree/master/spanner
.. _Spanner Documentation: https://googleapis.dev/python/spanner/latest

.. _Google Cloud Speech to Text: https://pypi.org/project/google-cloud-speech/
.. _Speech to Text README: https://github.com/googleapis/google-cloud-python/tree/master/speech
.. _Speech to Text Documentation: https://googleapis.dev/python/speech/latest

.. _Google Cloud Storage: https://pypi.org/project/google-cloud-storage/
.. _Storage README: https://github.com/googleapis/google-cloud-python/tree/master/storage
.. _Storage Documentation: https://googleapis.dev/python/storage/latest

.. _Google Cloud Tasks: https://pypi.org/project/google-cloud-tasks/
.. _Tasks README: https://github.com/googleapis/google-cloud-python/tree/master/tasks
.. _Tasks Documentation: https://googleapis.dev/python/cloudtasks/latest

.. _Google Cloud Translation: https://pypi.org/project/google-cloud-translate/
.. _Translation README: https://github.com/googleapis/google-cloud-python/tree/master/translate
.. _Translation Documentation: https://googleapis.dev/python/translation/latest

.. _Google Cloud Scheduler: https://pypi.org/project/google-cloud-scheduler/
.. _Scheduler README: https://github.com/googleapis/google-cloud-python/tree/master/scheduler
.. _Scheduler Documentation: https://googleapis.dev/python/cloudscheduler/latest

.. _Stackdriver Logging: https://pypi.org/project/google-cloud-logging/
.. _Logging README: https://github.com/googleapis/google-cloud-python/tree/master/logging
.. _Logging Documentation: https://googleapis.dev/python/logging/latest

Beta Support
------------

**Beta** indicates that the client library for a particular service is
mostly stable and is being prepared for release. Issues and requests
against beta libraries are addressed with a higher priority.

The following client libraries have **beta** support:

-  `Google Cloud Firestore`_ (`Firestore README`_, `Firestore Documentation`_)
-  `Google Cloud Video Intelligence`_ (`Video Intelligence README`_, `Video Intelligence Documentation`_)
-  `Google Cloud Vision`_ (`Vision README`_, `Vision Documentation`_)

.. _Google Cloud Firestore: https://pypi.org/project/google-cloud-firestore/
.. _Firestore README: https://github.com/googleapis/google-cloud-python/tree/master/firestore
.. _Firestore Documentation: https://googleapis.dev/python/firestore/latest

.. _Google Cloud Video Intelligence: https://pypi.org/project/google-cloud-videointelligence
.. _Video Intelligence README: https://github.com/googleapis/google-cloud-python/tree/master/videointelligence
.. _Video Intelligence Documentation: https://googleapis.dev/python/videointelligence/latest

.. _Google Cloud Vision: https://pypi.org/project/google-cloud-vision/
.. _Vision README: https://github.com/googleapis/google-cloud-python/tree/master/vision
.. _Vision Documentation: https://googleapis.dev/python/vision/latest


Alpha Support
-------------

**Alpha** indicates that the client library for a particular service is
still a work-in-progress and is more likely to get backwards-incompatible
updates. See `versioning`_ for more details.

The following client libraries have **alpha** support:

-  `Google Cloud Asset`_ (`Asset README`_, `Asset Documentation`_)
-  `Google Cloud AutoML`_ (`AutoML README`_, `AutoML Documentation`_)
-  `Google BigQuery Data Transfer`_ (`BigQuery Data Transfer README`_, `BigQuery Documentation`_)
-  `Google Cloud Bigtable - HappyBase`_ (`HappyBase README`_, `HappyBase Documentation`_)
-  `Google Cloud Container`_ (`Container README`_, `Container Documentation`_)
-  `Google Cloud Container Analysis`_ (`Container Analysis README`_, `Container Analysis Documentation`_)
-  `Google Cloud Dataproc`_ (`Dataproc README`_, `Dataproc Documentation`_)
-  `Google Cloud DLP`_ (`DLP README`_, `DLP Documentation`_)
-  `Google Cloud DNS`_ (`DNS README`_, `DNS Documentation`_)
-  `Google Cloud IoT`_ (`IoT README`_, `IoT Documentation`_)
-  `Google Cloud Memorystore for Redis`_ (`Redis README`_, `Redis Documentation`_)
-  `Google Cloud Recommender`_ (`Recommender README`_, `Recommender Documentation`_)
-  `Google Cloud Resource Manager`_ (`Resource Manager README`_, `Resource Manager Documentation`_)
-  `Google Cloud Runtime Configuration`_ (`Runtime Config README`_, `Runtime Config Documentation`_)
-  `Google Cloud Security Scanner`_ (`Security Scanner README`_ , `Security Scanner Documentation`_)
-  `Google Cloud Trace`_ (`Trace README`_, `Trace Documentation`_)
-  `Google Cloud Text-to-Speech`_ (`Text-to-Speech README`_, `Text-to-Speech Documentation`_)
-  `Grafeas`_ (`Grafeas README`_, `Grafeas Documentation`_)
-  `Stackdriver Error Reporting`_ (`Error Reporting README`_, `Error Reporting Documentation`_)
-  `Stackdriver Monitoring`_ (`Monitoring README`_, `Monitoring Documentation`_)

.. _Google Cloud Asset: https://pypi.org/project/google-cloud-asset/
.. _Asset README: https://github.com/googleapis/google-cloud-python/blob/master/asset
.. _Asset Documentation: https://googleapis.dev/python/cloudasset/latest

.. _Google Cloud AutoML: https://pypi.org/project/google-cloud-automl/
.. _AutoML README: https://github.com/googleapis/google-cloud-python/blob/master/automl
.. _AutoML Documentation: https://googleapis.dev/python/automl/latest

.. _Google BigQuery Data Transfer: https://pypi.org/project/google-cloud-bigquery-datatransfer/
.. _BigQuery Data Transfer README: https://github.com/googleapis/google-cloud-python/tree/master/bigquery_datatransfer
.. _BigQuery Documentation: https://googleapis.dev/python/bigquery/latest

.. _Google Cloud Bigtable - HappyBase: https://pypi.org/project/google-cloud-happybase/
.. _HappyBase README: https://github.com/googleapis/google-cloud-python-happybase
.. _HappyBase Documentation: https://google-cloud-python-happybase.readthedocs.io/en/latest/

.. _Google Cloud Container: https://pypi.org/project/google-cloud-container/
.. _Container README: https://github.com/googleapis/google-cloud-python/tree/master/container
.. _Container Documentation: https://googleapis.dev/python/container/latest

.. _Google Cloud Container Analysis: https://pypi.org/project/google-cloud-containeranalysis/
.. _Container Analysis README: https://github.com/googleapis/google-cloud-python/tree/master/containeranalysis
.. _Container Analysis Documentation: https://googleapis.dev/python/containeranalysis/latest

.. _Google Cloud Dataproc: https://pypi.org/project/google-cloud-dataproc/
.. _Dataproc README: https://github.com/googleapis/google-cloud-python/tree/master/dataproc
.. _Dataproc Documentation: https://googleapis.dev/python/dataproc/latest

.. _Google Cloud DLP: https://pypi.org/project/google-cloud-dlp/
.. _DLP README: https://github.com/googleapis/google-cloud-python/tree/master/dlp
.. _DLP Documentation: https://googleapis.dev/python/dlp/latest

.. _Google Cloud DNS: https://pypi.org/project/google-cloud-dns/
.. _DNS README: https://github.com/googleapis/google-cloud-python/tree/master/dns
.. _DNS Documentation: https://googleapis.dev/python/dns/latest

.. _Google Cloud IoT: https://pypi.org/project/google-cloud-iot/
.. _IoT README: https://github.com/googleapis/google-cloud-python/tree/master/iot
.. _IoT Documentation: https://googleapis.dev/python/cloudiot/latest

.. _Google Cloud Memorystore for Redis: https://pypi.org/project/google-cloud-redis/
.. _Redis README: https://github.com/googleapis/google-cloud-python/tree/master/redis
.. _Redis Documentation: https://googleapis.dev/python/redis/latest

.. _Google Cloud Recommender: https://pypi.org/project/google-cloud-recommender/
.. _Recommender README: https://github.com/googleapis/google-cloud-python/tree/master/recommender
.. _Recommender Documentation: https://googleapis.dev/python/recommender/latest

.. _Google Cloud Resource Manager: https://pypi.org/project/google-cloud-resource-manager/
.. _Resource Manager README: https://github.com/googleapis/google-cloud-python/tree/master/resource_manager
.. _Resource Manager Documentation: https://googleapis.dev/python/cloudresourcemanager/latest

.. _Google Cloud Runtime Configuration: https://pypi.org/project/google-cloud-runtimeconfig/
.. _Runtime Config README: https://github.com/googleapis/google-cloud-python/tree/master/runtimeconfig
.. _Runtime Config Documentation: https://googleapis.dev/python/runtimeconfig/latest

.. _Google Cloud Security Scanner: https://pypi.org/project/google-cloud-websecurityscanner/
.. _Security Scanner README: https://github.com/googleapis/google-cloud-python/blob/master/websecurityscanner
.. _Security Scanner Documentation: https://googleapis.dev/python/websecurityscanner/latest

.. _Google Cloud Text-to-Speech: https://pypi.org/project/google-cloud-texttospeech/
.. _Text-to-Speech README: https://github.com/googleapis/google-cloud-python/tree/master/texttospeech
.. _Text-to-Speech Documentation: https://googleapis.dev/python/texttospeech/latest

.. _Google Cloud Trace: https://pypi.org/project/google-cloud-trace/
.. _Trace README: https://github.com/googleapis/google-cloud-python/tree/master/trace
.. _Trace Documentation: https://googleapis.dev/python/cloudtrace/latest

.. _Grafeas: https://pypi.org/project/grafeas/
.. _Grafeas README: https://github.com/googleapis/google-cloud-python/tree/master/grafeas
.. _Grafeas Documentation: https://googleapis.dev/python/grafeas/latest

.. _Stackdriver Error Reporting: https://pypi.org/project/google-cloud-error-reporting/
.. _Error Reporting README: https://github.com/googleapis/google-cloud-python/tree/master/error_reporting
.. _Error Reporting Documentation: https://googleapis.dev/python/clouderrorreporting/latest

.. _Stackdriver Monitoring: https://pypi.org/project/google-cloud-monitoring/
.. _Monitoring README: https://github.com/googleapis/google-cloud-python/tree/master/monitoring
.. _Monitoring Documentation: https://googleapis.dev/python/monitoring/latest

.. _versioning: https://github.com/googleapis/google-cloud-python/blob/master/CONTRIBUTING.rst#versioning

If you need support for other Google APIs, check out the
`Google APIs Python Client library`_.

.. _Google APIs Python Client library: https://github.com/google/google-api-python-client


Example Applications
--------------------

-  `getting-started-python`_ - A sample and `tutorial`_ that demonstrates how to build a complete web application using Cloud Datastore, Cloud Storage, and Cloud Pub/Sub and deploy it to Google App Engine or Google Compute Engine.
-  `google-cloud-python-expenses-demo`_ - A sample expenses demo using Cloud Datastore and Cloud Storage

.. _getting-started-python: https://github.com/GoogleCloudPlatform/getting-started-python
.. _tutorial: https://cloud.google.com/python
.. _google-cloud-python-expenses-demo: https://github.com/GoogleCloudPlatform/google-cloud-python-expenses-demo


Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as possible.
Check out the `Authentication section`_ in our documentation to learn more.
You may also find the `authentication document`_ shared by all the
``google-cloud-*`` libraries to be helpful.

.. _Authentication section: https://googleapis.dev/python/google-api-core/latest/auth.html
.. _authentication document: https://github.com/googleapis/google-cloud-common/tree/master/authentication

Contributing
------------

Contributions to this library are always welcome and highly encouraged.

See the `CONTRIBUTING doc`_ for more information on how to get started.

.. _CONTRIBUTING doc: https://github.com/googleapis/google-cloud-python/blob/master/CONTRIBUTING.rst


Community
---------

Google Cloud Platform Python developers hang out in `Slack`_ in the ``#python``
channel, click here to `get an invitation`_.

.. _Slack: https://googlecloud-community.slack.com
.. _get an invitation: https://gcp-slack.appspot.com/


License
-------

Apache 2.0 - See `the LICENSE`_ for more information.

.. _the LICENSE: https://github.com/googleapis/google-cloud-python/blob/master/LICENSE
