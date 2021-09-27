Python Client for Google Cloud Deploy
=====================================

|beta| |pypi| |versions|

`Google Cloud Deploy`_: Deliver continuously to Google Kubernetes Engine. Deploy to Google 
Kubernetes Engine in minutes. Define pipelines in code and let Google Cloud Deploy handle rollouts. 
Scale pipelines across your organization, while having  a cross-project, centralized view.

- `Client Library Documentation`_
- `Product Documentation`_

.. |beta| image:: https://img.shields.io/badge/support-beta-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-deploy.svg
   :target: https://pypi.org/project/google-cloud-deploy/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-deploy.svg
   :target: https://pypi.org/project/google-cloud-deploy/
.. _Google Cloud Deploy: https://cloud.google.com/deploy
.. _Client Library Documentation: https://googleapis.dev/python/clouddeploy/latest
.. _Product Documentation:  https://cloud.google.com/deploy/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the APIs.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the APIs.: https://cloud.google.com/deploy/docs/quickstart-basic#before-you-begin
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
    <your-env>/bin/pip install google-cloud-deploy


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-deploy

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Cloud Deploy
   to see other available methods on the client.
-  Read the `Google Cloud Deploy Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Google Cloud Deploy Product documentation:  https://cloud.google.com/deploy/docs
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst