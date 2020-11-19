Python Client for Cloud Logging
=====================================

|pypi| |versions|

`Cloud Logging API`_: Writes log entries and manages your Cloud
Logging configuration.

- `Client Library Documentation`_
- `Product Documentation`_

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-logging.svg
   :target: https://pypi.org/project/google-cloud-logging/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-logging.svg
   :target: https://pypi.org/project/google-cloud-logging/
.. _Cloud Logging API: https://cloud.google.com/logging
.. _Client Library Documentation: https://googleapis.dev/python/logging/latest
.. _Product Documentation:  https://cloud.google.com/logging/docs
.. _Setting Up Cloud Logging for Python: https://cloud.google.com/logging/docs/setup/python
.. _Python's standard logging library: https://docs.python.org/2/library/logging.html

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Logging API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Logging API.:  https://cloud.google.com/logging
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a `venv`_ using pip. `venv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `venv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`venv`: https://docs.python.org/3/library/venv.html


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.6

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7. The last version of the library compatible with Python 2.7 is `google-cloud-logging==1.15.1`.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    python -m venv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-logging


Windows
^^^^^^^

.. code-block:: console

    python -m venv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-logging

Next Steps
~~~~~~~~~~

-  Read the `Setting Up Cloud Logging for Python`_ How-to Guide
-  Read the `Product documentation`_ to learn more about the product and see
   other How-to Guides.
-  Read the `Client Library Documentation`_ for to see other available
   methods on the client.
