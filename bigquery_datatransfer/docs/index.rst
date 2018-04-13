Python Client for BigQuery Data Transfer API (`Alpha`_)
=======================================================

`BigQuery Data Transfer API`_: Transfers data from partner SaaS applications to Google BigQuery on a
scheduled, managed basis.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Alpha: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _BigQuery Data Transfer API: https://cloud.google.com/bigquery/docs/transfer-service-overview
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery_datatransfer/index.html
.. _Product Documentation:  https://cloud.google.com/bigquery/transfer

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable the BigQuery Data Transfer API.`_
3. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable the BigQuery Data Transfer API.:  https://cloud.google.com/bigquery/docs/transfer-service-overview
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
    <your-env>/bin/pip install google-cloud-bigquerydatatransfer


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-bigquerydatatransfer

Preview
~~~~~~~

DataTransferServiceClient
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: py

    from google.cloud import bigquery_datatransfer_v1

    client = bigquery_datatransfer_v1.DataTransferServiceClient()

    parent = client.location_path('[PROJECT]', '[LOCATION]')


    # Iterate over all results
    for element in client.list_data_sources(parent):
        # process element
        pass

    # Or iterate over results one page at a time
    for page in client.list_data_sources(parent, options=CallOptions(page_token=INITIAL_PAGE)):
        for element in page:
            # process element
            pass

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for BigQuery Data Transfer API
   API to see other available methods on the client.
-  Read the `BigQuery Data Transfer API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _BigQuery Data Transfer API Product documentation:  https://cloud.google.com/bigquery/docs/transfer-service-overview
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst

Api Reference
-------------
.. toctree::
    :maxdepth: 2

    gapic/v1/api
    gapic/v1/types
    changelog
