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
     - Issue Tracker
   * - `A python wrapper of the C library 'CRC32C' <https://github.com/googleapis/python-crc32c>`_
     - stable
     - |PyPI-google-crc32c|
     - https://github.com/googleapis/python-crc32c/issues
   * - `AI Platform <https://github.com/googleapis/python-aiplatform>`_
     - stable
     - |PyPI-google-cloud-aiplatform|
     - https://issuetracker.google.com/savedsearches/559744
   * - `AI Platform Notebooks <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-notebooks>`_
     - stable
     - |PyPI-google-cloud-notebooks|
     - 
   * - `API Gateway <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-api-gateway>`_
     - stable
     - |PyPI-google-cloud-api-gateway|
     - 
   * - `Access Approval <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-access-approval>`_
     - stable
     - |PyPI-google-cloud-access-approval|
     - 
   * - `Apigee Connect <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-apigee-connect>`_
     - stable
     - |PyPI-google-cloud-apigee-connect|
     - 
   * - `App Engine Admin <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-appengine-admin>`_
     - stable
     - |PyPI-google-cloud-appengine-admin|
     - 
   * - `App Engine Logging Protos <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-appengine-logging>`_
     - stable
     - |PyPI-google-cloud-appengine-logging|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Artifact Registry <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-artifact-registry>`_
     - stable
     - |PyPI-google-cloud-artifact-registry|
     - 
   * - `Asset Inventory <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-asset>`_
     - stable
     - |PyPI-google-cloud-asset|
     - https://issuetracker.google.com/savedsearches/559757
   * - `Assured Workloads for Government <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-assured-workloads>`_
     - stable
     - |PyPI-google-cloud-assured-workloads|
     - 
   * - `AutoML <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-automl>`_
     - stable
     - |PyPI-google-cloud-automl|
     - https://issuetracker.google.com/savedsearches/559744
   * - `Bare Metal Solution <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bare-metal-solution>`_
     - stable
     - |PyPI-google-cloud-bare-metal-solution|
     - 
   * - `BigQuery <https://github.com/googleapis/python-bigquery>`_
     - stable
     - |PyPI-google-cloud-bigquery|
     - https://issuetracker.google.com/savedsearches/559654
   * - `BigQuery Connection <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery-connection>`_
     - stable
     - |PyPI-google-cloud-bigquery-connection|
     - 
   * - `BigQuery Data Transfer <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery-datatransfer>`_
     - stable
     - |PyPI-google-cloud-bigquery-datatransfer|
     - https://issuetracker.google.com/savedsearches/559654
   * - `BigQuery Logging Protos <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery-logging>`_
     - stable
     - |PyPI-google-cloud-bigquery-logging|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `BigQuery Reservation <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery-reservation>`_
     - stable
     - |PyPI-google-cloud-bigquery-reservation|
     - 
   * - `BigQuery Storage <https://github.com/googleapis/python-bigquery-storage>`_
     - stable
     - |PyPI-google-cloud-bigquery-storage|
     - https://issuetracker.google.com/savedsearches/559654
   * - `Bigtable <https://github.com/googleapis/python-bigtable>`_
     - stable
     - |PyPI-google-cloud-bigtable|
     - https://issuetracker.google.com/savedsearches/559777
   * - `Billing <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-billing>`_
     - stable
     - |PyPI-google-cloud-billing|
     - 
   * - `Billing Budget <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-billing-budgets>`_
     - stable
     - |PyPI-google-cloud-billing-budgets|
     - https://issuetracker.google.com/savedsearches/559770
   * - `Binary Authorization <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-binary-authorization>`_
     - stable
     - |PyPI-google-cloud-binary-authorization|
     - 
   * - `Build <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-build>`_
     - stable
     - |PyPI-google-cloud-build|
     - https://issuetracker.google.com/savedsearches/5226584
   * - `Certificate Manager <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-certificate-manager>`_
     - stable
     - |PyPI-google-cloud-certificate-manager|
     - 
   * - `Channel Services <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-channel>`_
     - stable
     - |PyPI-google-cloud-channel|
     - 
   * - `Common <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-common>`_
     - stable
     - |PyPI-google-cloud-common|
     - 
   * - `Composer <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-orchestration-airflow>`_
     - stable
     - |PyPI-google-cloud-orchestration-airflow|
     - 
   * - `Compute Engine <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-compute>`_
     - stable
     - |PyPI-google-cloud-compute|
     - https://issuetracker.google.com/issues/new?component=187134&template=0
   * - `Contact Center AI Insights <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-contact-center-insights>`_
     - stable
     - |PyPI-google-cloud-contact-center-insights|
     - 
   * - `Container Analysis <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-containeranalysis>`_
     - stable
     - |PyPI-google-cloud-containeranalysis|
     - https://issuetracker.google.com/savedsearches/559777
   * - `Data Catalog <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-datacatalog>`_
     - stable
     - |PyPI-google-cloud-datacatalog|
     - 
   * - `Data Fusion <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-data-fusion>`_
     - stable
     - |PyPI-google-cloud-data-fusion|
     - 
   * - `Data Loss Prevention <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-dlp>`_
     - stable
     - |PyPI-google-cloud-dlp|
     - 
   * - `Database Migration Service <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-dms>`_
     - stable
     - |PyPI-google-cloud-dms|
     - 
   * - `Dataplex <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-dataplex>`_
     - stable
     - |PyPI-google-cloud-dataplex|
     - 
   * - `Dataproc <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-dataproc>`_
     - stable
     - |PyPI-google-cloud-dataproc|
     - https://issuetracker.google.com/savedsearches/559745
   * - `Dataproc Metastore <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-dataproc-metastore>`_
     - stable
     - |PyPI-google-cloud-dataproc-metastore|
     - 
   * - `Datastore <https://github.com/googleapis/python-datastore>`_
     - stable
     - |PyPI-google-cloud-datastore|
     - https://issuetracker.google.com/savedsearches/559768
   * - `Datastream <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-datastream>`_
     - stable
     - |PyPI-google-cloud-datastream|
     - 
   * - `Deploy <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-deploy>`_
     - stable
     - |PyPI-google-cloud-deploy|
     - 
   * - `Dialogflow <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-dialogflow>`_
     - stable
     - |PyPI-google-cloud-dialogflow|
     - https://issuetracker.google.com/savedsearches/5300385
   * - `Dialogflow CX <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-dialogflow-cx>`_
     - stable
     - |PyPI-google-cloud-dialogflow-cx|
     - https://issuetracker.google.com/savedsearches/5300385
   * - `Document AI <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-documentai>`_
     - stable
     - |PyPI-google-cloud-documentai|
     - 
   * - `Domains <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-domains>`_
     - stable
     - |PyPI-google-cloud-domains|
     - 
   * - `Essential Contacts <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-essential-contacts>`_
     - stable
     - |PyPI-google-cloud-essential-contacts|
     - 
   * - `Eventarc <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-eventarc>`_
     - stable
     - |PyPI-google-cloud-eventarc|
     - 
   * - `Filestore <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-filestore>`_
     - stable
     - |PyPI-google-cloud-filestore|
     - 
   * - `Firestore <https://github.com/googleapis/python-firestore>`_
     - stable
     - |PyPI-google-cloud-firestore|
     - https://issuetracker.google.com/savedsearches/5337669
   * - `Functions <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-functions>`_
     - stable
     - |PyPI-google-cloud-functions|
     - https://issuetracker.google.com/savedsearches/559729
   * - `GKE Hub <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-gke-hub>`_
     - stable
     - |PyPI-google-cloud-gke-hub|
     - 
   * - `Grafeas <https://github.com/googleapis/google-cloud-python/tree/main/packages/grafeas>`_
     - stable
     - |PyPI-grafeas|
     - 
   * - `IAM Logging Protos <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-iam-logging>`_
     - stable
     - |PyPI-google-cloud-iam-logging|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `IAM Policy Troubleshooter API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-policy-troubleshooter>`_
     - stable
     - |PyPI-google-cloud-policy-troubleshooter|
     - 
   * - `IDS <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-ids>`_
     - stable
     - |PyPI-google-cloud-ids|
     - 
   * - `Identity and Access Management <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-iam>`_
     - stable
     - |PyPI-google-cloud-iam|
     - https://issuetracker.google.com/savedsearches/559761
   * - `Identity-Aware Proxy <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-iap>`_
     - stable
     - |PyPI-google-cloud-iap|
     - 
   * - `Key Management Service <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-kms>`_
     - stable
     - |PyPI-google-cloud-kms|
     - https://issuetracker.google.com/savedsearches/5264932
   * - `Kubernetes Engine <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-container>`_
     - stable
     - |PyPI-google-cloud-container|
     - https://issuetracker.google.com/savedsearches/559746
   * - `Live Stream <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-video-live-stream>`_
     - stable
     - |PyPI-google-cloud-video-live-stream|
     - 
   * - `Logging <https://github.com/googleapis/python-logging>`_
     - stable
     - |PyPI-google-cloud-logging|
     - https://issuetracker.google.com/savedsearches/559764
   * - `Managed Service for Microsoft Active Directory <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-managed-identities>`_
     - stable
     - |PyPI-google-cloud-managed-identities|
     - 
   * - `Memorystore for Memcached <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-memcache>`_
     - stable
     - |PyPI-google-cloud-memcache|
     - 
   * - `Metrics Scopes <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-monitoring-metrics-scopes>`_
     - stable
     - |PyPI-google-cloud-monitoring-metrics-scopes|
     - https://issuetracker.google.com/savedsearches/559785
   * - `Monitoring Dashboards <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-monitoring-dashboards>`_
     - stable
     - |PyPI-google-cloud-monitoring-dashboards|
     - https://issuetracker.google.com/savedsearches/559785
   * - `NDB Client Library for Datastore <https://github.com/googleapis/python-ndb>`_
     - stable
     - |PyPI-google-cloud-ndb|
     - https://github.com/googleapis/python-ndb/issues
   * - `Natural Language <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-language>`_
     - stable
     - |PyPI-google-cloud-language|
     - https://issuetracker.google.com/savedsearches/559753
   * - `Network Connectivity Center <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-network-connectivity>`_
     - stable
     - |PyPI-google-cloud-network-connectivity|
     - 
   * - `Network Management <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-network-management>`_
     - stable
     - |PyPI-google-cloud-network-management|
     - 
   * - `OS Config <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-os-config>`_
     - stable
     - |PyPI-google-cloud-os-config|
     - 
   * - `OS Login <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-os-login>`_
     - stable
     - |PyPI-google-cloud-os-login|
     - https://issuetracker.google.com/savedsearches/559755
   * - `Optimization <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-optimization>`_
     - stable
     - |PyPI-google-cloud-optimization|
     - 
   * - `Pandas Data Types for SQL systems (BigQuery, Spanner) <https://github.com/googleapis/python-db-dtypes-pandas>`_
     - stable
     - |PyPI-db-dtypes|
     - None
   * - `Private Certificate Authority <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-private-ca>`_
     - stable
     - |PyPI-google-cloud-private-ca|
     - 
   * - `Pub/Sub <https://github.com/googleapis/python-pubsub>`_
     - stable
     - |PyPI-google-cloud-pubsub|
     - https://issuetracker.google.com/savedsearches/559741
   * - `Pub/Sub Lite <https://github.com/googleapis/python-pubsublite>`_
     - stable
     - |PyPI-google-cloud-pubsublite|
     - 
   * - `Recommender <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-recommender>`_
     - stable
     - |PyPI-google-cloud-recommender|
     - 
   * - `Redis <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-redis>`_
     - stable
     - |PyPI-google-cloud-redis|
     - https://issuetracker.google.com/savedsearches/5169231
   * - `Resource Manager <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-resource-manager>`_
     - stable
     - |PyPI-google-cloud-resource-manager|
     - https://issuetracker.google.com/savedsearches/559757
   * - `Resource Settings <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-resource-settings>`_
     - stable
     - |PyPI-google-cloud-resource-settings|
     - 
   * - `Retail <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-retail>`_
     - stable
     - |PyPI-google-cloud-retail|
     - 
   * - `Scheduler <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-scheduler>`_
     - stable
     - |PyPI-google-cloud-scheduler|
     - https://issuetracker.google.com/savedsearches/5411429
   * - `Secret Manager <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-secret-manager>`_
     - stable
     - |PyPI-google-cloud-secret-manager|
     - 
   * - `Security Command Center <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-securitycenter>`_
     - stable
     - |PyPI-google-cloud-securitycenter|
     - https://issuetracker.google.com/savedsearches/559748
   * - `Security Scanner <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-websecurityscanner>`_
     - stable
     - |PyPI-google-cloud-websecurityscanner|
     - https://issuetracker.google.com/savedsearches/559748
   * - `Service Control <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-service-control>`_
     - stable
     - |PyPI-google-cloud-service-control|
     - 
   * - `Service Directory <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-service-directory>`_
     - stable
     - |PyPI-google-cloud-service-directory|
     - 
   * - `Service Management <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-service-management>`_
     - stable
     - |PyPI-google-cloud-service-management|
     - 
   * - `Service Usage <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-service-usage>`_
     - stable
     - |PyPI-google-cloud-service-usage|
     - 
   * - `Shell <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-shell>`_
     - stable
     - |PyPI-google-cloud-shell|
     - 
   * - `Source Context <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-source-context>`_
     - stable
     - |PyPI-google-cloud-source-context|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Spanner <https://github.com/googleapis/python-spanner>`_
     - stable
     - |PyPI-google-cloud-spanner|
     - https://issuetracker.google.com/issues?q=componentid:190851%2B%20status:open
   * - `Spanner Django <https://github.com/googleapis/python-spanner-django>`_
     - stable
     - |PyPI-django-google-spanner|
     - https://issuetracker.google.com/issues?q=componentid:190851%2B%20status:open
   * - `Speech <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-speech>`_
     - stable
     - |PyPI-google-cloud-speech|
     - https://issuetracker.google.com/savedsearches/559758
   * - `Stackdriver Monitoring <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-monitoring>`_
     - stable
     - |PyPI-google-cloud-monitoring|
     - https://issuetracker.google.com/savedsearches/559785
   * - `Storage <https://github.com/googleapis/python-storage>`_
     - stable
     - |PyPI-google-cloud-storage|
     - https://issuetracker.google.com/savedsearches/559782
   * - `Storage Transfer Service <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-storage-transfer>`_
     - stable
     - |PyPI-google-cloud-storage-transfer|
     - 
   * - `TPU <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-tpu>`_
     - stable
     - |PyPI-google-cloud-tpu|
     - 
   * - `Talent Solution <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-talent>`_
     - stable
     - |PyPI-google-cloud-talent|
     - https://issuetracker.google.com/savedsearches/559664
   * - `Tasks <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-tasks>`_
     - stable
     - |PyPI-google-cloud-tasks|
     - https://issuetracker.google.com/savedsearches/5433985
   * - `Text-to-Speech <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-texttospeech>`_
     - stable
     - |PyPI-google-cloud-texttospeech|
     - https://issuetracker.google.com/savedsearches/5235428
   * - `Trace <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-trace>`_
     - stable
     - |PyPI-google-cloud-trace|
     - https://issuetracker.google.com/savedsearches/559776
   * - `Transcoder <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-video-transcoder>`_
     - stable
     - |PyPI-google-cloud-video-transcoder|
     - 
   * - `Translation <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-translate>`_
     - stable
     - |PyPI-google-cloud-translate|
     - https://issuetracker.google.com/savedsearches/559749
   * - `VM Migration <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-vm-migration>`_
     - stable
     - |PyPI-google-cloud-vm-migration|
     - 
   * - `Video Intelligence <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-videointelligence>`_
     - stable
     - |PyPI-google-cloud-videointelligence|
     - https://issuetracker.google.com/savedsearches/5084810
   * - `Virtual Private Cloud <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-vpc-access>`_
     - stable
     - |PyPI-google-cloud-vpc-access|
     - 
   * - `Vision <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-vision>`_
     - stable
     - |PyPI-google-cloud-vision|
     - https://issuetracker.google.com/issues?q=status:open%20componentid:187174
   * - `Web Risk <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-webrisk>`_
     - stable
     - |PyPI-google-cloud-webrisk|
     - 
   * - `Workflows <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-workflows>`_
     - stable
     - |PyPI-google-cloud-workflows|
     - https://issuetracker.google.com/savedsearches/559729
   * - `reCAPTCHA Enterprise <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-recaptcha-enterprise>`_
     - stable
     - |PyPI-google-cloud-recaptcha-enterprise|
     - 
   * - `A unified Python API in BigQuery <https://github.com/googleapis/python-bigquery-dataframes>`_
     - preview
     - |PyPI-bigframes|
     - https://github.com/googleapis/python-bigquery-dataframes/issues
   * - `API Keys <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-api-keys>`_
     - preview
     - |PyPI-google-cloud-api-keys|
     - None
   * - `Ad Manager <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-ads-admanager>`_
     - preview
     - |PyPI-google-ads-admanager|
     - https://issuetracker.google.com/issues/new?component=1265187&template=1787490
   * - `Address Validation API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-addressvalidation>`_
     - preview
     - |PyPI-google-maps-addressvalidation|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Advisory Notifications <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-advisorynotifications>`_
     - preview
     - |PyPI-google-cloud-advisorynotifications|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `AlloyDB <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-alloydb>`_
     - preview
     - |PyPI-google-cloud-alloydb|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `AlloyDB connectors <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-alloydb-connectors>`_
     - preview
     - |PyPI-google-cloud-alloydb-connectors|
     - https://issuetracker.google.com/issues/new?component=1194526&template=1689942
   * - `Analytics Admin <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-analytics-admin>`_
     - preview
     - |PyPI-google-analytics-admin|
     - https://issuetracker.google.com/issues?q=componentid:187400
   * - `Analytics Data <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-analytics-data>`_
     - preview
     - |PyPI-google-analytics-data|
     - https://issuetracker.google.com/issues?q=componentid:187400%2B%20
   * - `Anthos Multicloud <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-gke-multicloud>`_
     - preview
     - |PyPI-google-cloud-gke-multicloud|
     - 
   * - `Apigee Registry API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-apigee-registry>`_
     - preview
     - |PyPI-google-cloud-apigee-registry|
     - 
   * - `App Hub API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-apphub>`_
     - preview
     - |PyPI-google-cloud-apphub|
     - https://issuetracker.google.com/issues/new?component=1509913
   * - `Apps Card Protos <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-apps-card>`_
     - preview
     - |PyPI-google-apps-card|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Apps Script Type Protos <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-apps-script-type>`_
     - preview
     - |PyPI-google-apps-script-type|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Area 120 Tables <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-area120-tables>`_
     - preview
     - |PyPI-google-area120-tables|
     - 
   * - `Backup and DR Service API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-backupdr>`_
     - preview
     - |PyPI-google-cloud-backupdr|
     - https://issuetracker.google.com/issues/new?component=966572
   * - `Backup for GKE <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-gke-backup>`_
     - preview
     - |PyPI-google-cloud-gke-backup|
     - 
   * - `Batch <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-batch>`_
     - preview
     - |PyPI-google-cloud-batch|
     - 
   * - `BeyondCorp AppConnections <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-beyondcorp-appconnections>`_
     - preview
     - |PyPI-google-cloud-beyondcorp-appconnections|
     - 
   * - `BeyondCorp AppConnectors <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-beyondcorp-appconnectors>`_
     - preview
     - |PyPI-google-cloud-beyondcorp-appconnectors|
     - 
   * - `BeyondCorp AppGateways <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-beyondcorp-appgateways>`_
     - preview
     - |PyPI-google-cloud-beyondcorp-appgateways|
     - 
   * - `BeyondCorp ClientConnectorServices <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-beyondcorp-clientconnectorservices>`_
     - preview
     - |PyPI-google-cloud-beyondcorp-clientconnectorservices|
     - 
   * - `BeyondCorp ClientGateways <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-beyondcorp-clientgateways>`_
     - preview
     - |PyPI-google-cloud-beyondcorp-clientgateways|
     - 
   * - `BigLake API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery-biglake>`_
     - preview
     - |PyPI-google-cloud-bigquery-biglake|
     - https://issuetracker.google.com/issues/new?component=187149&template=1019829
   * - `BigQuery Analytics Hub <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery-analyticshub>`_
     - preview
     - |PyPI-google-cloud-bigquery-analyticshub|
     - 
   * - `BigQuery Analytics Hub <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery-data-exchange>`_
     - preview
     - |PyPI-google-cloud-bigquery-data-exchange|
     - 
   * - `BigQuery Data Policy <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery-datapolicies>`_
     - preview
     - |PyPI-google-cloud-bigquery-datapolicies|
     - 
   * - `BigQuery Migration <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery-migration>`_
     - preview
     - |PyPI-google-cloud-bigquery-migration|
     - https://issuetracker.google.com/savedsearches/559654
   * - `BigQuery connector for pandas <https://github.com/googleapis/python-bigquery-pandas>`_
     - preview
     - |PyPI-pandas-gbq|
     - https://github.com/googleapis/python-bigquery-pandas/issues
   * - `CSS API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-shopping-css>`_
     - preview
     - |PyPI-google-shopping-css|
     - https://issuetracker.google.com/issues/new?component=826068&template=1564577
   * - `Chat API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-apps-chat>`_
     - preview
     - |PyPI-google-apps-chat|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Commerce Consumer Procurement API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-commerce-consumer-procurement>`_
     - preview
     - |PyPI-google-cloud-commerce-consumer-procurement|
     - https://issuetracker.google.com/issues/new?component=1396141
   * - `Confidential Computing API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-confidentialcomputing>`_
     - preview
     - |PyPI-google-cloud-confidentialcomputing|
     - https://issuetracker.google.com/issues/new?component=1166820
   * - `Controls Partner API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-cloudcontrolspartner>`_
     - preview
     - |PyPI-google-cloud-cloudcontrolspartner|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `DNS <https://github.com/googleapis/python-dns>`_
     - preview
     - |PyPI-google-cloud-dns|
     - https://issuetracker.google.com/savedsearches/559772
   * - `Data Labeling <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-datalabeling>`_
     - preview
     - |PyPI-google-cloud-datalabeling|
     - 
   * - `Data Lineage API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-datacatalog-lineage>`_
     - preview
     - |PyPI-google-cloud-datacatalog-lineage|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Data QnA <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-data-qna>`_
     - preview
     - |PyPI-google-cloud-data-qna|
     - 
   * - `Dataflow <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-dataflow-client>`_
     - preview
     - |PyPI-google-cloud-dataflow-client|
     - 
   * - `Dataform <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-dataform>`_
     - preview
     - |PyPI-google-cloud-dataform|
     - 
   * - `Discovery Engine API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-discoveryengine>`_
     - preview
     - |PyPI-google-cloud-discoveryengine|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Distributed Edge Container <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-edgecontainer>`_
     - preview
     - |PyPI-google-cloud-edgecontainer|
     - 
   * - `Distributed Edge Network API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-edgenetwork>`_
     - preview
     - |PyPI-google-cloud-edgenetwork|
     - https://issuetracker.google.com/issues/new?component=187192&template=1162689
   * - `Document AI Toolbox <https://github.com/googleapis/python-documentai-toolbox>`_
     - preview
     - |PyPI-google-cloud-documentai-toolbox|
     - https://github.com/googleapis/python-documentai-toolbox/issues
   * - `Document AI Warehouse <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-contentwarehouse>`_
     - preview
     - |PyPI-google-cloud-contentwarehouse|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Enterprise Knowledge Graph <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-enterpriseknowledgegraph>`_
     - preview
     - |PyPI-google-cloud-enterpriseknowledgegraph|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Error Reporting <https://github.com/googleapis/python-error-reporting>`_
     - preview
     - |PyPI-google-cloud-error-reporting|
     - https://issuetracker.google.com/savedsearches/559780
   * - `Eventarc Publishing <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-eventarc-publishing>`_
     - preview
     - |PyPI-google-cloud-eventarc-publishing|
     - 
   * - `GKE Connect Gateway <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-gke-connect-gateway>`_
     - preview
     - |PyPI-google-cloud-gke-connect-gateway|
     - 
   * - `Generative Language API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-ai-generativelanguage>`_
     - preview
     - |PyPI-google-ai-generativelanguage|
     - https://github.com/google/generative-ai-python/issues/new
   * - `Geo Type Protos <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-geo-type>`_
     - preview
     - |PyPI-google-geo-type|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Infrastructure Manager API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-config>`_
     - preview
     - |PyPI-google-cloud-config|
     - https://issuetracker.google.com/issues/new?component=536700
   * - `KMS Inventory API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-kms-inventory>`_
     - preview
     - |PyPI-google-cloud-kms-inventory|
     - https://issuetracker.google.com/issues/new?component=190860&template=819701
   * - `Last Mile Fleet Solution Delivery API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-fleetengine-delivery>`_
     - preview
     - |PyPI-google-maps-fleetengine-delivery|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Life Sciences <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-life-sciences>`_
     - preview
     - |PyPI-google-cloud-life-sciences|
     - 
   * - `Local Rides and Deliveries API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-fleetengine>`_
     - preview
     - |PyPI-google-maps-fleetengine|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Maps Platform Datasets API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-mapsplatformdatasets>`_
     - preview
     - |PyPI-google-maps-mapsplatformdatasets|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Maps Routing <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-routing>`_
     - preview
     - |PyPI-google-maps-routing|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Media Translation <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-media-translation>`_
     - preview
     - |PyPI-google-cloud-media-translation|
     - 
   * - `Meet API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-apps-meet>`_
     - preview
     - |PyPI-google-apps-meet|
     - https://issuetracker.google.com/issues/new?component=1216362&template=1766418
   * - `Memorystore for Redis API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-redis-cluster>`_
     - preview
     - |PyPI-google-cloud-redis-cluster|
     - https://issuetracker.google.com/issues/new?component=1288776&template=1161103
   * - `Merchant API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-shopping-merchant-conversions>`_
     - preview
     - |PyPI-google-shopping-merchant-conversions|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Merchant API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-shopping-merchant-lfp>`_
     - preview
     - |PyPI-google-shopping-merchant-lfp|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Merchant API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-shopping-merchant-notifications>`_
     - preview
     - |PyPI-google-shopping-merchant-notifications|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Merchant Inventories API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-shopping-merchant-inventories>`_
     - preview
     - |PyPI-google-shopping-merchant-inventories|
     - https://issuetracker.google.com/issues/new?component=171084&template=555201
   * - `Merchant Reports API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-shopping-merchant-reports>`_
     - preview
     - |PyPI-google-shopping-merchant-reports|
     - https://issuetracker.google.com/issues/new?component=171084&template=555201
   * - `Migration Center API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-migrationcenter>`_
     - preview
     - |PyPI-google-cloud-migrationcenter|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `NetApp API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-netapp>`_
     - preview
     - |PyPI-google-cloud-netapp|
     - https://issuetracker.google.com/issues/new?component=1144971
   * - `Network Security <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-network-security>`_
     - preview
     - |PyPI-google-cloud-network-security|
     - 
   * - `Network Services <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-network-services>`_
     - preview
     - |PyPI-google-cloud-network-services|
     - 
   * - `Parallelstore API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-parallelstore>`_
     - preview
     - |PyPI-google-cloud-parallelstore|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Phishing Protection <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-phishing-protection>`_
     - preview
     - |PyPI-google-cloud-phishing-protection|
     - 
   * - `Places API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-places>`_
     - preview
     - |PyPI-google-maps-places|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Policy Simulator API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-policysimulator>`_
     - preview
     - |PyPI-google-cloud-policysimulator|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Policy Troubleshooter API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-policytroubleshooter-iam>`_
     - preview
     - |PyPI-google-cloud-policytroubleshooter-iam|
     - https://issuetracker.google.com/issues/new?component=690790&template=1814512
   * - `Private Catalog <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-private-catalog>`_
     - preview
     - |PyPI-google-cloud-private-catalog|
     - 
   * - `Public Certificate Authority <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-public-ca>`_
     - preview
     - |PyPI-google-cloud-public-ca|
     - 
   * - `Quotas API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-cloudquotas>`_
     - preview
     - |PyPI-google-cloud-cloudquotas|
     - https://issuetracker.google.com/issues/new?component=445904
   * - `Rapid Migration Assessment API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-rapidmigrationassessment>`_
     - preview
     - |PyPI-google-cloud-rapidmigrationassessment|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Recommendations AI <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-recommendations-ai>`_
     - preview
     - |PyPI-google-cloud-recommendations-ai|
     - 
   * - `Route Optimization API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-routeoptimization>`_
     - preview
     - |PyPI-google-maps-routeoptimization|
     - https://issuetracker.google.com/issues/new?component=1546507
   * - `Run <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-run>`_
     - preview
     - |PyPI-google-cloud-run|
     - 
   * - `Runtime Configurator <https://github.com/googleapis/python-runtimeconfig>`_
     - preview
     - |PyPI-google-cloud-runtimeconfig|
     - https://issuetracker.google.com/savedsearches/559663
   * - `SQLAlchemy dialect for BigQuery <https://github.com/googleapis/python-bigquery-sqlalchemy>`_
     - preview
     - |PyPI-sqlalchemy-bigquery|
     - None
   * - `Secure Source Manager API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-securesourcemanager>`_
     - preview
     - |PyPI-google-cloud-securesourcemanager|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Security Center Management API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-securitycentermanagement>`_
     - preview
     - |PyPI-google-cloud-securitycentermanagement|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Service Health API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-servicehealth>`_
     - preview
     - |PyPI-google-cloud-servicehealth|
     - https://issuetracker.google.com/issues/new?component=1466723&template=1161103
   * - `Shopping Merchant Quota <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-shopping-merchant-quota>`_
     - preview
     - |PyPI-google-shopping-merchant-quota|
     - https://issuetracker.google.com/issues/new?component=171084&template=555201
   * - `Shopping Type Protos <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-shopping-type>`_
     - preview
     - |PyPI-google-shopping-type|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Solar API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-solar>`_
     - preview
     - |PyPI-google-maps-solar|
     - https://issuetracker.google.com/issues/new?component=1356349
   * - `Storage Control API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-storage-control>`_
     - preview
     - |PyPI-google-cloud-storage-control|
     - https://issuetracker.google.com/issues/new?component=187243&template=1162869
   * - `Storage Insights API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-storageinsights>`_
     - preview
     - |PyPI-google-cloud-storageinsights|
     - https://issuetracker.google.com/issues/new?component=1156610
   * - `Support API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-support>`_
     - preview
     - |PyPI-google-cloud-support|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Telco Automation API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-telcoautomation>`_
     - preview
     - |PyPI-google-cloud-telcoautomation|
     - https://issuetracker.google.com/issues/new?component=190865&template=1161103
   * - `VMware Engine <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-vmwareengine>`_
     - preview
     - |PyPI-google-cloud-vmwareengine|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Video Stitcher <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-video-stitcher>`_
     - preview
     - |PyPI-google-cloud-video-stitcher|
     - 
   * - `Vision AI API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-visionai>`_
     - preview
     - |PyPI-google-cloud-visionai|
     - https://issuetracker.google.com/issues/new?component=187174&pli=1&template=1161261
   * - `Workspace Add-ons API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-gsuiteaddons>`_
     - preview
     - |PyPI-google-cloud-gsuiteaddons|
     - 
   * - `Workspace Events API <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-apps-events-subscriptions>`_
     - preview
     - |PyPI-google-apps-events-subscriptions|
     - https://github.com/googleapis/google-cloud-python/issues
   * - `Workstations <https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-workstations>`_
     - preview
     - |PyPI-google-cloud-workstations|
     - https://github.com/googleapis/google-cloud-python/issues

.. |PyPI-google-crc32c| image:: https://img.shields.io/pypi/v/google-crc32c.svg
     :target: https://pypi.org/project/google-crc32c
.. |PyPI-google-cloud-aiplatform| image:: https://img.shields.io/pypi/v/google-cloud-aiplatform.svg
     :target: https://pypi.org/project/google-cloud-aiplatform
.. |PyPI-google-cloud-notebooks| image:: https://img.shields.io/pypi/v/google-cloud-notebooks.svg
     :target: https://pypi.org/project/google-cloud-notebooks
.. |PyPI-google-cloud-api-gateway| image:: https://img.shields.io/pypi/v/google-cloud-api-gateway.svg
     :target: https://pypi.org/project/google-cloud-api-gateway
.. |PyPI-google-cloud-access-approval| image:: https://img.shields.io/pypi/v/google-cloud-access-approval.svg
     :target: https://pypi.org/project/google-cloud-access-approval
.. |PyPI-google-cloud-apigee-connect| image:: https://img.shields.io/pypi/v/google-cloud-apigee-connect.svg
     :target: https://pypi.org/project/google-cloud-apigee-connect
.. |PyPI-google-cloud-appengine-admin| image:: https://img.shields.io/pypi/v/google-cloud-appengine-admin.svg
     :target: https://pypi.org/project/google-cloud-appengine-admin
.. |PyPI-google-cloud-appengine-logging| image:: https://img.shields.io/pypi/v/google-cloud-appengine-logging.svg
     :target: https://pypi.org/project/google-cloud-appengine-logging
.. |PyPI-google-cloud-artifact-registry| image:: https://img.shields.io/pypi/v/google-cloud-artifact-registry.svg
     :target: https://pypi.org/project/google-cloud-artifact-registry
.. |PyPI-google-cloud-asset| image:: https://img.shields.io/pypi/v/google-cloud-asset.svg
     :target: https://pypi.org/project/google-cloud-asset
.. |PyPI-google-cloud-assured-workloads| image:: https://img.shields.io/pypi/v/google-cloud-assured-workloads.svg
     :target: https://pypi.org/project/google-cloud-assured-workloads
.. |PyPI-google-cloud-automl| image:: https://img.shields.io/pypi/v/google-cloud-automl.svg
     :target: https://pypi.org/project/google-cloud-automl
.. |PyPI-google-cloud-bare-metal-solution| image:: https://img.shields.io/pypi/v/google-cloud-bare-metal-solution.svg
     :target: https://pypi.org/project/google-cloud-bare-metal-solution
.. |PyPI-google-cloud-bigquery| image:: https://img.shields.io/pypi/v/google-cloud-bigquery.svg
     :target: https://pypi.org/project/google-cloud-bigquery
.. |PyPI-google-cloud-bigquery-connection| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-connection.svg
     :target: https://pypi.org/project/google-cloud-bigquery-connection
.. |PyPI-google-cloud-bigquery-datatransfer| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-datatransfer.svg
     :target: https://pypi.org/project/google-cloud-bigquery-datatransfer
.. |PyPI-google-cloud-bigquery-logging| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-logging.svg
     :target: https://pypi.org/project/google-cloud-bigquery-logging
.. |PyPI-google-cloud-bigquery-reservation| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-reservation.svg
     :target: https://pypi.org/project/google-cloud-bigquery-reservation
.. |PyPI-google-cloud-bigquery-storage| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-storage.svg
     :target: https://pypi.org/project/google-cloud-bigquery-storage
.. |PyPI-google-cloud-bigtable| image:: https://img.shields.io/pypi/v/google-cloud-bigtable.svg
     :target: https://pypi.org/project/google-cloud-bigtable
.. |PyPI-google-cloud-billing| image:: https://img.shields.io/pypi/v/google-cloud-billing.svg
     :target: https://pypi.org/project/google-cloud-billing
.. |PyPI-google-cloud-billing-budgets| image:: https://img.shields.io/pypi/v/google-cloud-billing-budgets.svg
     :target: https://pypi.org/project/google-cloud-billing-budgets
.. |PyPI-google-cloud-binary-authorization| image:: https://img.shields.io/pypi/v/google-cloud-binary-authorization.svg
     :target: https://pypi.org/project/google-cloud-binary-authorization
.. |PyPI-google-cloud-build| image:: https://img.shields.io/pypi/v/google-cloud-build.svg
     :target: https://pypi.org/project/google-cloud-build
.. |PyPI-google-cloud-certificate-manager| image:: https://img.shields.io/pypi/v/google-cloud-certificate-manager.svg
     :target: https://pypi.org/project/google-cloud-certificate-manager
.. |PyPI-google-cloud-channel| image:: https://img.shields.io/pypi/v/google-cloud-channel.svg
     :target: https://pypi.org/project/google-cloud-channel
.. |PyPI-google-cloud-common| image:: https://img.shields.io/pypi/v/google-cloud-common.svg
     :target: https://pypi.org/project/google-cloud-common
.. |PyPI-google-cloud-orchestration-airflow| image:: https://img.shields.io/pypi/v/google-cloud-orchestration-airflow.svg
     :target: https://pypi.org/project/google-cloud-orchestration-airflow
.. |PyPI-google-cloud-compute| image:: https://img.shields.io/pypi/v/google-cloud-compute.svg
     :target: https://pypi.org/project/google-cloud-compute
.. |PyPI-google-cloud-contact-center-insights| image:: https://img.shields.io/pypi/v/google-cloud-contact-center-insights.svg
     :target: https://pypi.org/project/google-cloud-contact-center-insights
.. |PyPI-google-cloud-containeranalysis| image:: https://img.shields.io/pypi/v/google-cloud-containeranalysis.svg
     :target: https://pypi.org/project/google-cloud-containeranalysis
.. |PyPI-google-cloud-datacatalog| image:: https://img.shields.io/pypi/v/google-cloud-datacatalog.svg
     :target: https://pypi.org/project/google-cloud-datacatalog
.. |PyPI-google-cloud-data-fusion| image:: https://img.shields.io/pypi/v/google-cloud-data-fusion.svg
     :target: https://pypi.org/project/google-cloud-data-fusion
.. |PyPI-google-cloud-dlp| image:: https://img.shields.io/pypi/v/google-cloud-dlp.svg
     :target: https://pypi.org/project/google-cloud-dlp
.. |PyPI-google-cloud-dms| image:: https://img.shields.io/pypi/v/google-cloud-dms.svg
     :target: https://pypi.org/project/google-cloud-dms
.. |PyPI-google-cloud-dataplex| image:: https://img.shields.io/pypi/v/google-cloud-dataplex.svg
     :target: https://pypi.org/project/google-cloud-dataplex
.. |PyPI-google-cloud-dataproc| image:: https://img.shields.io/pypi/v/google-cloud-dataproc.svg
     :target: https://pypi.org/project/google-cloud-dataproc
.. |PyPI-google-cloud-dataproc-metastore| image:: https://img.shields.io/pypi/v/google-cloud-dataproc-metastore.svg
     :target: https://pypi.org/project/google-cloud-dataproc-metastore
.. |PyPI-google-cloud-datastore| image:: https://img.shields.io/pypi/v/google-cloud-datastore.svg
     :target: https://pypi.org/project/google-cloud-datastore
.. |PyPI-google-cloud-datastream| image:: https://img.shields.io/pypi/v/google-cloud-datastream.svg
     :target: https://pypi.org/project/google-cloud-datastream
.. |PyPI-google-cloud-deploy| image:: https://img.shields.io/pypi/v/google-cloud-deploy.svg
     :target: https://pypi.org/project/google-cloud-deploy
.. |PyPI-google-cloud-dialogflow| image:: https://img.shields.io/pypi/v/google-cloud-dialogflow.svg
     :target: https://pypi.org/project/google-cloud-dialogflow
.. |PyPI-google-cloud-dialogflow-cx| image:: https://img.shields.io/pypi/v/google-cloud-dialogflow-cx.svg
     :target: https://pypi.org/project/google-cloud-dialogflow-cx
.. |PyPI-google-cloud-documentai| image:: https://img.shields.io/pypi/v/google-cloud-documentai.svg
     :target: https://pypi.org/project/google-cloud-documentai
.. |PyPI-google-cloud-domains| image:: https://img.shields.io/pypi/v/google-cloud-domains.svg
     :target: https://pypi.org/project/google-cloud-domains
.. |PyPI-google-cloud-essential-contacts| image:: https://img.shields.io/pypi/v/google-cloud-essential-contacts.svg
     :target: https://pypi.org/project/google-cloud-essential-contacts
.. |PyPI-google-cloud-eventarc| image:: https://img.shields.io/pypi/v/google-cloud-eventarc.svg
     :target: https://pypi.org/project/google-cloud-eventarc
.. |PyPI-google-cloud-filestore| image:: https://img.shields.io/pypi/v/google-cloud-filestore.svg
     :target: https://pypi.org/project/google-cloud-filestore
.. |PyPI-google-cloud-firestore| image:: https://img.shields.io/pypi/v/google-cloud-firestore.svg
     :target: https://pypi.org/project/google-cloud-firestore
.. |PyPI-google-cloud-functions| image:: https://img.shields.io/pypi/v/google-cloud-functions.svg
     :target: https://pypi.org/project/google-cloud-functions
.. |PyPI-google-cloud-gke-hub| image:: https://img.shields.io/pypi/v/google-cloud-gke-hub.svg
     :target: https://pypi.org/project/google-cloud-gke-hub
.. |PyPI-grafeas| image:: https://img.shields.io/pypi/v/grafeas.svg
     :target: https://pypi.org/project/grafeas
.. |PyPI-google-cloud-iam-logging| image:: https://img.shields.io/pypi/v/google-cloud-iam-logging.svg
     :target: https://pypi.org/project/google-cloud-iam-logging
.. |PyPI-google-cloud-policy-troubleshooter| image:: https://img.shields.io/pypi/v/google-cloud-policy-troubleshooter.svg
     :target: https://pypi.org/project/google-cloud-policy-troubleshooter
.. |PyPI-google-cloud-ids| image:: https://img.shields.io/pypi/v/google-cloud-ids.svg
     :target: https://pypi.org/project/google-cloud-ids
.. |PyPI-google-cloud-iam| image:: https://img.shields.io/pypi/v/google-cloud-iam.svg
     :target: https://pypi.org/project/google-cloud-iam
.. |PyPI-google-cloud-iap| image:: https://img.shields.io/pypi/v/google-cloud-iap.svg
     :target: https://pypi.org/project/google-cloud-iap
.. |PyPI-google-cloud-kms| image:: https://img.shields.io/pypi/v/google-cloud-kms.svg
     :target: https://pypi.org/project/google-cloud-kms
.. |PyPI-google-cloud-container| image:: https://img.shields.io/pypi/v/google-cloud-container.svg
     :target: https://pypi.org/project/google-cloud-container
.. |PyPI-google-cloud-video-live-stream| image:: https://img.shields.io/pypi/v/google-cloud-video-live-stream.svg
     :target: https://pypi.org/project/google-cloud-video-live-stream
.. |PyPI-google-cloud-logging| image:: https://img.shields.io/pypi/v/google-cloud-logging.svg
     :target: https://pypi.org/project/google-cloud-logging
.. |PyPI-google-cloud-managed-identities| image:: https://img.shields.io/pypi/v/google-cloud-managed-identities.svg
     :target: https://pypi.org/project/google-cloud-managed-identities
.. |PyPI-google-cloud-memcache| image:: https://img.shields.io/pypi/v/google-cloud-memcache.svg
     :target: https://pypi.org/project/google-cloud-memcache
.. |PyPI-google-cloud-monitoring-metrics-scopes| image:: https://img.shields.io/pypi/v/google-cloud-monitoring-metrics-scopes.svg
     :target: https://pypi.org/project/google-cloud-monitoring-metrics-scopes
.. |PyPI-google-cloud-monitoring-dashboards| image:: https://img.shields.io/pypi/v/google-cloud-monitoring-dashboards.svg
     :target: https://pypi.org/project/google-cloud-monitoring-dashboards
.. |PyPI-google-cloud-ndb| image:: https://img.shields.io/pypi/v/google-cloud-ndb.svg
     :target: https://pypi.org/project/google-cloud-ndb
.. |PyPI-google-cloud-language| image:: https://img.shields.io/pypi/v/google-cloud-language.svg
     :target: https://pypi.org/project/google-cloud-language
.. |PyPI-google-cloud-network-connectivity| image:: https://img.shields.io/pypi/v/google-cloud-network-connectivity.svg
     :target: https://pypi.org/project/google-cloud-network-connectivity
.. |PyPI-google-cloud-network-management| image:: https://img.shields.io/pypi/v/google-cloud-network-management.svg
     :target: https://pypi.org/project/google-cloud-network-management
.. |PyPI-google-cloud-os-config| image:: https://img.shields.io/pypi/v/google-cloud-os-config.svg
     :target: https://pypi.org/project/google-cloud-os-config
.. |PyPI-google-cloud-os-login| image:: https://img.shields.io/pypi/v/google-cloud-os-login.svg
     :target: https://pypi.org/project/google-cloud-os-login
.. |PyPI-google-cloud-optimization| image:: https://img.shields.io/pypi/v/google-cloud-optimization.svg
     :target: https://pypi.org/project/google-cloud-optimization
.. |PyPI-db-dtypes| image:: https://img.shields.io/pypi/v/db-dtypes.svg
     :target: https://pypi.org/project/db-dtypes
.. |PyPI-google-cloud-private-ca| image:: https://img.shields.io/pypi/v/google-cloud-private-ca.svg
     :target: https://pypi.org/project/google-cloud-private-ca
.. |PyPI-google-cloud-pubsub| image:: https://img.shields.io/pypi/v/google-cloud-pubsub.svg
     :target: https://pypi.org/project/google-cloud-pubsub
.. |PyPI-google-cloud-pubsublite| image:: https://img.shields.io/pypi/v/google-cloud-pubsublite.svg
     :target: https://pypi.org/project/google-cloud-pubsublite
.. |PyPI-google-cloud-recommender| image:: https://img.shields.io/pypi/v/google-cloud-recommender.svg
     :target: https://pypi.org/project/google-cloud-recommender
.. |PyPI-google-cloud-redis| image:: https://img.shields.io/pypi/v/google-cloud-redis.svg
     :target: https://pypi.org/project/google-cloud-redis
.. |PyPI-google-cloud-resource-manager| image:: https://img.shields.io/pypi/v/google-cloud-resource-manager.svg
     :target: https://pypi.org/project/google-cloud-resource-manager
.. |PyPI-google-cloud-resource-settings| image:: https://img.shields.io/pypi/v/google-cloud-resource-settings.svg
     :target: https://pypi.org/project/google-cloud-resource-settings
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
.. |PyPI-google-cloud-service-usage| image:: https://img.shields.io/pypi/v/google-cloud-service-usage.svg
     :target: https://pypi.org/project/google-cloud-service-usage
.. |PyPI-google-cloud-shell| image:: https://img.shields.io/pypi/v/google-cloud-shell.svg
     :target: https://pypi.org/project/google-cloud-shell
.. |PyPI-google-cloud-source-context| image:: https://img.shields.io/pypi/v/google-cloud-source-context.svg
     :target: https://pypi.org/project/google-cloud-source-context
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
.. |PyPI-google-cloud-tpu| image:: https://img.shields.io/pypi/v/google-cloud-tpu.svg
     :target: https://pypi.org/project/google-cloud-tpu
.. |PyPI-google-cloud-talent| image:: https://img.shields.io/pypi/v/google-cloud-talent.svg
     :target: https://pypi.org/project/google-cloud-talent
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
.. |PyPI-google-cloud-vm-migration| image:: https://img.shields.io/pypi/v/google-cloud-vm-migration.svg
     :target: https://pypi.org/project/google-cloud-vm-migration
.. |PyPI-google-cloud-videointelligence| image:: https://img.shields.io/pypi/v/google-cloud-videointelligence.svg
     :target: https://pypi.org/project/google-cloud-videointelligence
.. |PyPI-google-cloud-vpc-access| image:: https://img.shields.io/pypi/v/google-cloud-vpc-access.svg
     :target: https://pypi.org/project/google-cloud-vpc-access
.. |PyPI-google-cloud-vision| image:: https://img.shields.io/pypi/v/google-cloud-vision.svg
     :target: https://pypi.org/project/google-cloud-vision
.. |PyPI-google-cloud-webrisk| image:: https://img.shields.io/pypi/v/google-cloud-webrisk.svg
     :target: https://pypi.org/project/google-cloud-webrisk
.. |PyPI-google-cloud-workflows| image:: https://img.shields.io/pypi/v/google-cloud-workflows.svg
     :target: https://pypi.org/project/google-cloud-workflows
.. |PyPI-google-cloud-recaptcha-enterprise| image:: https://img.shields.io/pypi/v/google-cloud-recaptcha-enterprise.svg
     :target: https://pypi.org/project/google-cloud-recaptcha-enterprise
.. |PyPI-bigframes| image:: https://img.shields.io/pypi/v/bigframes.svg
     :target: https://pypi.org/project/bigframes
.. |PyPI-google-cloud-api-keys| image:: https://img.shields.io/pypi/v/google-cloud-api-keys.svg
     :target: https://pypi.org/project/google-cloud-api-keys
.. |PyPI-google-ads-admanager| image:: https://img.shields.io/pypi/v/google-ads-admanager.svg
     :target: https://pypi.org/project/google-ads-admanager
.. |PyPI-google-maps-addressvalidation| image:: https://img.shields.io/pypi/v/google-maps-addressvalidation.svg
     :target: https://pypi.org/project/google-maps-addressvalidation
.. |PyPI-google-cloud-advisorynotifications| image:: https://img.shields.io/pypi/v/google-cloud-advisorynotifications.svg
     :target: https://pypi.org/project/google-cloud-advisorynotifications
.. |PyPI-google-cloud-alloydb| image:: https://img.shields.io/pypi/v/google-cloud-alloydb.svg
     :target: https://pypi.org/project/google-cloud-alloydb
.. |PyPI-google-cloud-alloydb-connectors| image:: https://img.shields.io/pypi/v/google-cloud-alloydb-connectors.svg
     :target: https://pypi.org/project/google-cloud-alloydb-connectors
.. |PyPI-google-analytics-admin| image:: https://img.shields.io/pypi/v/google-analytics-admin.svg
     :target: https://pypi.org/project/google-analytics-admin
.. |PyPI-google-analytics-data| image:: https://img.shields.io/pypi/v/google-analytics-data.svg
     :target: https://pypi.org/project/google-analytics-data
.. |PyPI-google-cloud-gke-multicloud| image:: https://img.shields.io/pypi/v/google-cloud-gke-multicloud.svg
     :target: https://pypi.org/project/google-cloud-gke-multicloud
.. |PyPI-google-cloud-apigee-registry| image:: https://img.shields.io/pypi/v/google-cloud-apigee-registry.svg
     :target: https://pypi.org/project/google-cloud-apigee-registry
.. |PyPI-google-cloud-apphub| image:: https://img.shields.io/pypi/v/google-cloud-apphub.svg
     :target: https://pypi.org/project/google-cloud-apphub
.. |PyPI-google-apps-card| image:: https://img.shields.io/pypi/v/google-apps-card.svg
     :target: https://pypi.org/project/google-apps-card
.. |PyPI-google-apps-script-type| image:: https://img.shields.io/pypi/v/google-apps-script-type.svg
     :target: https://pypi.org/project/google-apps-script-type
.. |PyPI-google-area120-tables| image:: https://img.shields.io/pypi/v/google-area120-tables.svg
     :target: https://pypi.org/project/google-area120-tables
.. |PyPI-google-cloud-backupdr| image:: https://img.shields.io/pypi/v/google-cloud-backupdr.svg
     :target: https://pypi.org/project/google-cloud-backupdr
.. |PyPI-google-cloud-gke-backup| image:: https://img.shields.io/pypi/v/google-cloud-gke-backup.svg
     :target: https://pypi.org/project/google-cloud-gke-backup
.. |PyPI-google-cloud-batch| image:: https://img.shields.io/pypi/v/google-cloud-batch.svg
     :target: https://pypi.org/project/google-cloud-batch
.. |PyPI-google-cloud-beyondcorp-appconnections| image:: https://img.shields.io/pypi/v/google-cloud-beyondcorp-appconnections.svg
     :target: https://pypi.org/project/google-cloud-beyondcorp-appconnections
.. |PyPI-google-cloud-beyondcorp-appconnectors| image:: https://img.shields.io/pypi/v/google-cloud-beyondcorp-appconnectors.svg
     :target: https://pypi.org/project/google-cloud-beyondcorp-appconnectors
.. |PyPI-google-cloud-beyondcorp-appgateways| image:: https://img.shields.io/pypi/v/google-cloud-beyondcorp-appgateways.svg
     :target: https://pypi.org/project/google-cloud-beyondcorp-appgateways
.. |PyPI-google-cloud-beyondcorp-clientconnectorservices| image:: https://img.shields.io/pypi/v/google-cloud-beyondcorp-clientconnectorservices.svg
     :target: https://pypi.org/project/google-cloud-beyondcorp-clientconnectorservices
.. |PyPI-google-cloud-beyondcorp-clientgateways| image:: https://img.shields.io/pypi/v/google-cloud-beyondcorp-clientgateways.svg
     :target: https://pypi.org/project/google-cloud-beyondcorp-clientgateways
.. |PyPI-google-cloud-bigquery-biglake| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-biglake.svg
     :target: https://pypi.org/project/google-cloud-bigquery-biglake
.. |PyPI-google-cloud-bigquery-analyticshub| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-analyticshub.svg
     :target: https://pypi.org/project/google-cloud-bigquery-analyticshub
.. |PyPI-google-cloud-bigquery-data-exchange| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-data-exchange.svg
     :target: https://pypi.org/project/google-cloud-bigquery-data-exchange
.. |PyPI-google-cloud-bigquery-datapolicies| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-datapolicies.svg
     :target: https://pypi.org/project/google-cloud-bigquery-datapolicies
.. |PyPI-google-cloud-bigquery-migration| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-migration.svg
     :target: https://pypi.org/project/google-cloud-bigquery-migration
.. |PyPI-pandas-gbq| image:: https://img.shields.io/pypi/v/pandas-gbq.svg
     :target: https://pypi.org/project/pandas-gbq
.. |PyPI-google-shopping-css| image:: https://img.shields.io/pypi/v/google-shopping-css.svg
     :target: https://pypi.org/project/google-shopping-css
.. |PyPI-google-apps-chat| image:: https://img.shields.io/pypi/v/google-apps-chat.svg
     :target: https://pypi.org/project/google-apps-chat
.. |PyPI-google-cloud-commerce-consumer-procurement| image:: https://img.shields.io/pypi/v/google-cloud-commerce-consumer-procurement.svg
     :target: https://pypi.org/project/google-cloud-commerce-consumer-procurement
.. |PyPI-google-cloud-confidentialcomputing| image:: https://img.shields.io/pypi/v/google-cloud-confidentialcomputing.svg
     :target: https://pypi.org/project/google-cloud-confidentialcomputing
.. |PyPI-google-cloud-cloudcontrolspartner| image:: https://img.shields.io/pypi/v/google-cloud-cloudcontrolspartner.svg
     :target: https://pypi.org/project/google-cloud-cloudcontrolspartner
.. |PyPI-google-cloud-dns| image:: https://img.shields.io/pypi/v/google-cloud-dns.svg
     :target: https://pypi.org/project/google-cloud-dns
.. |PyPI-google-cloud-datalabeling| image:: https://img.shields.io/pypi/v/google-cloud-datalabeling.svg
     :target: https://pypi.org/project/google-cloud-datalabeling
.. |PyPI-google-cloud-datacatalog-lineage| image:: https://img.shields.io/pypi/v/google-cloud-datacatalog-lineage.svg
     :target: https://pypi.org/project/google-cloud-datacatalog-lineage
.. |PyPI-google-cloud-data-qna| image:: https://img.shields.io/pypi/v/google-cloud-data-qna.svg
     :target: https://pypi.org/project/google-cloud-data-qna
.. |PyPI-google-cloud-dataflow-client| image:: https://img.shields.io/pypi/v/google-cloud-dataflow-client.svg
     :target: https://pypi.org/project/google-cloud-dataflow-client
.. |PyPI-google-cloud-dataform| image:: https://img.shields.io/pypi/v/google-cloud-dataform.svg
     :target: https://pypi.org/project/google-cloud-dataform
.. |PyPI-google-cloud-discoveryengine| image:: https://img.shields.io/pypi/v/google-cloud-discoveryengine.svg
     :target: https://pypi.org/project/google-cloud-discoveryengine
.. |PyPI-google-cloud-edgecontainer| image:: https://img.shields.io/pypi/v/google-cloud-edgecontainer.svg
     :target: https://pypi.org/project/google-cloud-edgecontainer
.. |PyPI-google-cloud-edgenetwork| image:: https://img.shields.io/pypi/v/google-cloud-edgenetwork.svg
     :target: https://pypi.org/project/google-cloud-edgenetwork
.. |PyPI-google-cloud-documentai-toolbox| image:: https://img.shields.io/pypi/v/google-cloud-documentai-toolbox.svg
     :target: https://pypi.org/project/google-cloud-documentai-toolbox
.. |PyPI-google-cloud-contentwarehouse| image:: https://img.shields.io/pypi/v/google-cloud-contentwarehouse.svg
     :target: https://pypi.org/project/google-cloud-contentwarehouse
.. |PyPI-google-cloud-enterpriseknowledgegraph| image:: https://img.shields.io/pypi/v/google-cloud-enterpriseknowledgegraph.svg
     :target: https://pypi.org/project/google-cloud-enterpriseknowledgegraph
.. |PyPI-google-cloud-error-reporting| image:: https://img.shields.io/pypi/v/google-cloud-error-reporting.svg
     :target: https://pypi.org/project/google-cloud-error-reporting
.. |PyPI-google-cloud-eventarc-publishing| image:: https://img.shields.io/pypi/v/google-cloud-eventarc-publishing.svg
     :target: https://pypi.org/project/google-cloud-eventarc-publishing
.. |PyPI-google-cloud-gke-connect-gateway| image:: https://img.shields.io/pypi/v/google-cloud-gke-connect-gateway.svg
     :target: https://pypi.org/project/google-cloud-gke-connect-gateway
.. |PyPI-google-ai-generativelanguage| image:: https://img.shields.io/pypi/v/google-ai-generativelanguage.svg
     :target: https://pypi.org/project/google-ai-generativelanguage
.. |PyPI-google-geo-type| image:: https://img.shields.io/pypi/v/google-geo-type.svg
     :target: https://pypi.org/project/google-geo-type
.. |PyPI-google-cloud-config| image:: https://img.shields.io/pypi/v/google-cloud-config.svg
     :target: https://pypi.org/project/google-cloud-config
.. |PyPI-google-cloud-kms-inventory| image:: https://img.shields.io/pypi/v/google-cloud-kms-inventory.svg
     :target: https://pypi.org/project/google-cloud-kms-inventory
.. |PyPI-google-maps-fleetengine-delivery| image:: https://img.shields.io/pypi/v/google-maps-fleetengine-delivery.svg
     :target: https://pypi.org/project/google-maps-fleetengine-delivery
.. |PyPI-google-cloud-life-sciences| image:: https://img.shields.io/pypi/v/google-cloud-life-sciences.svg
     :target: https://pypi.org/project/google-cloud-life-sciences
.. |PyPI-google-maps-fleetengine| image:: https://img.shields.io/pypi/v/google-maps-fleetengine.svg
     :target: https://pypi.org/project/google-maps-fleetengine
.. |PyPI-google-maps-mapsplatformdatasets| image:: https://img.shields.io/pypi/v/google-maps-mapsplatformdatasets.svg
     :target: https://pypi.org/project/google-maps-mapsplatformdatasets
.. |PyPI-google-maps-routing| image:: https://img.shields.io/pypi/v/google-maps-routing.svg
     :target: https://pypi.org/project/google-maps-routing
.. |PyPI-google-cloud-media-translation| image:: https://img.shields.io/pypi/v/google-cloud-media-translation.svg
     :target: https://pypi.org/project/google-cloud-media-translation
.. |PyPI-google-apps-meet| image:: https://img.shields.io/pypi/v/google-apps-meet.svg
     :target: https://pypi.org/project/google-apps-meet
.. |PyPI-google-cloud-redis-cluster| image:: https://img.shields.io/pypi/v/google-cloud-redis-cluster.svg
     :target: https://pypi.org/project/google-cloud-redis-cluster
.. |PyPI-google-shopping-merchant-conversions| image:: https://img.shields.io/pypi/v/google-shopping-merchant-conversions.svg
     :target: https://pypi.org/project/google-shopping-merchant-conversions
.. |PyPI-google-shopping-merchant-lfp| image:: https://img.shields.io/pypi/v/google-shopping-merchant-lfp.svg
     :target: https://pypi.org/project/google-shopping-merchant-lfp
.. |PyPI-google-shopping-merchant-notifications| image:: https://img.shields.io/pypi/v/google-shopping-merchant-notifications.svg
     :target: https://pypi.org/project/google-shopping-merchant-notifications
.. |PyPI-google-shopping-merchant-inventories| image:: https://img.shields.io/pypi/v/google-shopping-merchant-inventories.svg
     :target: https://pypi.org/project/google-shopping-merchant-inventories
.. |PyPI-google-shopping-merchant-reports| image:: https://img.shields.io/pypi/v/google-shopping-merchant-reports.svg
     :target: https://pypi.org/project/google-shopping-merchant-reports
.. |PyPI-google-cloud-migrationcenter| image:: https://img.shields.io/pypi/v/google-cloud-migrationcenter.svg
     :target: https://pypi.org/project/google-cloud-migrationcenter
.. |PyPI-google-cloud-netapp| image:: https://img.shields.io/pypi/v/google-cloud-netapp.svg
     :target: https://pypi.org/project/google-cloud-netapp
.. |PyPI-google-cloud-network-security| image:: https://img.shields.io/pypi/v/google-cloud-network-security.svg
     :target: https://pypi.org/project/google-cloud-network-security
.. |PyPI-google-cloud-network-services| image:: https://img.shields.io/pypi/v/google-cloud-network-services.svg
     :target: https://pypi.org/project/google-cloud-network-services
.. |PyPI-google-cloud-parallelstore| image:: https://img.shields.io/pypi/v/google-cloud-parallelstore.svg
     :target: https://pypi.org/project/google-cloud-parallelstore
.. |PyPI-google-cloud-phishing-protection| image:: https://img.shields.io/pypi/v/google-cloud-phishing-protection.svg
     :target: https://pypi.org/project/google-cloud-phishing-protection
.. |PyPI-google-maps-places| image:: https://img.shields.io/pypi/v/google-maps-places.svg
     :target: https://pypi.org/project/google-maps-places
.. |PyPI-google-cloud-policysimulator| image:: https://img.shields.io/pypi/v/google-cloud-policysimulator.svg
     :target: https://pypi.org/project/google-cloud-policysimulator
.. |PyPI-google-cloud-policytroubleshooter-iam| image:: https://img.shields.io/pypi/v/google-cloud-policytroubleshooter-iam.svg
     :target: https://pypi.org/project/google-cloud-policytroubleshooter-iam
.. |PyPI-google-cloud-private-catalog| image:: https://img.shields.io/pypi/v/google-cloud-private-catalog.svg
     :target: https://pypi.org/project/google-cloud-private-catalog
.. |PyPI-google-cloud-public-ca| image:: https://img.shields.io/pypi/v/google-cloud-public-ca.svg
     :target: https://pypi.org/project/google-cloud-public-ca
.. |PyPI-google-cloud-cloudquotas| image:: https://img.shields.io/pypi/v/google-cloud-cloudquotas.svg
     :target: https://pypi.org/project/google-cloud-cloudquotas
.. |PyPI-google-cloud-rapidmigrationassessment| image:: https://img.shields.io/pypi/v/google-cloud-rapidmigrationassessment.svg
     :target: https://pypi.org/project/google-cloud-rapidmigrationassessment
.. |PyPI-google-cloud-recommendations-ai| image:: https://img.shields.io/pypi/v/google-cloud-recommendations-ai.svg
     :target: https://pypi.org/project/google-cloud-recommendations-ai
.. |PyPI-google-maps-routeoptimization| image:: https://img.shields.io/pypi/v/google-maps-routeoptimization.svg
     :target: https://pypi.org/project/google-maps-routeoptimization
.. |PyPI-google-cloud-run| image:: https://img.shields.io/pypi/v/google-cloud-run.svg
     :target: https://pypi.org/project/google-cloud-run
.. |PyPI-google-cloud-runtimeconfig| image:: https://img.shields.io/pypi/v/google-cloud-runtimeconfig.svg
     :target: https://pypi.org/project/google-cloud-runtimeconfig
.. |PyPI-sqlalchemy-bigquery| image:: https://img.shields.io/pypi/v/sqlalchemy-bigquery.svg
     :target: https://pypi.org/project/sqlalchemy-bigquery
.. |PyPI-google-cloud-securesourcemanager| image:: https://img.shields.io/pypi/v/google-cloud-securesourcemanager.svg
     :target: https://pypi.org/project/google-cloud-securesourcemanager
.. |PyPI-google-cloud-securitycentermanagement| image:: https://img.shields.io/pypi/v/google-cloud-securitycentermanagement.svg
     :target: https://pypi.org/project/google-cloud-securitycentermanagement
.. |PyPI-google-cloud-servicehealth| image:: https://img.shields.io/pypi/v/google-cloud-servicehealth.svg
     :target: https://pypi.org/project/google-cloud-servicehealth
.. |PyPI-google-shopping-merchant-quota| image:: https://img.shields.io/pypi/v/google-shopping-merchant-quota.svg
     :target: https://pypi.org/project/google-shopping-merchant-quota
.. |PyPI-google-shopping-type| image:: https://img.shields.io/pypi/v/google-shopping-type.svg
     :target: https://pypi.org/project/google-shopping-type
.. |PyPI-google-maps-solar| image:: https://img.shields.io/pypi/v/google-maps-solar.svg
     :target: https://pypi.org/project/google-maps-solar
.. |PyPI-google-cloud-storage-control| image:: https://img.shields.io/pypi/v/google-cloud-storage-control.svg
     :target: https://pypi.org/project/google-cloud-storage-control
.. |PyPI-google-cloud-storageinsights| image:: https://img.shields.io/pypi/v/google-cloud-storageinsights.svg
     :target: https://pypi.org/project/google-cloud-storageinsights
.. |PyPI-google-cloud-support| image:: https://img.shields.io/pypi/v/google-cloud-support.svg
     :target: https://pypi.org/project/google-cloud-support
.. |PyPI-google-cloud-telcoautomation| image:: https://img.shields.io/pypi/v/google-cloud-telcoautomation.svg
     :target: https://pypi.org/project/google-cloud-telcoautomation
.. |PyPI-google-cloud-vmwareengine| image:: https://img.shields.io/pypi/v/google-cloud-vmwareengine.svg
     :target: https://pypi.org/project/google-cloud-vmwareengine
.. |PyPI-google-cloud-video-stitcher| image:: https://img.shields.io/pypi/v/google-cloud-video-stitcher.svg
     :target: https://pypi.org/project/google-cloud-video-stitcher
.. |PyPI-google-cloud-visionai| image:: https://img.shields.io/pypi/v/google-cloud-visionai.svg
     :target: https://pypi.org/project/google-cloud-visionai
.. |PyPI-google-cloud-gsuiteaddons| image:: https://img.shields.io/pypi/v/google-cloud-gsuiteaddons.svg
     :target: https://pypi.org/project/google-cloud-gsuiteaddons
.. |PyPI-google-apps-events-subscriptions| image:: https://img.shields.io/pypi/v/google-apps-events-subscriptions.svg
     :target: https://pypi.org/project/google-apps-events-subscriptions
.. |PyPI-google-cloud-workstations| image:: https://img.shields.io/pypi/v/google-cloud-workstations.svg
     :target: https://pypi.org/project/google-cloud-workstations

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
