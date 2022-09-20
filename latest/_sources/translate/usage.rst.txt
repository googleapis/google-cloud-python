Using the Translate Client
--------------------------

To create a client:

.. doctest::

   >>> from google.cloud import translate
   >>> client = translate.Client()

By default, the client targets English when doing detections
and translations, but a non-default value can be used as
well:

.. doctest::

   >>> from google.cloud import translate
   >>> client = translate.Client(target_language='es')

The Google Cloud Translation API has three supported methods, and they
map to three methods on a client:
:meth:`~google.cloud.translate.client.Client.get_languages`,
:meth:`~google.cloud.translate.client.Client.detect_language` and
:meth:`~google.cloud.translate.client.Client.translate`.

To get a list of languages supported by the Google Cloud Translation API

.. doctest::

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

To detect the language that some given text is written in:

.. doctest::

   >>> from google.cloud import translate
   >>> client = translate.Client()
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

The `confidence`_ value is an optional floating point value between 0 and 1.
The closer this value is to 1, the higher the confidence level for the
language detection. This member is not always available.

.. _confidence: https://cloud.google.com/translate/docs/detecting-language

To translate text into the default destination language without knowing
the source language:

.. doctest::

   >>> from google.cloud import translate
   >>> client = translate.Client()
   >>> client.translate('koszula')
   {
       'translatedText': 'shirt',
       'detectedSourceLanguage': 'pl',
       'input': 'koszula',
   }

If the source language is known:

.. doctest::

   >>> from google.cloud import translate
   >>> client = translate.Client()
   >>> client.translate('camisa', source_language='es')
   {
       'translatedText': 'shirt',
       'input': 'camisa',
   }

or to use a non-default target language:

.. doctest::

   >>> from google.cloud import translate
   >>> client = translate.Client()
   >>> client.translate(['Me llamo Jeff', 'My name is Jeff'],
   ...                  target_language='de')
   [
       {
           'translatedText': 'Mein Name ist Jeff',
           'detectedSourceLanguage': 'es',
           'input': 'Me llamo Jeff',
       }, {
           'translatedText': 'Mein Name ist Jeff',
           'detectedSourceLanguage': 'en',
           'input': 'My name is Jeff',
       },
   ]
