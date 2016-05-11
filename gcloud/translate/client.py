# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Client for interacting with the Google Cloud Translate API."""


import httplib2
import six

from gcloud._helpers import _to_bytes
from gcloud.translate.connection import Connection


ENGLISH_ISO_639 = 'en'
"""ISO 639-1 language code for English."""


class Client(object):
    """Client to bundle configuration needed for API requests.

    :type key: str
    :param key: The key used to send with requests as a query
                parameter.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: (Optional) HTTP object to make requests. If not
                 passed, an :class:`httplib.Http` object is created.

    :type target_language: str
    :param target_language: (Optional) The target language used for
                            translations and language names. (Defaults to
                            :data:`ENGLISH_ISO_639`.)
    """

    def __init__(self, key, http=None, target_language=ENGLISH_ISO_639):
        self.key = key
        if http is None:
            http = httplib2.Http()
        self.connection = Connection(http=http)
        self.target_language = target_language

    def get_languages(self, target_language=None):
        """Get list of supported languages for translation.

        Response

        See: https://cloud.google.com/translate/v2/\
        discovering-supported-languages-with-rest

        :type target_language: str
        :param target_language: (Optional) The language used to localize
                                returned language names. Defaults to the
                                target language on the current client.

        :rtype: list
        :returns: List of dictionaries. Each dictionary contains a supported
                  ISO 639-1 language code (using the dictionary key
                  ``language``). If ``target_language`` is passed, each
                  dictionary will also contain the name of each supported
                  language (localized to the target language).
        """
        query_params = {'key': self.key}
        if target_language is None:
            target_language = self.target_language
        if target_language is not None:
            query_params['target'] = target_language
        response = self.connection.api_request(
            method='GET', path='/languages', query_params=query_params)
        return response.get('data', {}).get('languages', ())

    def detect_language(self, *values):
        """Detect the language of a string or list of strings.

        See: https://cloud.google.com/translate/v2/\
        detecting-language-with-rest

        :type values: tuple
        :param values: Tuple of strings that will have language detected.

        :rtype: list
        :returns: A list of dictionaries for each queried value. Each
                  dictionary typically contains three keys (though not
                  all will be present in all cases)

                  * ``confidence``: The confidence in language detection, a
                    float between 0 and 1.
                  * ``input``: The corresponding input value.
                  * ``language``: The detected language (as an ISO 639-1
                    language code).

                  If multiple languages are detected for a given input, then
                  the there will be a list of dictionaries (instead of a single
                  dictionary) for that queried value.
        :raises: :class:`ValueError <exceptions.ValueError>` if the number of
                 detections is not equal to the number of values.
                 :class:`ValueError <exceptions.ValueError>` if a value
                 produces a list of detections with 0 or multiple results in it.
        """
        query_params = [('key', self.key)]
        query_params.extend(('q', _to_bytes(value, 'utf-8'))
                            for value in values)
        response = self.connection.api_request(
            method='GET', path='/detect', query_params=query_params)
        detections = response.get('data', {}).get('detections', ())

        if len(values) != len(detections):
            raise ValueError('Expected same number of values and detections',
                             values, detections)

        for index, value in enumerate(values):
            # Empirically, even clearly ambiguous text like "no" only returns
            # a single detection, so we replace the list of detections with
            # the single detection contained.
            if len(detections[index]) == 1:
                detections[index] = detections[index][0]
            else:
                message = ('Expected a single detection per value, API '
                           'returned %d') % (len(detections[index]),)
                raise ValueError(message, value, detections[index])

            detections[index]['input'] = value
            # The ``isReliable`` field is deprecated.
            detections[index].pop('isReliable', None)

        return detections

    def translate(self, *values, **kwargs):
        """Translate a string or list of strings.

        See: https://cloud.google.com/translate/v2/\
        translating-text-with-rest

        Accepted keyword arguments are:

        * ``target_language`` (str): The language to translate results into.
          This is required by the API and defaults to :data:`ENGLISH_ISO_639`.
        * ``format`` (str): (Optional) One of ``text`` or ``html``, to specify
          if the input text is plain text or HTML.
        * ``source_language`` (str): (Optional) The language of the text to
          be translated.
        * ``customization_ids`` (list): (Optional) List of customization IDs
          for translation. Sets the ``cid`` parameter in the query.

        :type values: tuple
        :param values: Tuple of strings to translate.

        :type kwargs: dict
        :param kwargs: Keyword arguments to be passed in.

        :rtype: list
        :returns: A list of dictionaries for each queried value. Each
                  dictionary typically contains three keys (though not
                  all will be present in all cases)

                  * ``detectedSourceLanguage``: The detected language (as an
                    ISO 639-1 language code) of the text.
                  * ``translatedText``: The translation of the text into the
                    target language.
                  * ``input``: The corresponding input value.
        :raises: :class:`ValueError <exceptions.ValueError>` if the number of
                 values and translations differ.
        """
        target_language = kwargs.get('target_language', self.target_language)
        customization_ids = kwargs.get('customization_ids', ())
        if isinstance(customization_ids, six.string_types):
            customization_ids = [customization_ids]

        query_params = [('key', self.key), ('target', target_language)]
        query_params.extend(('q', _to_bytes(value, 'utf-8'))
                            for value in values)
        query_params.extend(('cid', cid) for cid in customization_ids)
        if 'format' in kwargs:
            query_params.append(('format', kwargs['format']))
        if 'source_language' in kwargs:
            query_params.append(('source', kwargs['source_language']))

        response = self.connection.api_request(
            method='GET', path='', query_params=query_params)

        translations = response.get('data', {}).get('translations', ())
        if len(values) != len(translations):
            raise ValueError('Expected iterations to have same length',
                             values, translations)
        for value, translation in six.moves.zip(values, translations):
            translation['input'] = value
        return translations
