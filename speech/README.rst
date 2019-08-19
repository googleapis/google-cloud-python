Python Client for Cloud Speech API
==================================


|GA| |pypi| |versions| 

The `Cloud Speech API`_ enables developers to convert audio to text by applying
powerful neural network models.  The API recognizes over 80 languages and
variants, to support your global user base.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-speech.svg
   :target: https://pypi.org/project/google-cloud-speech/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-speech.svg
   :target: https://pypi.org/project/google-cloud-speech/
.. _Cloud Speech API: https://cloud.google.com/speech
.. _Client Library Documentation: https://googleapis.dev/python/speech/latest
.. _Product Documentation:  https://cloud.google.com/speech

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Speech API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Speech API.:  https://cloud.google.com/speech
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
    <your-env>/bin/pip install google-cloud-speech


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-speech

Example Usage
~~~~~~~~~~~~~

.. code:: py

    from google.cloud import speech_v1
    from google.cloud.speech_v1 import enums

    client = speech_v1.SpeechClient()

    encoding = enums.RecognitionConfig.AudioEncoding.FLAC
    sample_rate_hertz = 44100
    language_code = 'en-US'
    config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code}
    uri = 'gs://bucket_name/file_name.flac'
    audio = {'uri': uri}

    response = client.recognize(config, audio)

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Speech API
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
   APIs that we cover.
