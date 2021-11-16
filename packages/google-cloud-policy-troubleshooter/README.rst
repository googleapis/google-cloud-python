Python Client for IAM Policy Troubleshooter
===========================================

|GA| |pypi| |versions|

`IAM Policy Troubleshooter`_ makes it easier to understand why a user has
access to a resource or doesn't have permission to call an API. Given an email,
resource, and permission, Policy Troubleshooter examines all Identity and
Access Management (IAM) policies that apply to the resource. It then reveals
whether the member's roles include the permission on that resource and, if so,
which policies bind the member to those roles.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-policy-troubleshooter.svg
   :target: https://pypi.org/project/google-cloud-policy-troubleshooter/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-policy-troubleshooter.svg
   :target: https://pypi.org/project/google-cloud-policy-troubleshooter/
.. _IAM Policy Troubleshooter: https://cloud.google.com/iam/docs/troubleshooting-access#rest-api/
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/policytroubleshooter/latest
.. _Product Documentation:  https://cloud.google.com/iam/docs/troubleshooting-access#rest-api/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Resource Manager API Service.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Resource Manager API Service.:  https://cloud.google.com/iam/docs/quickstart-client-libraries
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
    <your-env>/bin/pip install google-cloud-policy-troubleshooter


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-policy-troubleshooter

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for IAM Policy Troubleshooter
   to see other available methods on the client.
-  Read the `IAM Policy Troubleshooter Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _IAM Policy Troubleshooter Product documentation:  https://cloud.google.com/iam/docs/quickstart-client-libraries
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
