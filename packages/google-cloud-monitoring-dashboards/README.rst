Python Client for Monitoring Dashboards API
===========================================

|stable| |pypi| |versions|

`Monitoring Dashboards API`_: are one way for you to view and analyze metric data. The Cloud Console provides predefined dashboards that require no setup or configuration. You can also define custom dashboards. With custom dashboards, you have complete control over the charts that are displayed and their configuration.

- `Client Library Documentation`_
- `Product Documentation`_

.. |stable| image:: https://img.shields.io/badge/support-stable-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#stability-levels
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-monitoring-dashboards.svg
   :target: https://pypi.org/project/google-cloud-monitoring-dashboards/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-monitoring-dashboards.svg
   :target: https://pypi.org/project/google-cloud-monitoring-dashboards/
.. _Monitoring Dashboards API: https://cloud.google.com/monitoring/dashboards/
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/monitoring-dashboards/latest
.. _Product Documentation:  https://cloud.google.com/monitoring/dashboards/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Monitoring Dashboards API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Monitoring Dashboards API.:  https://cloud.google.com/monitoring/dashboards/
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
    <your-env>/bin/pip install google-cloud-monitoring-dashboards


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-monitoring-dashboards

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Monitoring Dashboards API
   to see other available methods on the client.
-  Read the `Monitoring Dashboards API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Monitoring Dashboards API Product documentation:  https://cloud.google.com/monitoring/dashboards/
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
