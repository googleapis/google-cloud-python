Python Client for Google Cloud Translation
==========================================

|GA| |pypi| |versions| 

With `Google Cloud Translation`_, you can dynamically translate text between
thousands of language pairs. The Google Cloud Translation API lets websites
and programs integrate with Google Cloud Translation programmatically. Google
Cloud Translation is available as a paid service. See the `Pricing`_ and
`FAQ`_ pages for details.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-translate.svg
   :target: https://pypi.org/project/google-cloud-translate/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-translate.svg
   :target: https://pypi.org/project/google-cloud-translate/
.. _Google Cloud Translation: https://cloud.google.com/translate/
.. _Pricing: https://cloud.google.com/translate/pricing
.. _FAQ: https://cloud.google.com/translate/faq
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/translation/latest
.. _Product Documentation: https://cloud.google.com/translate/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Translate API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Translate API.:  https://cloud.google.com/translate
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

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7.
The last version of this library compatible with Python 2.7 is google-cloud-translate==2.0.1.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-translate


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-translate

Samples
-----------

The `samples folder`_ contains all of the Cloud Translation API code snippets
found in `its documentation`_ as well as complete sample apps:

- `Mini Google Translate "MVP"`_ app

  - Shows how to use the API in a Python/Flask web app
  - Deployable locally or any on-prem or cloud host supporting Flask apps
  - Also deployable to `Google Cloud serverless hosting platforms`_ (`App Engine`_, `Cloud Functions`_, or `Cloud Run`_) with only minor configuration changes

.. _samples folder: samples
.. _its documentation: https://cloud.google.com/translate/docs
.. _Mini Google Translate "MVP": https://github.com/googlecodelabs/cloud-nebulous-serverless-python
.. _Google Cloud serverless hosting platforms: https://cloud.google.com/serverless#serverless-products
.. _App Engine: https://cloud.google.com/appengine
.. _Cloud Functions: https://cloud.google.com/functions
.. _Cloud Run: https://cloud.google.com/run

