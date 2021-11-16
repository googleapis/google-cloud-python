Python Client for BigQuery Data Transfer API
============================================

|GA| |pypi| |versions|

The `BigQuery Data Transfer API`_ allows users to transfer data from partner
SaaS applications to Google BigQuery on a scheduled, managed basis.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-datatransfer.svg
   :target: https://pypi.org/project/google-cloud-bigquery-datatransfer/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-bigquery-datatransfer.svg
   :target: https://pypi.org/project/google-cloud-bigquery-datatransfer/
.. _BigQuery Data Transfer API: https://cloud.google.com/bigquery/transfer
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/bigquerydatatransfer/latest
.. _Product Documentation:  https://cloud.google.com/bigquery/docs/transfer-service-overview

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable the BigQuery Data Transfer API.`_
3. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable the BigQuery Data Transfer API.:  https://cloud.google.com/bigquery/docs/transfer-service-overview
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
Python >= 3.6

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7.

The last version of this library compatible with Python 2.7 is
``google-cloud-bigquery-datatransfer==1.1.1``.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-bigquery-datatransfer


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-bigquery-datatransfer

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for BigQuery Data Transfer API
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
