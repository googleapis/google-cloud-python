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
     - |ga|
     - |PyPI-google-cloud-aiplatform|
   * - `API Gateway <https://github.com/googleapis/python-api-gateway>`_
     - |ga|
     - |PyPI-google-cloud-api-gateway|
   * - `Access Approval <https://github.com/googleapis/python-access-approval>`_
     - |ga|
     - |PyPI-google-cloud-access-approval|
   * - `App Engine Admin API <https://github.com/googleapis/python-appengine-admin>`_
     - |ga|
     - |PyPI-google-cloud-appengine-admin|
   * - `Asset Inventory <https://github.com/googleapis/python-asset>`_
     - |ga|
     - |PyPI-google-cloud-asset|
   * - `AutoML <https://github.com/googleapis/python-automl>`_
     - |ga|
     - |PyPI-google-cloud-automl|
   * - `BigQuery <https://github.com/googleapis/python-bigquery>`_
     - |ga|
     - |PyPI-google-cloud-bigquery|
   * - `BigQuery Connection <https://github.com/googleapis/python-bigquery-connection>`_
     - |ga|
     - |PyPI-google-cloud-bigquery-connection|
   * - `BigQuery Data Transfer Service <https://github.com/googleapis/python-bigquery-datatransfer>`_
     - |ga|
     - |PyPI-google-cloud-bigquery-datatransfer|
   * - `BigQuery Reservation <https://github.com/googleapis/python-bigquery-reservation>`_
     - |ga|
     - |PyPI-google-cloud-bigquery-reservation|
   * - `BigQuery Storage <https://github.com/googleapis/python-bigquery-storage>`_
     - |ga|
     - |PyPI-google-cloud-bigquery-storage|
   * - `Bigtable <https://github.com/googleapis/python-bigtable>`_
     - |ga|
     - |PyPI-google-cloud-bigtable|
   * - `Billing <https://github.com/googleapis/python-billing>`_
     - |ga|
     - |PyPI-google-cloud-billing|
   * - `Build <https://github.com/googleapis/python-cloudbuild>`_
     - |ga|
     - |PyPI-google-cloud-build|
   * - `Channel Services <https://github.com/googleapis/python-channel>`_
     - |ga|
     - |PyPI-google-cloud-channel|
   * - `Container Analysis <https://github.com/googleapis/python-containeranalysis>`_
     - |ga|
     - |PyPI-google-cloud-containeranalysis|
   * - `Data Catalog <https://github.com/googleapis/python-datacatalog>`_
     - |ga|
     - |PyPI-google-cloud-datacatalog|
   * - `Data Loss Prevention <https://github.com/googleapis/python-dlp>`_
     - |ga|
     - |PyPI-google-cloud-dlp|
   * - `Dataproc <https://github.com/googleapis/python-dataproc>`_
     - |ga|
     - |PyPI-google-cloud-dataproc|
   * - `Datastore <https://github.com/googleapis/python-datastore>`_
     - |ga|
     - |PyPI-google-cloud-datastore|
   * - `Dialogflow <https://github.com/googleapis/python-dialogflow>`_
     - |ga|
     - |PyPI-google-cloud-dialogflow|
   * - `Document Understanding API <https://github.com/googleapis/python-documentai>`_
     - |ga|
     - |PyPI-google-cloud-documentai|
   * - `Firestore <https://github.com/googleapis/python-firestore>`_
     - |ga|
     - |PyPI-google-cloud-firestore|
   * - `Grafeas <https://github.com/googleapis/python-grafeas>`_
     - |ga|
     - |PyPI-grafeas|
   * - `IAM Policy Troubleshooter API <https://github.com/googleapis/python-policy-troubleshooter>`_
     - |ga|
     - |PyPI-google-cloud-policy-troubleshooter|
   * - `Identity and Access Management <https://github.com/googleapis/python-iam>`_
     - |ga|
     - |PyPI-google-cloud-iam|
   * - `Internet of Things (IoT) Core <https://github.com/googleapis/python-iot>`_
     - |ga|
     - |PyPI-google-cloud-iot|
   * - `Key Management Service <https://github.com/googleapis/python-kms>`_
     - |ga|
     - |PyPI-google-cloud-kms|
   * - `Kubernetes Engine <https://github.com/googleapis/python-container>`_
     - |ga|
     - |PyPI-google-cloud-container|
   * - `Logging <https://github.com/googleapis/python-logging>`_
     - |ga|
     - |PyPI-google-cloud-logging|
   * - `Memorystore for Memcached <https://github.com/googleapis/python-memcache>`_
     - |ga|
     - |PyPI-google-cloud-memcache|
   * - `Monitoring Dashboards <https://github.com/googleapis/python-monitoring-dashboards>`_
     - |ga|
     - |PyPI-google-cloud-monitoring-dashboards|
   * - `NDB Client Library for Datastore <https://github.com/googleapis/python-ndb>`_
     - |ga|
     - |PyPI-google-cloud-ndb|
   * - `Natural Language <https://github.com/googleapis/python-language>`_
     - |ga|
     - |PyPI-google-cloud-language|
   * - `OS Login <https://github.com/googleapis/python-oslogin>`_
     - |ga|
     - |PyPI-google-cloud-os-login|
   * - `Pub/Sub <https://github.com/googleapis/python-pubsub>`_
     - |ga|
     - |PyPI-google-cloud-pubsub|
   * - `Recommender API <https://github.com/googleapis/python-recommender>`_
     - |ga|
     - |PyPI-google-cloud-recommender|
   * - `Redis <https://github.com/googleapis/python-redis>`_
     - |ga|
     - |PyPI-google-cloud-redis|
   * - `Retail API <https://github.com/googleapis/python-retail>`_
     - |ga|
     - |PyPI-google-cloud-retail|
   * - `Scheduler <https://github.com/googleapis/python-scheduler>`_
     - |ga|
     - |PyPI-google-cloud-scheduler|
   * - `Secret Manager <https://github.com/googleapis/python-secret-manager>`_
     - |ga|
     - |PyPI-google-cloud-secret-manager|
   * - `Security Command Center <https://github.com/googleapis/python-securitycenter>`_
     - |ga|
     - |PyPI-google-cloud-securitycenter|
   * - `Security Scanner <https://github.com/googleapis/python-websecurityscanner>`_
     - |ga|
     - |PyPI-google-cloud-websecurityscanner|
   * - `Service Control API <https://github.com/googleapis/python-service-control>`_
     - |ga|
     - |PyPI-google-cloud-service-control|
   * - `Service Directory <https://github.com/googleapis/python-service-directory>`_
     - |ga|
     - |PyPI-google-cloud-service-directory|
   * - `Service Management API <https://github.com/googleapis/python-service-management>`_
     - |ga|
     - |PyPI-google-cloud-service-management|
   * - `Spanner <https://github.com/googleapis/python-spanner>`_
     - |ga|
     - |PyPI-google-cloud-spanner|
   * - `Speech <https://github.com/googleapis/python-speech>`_
     - |ga|
     - |PyPI-google-cloud-speech|
   * - `Stackdriver Monitoring <https://github.com/googleapis/python-monitoring>`_
     - |ga|
     - |PyPI-google-cloud-monitoring|
   * - `Storage <https://github.com/googleapis/python-storage>`_
     - |ga|
     - |PyPI-google-cloud-storage|
   * - `Tasks <https://github.com/googleapis/python-tasks>`_
     - |ga|
     - |PyPI-google-cloud-tasks|
   * - `Text-to-Speech <https://github.com/googleapis/python-texttospeech>`_
     - |ga|
     - |PyPI-google-cloud-texttospeech|
   * - `Trace <https://github.com/googleapis/python-trace>`_
     - |ga|
     - |PyPI-google-cloud-trace|
   * - `Translation <https://github.com/googleapis/python-translate>`_
     - |ga|
     - |PyPI-google-cloud-translate|
   * - `Video Intelligence <https://github.com/googleapis/python-videointelligence>`_
     - |ga|
     - |PyPI-google-cloud-videointelligence|
   * - `Vision <https://github.com/googleapis/python-vision>`_
     - |ga|
     - |PyPI-google-cloud-vision|
   * - `Web Risk <https://github.com/googleapis/python-webrisk>`_
     - |ga|
     - |PyPI-google-cloud-webrisk|
   * - `Workflows <https://github.com/googleapis/python-workflows>`_
     - |ga|
     - |PyPI-google-cloud-workflows|
   * - `AI Platform Notebooks <https://github.com/googleapis/python-notebooks>`_
     - |beta|
     - |PyPI-google-cloud-notebooks|
   * - `Analytics Data API <https://github.com/googleapis/python-analytics-data>`_
     - |beta|
     - |PyPI-google-analytics-data|
   * - `Apigee Connect API <https://github.com/googleapis/python-apigee-connect>`_
     - |beta|
     - |PyPI-google-cloud-apigee-connect|
   * - `App Engine Logging Protos <https://github.com/googleapis/python-appengine-logging>`_
     - |beta|
     - |PyPI-google-cloud-appengine-logging|
   * - `Artifact Registry <https://github.com/googleapis/python-artifact-registry>`_
     - |beta|
     - |PyPI-google-cloud-artifact-registry|
   * - `Assured Workloads for Government <https://github.com/googleapis/python-assured-workloads>`_
     - |beta|
     - |PyPI-google-cloud-assured-workloads|
   * - `Audit Log <https://github.com/googleapis/python-audit-log>`_
     - |beta|
     - |PyPI-google-cloud-audit-log|
   * - `BigQuery Logging Protos <https://github.com/googleapis/python-bigquery-logging>`_
     - |beta|
     - |PyPI-google-cloud-bigquery-logging|
   * - `Billing Budget <https://github.com/googleapis/python-billingbudgets>`_
     - |beta|
     - |PyPI-google-cloud-billing-budgets|
   * - `Binary Authorization <https://github.com/googleapis/python-binary-authorization>`_
     - |beta|
     - |PyPI-google-cloud-binary-authorization|
   * - `Data Labeling <https://github.com/googleapis/python-datalabeling>`_
     - |beta|
     - |PyPI-google-cloud-datalabeling|
   * - `Database Migration Service <https://github.com/googleapis/python-dms>`_
     - |beta|
     - |PyPI-google-cloud-dms|
   * - `Dataproc Metastore <https://github.com/googleapis/python-dataproc-metastore>`_
     - |beta|
     - |PyPI-google-cloud-dataproc-metastore|
   * - `Dialogflow CX <https://github.com/googleapis/python-dialogflow-cx>`_
     - |beta|
     - |PyPI-google-cloud-dialogflow-cx|
   * - `Domains <https://github.com/googleapis/python-domains>`_
     - |beta|
     - |PyPI-google-cloud-domains|
   * - `Error Reporting <https://github.com/googleapis/python-error-reporting>`_
     - |beta|
     - |PyPI-google-cloud-error-reporting|
   * - `Essential Contacts API <https://github.com/googleapis/python-essential-contacts>`_
     - |beta|
     - |PyPI-google-cloud-essential-contacts|
   * - `Functions <https://github.com/googleapis/python-functions>`_
     - |beta|
     - |PyPI-google-cloud-functions|
   * - `GKE Hub API <https://github.com/googleapis/python-gke-hub>`_
     - |beta|
     - |PyPI-google-cloud-gke-hub|
   * - `Game Servers <https://github.com/googleapis/python-game-servers>`_
     - |beta|
     - |PyPI-google-cloud-game-servers|
   * - `IAM Logging Protos <https://github.com/googleapis/python-iam-logging>`_
     - |beta|
     - |PyPI-google-cloud-iam-logging|
   * - `Life Sciences <https://github.com/googleapis/python-life-sciences>`_
     - |beta|
     - |PyPI-google-cloud-life-sciences|
   * - `Managed Service for Microsoft Active Directory <https://github.com/googleapis/python-managed-identities>`_
     - |beta|
     - |PyPI-google-cloud-managed-identities|
   * - `Media Translation <https://github.com/googleapis/python-media-translation>`_
     - |beta|
     - |PyPI-google-cloud-media-translation|
   * - `Phishing Protection <https://github.com/googleapis/python-phishingprotection>`_
     - |beta|
     - |PyPI-google-cloud-phishing-protection|
   * - `Private Catalog <https://github.com/googleapis/python-private-catalog>`_
     - |beta|
     - |PyPI-google-cloud-private-catalog|
   * - `Private Certificate Authority <https://github.com/googleapis/python-security-private-ca>`_
     - |beta|
     - |PyPI-google-cloud-private-ca|
   * - `Pub/Sub Lite <https://github.com/googleapis/python-pubsublite>`_
     - |beta|
     - |PyPI-google-cloud-pubsublite|
   * - `Recommendations AI <https://github.com/googleapis/python-recommendations-ai>`_
     - |beta|
     - |PyPI-google-cloud-recommendations-ai|
   * - `Resource Manager API <https://github.com/googleapis/python-resource-manager>`_
     - |beta|
     - |PyPI-google-cloud-resource-manager|
   * - `Runtime Configurator <https://github.com/googleapis/python-runtimeconfig>`_
     - |beta|
     - |PyPI-google-cloud-runtimeconfig|
   * - `SQLAlchemy dialect for BigQuery <https://github.com/googleapis/python-bigquery-sqlalchemy>`_
     - |beta|
     - |PyPI-pybigquery|
   * - `Service Usage <https://github.com/googleapis/python-service-usage>`_
     - |beta|
     - |PyPI-google-cloud-service-usage|
   * - `Shell <https://github.com/googleapis/python-shell>`_
     - |beta|
     - |PyPI-google-cloud-shell|
   * - `TPU <https://github.com/googleapis/python-tpu>`_
     - |beta|
     - |PyPI-google-cloud-tpu|
   * - `Talent Solution <https://github.com/googleapis/python-talent>`_
     - |beta|
     - |PyPI-google-cloud-talent|
   * - `Transcoder <https://github.com/googleapis/python-video-transcoder>`_
     - |beta|
     - |PyPI-google-cloud-video-transcoder|
   * - `Virtual Private Cloud <https://github.com/googleapis/python-vpc-access>`_
     - |beta|
     - |PyPI-google-cloud-vpc-access|
   * - `reCAPTCHA Enterprise <https://github.com/googleapis/python-recaptcha-enterprise>`_
     - |beta|
     - |PyPI-google-cloud-recaptcha-enterprise|
   * - `Analytics Admin <https://github.com/googleapis/python-analytics-admin>`_
     - |alpha|
     - |PyPI-google-analytics-admin|
   * - `Area 120 Tables API <https://github.com/googleapis/python-area120-tables>`_
     - |alpha|
     - |PyPI-google-area120-tables|
   * - `Compute Engine <https://github.com/googleapis/python-compute>`_
     - |alpha|
     - |PyPI-google-cloud-compute|
   * - `DNS <https://github.com/googleapis/python-dns>`_
     - |alpha|
     - |PyPI-google-cloud-dns|
   * - `Data QnA <https://github.com/googleapis/python-data-qna>`_
     - |alpha|
     - |PyPI-google-cloud-data-qna|
   * - `Network Connectivity Center <https://github.com/googleapis/python-network-connectivity>`_
     - |alpha|
     - |PyPI-google-cloud-network-connectivity|

