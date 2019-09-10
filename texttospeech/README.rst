Python Client for Cloud Text-to-Speech API
==========================================

|alpha| |pypi| |versions| 

`Cloud Text-to-Speech API`_: Synthesizes natural-sounding speech by applying
powerful neural network models.

- `Client Library Documentation`_
- `Product Documentation`_

.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-texttospeech.svg
   :target: https://pypi.org/project/google-cloud-texttospeech/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-texttospeech.svg
   :target: https://pypi.org/project/google-cloud-texttospeech/
.. _Cloud Text-to-Speech API: https://cloud.google.com/texttospeech
.. _Client Library Documentation: https://googleapis.dev/python/texttospeech/latest
.. _Product Documentation: https://cloud.google.com/texttospeech

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Text-to-Speech API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Text-to-Speech API.:  https://cloud.google.com/texttospeech
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
    <your-env>/bin/pip install google-cloud-texttospeech


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-texttospeech

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Text-to-Speech API
   API to see other available methods on the client.
-  Read the `Cloud Text-to-Speech API Product documentation`_ to learn
   more about the product and see How-to Guides.
   APIs that we cover.

.. _Cloud Text-to-Speech API Product documentation:  https://cloud.google.com/texttospeech
