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

-  `Google Cloud Asset`_ (`Asset README`_, `Asset Documentation`_)
-  `Google Cloud AutoML`_ (`AutoML README`_, `AutoML Documentation`_)
-  `Google BigQuery`_ (`BigQuery README`_, `BigQuery Documentation`_)
-  `Google BigQuery Data Transfer`_ (`BigQuery Data Transfer README`_, `BigQuery Data Transfer Documentation`_)
-  `Google BigQuery Storage`_ (`BigQuery Storage README`_, `BigQuery Storage Documentation`_)
-  `Google Cloud Bigtable`_ (`Bigtable README`_, `Bigtable Documentation`_)
-  `Google Cloud Billing`_ (`Billing README`_, `Billing Documentation`_)
-  `Google Cloud Build`_ (`Cloud Build README`_, `Cloud Build Documentation`_)
-  `Google Cloud Container`_ (`Container README`_, `Container Documentation`_)
-  `Google Cloud Container Analysis`_ (`Container Analysis README`_, `Container Analysis Documentation`_)
-  `Google Cloud Dataproc`_ (`Dataproc README`_, `Dataproc Documentation`_)
-  `Google Cloud Datastore`_ (`Datastore README`_, `Datastore Documentation`_)
-  `Google Cloud DLP`_ (`DLP README`_, `DLP Documentation`_)
-  `Google Cloud Firestore`_ (`Firestore README`_, `Firestore Documentation`_)
-  `Google Cloud IAM Credentials`_ (`IAM Credentials README`_, `IAM Credentials Documentation`_)
-  `Google Cloud IoT`_ (`IoT README`_, `IoT Documentation`_)
-  `Google Cloud KMS`_ (`KMS README`_, `KMS Documentation`_)
-  `Google Cloud Memorystore for Redis`_ (`Redis README`_, `Redis Documentation`_)
-  `Google Cloud Monitoring Dashboards`_ (`Monitoring Dashboards README`_, `Monitoring Dashboards Documentation`_)
-  `Google Cloud Natural Language`_ (`Natural Language README`_, `Natural Language Documentation`_)
-  `Google Cloud OS Login`_ (`OS Login README`_, `OS Login Documentation`_)
-  `Google Cloud Pub/Sub`_ (`Pub/Sub README`_, `Pub/Sub Documentation`_)
-  `Google Cloud Recommender`_ (`Recommender README`_, `Recommender Documentation`_)
-  `Google Cloud Scheduler`_ (`Scheduler README`_, `Scheduler Documentation`_)
-  `Google Cloud Secret Manager`_ (`Secret Manager README`_, `Secret Manager Documentation`_)
-  `Google Cloud Spanner`_ (`Spanner README`_, `Spanner Documentation`_)
-  `Google Cloud Speech to Text`_ (`Speech to Text README`_, `Speech to Text Documentation`_)
-  `Google Cloud Storage`_ (`Storage README`_, `Storage Documentation`_)
-  `Google Cloud Tasks`_ (`Tasks README`_, `Tasks Documentation`_)
-  `Google Cloud Text-to-Speech`_ (`Text-to-Speech README`_, `Text-to-Speech Documentation`_)
-  `Google Cloud Translation`_ (`Translation README`_, `Translation Documentation`_)
-  `Google Cloud Video Intelligence`_ (`Video Intelligence README`_, `Video Intelligence Documentation`_)
-  `Google Cloud Vision`_ (`Vision README`_, `Vision Documentation`_)
-  `Stackdriver Logging`_ (`Logging README`_, `Logging Documentation`_)
-  `Stackdriver Monitoring`_ (`Monitoring README`_, `Monitoring Documentation`_)

.. _Google Cloud Asset: https://pypi.org/project/google-cloud-asset/
.. _Asset README: https://github.com/googleapis/python-asset
.. _Asset Documentation: https://googleapis.dev/python/cloudasset/latest

.. _Google Cloud AutoML: https://pypi.org/project/google-cloud-automl/
.. _AutoML README: https://github.com/googleapis/python-automl
.. _AutoML Documentation: https://googleapis.dev/python/automl/latest

.. _Google BigQuery: https://pypi.org/project/google-cloud-bigquery/
.. _BigQuery README: https://github.com/googleapis/python-bigquery#python-client-for-google-bigquery
.. _BigQuery Documentation: https://googleapis.dev/python/bigquery/latest

.. _Google BigQuery Data Transfer: https://pypi.org/project/google-cloud-bigquery-datatransfer/
.. _BigQuery Data Transfer README: https://github.com/googleapis/python-bigquery-datatransfer
.. _BigQuery Data Transfer Documentation: https://googleapis.dev/python/bigquerydatatransfer/latest/index.html

.. _Google BigQuery Storage: https://pypi.org/project/google-cloud-bigquery-storage/
.. _BigQuery Storage README: https://github.com/googleapis/python-bigquery-storage/
.. _BigQuery Storage Documentation: https://googleapis.dev/python/bigquerystorage/latest/index.html

.. _Google Cloud Bigtable: https://pypi.org/project/google-cloud-bigtable/
.. _Bigtable README: https://github.com/googleapis/python-bigtable
.. _Bigtable Documentation: https://googleapis.dev/python/bigtable/latest

.. _Google Cloud Billing: https://pypi.org/project/google-cloud-billing/
.. _Billing README: https://github.com/googleapis/python-billing
.. _Billing Documentation: https://googleapis.dev/python/cloudbilling/latest

.. _Google Cloud Build: https://pypi.org/project/google-cloud-build/
.. _Cloud Build README: https://github.com/googleapis/python-cloudbuild
.. _Cloud Build Documentation: https://googleapis.dev/python/cloudbuild/latest

.. _Google Cloud Container: https://pypi.org/project/google-cloud-container/
.. _Container README: https://github.com/googleapis/python-container
.. _Container Documentation: https://googleapis.dev/python/container/latest

.. _Google Cloud Container Analysis: https://pypi.org/project/google-cloud-containeranalysis/
.. _Container Analysis README: https://github.com/googleapis/python-containeranalysis
.. _Container Analysis Documentation: https://googleapis.dev/python/containeranalysis/latest

.. _Google Cloud Dataproc: https://pypi.org/project/google-cloud-dataproc/
.. _Dataproc README: https://github.com/googleapis/python-dataproc
.. _Dataproc Documentation: https://googleapis.dev/python/dataproc/latest

.. _Google Cloud Datastore: https://pypi.org/project/google-cloud-datastore/
.. _Datastore README: https://github.com/googleapis/python-datastore
.. _Datastore Documentation: https://googleapis.dev/python/datastore/latest

.. _Google Cloud DLP: https://pypi.org/project/google-cloud-dlp/
.. _DLP README: https://github.com/googleapis/python-dlp#python-client-for-cloud-data-loss-prevention-dlp-api
.. _DLP Documentation: https://googleapis.dev/python/dlp/latest

.. _Google Cloud Firestore: https://pypi.org/project/google-cloud-firestore/
.. _Firestore README: https://github.com/googleapis/python-firestore
.. _Firestore Documentation: https://googleapis.dev/python/firestore/latest

.. _Google Cloud IAM Credentials: https://pypi.org/project/google-cloud-iam/
.. _IAM Credentials README: https://github.com/googleapis/python-iam
.. _IAM Credentials Documentation: https://googleapis.dev/python/iam/latest

.. _Google Cloud IoT: https://pypi.org/project/google-cloud-iot/
.. _IoT README: https://github.com/googleapis/python-iot/
.. _IoT Documentation: https://googleapis.dev/python/cloudiot/latest

.. _Google Cloud KMS: https://pypi.org/project/google-cloud-kms/
.. _KMS README: https://github.com/googleapis/python-kms
.. _KMS Documentation: https://googleapis.dev/python/cloudkms/latest

