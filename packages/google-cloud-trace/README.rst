Python Client for Google Cloud Trace API
========================================

|GA| |pypi| |versions|

`Google Cloud Trace`_: is a distributed tracing system for Google Cloud that collects latency data
from applications and displays it in near real-time in the Google Cloud Console.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-trace.svg
   :target: https://pypi.org/project/google-cloud-trace/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-trace.svg
   :target: https://pypi.org/project/google-cloud-trace/
.. _Google Cloud Trace: https://cloud.google.com/trace
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/cloudtrace/latest
.. _Product Documentation:  https://cloud.google.com/trace/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Trace API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Trace API.: https://console.cloud.google.com/flows/enableapi?apiid=cloudtrace.googleapis.com
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
    <your-env>/bin/pip install google-cloud-trace


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-trace

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Trace API
   to see other available methods on the client.
-  Read the `Cloud Trace Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud Trace Product documentation:  https://cloud.google.com/trace/docs
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
