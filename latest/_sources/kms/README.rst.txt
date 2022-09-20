Python Client for Cloud Key Management Service (KMS) API
========================================================

|GA| |pypi| |versions| 

`Cloud Key Management Service (KMS) API`_: Manages keys and performs
cryptographic operations in a central cloud service, for direct use by other
cloud resources and applications.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availabilityt
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-kms.svg
   :target: https://pypi.org/project/google-cloud-kms/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-kms.svg
   :target: https://pypi.org/project/google-cloud-kms/
.. _Cloud Key Management Service (KMS) API: https://cloud.google.com/kms
.. _Client Library Documentation: https://googleapis.dev/python/cloudkms/latest
.. _Product Documentation:  https://cloud.google.com/kms

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Key Management Service (KMS) API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Key Management Service (KMS) API.:  https://cloud.google.com/kms
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
    <your-env>/bin/pip install google-cloud-kms


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-kms

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ to see other available methods on
   the client.
-  Read the `Product Documentation`_ to learn more about the product and see
   How-to Guides.

