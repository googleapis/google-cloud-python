Python Client for Organization Policy
=================================================

|GA| |pypi| |versions|

`Organization Policy`_: The Organization Policy API allows users to configure governance rules on their GCP
resources across the Cloud Resource Hierarchy.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-org-policy.svg
   :target: https://pypi.org/project/google-cloud-org-policy/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-org-policy.svg
   :target: https://pypi.org/project/google-cloud-org-policy/
.. _Organization Policy: https://cloud.google.com/resource-manager/docs/organization-policy/overview
.. _Client Library Documentation: https://googleapis.dev/python/orgpolicy/latest
.. _Product Documentation:  https://cloud.google.com/resource-manager/docs/organization-policy/overview

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Organization Policy API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Organization Policy API.:  https://cloud.google.com/resource-manager/docs/organization-policy/overview
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
    <your-env>/bin/pip install google-cloud-org-policy


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-org-policy

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Organization Policy
   to see other available methods on the client.
-  Read the `Organization Policy Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Organization Policy Product documentation:  https://cloud.google.com/resource-manager/docs/organization-policy/overview
.. _README: https://github.com/googleapis/google-cloud-python/blob/master/README.rst