.. _Google Cloud Memorystore for Redis: https://pypi.org/project/google-cloud-redis/
.. _Redis README: https://github.com/googleapis/python-redis
.. _Redis Documentation: https://googleapis.dev/python/redis/latest

.. _Google Cloud Monitoring Dashboards: https://pypi.org/project/google-cloud-monitoring-dashboards/
.. _Monitoring Dashboards README: https://github.com/googleapis/python-monitoring-dashboards
.. _Monitoring Dashboards Documentation: https://googleapis.dev/python/monitoring-dashboards/latest

.. _Google Cloud Natural Language: https://pypi.org/project/google-cloud-language/
.. _Natural Language README: https://github.com/googleapis/python-language
.. _Natural Language Documentation: https://googleapis.dev/python/language/latest

.. _Google Cloud OS Login: https://pypi.org/project/google-cloud-os-login/
.. _OS Login README: https://github.com/googleapis/python-oslogin
.. _OS Login Documentation: https://googleapis.dev/python/oslogin/latest

.. _Google Cloud Pub/Sub: https://pypi.org/project/google-cloud-pubsub/
.. _Pub/Sub README: https://github.com/googleapis/python-pubsub
.. _Pub/Sub Documentation: https://googleapis.dev/python/pubsub/latest

.. _Google Cloud Recommender: https://pypi.org/project/google-cloud-recommender/
.. _Recommender README: https://github.com/googleapis/python-recommender
.. _Recommender Documentation: https://googleapis.dev/python/recommender/latest

.. _Google Cloud Scheduler: https://pypi.org/project/google-cloud-scheduler/
.. _Scheduler README: https://github.com/googleapis/python-scheduler
.. _Scheduler Documentation: https://googleapis.dev/python/cloudscheduler/latest

.. _Google Cloud Secret Manager: https://pypi.org/project/google-cloud-secret-manager/
.. _Secret Manager README: https://github.com/googleapis/python-secret-manager
.. _Secret Manager Documentation: https://googleapis.dev/python/secretmanager/latest

.. _Google Cloud Spanner: https://pypi.org/project/google-cloud-spanner
.. _Spanner README: https://github.com/googleapis/python-spanner
.. _Spanner Documentation: https://googleapis.dev/python/spanner/latest

.. _Google Cloud Speech to Text: https://pypi.org/project/google-cloud-speech/
.. _Speech to Text README: https://github.com/googleapis/python-speech
.. _Speech to Text Documentation: https://googleapis.dev/python/speech/latest

.. _Google Cloud Storage: https://pypi.org/project/google-cloud-storage/
.. _Storage README: https://github.com/googleapis/python-storage
.. _Storage Documentation: https://googleapis.dev/python/storage/latest

.. _Google Cloud Tasks: https://pypi.org/project/google-cloud-tasks/
.. _Tasks README: https://github.com/googleapis/python-tasks
.. _Tasks Documentation: https://googleapis.dev/python/cloudtasks/latest

.. _Google Cloud Text-to-Speech: https://pypi.org/project/google-cloud-texttospeech/
.. _Text-to-Speech README: https://github.com/googleapis/python-texttospeech#python-client-for-cloud-text-to-speech-api
.. _Text-to-Speech Documentation: https://googleapis.dev/python/texttospeech/latest

.. _Google Cloud Translation: https://pypi.org/project/google-cloud-translate/
.. _Translation README: https://github.com/googleapis/python-translate#python-client-for-google-cloud-translation
.. _Translation Documentation: https://googleapis.dev/python/translation/latest

.. _Google Cloud Video Intelligence: https://pypi.org/project/google-cloud-videointelligence
.. _Video Intelligence README: https://github.com/googleapis/python-videointelligence
.. _Video Intelligence Documentation: https://googleapis.dev/python/videointelligence/latest

.. _Google Cloud Vision: https://pypi.org/project/google-cloud-vision/
.. _Vision README: https://github.com/googleapis/python-vision
.. _Vision Documentation: https://googleapis.dev/python/vision/latest

