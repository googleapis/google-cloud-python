Google Cloud Python Client
==========================

    Python idiomatic client for `Google Cloud Platform`_ services.

.. _Google Cloud Platform: https://cloud.google.com/

|pypi| |circleci| |appveyor| |coverage| |versions|

-  `Homepage`_
-  `API Documentation`_
-  `Read The Docs Documentation`_

.. _Homepage: https://googlecloudplatform.github.io/google-cloud-python/
.. _API Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/
.. _Read The Docs Documentation: https://google-cloud-python.readthedocs.io/en/latest/

.. note::

    These libraries currently do not run on Google App Engine Standard.
    We are actively working on adding this support.

The following client libraries have **GA** support:

-  `Google Cloud Datastore`_ (`Datastore README`_)
-  `Google Cloud Natural Language`_ (`Natural Language README`_)
-  `Google Cloud Storage`_ (`Storage README`_)
-  `Google Cloud Translation`_ (`Translation README`_)
-  `Stackdriver Logging`_ (`Logging README`_)

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

The following client libraries have **beta** support:

-  `Google BigQuery`_ (`BigQuery README`_)
-  `Google Cloud Firestore`_ (`Firestore README`_)
-  `Google Cloud Pub/Sub`_ (`Pub/Sub README`_)
-  `Google Cloud Spanner`_ (`Spanner README`_)
-  `Google Cloud Speech`_ (`Speech README`_)
-  `Google Cloud Video Intelligence`_ (`Video Intelligence README`_)
-  `Google Cloud Vision`_ (`Vision README`_)

**Beta** indicates that the client library for a particular service is
mostly stable and is being prepared for release. Issues and requests
against beta libraries are addressed with a higher priority.

This client library has **alpha** support for the following Google
Cloud Platform services:

-  `Google Cloud Bigtable`_ (`Bigtable README`_)
-  `Google Cloud Bigtable - HappyBase`_ (`HappyBase README`_)
-  `Google Cloud DNS`_ (`DNS README`_)
-  `Google Cloud Resource Manager`_ (`Resource Manager README`_)
-  `Google Cloud Runtime Configuration`_ (`Runtime Config README`_)
-  `Stackdriver Error Reporting`_ (`Error Reporting README`_)
-  `Stackdriver Monitoring`_ (`Monitoring README`_)

**Alpha** indicates that the client library for a particular service is
still a work-in-progress and is more likely to get backwards-incompatible
updates. See `versioning`_ for more details.

.. _Google Cloud Datastore: https://pypi.org/project/google-cloud-datastore/
.. _Datastore README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/datastore
.. _Google Cloud Storage: https://pypi.org/project/google-cloud-storage/
.. _Storage README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/storage
.. _Google Cloud Pub/Sub: https://pypi.org/project/google-cloud-pubsub/
.. _Pub/Sub README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/pubsub
.. _Google BigQuery: https://pypi.org/project/google-cloud-bigquery/
.. _BigQuery README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/bigquery
.. _Google Cloud Resource Manager: https://pypi.org/project/google-cloud-resource-manager/
.. _Resource Manager README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/resource_manager
.. _Stackdriver Logging: https://pypi.org/project/google-cloud-logging/
.. _Logging README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/logging
.. _Stackdriver Monitoring: https://pypi.org/project/google-cloud-monitoring/
.. _Monitoring README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/monitoring
.. _Google Cloud Bigtable: https://pypi.org/project/google-cloud-bigtable/
.. _Bigtable README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/bigtable
.. _Google Cloud DNS: https://pypi.org/project/google-cloud-dns/
.. _DNS README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/dns
.. _Stackdriver Error Reporting: https://pypi.org/project/google-cloud-error-reporting/
.. _Error Reporting README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/error_reporting
.. _Google Cloud Natural Language: https://pypi.org/project/google-cloud-language/
.. _Natural Language README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/language
.. _Google Cloud Translation: https://pypi.org/project/google-cloud-translate/
.. _Translation README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/translate
.. _Google Cloud Speech: https://pypi.org/project/google-cloud-speech/
.. _Speech README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/speech
.. _Google Cloud Vision: https://pypi.org/project/google-cloud-vision/
.. _Vision README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/vision
.. _Google Cloud Bigtable - HappyBase: https://pypi.org/project/google-cloud-happybase/
.. _HappyBase README: https://github.com/GoogleCloudPlatform/google-cloud-python-happybase
.. _Google Cloud Runtime Configuration: https://cloud.google.com/deployment-manager/runtime-configurator/
.. _Runtime Config README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/runtimeconfig
.. _Google Cloud Spanner: https://pypi.python.org/pypi/google-cloud-spanner
.. _Spanner README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/spanner
.. _Google Cloud Video Intelligence: https://pypi.python.org/pypi/google-cloud-videointelligence
.. _Video Intelligence README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/videointelligence
.. _versioning: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/CONTRIBUTING.rst#versioning
.. _Google Cloud Firestore: https://pypi.org/project/google-cloud-firestore/
.. _Firestore README: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/firestore

If you need support for other Google APIs, check out the
`Google APIs Python Client library`_.

.. _Google APIs Python Client library: https://github.com/google/google-api-python-client

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud

For more information on setting up your Python development environment,
such as installing ``pip`` and ``virtualenv`` on your system, please refer
to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup

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

.. _Authentication section: https://google-cloud-python.readthedocs.io/en/latest/core/auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/google-cloud-common/tree/master/authentication

Contributing
------------

Contributions to this library are always welcome and highly encouraged.

See the `CONTRIBUTING doc`_ for more information on how to get started.

.. _CONTRIBUTING doc: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/CONTRIBUTING.rst

Community
---------

Google Cloud Platform Python developers hang out in `Slack`_ in the ``#python``
channel, click here to `get an invitation`_.


.. _Slack: https://googlecloud-community.slack.com
.. _get an invitation: https://gcp-slack.appspot.com/

License
-------

Apache 2.0 - See `the LICENSE`_ for more information.

.. _the LICENSE: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/LICENSE

.. |circleci| image:: https://circleci.com/gh/GoogleCloudPlatform/google-cloud-python.svg?style=shield
   :target: https://circleci.com/gh/GoogleCloudPlatform/google-cloud-python
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/googlecloudplatform/google-cloud-python?branch=master&svg=true
   :target: https://ci.appveyor.com/project/GoogleCloudPlatform/google-cloud-python
.. |coverage| image:: https://coveralls.io/repos/GoogleCloudPlatform/google-cloud-python/badge.svg?branch=master
   :target: https://coveralls.io/r/GoogleCloudPlatform/google-cloud-python?branch=master
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud.svg
   :target: https://pypi.org/project/google-cloud/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud.svg
   :target: https://pypi.org/project/google-cloud/
