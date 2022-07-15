Python Client for Cloud Data Loss Prevention API
================================================

|stable| |pypi| |versions|

`Cloud Data Loss Prevention API`_: provides programmatic access to a powerful detection engine for personally identifiable information and other privacy-sensitive data in unstructured data streams, like text blocks and images.

- `Client Library Documentation`_
- `Product Documentation`_

.. |stable| image:: https://img.shields.io/badge/support-stable-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#stability-levels
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-dlp.svg
   :target: https://pypi.org/project/google-cloud-dlp/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-dlp.svg
   :target: https://pypi.org/project/google-cloud-dlp/
.. _Cloud Data Loss Prevention API: https://cloud.google.com/dlp/docs/
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/dlp/latest
.. _Product Documentation:  https://cloud.google.com/dlp/docs/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Data Loss Prevention API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Data Loss Prevention API.:  https://cloud.google.com/dlp/docs/
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


Code samples and snippets
~~~~~~~~~~~~~~~~~~~~~~~~~

Code samples and snippets live in the `samples/` folder.


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Our client libraries are compatible with all current `active`_ and `maintenance`_ versions of
Python.

Python >= 3.7

.. _active: https://devguide.python.org/devcycle/#in-development-main-branch
.. _maintenance: https://devguide.python.org/devcycle/#maintenance-branches

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python <= 3.6

If you are using an `end-of-life`_
version of Python, we recommend that you update as soon as possible to an actively supported version.

.. _end-of-life: https://devguide.python.org/devcycle/#end-of-life-branches

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

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Data Loss Prevention API
   to see other available methods on the client.
-  Read the `Cloud Data Loss Prevention API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud Data Loss Prevention API Product documentation:  https://cloud.google.com/dlp/docs/
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
