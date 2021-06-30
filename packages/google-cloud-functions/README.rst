Python Client for Cloud Functions
=================================================

|GA| |pypi| |versions|

`Cloud Functions API`_: Manages lightweight user-provided functions executed in response to events.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-functions.svg
   :target: https://pypi.org/project/google-cloud-functions/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-functions.svg
   :target: https://pypi.org/project/google-cloud-functions
.. _Cloud Functions API: https://cloud.google.com/functions/
.. _Client Library Documentation: https://googleapis.dev/python/cloudfunctions/latest
.. _Product Documentation:  https://cloud.google.com/functions/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Functions API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Functions API.:  https://cloud.google.com/functions
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
    <your-env>/bin/pip install google-cloud-functions


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-functions

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Functions API
   to see other available methods on the client.
-  Read the `Cloud Functions API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud Functions API Product documentation:  https://cloud.google.com/functions/docs
.. _README: https://github.com/googleapis/google-cloud-python/blob/master/README.rst
