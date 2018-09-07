Python Client for Cloud Data Loss Prevention (DLP) API (`Alpha`_)
=================================================================

`Cloud Data Loss Prevention (DLP) API`_: Provides methods for detection, risk analysis, and de-identification of
privacy-sensitive fragments in text, images, and Google Cloud Platform
storage repositories.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Alpha: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _Cloud Data Loss Prevention (DLP) API: https://cloud.google.com/dlp
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/dlp/usage.html
.. _Product Documentation:  https://cloud.google.com/dlp

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Data Loss Prevention (DLP) API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Data Loss Prevention (DLP) API.:  https://cloud.google.com/dlp
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
    <your-env>/bin/pip install google-cloud-dlp


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-dlp

Preview
~~~~~~~

DlpServiceClient
^^^^^^^^^^^^^^^^

.. code:: py

    from google.cloud import dlp_v2

    client = dlp_v2.DlpServiceClient()

    name = 'EMAIL_ADDRESS'
    info_types_element = {'name': name}
    info_types = [info_types_element]
    inspect_config = {'info_types': info_types}
    type_ = 'text/plain'
    value = 'My email is example@example.com.'
    items_element = {'type': type_, 'value': value}
    items = [items_element]

    response = client.inspect_content(inspect_config, items)

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Data Loss Prevention (DLP) API
   API to see other available methods on the client.
-  Read the `Cloud Data Loss Prevention (DLP) API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud Data Loss Prevention (DLP) API Product documentation:  https://cloud.google.com/dlp
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
