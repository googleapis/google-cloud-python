Python Client for Service Control
=================================

|GA| |pypi| |versions|

`Service Control`_:  Service Infrastructure is a foundational platform for
creating, managing, securing, and consuming APIs and services across
organizations. It is used by Google APIs, Cloud APIs, Cloud Endpoints, and API
Gateway. Service Infrastructure provides a wide range of features to service
consumers and service producers, including authentication, authorization,
auditing, rate limiting, analytics, billing, logging, and monitoring.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-service-control.svg
   :target: https://pypi.org/project/google-cloud-service-control/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-service-control.svg
   :target: https://pypi.org/project/google-cloud-service-control/
.. _Service Control: https://cloud.google.com/service-infrastructure/docs/overview/
.. _Client Library Documentation: https://googleapis.dev/python/servicecontrol/latest
.. _Product Documentation:  https://cloud.google.com/service-infrastructure/docs/overview/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Service Control API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Service Control API.:  https://cloud.google.com/service-infrastructure/docs/service-control/getting-starteds
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
    <your-env>/bin/pip install google-cloud-service-control


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-service-control

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Service Control
   to see other available methods on the client.
-  Read the `Service Control Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Service Control Product documentation:  https://cloud.google.com/service-infrastructure/docs/service-control/getting-started
.. _README: https://github.com/googleapis/google-cloud-python/blob/master/README.rst