.. |PyPI-google-cloud-aiplatform| image:: https://img.shields.io/pypi/v/google-cloud-aiplatform.svg
     :target: https://pypi.org/project/google-cloud-aiplatform
.. |PyPI-google-cloud-api-gateway| image:: https://img.shields.io/pypi/v/google-cloud-api-gateway.svg
     :target: https://pypi.org/project/google-cloud-api-gateway
.. |PyPI-google-cloud-access-approval| image:: https://img.shields.io/pypi/v/google-cloud-access-approval.svg
     :target: https://pypi.org/project/google-cloud-access-approval
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
.. |PyPI-google-cloud-billing| image:: https://img.shields.io/pypi/v/google-cloud-billing.svg
     :target: https://pypi.org/project/google-cloud-billing
.. |PyPI-google-cloud-build| image:: https://img.shields.io/pypi/v/google-cloud-build.svg
     :target: https://pypi.org/project/google-cloud-build
.. |PyPI-google-cloud-channel| image:: https://img.shields.io/pypi/v/google-cloud-channel.svg
     :target: https://pypi.org/project/google-cloud-channel
.. |PyPI-google-cloud-containeranalysis| image:: https://img.shields.io/pypi/v/google-cloud-containeranalysis.svg
     :target: https://pypi.org/project/google-cloud-containeranalysis
.. |PyPI-google-cloud-datacatalog| image:: https://img.shields.io/pypi/v/google-cloud-datacatalog.svg
     :target: https://pypi.org/project/google-cloud-datacatalog
.. |PyPI-google-cloud-dlp| image:: https://img.shields.io/pypi/v/google-cloud-dlp.svg
     :target: https://pypi.org/project/google-cloud-dlp
.. |PyPI-google-cloud-dataproc| image:: https://img.shields.io/pypi/v/google-cloud-dataproc.svg
     :target: https://pypi.org/project/google-cloud-dataproc
.. |PyPI-google-cloud-datastore| image:: https://img.shields.io/pypi/v/google-cloud-datastore.svg
     :target: https://pypi.org/project/google-cloud-datastore
.. |PyPI-google-cloud-dialogflow| image:: https://img.shields.io/pypi/v/google-cloud-dialogflow.svg
     :target: https://pypi.org/project/google-cloud-dialogflow
.. |PyPI-google-cloud-documentai| image:: https://img.shields.io/pypi/v/google-cloud-documentai.svg
     :target: https://pypi.org/project/google-cloud-documentai
.. |PyPI-google-cloud-firestore| image:: https://img.shields.io/pypi/v/google-cloud-firestore.svg
     :target: https://pypi.org/project/google-cloud-firestore
