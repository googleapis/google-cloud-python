Python Client for Cloud IoT API (`Alpha`_)
==========================================

`Cloud IoT API`_: Registers and manages IoT (Internet of Things) devices that connect to the
Google Cloud Platform.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Alpha: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _Cloud IoT API: https://cloud.google.com/iot
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/iot/index.html
.. _Product Documentation:  https://cloud.google.com/iot

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud IoT API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud IoT API.:  https://cloud.google.com/iot
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
    <your-env>/bin/pip install google-cloud-iot


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-iot

Preview
~~~~~~~

DeviceManagerClient
^^^^^^^^^^^^^^^^^^^

.. code:: py

    from google.cloud import iot_v1

    client = iot_v1.DeviceManagerClient()

    parent = client.location_path('[PROJECT]', '[LOCATION]')


    # Iterate over all results
    for element in client.list_device_registries(parent):
        # process element
        pass

    # Or iterate over results one page at a time
    for page in client.list_device_registries(parent, options=CallOptions(page_token=INITIAL_PAGE)):
        for element in page:
            # process element
            pass

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud IoT API
   API to see other available methods on the client.
-  Read the `Cloud IoT API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud IoT API Product documentation:  https://cloud.google.com/iot
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst

Api Reference
-------------
.. toctree::
    :maxdepth: 2

    gapic/v1/api
    gapic/v1/types
