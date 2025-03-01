Python Client for Advisory Notifications
========================================

|preview| |pypi| |versions|

`Advisory Notifications`_: Advisory Notifications provides well-targeted, timely, and compliant communications about critical security and privacy events in the Google Cloud console and allows you to securely investigate the event, take action, and get support.

- `Client Library Documentation`_
- `Product Documentation`_

.. |preview| image:: https://img.shields.io/badge/support-preview-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#stability-levels
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-advisorynotifications.svg
   :target: https://pypi.org/project/google-cloud-advisorynotifications/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-advisorynotifications.svg
   :target: https://pypi.org/project/google-cloud-advisorynotifications/
.. _Advisory Notifications: https://cloud.google.com/advisory-notifications/
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/advisorynotifications/latest/summary_overview
.. _Product Documentation:  https://cloud.google.com/advisory-notifications/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Advisory Notifications.`_
4. `Set up Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Advisory Notifications.:  https://cloud.google.com/advisory-notifications/
.. _Set up Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a virtual environment using `venv`_. `venv`_ is a tool that
creates isolated Python environments. These isolated environments can have separate
versions of Python packages, which allows you to isolate one project's dependencies
from the dependencies of other projects.

With `venv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`venv`: https://docs.python.org/3/library/venv.html


Code samples and snippets
~~~~~~~~~~~~~~~~~~~~~~~~~

Code samples and snippets live in the `samples/`_ folder.

.. _samples/: https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-advisorynotifications/samples


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

    python3 -m venv <your-env>
    source <your-env>/bin/activate
    pip install google-cloud-advisorynotifications


Windows
^^^^^^^

.. code-block:: console

    py -m venv <your-env>
    .\<your-env>\Scripts\activate
    pip install google-cloud-advisorynotifications

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Advisory Notifications
   to see other available methods on the client.
-  Read the `Advisory Notifications Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Advisory Notifications Product documentation:  https://cloud.google.com/advisory-notifications/
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