.. |PyPI-grafeas| image:: https://img.shields.io/pypi/v/grafeas.svg
     :target: https://pypi.org/project/grafeas
.. |PyPI-google-cloud-policy-troubleshooter| image:: https://img.shields.io/pypi/v/google-cloud-policy-troubleshooter.svg
     :target: https://pypi.org/project/google-cloud-policy-troubleshooter
.. |PyPI-google-cloud-iam| image:: https://img.shields.io/pypi/v/google-cloud-iam.svg
     :target: https://pypi.org/project/google-cloud-iam
.. |PyPI-google-cloud-iot| image:: https://img.shields.io/pypi/v/google-cloud-iot.svg
     :target: https://pypi.org/project/google-cloud-iot
.. |PyPI-google-cloud-kms| image:: https://img.shields.io/pypi/v/google-cloud-kms.svg
     :target: https://pypi.org/project/google-cloud-kms
.. |PyPI-google-cloud-container| image:: https://img.shields.io/pypi/v/google-cloud-container.svg
     :target: https://pypi.org/project/google-cloud-container
.. |PyPI-google-cloud-logging| image:: https://img.shields.io/pypi/v/google-cloud-logging.svg
     :target: https://pypi.org/project/google-cloud-logging
.. |PyPI-google-cloud-memcache| image:: https://img.shields.io/pypi/v/google-cloud-memcache.svg
     :target: https://pypi.org/project/google-cloud-memcache
.. |PyPI-google-cloud-monitoring-dashboards| image:: https://img.shields.io/pypi/v/google-cloud-monitoring-dashboards.svg
     :target: https://pypi.org/project/google-cloud-monitoring-dashboards
.. |PyPI-google-cloud-ndb| image:: https://img.shields.io/pypi/v/google-cloud-ndb.svg
     :target: https://pypi.org/project/google-cloud-ndb
.. |PyPI-google-cloud-language| image:: https://img.shields.io/pypi/v/google-cloud-language.svg
     :target: https://pypi.org/project/google-cloud-language
.. |PyPI-google-cloud-os-login| image:: https://img.shields.io/pypi/v/google-cloud-os-login.svg
     :target: https://pypi.org/project/google-cloud-os-login
.. |PyPI-google-cloud-pubsub| image:: https://img.shields.io/pypi/v/google-cloud-pubsub.svg
     :target: https://pypi.org/project/google-cloud-pubsub
.. |PyPI-google-cloud-recommender| image:: https://img.shields.io/pypi/v/google-cloud-recommender.svg
     :target: https://pypi.org/project/google-cloud-recommender
.. |PyPI-google-cloud-redis| image:: https://img.shields.io/pypi/v/google-cloud-redis.svg
     :target: https://pypi.org/project/google-cloud-redis
.. |PyPI-google-cloud-retail| image:: https://img.shields.io/pypi/v/google-cloud-retail.svg
     :target: https://pypi.org/project/google-cloud-retail
.. |PyPI-google-cloud-scheduler| image:: https://img.shields.io/pypi/v/google-cloud-scheduler.svg
     :target: https://pypi.org/project/google-cloud-scheduler
.. |PyPI-google-cloud-secret-manager| image:: https://img.shields.io/pypi/v/google-cloud-secret-manager.svg
     :target: https://pypi.org/project/google-cloud-secret-manager
.. |PyPI-google-cloud-securitycenter| image:: https://img.shields.io/pypi/v/google-cloud-securitycenter.svg
     :target: https://pypi.org/project/google-cloud-securitycenter
.. |PyPI-google-cloud-websecurityscanner| image:: https://img.shields.io/pypi/v/google-cloud-websecurityscanner.svg
     :target: https://pypi.org/project/google-cloud-websecurityscanner
.. |PyPI-google-cloud-service-control| image:: https://img.shields.io/pypi/v/google-cloud-service-control.svg
     :target: https://pypi.org/project/google-cloud-service-control
.. |PyPI-google-cloud-service-directory| image:: https://img.shields.io/pypi/v/google-cloud-service-directory.svg
     :target: https://pypi.org/project/google-cloud-service-directory
.. |PyPI-google-cloud-service-management| image:: https://img.shields.io/pypi/v/google-cloud-service-management.svg
     :target: https://pypi.org/project/google-cloud-service-management
.. |PyPI-google-cloud-spanner| image:: https://img.shields.io/pypi/v/google-cloud-spanner.svg
     :target: https://pypi.org/project/google-cloud-spanner
.. |PyPI-google-cloud-speech| image:: https://img.shields.io/pypi/v/google-cloud-speech.svg
     :target: https://pypi.org/project/google-cloud-speech
.. |PyPI-google-cloud-monitoring| image:: https://img.shields.io/pypi/v/google-cloud-monitoring.svg
     :target: https://pypi.org/project/google-cloud-monitoring
.. |PyPI-google-cloud-storage| image:: https://img.shields.io/pypi/v/google-cloud-storage.svg
     :target: https://pypi.org/project/google-cloud-storage
.. |PyPI-google-cloud-tasks| image:: https://img.shields.io/pypi/v/google-cloud-tasks.svg
     :target: https://pypi.org/project/google-cloud-tasks
.. |PyPI-google-cloud-texttospeech| image:: https://img.shields.io/pypi/v/google-cloud-texttospeech.svg
     :target: https://pypi.org/project/google-cloud-texttospeech
.. |PyPI-google-cloud-trace| image:: https://img.shields.io/pypi/v/google-cloud-trace.svg
     :target: https://pypi.org/project/google-cloud-trace
.. |PyPI-google-cloud-translate| image:: https://img.shields.io/pypi/v/google-cloud-translate.svg
     :target: https://pypi.org/project/google-cloud-translate
.. |PyPI-google-cloud-videointelligence| image:: https://img.shields.io/pypi/v/google-cloud-videointelligence.svg
     :target: https://pypi.org/project/google-cloud-videointelligence
.. |PyPI-google-cloud-vision| image:: https://img.shields.io/pypi/v/google-cloud-vision.svg
     :target: https://pypi.org/project/google-cloud-vision
.. |PyPI-google-cloud-webrisk| image:: https://img.shields.io/pypi/v/google-cloud-webrisk.svg
     :target: https://pypi.org/project/google-cloud-webrisk
.. |PyPI-google-cloud-workflows| image:: https://img.shields.io/pypi/v/google-cloud-workflows.svg
     :target: https://pypi.org/project/google-cloud-workflows
.. |PyPI-google-cloud-notebooks| image:: https://img.shields.io/pypi/v/google-cloud-notebooks.svg
     :target: https://pypi.org/project/google-cloud-notebooks
.. |PyPI-google-analytics-data| image:: https://img.shields.io/pypi/v/google-analytics-data.svg
     :target: https://pypi.org/project/google-analytics-data
.. |PyPI-google-cloud-apigee-connect| image:: https://img.shields.io/pypi/v/google-cloud-apigee-connect.svg
     :target: https://pypi.org/project/google-cloud-apigee-connect
.. |PyPI-google-cloud-appengine-logging| image:: https://img.shields.io/pypi/v/google-cloud-appengine-logging.svg
     :target: https://pypi.org/project/google-cloud-appengine-logging
.. |PyPI-google-cloud-artifact-registry| image:: https://img.shields.io/pypi/v/google-cloud-artifact-registry.svg
     :target: https://pypi.org/project/google-cloud-artifact-registry
.. |PyPI-google-cloud-assured-workloads| image:: https://img.shields.io/pypi/v/google-cloud-assured-workloads.svg
     :target: https://pypi.org/project/google-cloud-assured-workloads
.. |PyPI-google-cloud-audit-log| image:: https://img.shields.io/pypi/v/google-cloud-audit-log.svg
     :target: https://pypi.org/project/google-cloud-audit-log
