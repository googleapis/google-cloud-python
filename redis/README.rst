Python Client for Google Cloud Memorystore for Redis API
========================================================

|alpha| |pypi| |versions| 

`Google Cloud Memorystore for Redis API`_: The Google Cloud Memorystore for
Redis API is used for creating and managing Redis instances on the Google
Cloud Platform.

- `Client Library Documentation`_
- `Product Documentation`_

.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-redis.svg
   :target: https://pypi.org/project/google-cloud-redis/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-redis.svg
   :target: https://pypi.org/project/google-cloud-redis/
.. _Google Cloud Memorystore for Redis API: https://cloud.google.com/memorystore/
.. _Client Library Documentation: https://googleapis.dev/python/redis/latest
.. _Product Documentation:  https://cloud.google.com/memorystore/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Memorystore for Redis API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Memorystore for Redis API.:  https://console.cloud.google.com/apis/library/redis.googleapis.com
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.5

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7. Python 2.7 support will be removed on January 1, 2020.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-redis


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-redis

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Cloud Memorystore for
   Redis API to see other available methods on the client.
-  Read the `Product documentation`_ to learn more about the product and see
   How-to Guides.
