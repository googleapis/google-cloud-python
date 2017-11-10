# Copyright 2017 Google LLC
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

"""HTTP module for managing Speech API requests."""

from base64 import b64encode

from google.cloud._helpers import _bytes_to_unicode
from google.cloud._helpers import _to_bytes
from google.cloud import _http

from google.cloud.speech import __version__
from google.cloud.speech.result import Result
from google.cloud.speech.operation import Operation


_CLIENT_INFO = _http.CLIENT_INFO_TEMPLATE.format(__version__)


class Connection(_http.JSONConnection):
    """A connection to Google Cloud Speech JSON REST API.

    :type client: :class:`~google.cloud.speech.client.Client`
    :param client: The client that owns the current connection.
    """

    API_BASE_URL = 'https://speech.googleapis.com'
    """The base of the API call URL."""

    API_VERSION = 'v1'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = '{api_base_url}/{api_version}/{path}'
    """A template for the URL of a particular API call."""

    _EXTRA_HEADERS = {
        _http.CLIENT_INFO_HEADER: _CLIENT_INFO,
    }


class HTTPSpeechAPI(object):
    """Speech API for interacting with the HTTP version of the API.

    :type client: :class:`google.cloud.core.client.Client`
    :param client: Instance of a ``Client`` object.
    """
    def __init__(self, client):
        self._client = client
        self._connection = Connection(client)

    def long_running_recognize(self, sample, language_code,
                               max_alternatives=None, profanity_filter=None,
                               speech_contexts=()):
        """Long-running Recognize request to Google Speech API.

        .. _long_running_recognize: https://cloud.google.com/speech/reference/\
                                    rest/v1/speech/longrunningrecognize

        See `long_running_recognize`_.

        :type sample: :class:`~google.cloud.speech.sample.Sample`
        :param sample: Instance of ``Sample`` containing audio information.

        :type language_code: str
        :param language_code: The language of the supplied audio as
                              BCP-47 language tag. Example: ``'en-US'``.

        :type max_alternatives: int
        :param max_alternatives: (Optional) Maximum number of recognition
                                 hypotheses to be returned. The server may
                                 return fewer than maxAlternatives.
                                 Valid values are 0-30. A value of 0 or 1
                                 will return a maximum of 1. Defaults to 1

        :type profanity_filter: bool
        :param profanity_filter: If True, the server will attempt to filter
                                 out profanities, replacing all but the
                                 initial character in each filtered word with
                                 asterisks, e.g. ``'f***'``. If False or
                                 omitted, profanities won't be filtered out.

        :type speech_contexts: list
        :param speech_contexts: A list of strings (max 50) containing words and
                               phrases "hints" so that the speech recognition
                               is more likely to recognize them. This can be
                               used to improve the accuracy for specific words
                               and phrases. This can also be used to add new
                               words to the vocabulary of the recognizer.

        :rtype: :class:`~google.cloud.speech.operation.Operation`
        :returns: Operation for asynchronous request to Google Speech API.
        """
        data = _build_request_data(sample, language_code, max_alternatives,
                                   profanity_filter, speech_contexts)
        api_response = self._connection.api_request(
            method='POST', path='speech:longrunningrecognize', data=data)

        operation = Operation.from_dict(api_response, self._client)
        operation.caller_metadata['request_type'] = 'LongRunningRecognize'
        return operation

    def recognize(self, sample, language_code, max_alternatives=None,
                  profanity_filter=None, speech_contexts=()):
        """Synchronous Speech Recognition.

        .. _recognize: https://cloud.google.com/speech/reference/\
                       rest/v1/speech/recognize

        See `recognize`_.

        :type sample: :class:`~google.cloud.speech.sample.Sample`
        :param sample: Instance of ``Sample`` containing audio information.

        :type language_code: str
        :param language_code: (Optional) The language of the supplied audio as
                              BCP-47 language tag. Example: ``'en-US'``.

        :type max_alternatives: int
        :param max_alternatives: (Optional) Maximum number of recognition
                                 hypotheses to be returned. The server may
                                 return fewer than maxAlternatives.
                                 Valid values are 0-30. A value of 0 or 1
                                 will return a maximum of 1. Defaults to 1

        :type profanity_filter: bool
        :param profanity_filter: If True, the server will attempt to filter
                                 out profanities, replacing all but the
                                 initial character in each filtered word with
                                 asterisks, e.g. ``'f***'``. If False or
                                 omitted, profanities won't be filtered out.

        :type speech_contexts: list
        :param speech_contexts: A list of strings (max 50) containing words and
                               phrases "hints" so that the speech recognition
                               is more likely to recognize them. This can be
                               used to improve the accuracy for specific words
                               and phrases. This can also be used to add new
                               words to the vocabulary of the recognizer.

        :rtype: list
        :returns: A list of dictionaries. One dict for each alternative. Each
                  dictionary typically contains two keys (though not
                  all will be present in all cases)

                  * ``transcript``: The detected text from the audio recording.
                  * ``confidence``: The confidence in language detection, float
                    between 0 and 1.

        :raises: ValueError if more than one result is returned or no results.
        """
        data = _build_request_data(sample, language_code, max_alternatives,
                                   profanity_filter, speech_contexts)
        api_response = self._connection.api_request(
            method='POST', path='speech:recognize', data=data)

        if len(api_response['results']) > 0:
            results = api_response['results']
            return [Result.from_api_repr(result) for result in results]
        else:
            raise ValueError('No results were returned from the API')


def _build_request_data(sample, language_code, max_alternatives=None,
                        profanity_filter=None, speech_contexts=()):
    """Builds the request data before making API request.

    :type sample: :class:`~google.cloud.speech.sample.Sample`
    :param sample: Instance of ``Sample`` containing audio information.

    :type language_code: str
    :param language_code: The language of the supplied audio as
                          BCP-47 language tag. Example: ``'en-US'``.

    :type max_alternatives: int
    :param max_alternatives: (Optional) Maximum number of recognition
                             hypotheses to be returned. The server may
                             return fewer than maxAlternatives.
                             Valid values are 0-30. A value of 0 or 1
                             will return a maximum of 1. Defaults to 1

    :type profanity_filter: bool
    :param profanity_filter: If True, the server will attempt to filter
                             out profanities, replacing all but the
                             initial character in each filtered word with
                             asterisks, e.g. ``'f***'``. If False or
                             omitted, profanities won't be filtered out.

    :type speech_contexts: list
    :param speech_contexts: A list of strings (max 50) containing words and
                           phrases "hints" so that the speech recognition
                           is more likely to recognize them. This can be
                           used to improve the accuracy for specific words
                           and phrases. This can also be used to add new
                           words to the vocabulary of the recognizer.

    :rtype: dict
    :returns: Dictionary with required data for Google Speech API.
    """
    if sample.content is not None:
        audio = {'content':
                 _bytes_to_unicode(b64encode(_to_bytes(sample.content)))}
    else:
        audio = {'uri': sample.source_uri}

    config = {
        'encoding': sample.encoding,
        'languageCode': language_code,
        'sampleRateHertz': sample.sample_rate_hertz,
    }

    if max_alternatives is not None:
        config['maxAlternatives'] = max_alternatives
    if profanity_filter is not None:
        config['profanityFilter'] = profanity_filter
    if speech_contexts:
        config['speechContexts'] = {'phrases': speech_contexts}

    data = {
        'audio': audio,
        'config': config,
    }

    return data