.. |PyPI-google-cloud-bigquery-logging| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-logging.svg
     :target: https://pypi.org/project/google-cloud-bigquery-logging
.. |PyPI-google-cloud-billing-budgets| image:: https://img.shields.io/pypi/v/google-cloud-billing-budgets.svg
     :target: https://pypi.org/project/google-cloud-billing-budgets
.. |PyPI-google-cloud-binary-authorization| image:: https://img.shields.io/pypi/v/google-cloud-binary-authorization.svg
     :target: https://pypi.org/project/google-cloud-binary-authorization
.. |PyPI-google-cloud-datalabeling| image:: https://img.shields.io/pypi/v/google-cloud-datalabeling.svg
     :target: https://pypi.org/project/google-cloud-datalabeling
.. |PyPI-google-cloud-dms| image:: https://img.shields.io/pypi/v/google-cloud-dms.svg
     :target: https://pypi.org/project/google-cloud-dms
.. |PyPI-google-cloud-dataproc-metastore| image:: https://img.shields.io/pypi/v/google-cloud-dataproc-metastore.svg
     :target: https://pypi.org/project/google-cloud-dataproc-metastore
.. |PyPI-google-cloud-dialogflow-cx| image:: https://img.shields.io/pypi/v/google-cloud-dialogflow-cx.svg
     :target: https://pypi.org/project/google-cloud-dialogflow-cx
.. |PyPI-google-cloud-domains| image:: https://img.shields.io/pypi/v/google-cloud-domains.svg
     :target: https://pypi.org/project/google-cloud-domains
.. |PyPI-google-cloud-error-reporting| image:: https://img.shields.io/pypi/v/google-cloud-error-reporting.svg
     :target: https://pypi.org/project/google-cloud-error-reporting
.. |PyPI-google-cloud-essential-contacts| image:: https://img.shields.io/pypi/v/google-cloud-essential-contacts.svg
     :target: https://pypi.org/project/google-cloud-essential-contacts
.. |PyPI-google-cloud-functions| image:: https://img.shields.io/pypi/v/google-cloud-functions.svg
     :target: https://pypi.org/project/google-cloud-functions
.. |PyPI-google-cloud-gke-hub| image:: https://img.shields.io/pypi/v/google-cloud-gke-hub.svg
     :target: https://pypi.org/project/google-cloud-gke-hub
.. |PyPI-google-cloud-game-servers| image:: https://img.shields.io/pypi/v/google-cloud-game-servers.svg
     :target: https://pypi.org/project/google-cloud-game-servers
.. |PyPI-google-cloud-iam-logging| image:: https://img.shields.io/pypi/v/google-cloud-iam-logging.svg
     :target: https://pypi.org/project/google-cloud-iam-logging
.. |PyPI-google-cloud-life-sciences| image:: https://img.shields.io/pypi/v/google-cloud-life-sciences.svg
     :target: https://pypi.org/project/google-cloud-life-sciences
.. |PyPI-google-cloud-managed-identities| image:: https://img.shields.io/pypi/v/google-cloud-managed-identities.svg
     :target: https://pypi.org/project/google-cloud-managed-identities
.. |PyPI-google-cloud-media-translation| image:: https://img.shields.io/pypi/v/google-cloud-media-translation.svg
     :target: https://pypi.org/project/google-cloud-media-translation
.. |PyPI-google-cloud-phishing-protection| image:: https://img.shields.io/pypi/v/google-cloud-phishing-protection.svg
     :target: https://pypi.org/project/google-cloud-phishing-protection
.. |PyPI-google-cloud-private-catalog| image:: https://img.shields.io/pypi/v/google-cloud-private-catalog.svg
     :target: https://pypi.org/project/google-cloud-private-catalog
.. |PyPI-google-cloud-private-ca| image:: https://img.shields.io/pypi/v/google-cloud-private-ca.svg
     :target: https://pypi.org/project/google-cloud-private-ca
.. |PyPI-google-cloud-pubsublite| image:: https://img.shields.io/pypi/v/google-cloud-pubsublite.svg
     :target: https://pypi.org/project/google-cloud-pubsublite
.. |PyPI-google-cloud-recommendations-ai| image:: https://img.shields.io/pypi/v/google-cloud-recommendations-ai.svg
     :target: https://pypi.org/project/google-cloud-recommendations-ai
