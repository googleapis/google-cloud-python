Python Client for BigQuery Connection
=================================================

|GA| |pypi| |versions|

`BigQuery Connection API`_: Manage BigQuery connections to external data sources.

- `Client Library Documentation`_
- `Product Documentation`_
- `Introduction to BigQuery external data sources`_

.. |GA| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-connection.svg
   :target: https://pypi.org/project/google-cloud-bigquery-connection/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-bigquery-connection.svg
   :target: https://pypi.org/project/google-cloud-bigquery-connection/
.. _BigQuery Connection API: https://cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/bigqueryconnection/latest
.. _Product Documentation:  https://cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest
.. _Introduction to BigQuery external data sources:  https://cloud.google.com/bigquery/external-data-sources

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the BigQuery Connection API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the BigQuery Connection API.:  https://console.cloud.google.com/apis/library/bigqueryconnection.googleapis.com
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
    <your-env>/bin/pip install google-cloud-bigquery-connection


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-bigquery-connection

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for BigQuery Connection
   API to see other available methods on the client.
-  Read the `BigQuery Connection API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _BigQuery Connection API Product documentation:  https://cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest
.. _repository’s main README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst