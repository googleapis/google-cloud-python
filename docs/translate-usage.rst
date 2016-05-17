Using the API
=============

With `Google Translate`_, you can dynamically translate text
between thousands of language pairs. The Google Translate API
lets websites and programs integrate with Google Translate
programmatically. Google Translate API is available as a
paid service. See the `Pricing`_ and `FAQ`_ pages for details.

Authentication / Configuration
------------------------------

- Use :class:`~gcloud.translate.client.Client` objects to configure
  your applications.

- :class:`~gcloud.translate.client.Client` objects hold both a ``key``
  and a connection to the Translate service.

- **An API key is required for Translate.** See
  `Identifying your application to Google`_ for details. This is
  significantly different than the other clients in ``gcloud-python``.

Methods
-------

To create a client:

  .. code::

     >>> from gcloud import translate
     >>> client = translate.Client('my-api-key')

By default, the client targets English when doing detections
and translations, but a non-default value can be used as
well:

  .. code::

     >>> from gcloud import translate
     >>> client = translate.Client('my-api-key', target_language='es')

The Google Translate API has three supported methods, and they
map to three methods on a client:
:meth:`~gcloud.translate.client.Client.get_languages`,
:meth:`~gcloud.translate.client.Client.detect_language` and
:meth:`~gcloud.translate.client.Client.translate`.

To get a list of languages supported by Google Translate

  .. code::

     >>> from gcloud import translate
     >>> client = translate.Client('my-api-key')
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

     >>> from gcloud import translate
     >>> client = translate.Client('my-api-key')
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

To translate text:

  .. code::

     >>> from gcloud import translate
     >>> client = translate.Client('my-api-key')
     >>> client.translate('koszula')
     {
         'translatedText': 'shirt',
         'detectedSourceLanguage': 'pl',
         'input': 'koszula',
     }

or to use a non-default target language:

  .. code::

     >>> from gcloud import translate
     >>> client = translate.Client('my-api-key')
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

.. _Google Translate: https://cloud.google.com/translate
.. _Pricing: https://cloud.google.com/translate/v2/pricing.html
.. _FAQ: https://cloud.google.com/translate/v2/faq.html
.. _Identifying your application to Google: https://cloud.google.com/translate/v2/using_rest#auth
