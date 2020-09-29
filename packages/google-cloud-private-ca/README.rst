Python Client for Certificate Authority Service
=================================================

|beta| |pypi| |versions|

`Certificate Authority Service`_: Highly available and scalable certificate authority
hosted by Google and managed by the customer, to simplify certificate deployment and management
within infrastructure and cloud native applications.

- `Client Library Documentation`_
- `Product Documentation`_

.. |beta| image:: https://img.shields.io/badge/support-beta-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#beta-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-private-ca.svg
   :target: https://pypi.org/project/google-cloud-private-ca/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-private-ca.svg
   :target: https://pypi.org/project/google-cloud-private-ca/
.. _Certificate Authority Service: https://cloud.google.com/certificate-authority-service
.. _Client Library Documentation: https://googleapis.dev/python/privateca/latest
.. _Product Documentation:  https://cloud.google.com/certificate-authority-service

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Certificate Authority Service.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Certificate Authority Service.:  https://cloud.google.com/privateca/docs
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
    <your-env>/bin/pip install google-cloud-private-ca


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-private-ca

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Certificate Authority Service
   to see other available methods on the client.
-  Read the `Certificate Authority Service Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Certificate Authority Service Product documentation:  https://cloud.google.com/privateca/docs
.. _README: https://github.com/googleapis/google-cloud-python/blob/master/README.rst