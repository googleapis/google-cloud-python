Python Client for Cloud Asset API
=================================

|alpha| |pypi| |versions|

`Cloud Asset API`_: The cloud asset API manages the history and inventory of cloud resources.

- `Client Library Documentation`_
- `Product Documentation`_

.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-asset.svg
   :target: https://pypi.org/project/google-cloud-asset/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-asset.svg
   :target: https://pypi.org/project/google-cloud-asset/
.. _Cloud Asset API: https://cloud.google.com/cloudasset
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/asset/index.html
.. _Product Documentation:  https://cloud.google.com/cloudasset

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Asset API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Asset API.:  https://cloud.google.com/cloudasset
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
    <your-env>/bin/pip install google-cloud-asset


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-asset

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Asset API
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