.. |PyPI-google-cloud-resource-manager| image:: https://img.shields.io/pypi/v/google-cloud-resource-manager.svg
     :target: https://pypi.org/project/google-cloud-resource-manager
.. |PyPI-google-cloud-runtimeconfig| image:: https://img.shields.io/pypi/v/google-cloud-runtimeconfig.svg
     :target: https://pypi.org/project/google-cloud-runtimeconfig
.. |PyPI-pybigquery| image:: https://img.shields.io/pypi/v/pybigquery.svg
     :target: https://pypi.org/project/pybigquery
.. |PyPI-google-cloud-service-usage| image:: https://img.shields.io/pypi/v/google-cloud-service-usage.svg
     :target: https://pypi.org/project/google-cloud-service-usage
.. |PyPI-google-cloud-shell| image:: https://img.shields.io/pypi/v/google-cloud-shell.svg
     :target: https://pypi.org/project/google-cloud-shell
.. |PyPI-google-cloud-tpu| image:: https://img.shields.io/pypi/v/google-cloud-tpu.svg
     :target: https://pypi.org/project/google-cloud-tpu
.. |PyPI-google-cloud-talent| image:: https://img.shields.io/pypi/v/google-cloud-talent.svg
     :target: https://pypi.org/project/google-cloud-talent
.. |PyPI-google-cloud-video-transcoder| image:: https://img.shields.io/pypi/v/google-cloud-video-transcoder.svg
     :target: https://pypi.org/project/google-cloud-video-transcoder
.. |PyPI-google-cloud-vpc-access| image:: https://img.shields.io/pypi/v/google-cloud-vpc-access.svg
     :target: https://pypi.org/project/google-cloud-vpc-access
.. |PyPI-google-cloud-recaptcha-enterprise| image:: https://img.shields.io/pypi/v/google-cloud-recaptcha-enterprise.svg
     :target: https://pypi.org/project/google-cloud-recaptcha-enterprise
.. |PyPI-google-analytics-admin| image:: https://img.shields.io/pypi/v/google-analytics-admin.svg
     :target: https://pypi.org/project/google-analytics-admin
.. |PyPI-google-area120-tables| image:: https://img.shields.io/pypi/v/google-area120-tables.svg
     :target: https://pypi.org/project/google-area120-tables
.. |PyPI-google-cloud-compute| image:: https://img.shields.io/pypi/v/google-cloud-compute.svg
     :target: https://pypi.org/project/google-cloud-compute
.. |PyPI-google-cloud-dns| image:: https://img.shields.io/pypi/v/google-cloud-dns.svg
     :target: https://pypi.org/project/google-cloud-dns
.. |PyPI-google-cloud-data-qna| image:: https://img.shields.io/pypi/v/google-cloud-data-qna.svg
     :target: https://pypi.org/project/google-cloud-data-qna
.. |PyPI-google-cloud-network-connectivity| image:: https://img.shields.io/pypi/v/google-cloud-network-connectivity.svg
     :target: https://pypi.org/project/google-cloud-network-connectivity

.. API_TABLE_END

.. |ga| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability

.. |beta| image:: https://img.shields.io/badge/support-beta-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#beta-support


.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#alpha-support


Example Applications
********************

-  `getting-started-python`_ - A sample and `tutorial`_ that demonstrates how to build a complete web application using Cloud Datastore, Cloud Storage, and Cloud Pub/Sub and deploy it to Google App Engine or Google Compute Engine.
-  `google-cloud-python-expenses-demo`_ - A sample expenses demo using Cloud Datastore and Cloud Storage

.. _getting-started-python: https://github.com/GoogleCloudPlatform/getting-started-python
.. _tutorial: https://cloud.google.com/python
.. _google-cloud-python-expenses-demo: https://github.com/GoogleCloudPlatform/google-cloud-python-expenses-demo


Authentication
********************


With ``google-cloud-python`` we try to make authentication as painless as possible.
Check out the `Authentication section`_ in our documentation to learn more.
You may also find the `authentication document`_ shared by all the
``google-cloud-*`` libraries to be helpful.

.. _Authentication section: https://googleapis.dev/python/google-api-core/latest/auth.html
.. _authentication document: https://github.com/googleapis/google-cloud-common/tree/master/authentication



License
********************


Apache 2.0 - See `the LICENSE`_ for more information.

.. _the LICENSE: https://github.com/googleapis/google-cloud-python/blob/master/LICENSE
