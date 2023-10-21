Python Client for Compute Engine
=================================================

|stable| |pypi| |versions|

`Compute Engine API`_: Create and runs virtual machines on Google Cloud Platform.

- `Client Library Documentation`_
- `Product Documentation`_

.. |stable| image:: https://img.shields.io/badge/support-stable-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-compute.svg
   :target: https://pypi.org/project/google-cloud-compute/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-compute.svg
   :target: https://pypi.org/project/google-cloud-compute/
.. _Compute Engine API: https://cloud.google.com/compute/
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/compute/latest
.. _Product Documentation:  https://cloud.google.com/compute/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Compute Engine API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Compute Engine API.:  https://cloud.google.com/compute/
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
    <your-env>/bin/pip install google-cloud-compute


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-compute


Authentication and Authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This client library supports authentication via `Google Application Default Credentials`_
, or by providing a JSON key file for a Service Account. See examples below.

`Google Application Default Credentials`_ (ADC) is the recommended way to authorize and authenticate
clients. Here is an example of a client using ADC to authenticate:

.. code-block:: python

    from google.cloud import compute_v1

    networks_client = compute_v1.NetworksClient()
    for network in networks_client.list(project='YOUR_PROJECT'):
        print(network)


You can use a file with credentials to authenticate and authorize, such as a JSON key
file associated with a Google service account. You can create service account keys and
download them using the Google Cloud Console. For more information, see
`Creating and managing Service Account keys`_.

The library used to create the credentials objects is ``google-auth``. This example uses
the Networks Client, but the same steps apply to the other clients in this package.
Example:

.. code-block:: python

    from google.oauth2 import service_account
    from google.cloud import compute_v1

    credentials = service_account.Credentials.from_service_account_file(
        '/path/to/key.json')

    networks_client = compute_v1.NetworksClient(credentials=credentials)
    for network in networks_client.list(project='YOUR_PROJECT'):
        print(network)


When you don't want to store secrets on disk, you can create credentials
from in-memory JSON and use the ``from_service_account_info`` method. You can also limit the use of
your credentials only to specified scopes. For more information about OAuth 2.0 scopes for Google APIs,
see `Scopes documentation page`_. Example:

.. code-block:: python

    import json

    from google.oauth2 import service_account
    from google.cloud import compute_v1

    json_acct_info = json.loads(function_to_get_json_creds())
    credentials = service_account.Credentials.from_service_account_info(
        json_acct_info)

    scoped_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/cloud-platform'])

    networks_client = compute_v1.NetworksClient(credentials=scoped_credentials)
    for network in networks_client.list(project='YOUR_PROJECT'):
        print(network)

.. _Google Application Default Credentials: https://cloud.google.com/docs/authentication/production
.. _Creating and managing Service Account keys: https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating
.. _Scopes documentation page: https://developers.google.com/identity/protocols/oauth2/scopes

Long Running Operations
~~~~~~~~~~~~~~~~~~~~~~~
Long-Running Operations (LROs), like the many ``insert()`` operations, can be handled using
the ``ExtendedOperation`` object that is returned when the LRO is started.

You can wait for the completion of an operation using its ``result()`` method. This method accepts
a ``timeout`` argument, specifying how long you want your process to wait for completion of the
operation (in seconds). When the call to ``result()`` times out, the operation is not automatically
cancelled. At any time, you can check whether the operation is complete by using its ``done()`` method.

A sample method to handle LROs featuring error and warning reporting can be found in the Python
code samples repository: `GoogleCloudPlatform/python-docs-samples`_

.. _GoogleCloudPlatform/python-docs-samples: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/compute/client_library/snippets/operations/wait_for_extended_operation.py


Code Samples
~~~~~~~~~~~~
You can find useful code samples that will demonstrate the usage of this library on `the
Google Cloud samples page`_.

.. _the Google Cloud samples page: https://cloud.google.com/docs/samples?language=python&product=computeengine



PyCharm/JetBrains IDEs
~~~~~~~~~~~~~~~~~~~~~~
This library has now grown in size past the `JetBrains default size limit of ~2.5Mb`_.
As a result, code completion in JetBrains products can fail to work with the classes from our library. To
fix this, you need to update the ``idea.max.intellisense.filesize`` setting in custom properties
(Help -> Edit custom properties...). Just add the line ``idea.max.intellisense.filesize = 10000`` to change this
limit to ~10Mb.

.. _JetBrains default size limit of ~2.5Mb: https://www.jetbrains.com/help/pycharm/file-idea-properties.html

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Compute Engine API
   to see other available methods on the client.
-  Read the `Compute Engine API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Compute Engine API Product documentation:  https://cloud.google.com/compute/docs/api/libraries
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
