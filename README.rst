Google Cloud Python Client
==========================

    Python idiomatic client for `Google Cloud Platform`_ services.

.. _Google Cloud Platform: https://cloud.google.com/

|pypi| |build| |appveyor| |coverage| |versions|

-  `Homepage`_
-  `API Documentation`_

.. _Homepage: https://googlecloudplatform.github.io/google-cloud-python/
.. _API Documentation: http://googlecloudplatform.github.io/google-cloud-python/

This client supports the following Google Cloud Platform services:

-  `Google Cloud Datastore`_
-  `Google Cloud Storage`_
-  `Google Cloud Pub/Sub`_
-  `Google BigQuery`_
-  `Google Cloud Resource Manager`_
-  `Google Stackdriver Logging`_
-  `Google Stackdriver Monitoring`_

.. _Google Cloud Datastore: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/datastore
.. _Google Cloud Storage: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/storage
.. _Google Cloud Pub/Sub: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/pubsub
.. _Google BigQuery: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/bigquery
.. _Google Cloud Resource Manager: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/resource_manager
.. _Google Stackdriver Logging: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/logging
.. _Google Stackdriver Monitoring: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/monitoring

If you need support for other Google APIs, check out the
`Google APIs Python Client library`_.

.. _Google APIs Python Client library: https://github.com/google/google-api-python-client

Quick Start
-----------

::

    $ pip install --upgrade google-cloud

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

.. _Authentication section: http://google-cloud-python.readthedocs.io/en/latest/google-cloud-auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/gcloud-common/tree/master/authentication

Contributing
------------

Contributions to this library are always welcome and highly encouraged.

See `CONTRIBUTING`_ for more information on how to get started.

.. _CONTRIBUTING: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/CONTRIBUTING.rst

License
-------

Apache 2.0 - See `LICENSE`_ for more information.

.. _LICENSE: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/LICENSE

.. |build| image:: https://travis-ci.org/GoogleCloudPlatform/google-cloud-python.svg?branch=master
   :target: https://travis-ci.org/GoogleCloudPlatform/google-cloud-python
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/googlecloudplatform/google-cloud-python?branch=master&svg=true
   :target: https://ci.appveyor.com/project/GoogleCloudPlatform/google-cloud-python
.. |coverage| image:: https://coveralls.io/repos/GoogleCloudPlatform/google-cloud-python/badge.png?branch=master
   :target: https://coveralls.io/r/GoogleCloudPlatform/google-cloud-python?branch=master
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud.svg
   :target: https://pypi.python.org/pypi/google-cloud
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud.svg
   :target: https://pypi.python.org/pypi/google-cloud