.. _Stackdriver Logging: https://pypi.org/project/google-cloud-logging/
.. _Logging README: https://github.com/googleapis/python-logging
.. _Logging Documentation: https://googleapis.dev/python/logging/latest

.. _Stackdriver Monitoring: https://pypi.org/project/google-cloud-monitoring/
.. _Monitoring README: https://github.com/googleapis/python-monitoring
.. _Monitoring Documentation: https://googleapis.dev/python/monitoring/latest


Beta Support
------------

**Beta** indicates that the client library for a particular service is
mostly stable and is being prepared for release. Issues and requests
against beta libraries are addressed with a higher priority.

The following client libraries have **beta** support:

-  `Google Cloud Access Approval`_ (`Access Approval README`_, `Access Approval Documentation`_)
-  `Google Cloud Billing Budgets`_ (`Billing Budgets README`_, `Billing Budgets Documentation`_)
-  `Google Cloud Data Catalog`_ (`Data Catalog README`_, `Data Catalog Documentation`_)
-  `Google Cloud Data Labeling`_ (`Data Labeling README`_, `Data Labeling Documentation`_)
-  `Google Cloud Notebooks`_ (`Notebooks README`_, `Notebooks Documentation`_)
-  `Google Cloud OS Config`_ (`OS Config README`_, `OS Config Documentation`_)
-  `Google Cloud Phishing Protection`_ (`Phishing Protection README`_, `Phishing Protection Documentation`_)
-  `Google Cloud Runtime Configuration`_ (`Runtime Config README`_, `Runtime Config Documentation`_)
-  `Google Cloud Talent`_ (`Talent README`_, `Talent Documentation`_)
-  `Stackdriver Error Reporting`_ (`Error Reporting README`_, `Error Reporting Documentation`_)

.. _Google Cloud Access Approval: https://pypi.org/project/google-cloud-access-approval/
.. _Access Approval README: https://github.com/googleapis/python-access-approval
.. _Access Approval Documentation: https://googleapis.dev/python/accessapproval/latest

.. _Google Cloud Billing Budgets: https://pypi.org/project/google-cloud-billing-budgets/
.. _Billing Budgets README: https://github.com/googleapis/python-billingbudgets
.. _Billing Budgets Documentation: https://googleapis.dev/python/billingbudgets/latest

.. _Google Cloud Data Catalog: https://pypi.org/project/google-cloud-datacatalog/
.. _Data Catalog README: https://github.com/googleapis/python-datacatalog
.. _Data Catalog Documentation: https://googleapis.dev/python/datacatalog/latest

.. _Google Cloud Data Labeling: https://pypi.org/project/google-cloud-datalabeling/
.. _Data Labeling README: https://github.com/googleapis/python-datalabeling#python-client-for-data-labeling-api-beta
.. _Data Labeling Documentation: https://googleapis.dev/python/datalabeling/latest

.. _Google Cloud Notebooks: https://pypi.org/project/google-cloud-notebooks/
.. _Notebooks README: https://github.com/googleapis/python-notebooks
.. _Notebooks Documentation: https://googleapis.dev/python/notebooks/latest

.. _Google Cloud OS Config: https://pypi.org/project/google-cloud-os-config
.. _OS Config README: https://github.com/googleapis/python-os-config
.. _OS Config Documentation: https://googleapis.dev/python/osconfig/latest

.. _Google Cloud Phishing Protection: https://pypi.org/project/google-cloud-phishing-protection/
.. _Phishing Protection README: https://github.com/googleapis/python-phishingprotection
.. _Phishing Protection Documentation: https://googleapis.dev/python/phishingprotection/latest

.. _Google Cloud Runtime Configuration: https://pypi.org/project/google-cloud-runtimeconfig/
.. _Runtime Config README: https://github.com/googleapis/python-runtimeconfig
.. _Runtime Config Documentation: https://googleapis.dev/python/runtimeconfig/latest

