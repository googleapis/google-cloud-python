Python Client for Google Cloud Natural Language
===============================================

|GA| |pypi| |versions| 

The `Google Cloud Natural Language`_ API can be used to reveal the
structure and meaning of text via powerful machine
learning models. You can use it to extract information about
people, places, events and much more, mentioned in text documents,
news articles or blog posts. You can use it to understand
sentiment about your product on social media or parse intent from
customer conversations happening in a call center or a messaging
app. You can analyze text uploaded in your request or integrate
with your document storage on Google Cloud Storage.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-language.svg
   :target: https://pypi.org/project/google-cloud-language/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-language.svg
   :target: https://pypi.org/project/google-cloud-language/
.. _Google Cloud Natural Language: https://cloud.google.com/natural-language/
.. _Product Documentation:  https://cloud.google.com/natural-language/docs
.. _Client Library Documentation: https://googleapis.dev/python/language/latest

.. note::

    This library currently does not run on Google App Engine Standard.
    We are actively working on adding this support.

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Language API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Language API.:  https://cloud.google.com/natural-language
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
Python >= 3.5

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7. Python 2.7 support will be removed on January 1, 2020.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-language


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-language


Next Steps
~~~~~~~~~~

-  Read the `Usage documentation`_ for the language client
   to see available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.

.. _Usage documentation: https://googleapis.dev/python/language/latest
