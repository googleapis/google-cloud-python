Python Client for Cloud Data Loss Prevention (DLP) API
======================================================

|alpha| |pypi| |versions| 

`Cloud Data Loss Prevention (DLP) API`_: Provides methods for detection, risk analysis, and de-identification of
privacy-sensitive fragments in text, images, and Google Cloud Platform
storage repositories.

- `Client Library Documentation`_
- `Product Documentation`_

.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-dlp.svg
   :target: https://pypi.org/project/google-cloud-dlp/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-dlp.svg
   :target: https://pypi.org/project/google-cloud-dlp/
.. _Cloud Data Loss Prevention (DLP) API: https://cloud.google.com/dlp
.. _Client Library Documentation: https://googleapis.dev/python/dlp/latest
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

-  Read the `Client Library Documentation`_ for Cloud Data Loss Prevention
   (DLP) API to see other available methods on the client.
-  Read the `Product documentation`_ to
   learn more about the product and see How-to Guides.