.. _Google Cloud Talent: https://pypi.org/project/google-cloud-talent/
.. _Talent README: https://github.com/googleapis/python-talent
.. _Talent Documentation: https://googleapis.dev/python/talent/latest

.. _Stackdriver Error Reporting: https://pypi.org/project/google-cloud-error-reporting/
.. _Error Reporting README: https://github.com/googleapis/python-error-reporting#python-client-for-stackdriver-error-reporting
.. _Error Reporting Documentation: https://googleapis.dev/python/clouderrorreporting/latest


Alpha Support
-------------

**Alpha** indicates that the client library for a particular service is
still a work-in-progress and is more likely to get backwards-incompatible
updates. See `versioning`_ for more details.

The following client libraries have **alpha** support:

-  `Google Cloud Bigtable - HappyBase`_ (`HappyBase README`_, `HappyBase Documentation`_)
-  `Google Cloud DNS`_ (`DNS README`_, `DNS Documentation`_)
-  `Google Cloud Resource Manager`_ (`Resource Manager README`_, `Resource Manager Documentation`_)
-  `Google Cloud Security Command Center`_ (`Security Center README`_, `Security Center Documentation`_)
-  `Google Cloud Security Scanner`_ (`Security Scanner README`_ , `Security Scanner Documentation`_)
-  `Google Cloud Trace`_ (`Trace README`_, `Trace Documentation`_)
-  `Grafeas`_ (`Grafeas README`_, `Grafeas Documentation`_)
-  `Webrisk`_ (`Webrisk README`_, `Webrisk Documentation`_)

.. _Google Cloud Bigtable - HappyBase: https://pypi.org/project/google-cloud-happybase/
.. _HappyBase README: https://github.com/googleapis/google-cloud-python-happybase
.. _HappyBase Documentation: https://google-cloud-python-happybase.readthedocs.io/en/latest/

.. _Google Cloud DNS: https://pypi.org/project/google-cloud-dns/
.. _DNS README: https://github.com/googleapis/python-dns#python-client-for-google-cloud-dns
.. _DNS Documentation: https://googleapis.dev/python/dns/latest

.. _Google Cloud Resource Manager: https://pypi.org/project/google-cloud-resource-manager/
.. _Resource Manager README: https://github.com/googleapis/python-resource-manager
.. _Resource Manager Documentation: https://googleapis.dev/python/cloudresourcemanager/latest

.. _Google Cloud Security Command Center: https://pypi.org/project/google-cloud-securitycenter/
.. _Security Center README: https://github.com/googleapis/python-securitycenter
.. _Security Center Documentation: https://googleapis.dev/python/securitycenter/latest/index.html

.. _Google Cloud Security Scanner: https://pypi.org/project/google-cloud-websecurityscanner/
.. _Security Scanner README: https://github.com/googleapis/google-cloud-python/blob/master/websecurityscanner
.. _Security Scanner Documentation: https://googleapis.dev/python/websecurityscanner/latest

.. _Google Cloud Trace: https://pypi.org/project/google-cloud-trace/
.. _Trace README: https://github.com/googleapis/python-trace
.. _Trace Documentation: https://googleapis.dev/python/cloudtrace/latest

.. _Grafeas: https://pypi.org/project/grafeas/
.. _Grafeas README: https://github.com/googleapis/python-grafeas#python-client-for-grafeas-api-alpha
.. _Grafeas Documentation: https://googleapis.dev/python/grafeas/latest

.. _Webrisk: https://pypi.org/project/google-cloud-webrisk
.. _Webrisk README: https://github.com/googleapis/python-webrisk#python-client-for-web-risk-api-alpha
.. _Webrisk Documentation: https://googleapis.dev/python/webrisk/latest

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



License
-------

Apache 2.0 - See `the LICENSE`_ for more information.

.. _the LICENSE: https://github.com/googleapis/google-cloud-python/blob/master/LICENSE
