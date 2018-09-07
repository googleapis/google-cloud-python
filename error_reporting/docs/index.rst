Python Client for Stackdriver Error Reporting API (`Alpha`_)
============================================================

`Stackdriver Error Reporting API`_: 
Stackdriver Error Reporting groups and counts similar errors from cloud services. The Stackdriver Error Reporting API provides a way to report new errors and read access to error groups and their associated errors.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Alpha: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _Stackdriver Error Reporting API: https://cloud.google.com/error-reporting
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/error-reporting/usage.html
.. _Product Documentation:  https://cloud.google.com/error-reporting

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Stackdriver Error Reporting API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Stackdriver Error Reporting API.:  https://cloud.google.com/error-reporting
.. _Setup Authentication.: https://googlecloudplatform.github.io/google-cloud-python/latest/core/auth.html

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
    <your-env>/bin/pip install google-cloud-error-reporting


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-error-reporting

Preview
~~~~~~~

ReportErrorsServiceClient
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: py

    from google.cloud import errorreporting_v1beta1

    client = errorreporting_v1beta1.ReportErrorsServiceClient()

    project_name = client.project_path('[PROJECT]')
    event = {}

    response = client.report_error_event(project_name, event)

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Stackdriver Error Reporting API
   API to see other available methods on the client.
-  Read the `Stackdriver Error Reporting API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Stackdriver Error Reporting API Product documentation:  https://cloud.google.com/error-reporting
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst

Api Reference
-------------
.. toctree::
    :maxdepth: 2

    gapic/v1beta1/api
    gapic/v1beta1/types
