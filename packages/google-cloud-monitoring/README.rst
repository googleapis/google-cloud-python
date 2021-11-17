Python Client for Cloud Monitoring API
=======================================================

|ga| |pypi| |versions| 

`Cloud Monitoring API`_: Manages your Cloud Monitoring data and
configurations. Most projects must be associated with a Google Cloud account,
with a few exceptions as noted on the individual method pages.

- `Client Library Documentation`_
- `Product Documentation`_

.. |ga| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-monitoring.svg
   :target: https://pypi.org/project/google-cloud-monitoring/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-monitoring.svg
   :target: https://pypi.org/project/google-cloud-monitoring/
.. _Cloud Monitoring API: https://cloud.google.com/monitoring/api/ref_v3/rest/
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/monitoring/latest
.. _Product Documentation:  https://cloud.google.com/monitoring/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Monitoring API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Monitoring API.:  https://cloud.google.com/monitoring/api/enable-api
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
Python >= 3.6

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7.

The last version of this library compatible with Python 2.7 is google-cloud-monitoring==1.1.0.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-monitoring


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-monitoring


Next Steps
~~~~~~~~~~


-  Read the `Client Library Documentation`_ for Cloud Monitoring API
   to see other available methods on the client.
-  Read the `Product documentation`_ to learn more about the product and see
   How-to Guides.
