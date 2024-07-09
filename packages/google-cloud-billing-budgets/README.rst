Python Client for Cloud Billing Budget
======================================

|stable| |pypi| |versions|

`Cloud Billing Budget`_: The Cloud Billing Budget API stores Cloud Billing budgets, which define a budget plan and the rules to execute as spend is tracked against that plan.

- `Client Library Documentation`_
- `Product Documentation`_

.. |stable| image:: https://img.shields.io/badge/support-stable-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#stability-levels
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-billing-budgets.svg
   :target: https://pypi.org/project/google-cloud-billing-budgets/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-billing-budgets.svg
   :target: https://pypi.org/project/google-cloud-billing-budgets/
.. _Cloud Billing Budget: https://cloud.google.com/billing/docs/how-to/budget-api-overview
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/billingbudgets/latest/summary_overview
.. _Product Documentation:  https://cloud.google.com/billing/docs/how-to/budget-api-overview

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Billing Budget.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Billing Budget.:  https://cloud.google.com/billing/docs/how-to/budget-api-overview
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

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

.. _samples/: https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-billing-budgets/samples


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
    pip install google-cloud-billing-budgets


Windows
^^^^^^^

.. code-block:: console

    py -m venv <your-env>
    .\<your-env>\Scripts\activate
    pip install google-cloud-billing-budgets

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Billing Budget
   to see other available methods on the client.
-  Read the `Cloud Billing Budget Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud Billing Budget Product documentation:  https://cloud.google.com/billing/docs/how-to/budget-api-overview
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
