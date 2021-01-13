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
   * - `Firestore <https://github.com/googleapis/python-firestore>`_
     - |ga|
     - |PyPI-google-cloud-firestore|
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
   * - `Scheduler <https://github.com/googleapis/python-scheduler>`_
     - |ga|
     - |PyPI-google-cloud-scheduler|
   * - `Secret Manager <https://github.com/googleapis/python-secret-manager>`_
     - |ga|
     - |PyPI-google-cloud-secret-manager|
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
   * - `AI Platform Notebooks <https://github.com/googleapis/python-notebooks>`_
     - |beta|
     - |PyPI-google-cloud-notebooks|
   * - `Access Approval <https://github.com/googleapis/python-access-approval>`_
     - |beta|
     - |PyPI-google-cloud-access-approval|
   * - `Assured Workloads for Government <https://github.com/googleapis/python-assured-workloads>`_
     - |beta|
     - |PyPI-google-cloud-assured-workflows|
   * - `Audit Log <https://github.com/googleapis/python-audit-log>`_
     - |beta|
     - |PyPI-google-cloud-audit-log|
   * - `Billing Budget <https://github.com/googleapis/python-billingbudgets>`_
     - |beta|
     - |PyPI-google-cloud-billing-budgets|
   * - `Binary Authorization <https://github.com/googleapis/python-binary-authorization>`_
     - |beta|
     - |PyPI-google-cloud-binary-authorization|
   * - `Compute Engine <https://github.com/googleapis/python-compute>`_
     - |beta|
     - |PyPI-google-cloud-compute|
   * - `Data Labeling <https://github.com/googleapis/python-datalabeling>`_
     - |beta|
     - |PyPI-google-cloud-datalabeling|
   * - `Dialogflow CX <https://github.com/googleapis/python-dialogflow-cx>`_
     - |beta|
     - |PyPI-google-cloud-dialogflow-cx|
   * - `Document Understanding API <https://github.com/googleapis/python-documentai>`_
     - |beta|
     - |PyPI-google-cloud-documentai|
   * - `Error Reporting <https://github.com/googleapis/python-error-reporting>`_
     - |beta|
     - |PyPI-google-cloud-error-reporting|
   * - `Functions <https://github.com/googleapis/python-functions>`_
     - |beta|
     - |PyPI-google-cloud-functions|
   * - `Game Servers <https://github.com/googleapis/python-game-servers>`_
     - |beta|
     - |PyPI-google-cloud-game-servers|
   * - `Media Translation <https://github.com/googleapis/python-media-translation>`_
     - |beta|
     - |PyPI-google-cloud-media-translation|
   * - `Memorystore for Memcached <https://github.com/googleapis/python-memcache>`_
     - |beta|
     - |PyPI-google-cloud-memcache|
   * - `Phishing Protection <https://github.com/googleapis/python-phishingprotection>`_
     - |beta|
     - |PyPI-google-cloud-phishingprotection|
   * - `Private Certificate Authority <https://github.com/googleapis/python-security-private-ca>`_
     - |beta|
     - |PyPI-google-cloud-security-private-ca|
   * - `Pub/Sub Lite <https://github.com/googleapis/python-pubsublite>`_
     - |beta|
     - |PyPI-google-cloud-pubsublite|
   * - `Recommendations AI <https://github.com/googleapis/python-recommendations-ai>`_
     - |beta|
     - |PyPI-google-cloud-recommendations-ai|
   * - `Runtime Configurator <https://github.com/googleapis/python-runtimeconfig>`_
     - |beta|
     - |PyPI-google-cloud-runtimeconfig|
   * - `Service Directory <https://github.com/googleapis/python-service-directory>`_
     - |beta|
     - |PyPI-google-cloud-service-directory|
   * - `Talent Solution <https://github.com/googleapis/python-talent>`_
     - |beta|
     - |PyPI-google-cloud-talent|
   * - `Transcoder <https://github.com/googleapis/python-video-transcoder>`_
     - |beta|
     - |PyPI-google-cloud-video-transcoder|
   * - `Workflows <https://github.com/googleapis/python-workflows>`_
     - |beta|
     - |PyPI-google-cloud-workflows|
   * - `reCAPTCHA Enterprise <https://github.com/googleapis/python-recaptcha-enterprise>`_
     - |beta|
     - |PyPI-google-cloud-recpatcha-enterprise|
   * - `Analytics Admin <https://github.com/googleapis/python-analytics-admin>`_
     - |alpha|
     - |PyPI-google-analytics-admin|
   * - `Analytics Data API <https://github.com/googleapis/python-analytics-data>`_
     - |alpha|
     - |PyPI-google-analytics-data|
   * - `Area 120 Tables API <https://github.com/googleapis/python-area120-tables>`_
     - |alpha|
     - |PyPI-google-area120-tables|
   * - `DNS <https://github.com/googleapis/python-dns>`_
     - |alpha|
     - |PyPI-google-cloud-dns|
   * - `Data QnA <https://github.com/googleapis/python-data-qna>`_
     - |alpha|
     - |PyPI-google-cloud-data-qna|
   * - `Grafeas <https://github.com/googleapis/python-grafeas>`_
     - |alpha|
     - |PyPI-grafeas|
   * - `Resource Manager API <https://github.com/googleapis/python-resource-manager>`_
     - |alpha|
     - |PyPI-google-cloud-resource-manager|
   * - `Security Command Center <https://github.com/googleapis/python-securitycenter>`_
     - |alpha|
     - |PyPI-google-cloud-securitycenter|
   * - `Security Scanner <https://github.com/googleapis/python-websecurityscanner>`_
     - |alpha|
     - |PyPI-google-cloud-websecurityscanner|
   * - `Web Risk <https://github.com/googleapis/python-webrisk>`_
     - |alpha|
     - |PyPI-google-cloud-webrisk|

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
.. |PyPI-google-cloud-firestore| image:: https://img.shields.io/pypi/v/google-cloud-firestore.svg
     :target: https://pypi.org/project/google-cloud-firestore
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
.. |PyPI-google-cloud-scheduler| image:: https://img.shields.io/pypi/v/google-cloud-scheduler.svg
     :target: https://pypi.org/project/google-cloud-scheduler
.. |PyPI-google-cloud-secret-manager| image:: https://img.shields.io/pypi/v/google-cloud-secret-manager.svg
     :target: https://pypi.org/project/google-cloud-secret-manager
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
.. |PyPI-google-cloud-notebooks| image:: https://img.shields.io/pypi/v/google-cloud-notebooks.svg
     :target: https://pypi.org/project/google-cloud-notebooks
.. |PyPI-google-cloud-access-approval| image:: https://img.shields.io/pypi/v/google-cloud-access-approval.svg
     :target: https://pypi.org/project/google-cloud-access-approval
.. |PyPI-google-cloud-assured-workflows| image:: https://img.shields.io/pypi/v/google-cloud-assured-workflows.svg
     :target: https://pypi.org/project/google-cloud-assured-workflows
.. |PyPI-google-cloud-audit-log| image:: https://img.shields.io/pypi/v/google-cloud-audit-log.svg
     :target: https://pypi.org/project/google-cloud-audit-log
.. |PyPI-google-cloud-billing-budgets| image:: https://img.shields.io/pypi/v/google-cloud-billing-budgets.svg
     :target: https://pypi.org/project/google-cloud-billing-budgets
.. |PyPI-google-cloud-binary-authorization| image:: https://img.shields.io/pypi/v/google-cloud-binary-authorization.svg
     :target: https://pypi.org/project/google-cloud-binary-authorization
.. |PyPI-google-cloud-compute| image:: https://img.shields.io/pypi/v/google-cloud-compute.svg
     :target: https://pypi.org/project/google-cloud-compute
.. |PyPI-google-cloud-datalabeling| image:: https://img.shields.io/pypi/v/google-cloud-datalabeling.svg
     :target: https://pypi.org/project/google-cloud-datalabeling
.. |PyPI-google-cloud-dialogflow-cx| image:: https://img.shields.io/pypi/v/google-cloud-dialogflow-cx.svg
     :target: https://pypi.org/project/google-cloud-dialogflow-cx
.. |PyPI-google-cloud-documentai| image:: https://img.shields.io/pypi/v/google-cloud-documentai.svg
     :target: https://pypi.org/project/google-cloud-documentai
.. |PyPI-google-cloud-error-reporting| image:: https://img.shields.io/pypi/v/google-cloud-error-reporting.svg
     :target: https://pypi.org/project/google-cloud-error-reporting
.. |PyPI-google-cloud-functions| image:: https://img.shields.io/pypi/v/google-cloud-functions.svg
     :target: https://pypi.org/project/google-cloud-functions
.. |PyPI-google-cloud-game-servers| image:: https://img.shields.io/pypi/v/google-cloud-game-servers.svg
     :target: https://pypi.org/project/google-cloud-game-servers
.. |PyPI-google-cloud-media-translation| image:: https://img.shields.io/pypi/v/google-cloud-media-translation.svg
     :target: https://pypi.org/project/google-cloud-media-translation
.. |PyPI-google-cloud-memcache| image:: https://img.shields.io/pypi/v/google-cloud-memcache.svg
     :target: https://pypi.org/project/google-cloud-memcache
.. |PyPI-google-cloud-phishingprotection| image:: https://img.shields.io/pypi/v/google-cloud-phishingprotection.svg
     :target: https://pypi.org/project/google-cloud-phishingprotection
.. |PyPI-google-cloud-security-private-ca| image:: https://img.shields.io/pypi/v/google-cloud-security-private-ca.svg
     :target: https://pypi.org/project/google-cloud-security-private-ca
.. |PyPI-google-cloud-pubsublite| image:: https://img.shields.io/pypi/v/google-cloud-pubsublite.svg
     :target: https://pypi.org/project/google-cloud-pubsublite
.. |PyPI-google-cloud-recommendations-ai| image:: https://img.shields.io/pypi/v/google-cloud-recommendations-ai.svg
     :target: https://pypi.org/project/google-cloud-recommendations-ai
.. |PyPI-google-cloud-runtimeconfig| image:: https://img.shields.io/pypi/v/google-cloud-runtimeconfig.svg
     :target: https://pypi.org/project/google-cloud-runtimeconfig
.. |PyPI-google-cloud-service-directory| image:: https://img.shields.io/pypi/v/google-cloud-service-directory.svg
     :target: https://pypi.org/project/google-cloud-service-directory
.. |PyPI-google-cloud-talent| image:: https://img.shields.io/pypi/v/google-cloud-talent.svg
     :target: https://pypi.org/project/google-cloud-talent
.. |PyPI-google-cloud-video-transcoder| image:: https://img.shields.io/pypi/v/google-cloud-video-transcoder.svg
     :target: https://pypi.org/project/google-cloud-video-transcoder
.. |PyPI-google-cloud-workflows| image:: https://img.shields.io/pypi/v/google-cloud-workflows.svg
     :target: https://pypi.org/project/google-cloud-workflows
.. |PyPI-google-cloud-recpatcha-enterprise| image:: https://img.shields.io/pypi/v/google-cloud-recpatcha-enterprise.svg
     :target: https://pypi.org/project/google-cloud-recpatcha-enterprise
.. |PyPI-google-analytics-admin| image:: https://img.shields.io/pypi/v/google-analytics-admin.svg
     :target: https://pypi.org/project/google-analytics-admin
.. |PyPI-google-analytics-data| image:: https://img.shields.io/pypi/v/google-analytics-data.svg
     :target: https://pypi.org/project/google-analytics-data
.. |PyPI-google-area120-tables| image:: https://img.shields.io/pypi/v/google-area120-tables.svg
     :target: https://pypi.org/project/google-area120-tables
.. |PyPI-google-cloud-dns| image:: https://img.shields.io/pypi/v/google-cloud-dns.svg
     :target: https://pypi.org/project/google-cloud-dns
.. |PyPI-google-cloud-data-qna| image:: https://img.shields.io/pypi/v/google-cloud-data-qna.svg
     :target: https://pypi.org/project/google-cloud-data-qna
.. |PyPI-grafeas| image:: https://img.shields.io/pypi/v/grafeas.svg
     :target: https://pypi.org/project/grafeas
.. |PyPI-google-cloud-resource-manager| image:: https://img.shields.io/pypi/v/google-cloud-resource-manager.svg
     :target: https://pypi.org/project/google-cloud-resource-manager
.. |PyPI-google-cloud-securitycenter| image:: https://img.shields.io/pypi/v/google-cloud-securitycenter.svg
     :target: https://pypi.org/project/google-cloud-securitycenter
.. |PyPI-google-cloud-websecurityscanner| image:: https://img.shields.io/pypi/v/google-cloud-websecurityscanner.svg
     :target: https://pypi.org/project/google-cloud-websecurityscanner
.. |PyPI-google-cloud-webrisk| image:: https://img.shields.io/pypi/v/google-cloud-webrisk.svg
     :target: https://pypi.org/project/google-cloud-webrisk

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
