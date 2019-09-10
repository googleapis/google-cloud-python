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
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-translate.svg
   :target: https://pypi.org/project/google-cloud-translate/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-translate.svg
   :target: https://pypi.org/project/google-cloud-translate/
.. _Google Cloud Translation: https://cloud.google.com/translate/
.. _Pricing: https://cloud.google.com/translate/pricing
.. _FAQ: https://cloud.google.com/translate/faq
.. _Client Library Documentation: https://googleapis.dev/python/translation/latest
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
    <your-env>/bin/pip install google-cloud-translate


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-translate


Example Usage
~~~~~~~~~~~~~

.. code-block:: python

     >>> from google.cloud import translate
     >>> client = translate.Client()
     >>> client.get_languages()
     [
         {
             'language': 'af',
             'name': 'Afrikaans',
         },
          ...
     ]
     >>> client.detect_language(['Me llamo', 'I am'])
     [
         {
             'confidence': 0.25830904,
             'input': 'Me llamo',
             'language': 'es',
         }, {
             'confidence': 0.17112699,
             'input': 'I am',
             'language': 'en',
         },
     ]
     >>> from google.cloud import translate
     >>> client = translate.Client()
     >>> client.translate('koszula')
     {
         'translatedText': 'shirt',
         'detectedSourceLanguage': 'pl',
         'input': 'koszula',
     }
