Python Client for Cloud Storage Transfer API
============================================

|GA| |pypi| |versions|

`Storage Transfer Service`_ is a product that enables you to:
- Move or backup data to a Cloud Storage bucket either from other cloud storage providers or from your on-premises storage.
- Move data from one Cloud Storage bucket to another, so that it is available to different groups of users or applications.
- Periodically move data as part of a data processing pipeline or analytical workflow.


- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-storage-transfer.svg
   :target: https://pypi.org/project/google-cloud-storage-transfer/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-storage-transfer.svg
   :target: https://pypi.org/project/google-cloud-storage-transfer/
.. _Storage Transfer Service: https://cloud.google.com/storage-transfer
.. _Client Library Documentation: https://googleapis.dev/python/storagetransfer/latest
.. _Product Documentation:  https://cloud.google.com/storage-transfer/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Storage Transfer API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Storage Transfer API.:  https://cloud.google.com/storage-transfer/docs/how-to
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


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-storage-transfer


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-storage-transfer

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Storage Transfer Service
   to see other available methods on the client.
-  Read the `Storage Transfer Service Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Storage Transfer Service Product documentation:  https://cloud.google.com/storage-transfer/docs
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst