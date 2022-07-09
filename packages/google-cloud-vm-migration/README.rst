Python Client for Cloud VM Migration API
========================================

|stable| |pypi| |versions|

`Cloud VM Migration API`_:  for Compute Engine migrates VMs from your on-premises data center into Compute Engine.

- `Client Library Documentation`_
- `Product Documentation`_

.. |stable| image:: https://img.shields.io/badge/support-stable-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#stability-levels
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-vm-migration.svg
   :target: https://pypi.org/project/google-cloud-vm-migration/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-vm-migration.svg
   :target: https://pypi.org/project/google-cloud-vm-migration/
.. _Cloud VM Migration API: https://cloud.google.com/migrate/compute-engine/docs
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/vmmigration/latest
.. _Product Documentation:  https://cloud.google.com/migrate/compute-engine/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud VM Migration API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud VM Migration API.:  https://cloud.google.com/migrate/compute-engine/docs
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
Our client libraries are compatible with all current [active](https://devguide.python.org/devcycle/#in-development-main-branch) and [maintenance](https://devguide.python.org/devcycle/#maintenance-branches) versions of
Python.

Python >= 3.7

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python <= 3.6

If you are using an [end-of-life](https://devguide.python.org/devcycle/#end-of-life-branches)
version of Python, we recommend that you update as soon as possible to an actively supported version.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-vm-migration


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-vm-migration

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud VM Migration API
   to see other available methods on the client.
-  Read the `Cloud VM Migration API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud VM Migration API Product documentation:  https://cloud.google.com/migrate/compute-engine/docs
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
