Python Client for Google Cloud DNS
==================================

The `Google Cloud DNS`_ API provides methods that you can use to
manage DNS for your applications.


|pypi| |versions|

- `Client Library Documentation`_
- `Product Documentation`_

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-dns.svg
   :target: https://pypi.org/project/google-cloud-dns/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-dns.svg
.. _Google Cloud DNS: https://cloud.google.com/dns/
   :target: https://pypi.org/project/google-cloud-dns/
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/dns/index.html
.. _Product Documentation: https://cloud.google.com/dns/docs/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Datastore API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Datastore API.:  https://cloud.google.com/dns
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
    <your-env>/bin/pip install google-cloud-dns


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-dns


Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Cloud DNS
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
