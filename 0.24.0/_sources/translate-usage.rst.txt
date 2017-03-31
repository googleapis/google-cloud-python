Using the API
=============

With `Google Cloud Translation`_, you can dynamically translate text
between thousands of language pairs. The Google Cloud Translation API
lets websites and programs integrate with Google Cloud Translation
programmatically. Google Cloud Translation is available as a
paid service. See the `Pricing`_ and `FAQ`_ pages for details.

Authentication / Configuration
------------------------------

- Use :class:`~google.cloud.translate.client.Client` objects to configure
  your applications.

- :class:`~google.cloud.translate.client.Client` objects hold
  a connection to the Cloud Translation service.

Methods
-------

To create a client:

  .. code::

     >>> from google.cloud import translate
     >>> client = translate.Client()

By default, the client targets English when doing detections
and translations, but a non-default value can be used as
well:

  .. code::

     >>> from google.cloud import translate
     >>> client = translate.Client(target_language='es')

The Google Cloud Translation API has three supported methods, and they
map to three methods on a client:
:meth:`~google.cloud.translate.client.Client.get_languages`,
:meth:`~google.cloud.translate.client.Client.detect_language` and
:meth:`~google.cloud.translate.client.Client.translate`.

To get a list of languages supported by the Google Cloud Translation API

  .. code::

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

  .. code::

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

To translate text:

  .. code::

     >>> from google.cloud import translate
     >>> client = translate.Client()
     >>> client.translate('koszula')
     {
         'translatedText': 'shirt',
         'detectedSourceLanguage': 'pl',
         'input': 'koszula',
     }

or to use a non-default target language:

  .. code::

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

.. _Google Cloud Translation: https://cloud.google.com/translate/
.. _Pricing: https://cloud.google.com/translate/pricing
.. _FAQ: https://cloud.google.com/translate/faq
.. _Identifying your application to Google: https://cloud.google.com/translate/docs/translating-text
.. _confidence: https://cloud.google.com/translate/docs/detecting-language
