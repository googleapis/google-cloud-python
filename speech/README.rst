Python Client for Cloud Speech API (`Alpha`_)
=============================================

`Cloud Speech API`_: Converts audio to text by applying powerful neural network models.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Alpha: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _Cloud Speech API: https://cloud.google.com/speech
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/speech/usage.html
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
.. _Setup Authentication.: https://googlecloudplatform.github.io/google-cloud-python/stable/core/auth.html

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
    <your-env>/bin/pip install google-cloud-speech


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-speech

Preview
~~~~~~~

SpeechClient
^^^^^^^^^^^^

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
-  Read the `Cloud Speech API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud Speech API Product documentation:  https://cloud.google.com/speech
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst