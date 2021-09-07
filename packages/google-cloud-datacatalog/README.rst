Python Client for Google Cloud Data Catalog API
===============================================

|ga| |pypi| |versions|

`Google Cloud Data Catalog API`_: Google Cloud Data Catalog API provides features to attach metadata to
Google Cloud Platform resources like BigQuery Tables. Key critical resources
include: Entries (Data Catalog representation of a cloud resource).

- `Client Library Documentation`_
- `Product Documentation`_

.. |ga| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-datacatalog.svg
   :target: https://pypi.org/project/google-cloud-datacatalog/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-datacatalog.svg
   :target: https://pypi.org/project/google-cloud-datacatalog/
.. _Google Cloud Data Catalog API: https://cloud.google.com/data-catalog
.. _Client Library Documentation: https://googleapis.dev/python/datacatalog/latest
.. _Product Documentation:  https://cloud.google.com/data-catalog

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Data Catalog API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Data Catalog API.:  https://cloud.google.com/data-catalog
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.6

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7.

The last version of this library compatible with Python 2.7 is google-cloud-datacatalog==1.0.0.

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
    <your-env>/bin/pip install google-cloud-datacatalog


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-datacatalog

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Cloud Data Catalog API
   API to see other available methods on the client.
-  Read the `Google Cloud Data Catalog API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Google Cloud Data Catalog API Product documentation:  https://cloud.google.com/data-catalog
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
