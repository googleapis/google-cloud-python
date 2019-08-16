Python Client for Stackdriver Error Reporting
=============================================

|pypi| |versions| 

The Stackdriver `Error Reporting`_ API counts, analyzes and aggregates the
crashes in your running cloud services.  A centralized error management
interface displays the results with sorting and filtering capabilities. A
dedicated view shows the error details: time chart, occurrences, affected user
count, first and last seen dates and a cleaned exception stack trace. Opt-in
to receive email and mobile alerts on new errors.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Error Reporting: https://cloud.google.com/error-reporting/
.. _Client Library Documentation: https://googleapis.dev/python/clouderroreporting/latest
.. _Product Documentation: https://cloud.google.com/error-reporting/reference/
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-error-reporting.svg
   :target: https://pypi.org/project/google-cloud-error-reporting/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-error-reporting.svg
   :target: https://pypi.org/project/google-cloud-error-reporting/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Error Reporting API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Error Reporting API.:  https://cloud.google.com/error-reporting
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
    <your-env>/bin/pip install google-cloud-error-reporting


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-error-reporting



Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Cloud Datastore API
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
