Python Client for Cloud Talent Solution API
======================================================

|beta| |pypi| |versions| 

`Cloud Talent Solution API`_: Cloud Talent Solution provides the capability to create, read, update, and
delete job postings, as well as search jobs based on keywords and filters.

- `Client Library Documentation`_
- `Product Documentation`_

.. |beta| image:: https://img.shields.io/badge/support-beta-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#beta-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-talent.svg
   :target: https://pypi.org/project/google-cloud-talent/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-talent.svg
   :target: https://pypi.org/project/google-cloud-talent/
.. _Cloud Talent Solution API: https://cloud.google.com/jobs
.. _Client Library Documentation: https://googleapis.dev/python/talent/latest
.. _Product Documentation:  https://cloud.google.com/jobs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Talent Solution API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Talent Solution API.:  https://cloud.google.com/jobs
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.6

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7.

The last version of this library compatible with Python 2.7 is google-cloud-talent==0.6.1.

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
    <your-env>/bin/pip install google-cloud-talent


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-talent

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Talent Solution API
   API to see other available methods on the client.
-  Read the `Cloud Talent Solution API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud Talent Solution API Product documentation:  https://cloud.google.com/jobs
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
