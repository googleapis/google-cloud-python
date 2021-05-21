Python Client for Cloud Security Command Center API
===================================================
|GA| |pypi| |versions| 

`Cloud Security Command Center API`_: The public Cloud Security Command Center API.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-securitycenter.svg
   :target: https://pypi.org/project/google-cloud-securitycenter/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-securitycenter.svg
   :target: https://pypi.org/project/google-cloud-securitycenter/
.. _Alpha: https://github.com/googleapis/google-cloud-python/blob/master/README.rst
.. _Cloud Security Command Center API: https://cloud.google.com/security-command-center
.. _Client Library Documentation: https://googleapis.dev/python/securitycenter/latest
.. _Product Documentation:  https://cloud.google.com/security-command-center


Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Security Command Center API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Security Command Center API.:  https://cloud.google.com/security-command-center
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

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7.

The last version of this library compatible with Python 2.7 is google-cloud-securitycenter==0.6.0.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-securitycenter


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-securitycenter

Next Steps
~~~~~~~~~~

-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
