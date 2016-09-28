# Copyright 2016 Google Inc.
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

"""Basic client for Google Cloud Speech API."""

from base64 import b64encode

from google.cloud._helpers import _to_bytes
from google.cloud import client as client_module
from google.cloud.speech.connection import Connection
from google.cloud.speech.encoding import Encoding
from google.cloud.speech.operation import Operation


class Client(client_module.Client):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: The project which the client acts on behalf of. Will be
                    passed when creating a dataset / job.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def async_recognize(self, content, source_uri, encoding, sample_rate,
                        language_code=None, max_alternatives=None,
                        profanity_filter=None, speech_context=None):
        """Asychronous Recognize request to Google Speech API.

        .. _async_recognize: https://cloud.google.com/speech/reference/\
                             rest/v1beta1/speech/asyncrecognize

        See `async_recognize`_.

        :type content: bytes
        :param content: Byte stream of audio.

        :type source_uri: str
        :param source_uri: URI that points to a file that contains audio
                           data bytes as specified in RecognitionConfig.
                           Currently, only Google Cloud Storage URIs are
                           supported, which must be specified in the following
                           format: ``gs://bucket_name/object_name``.

        :type encoding: str
        :param encoding: encoding of audio data sent in all RecognitionAudio
                         messages, can be one of: :attr:`~.Encoding.LINEAR16`,
                         :attr:`~.Encoding.FLAC`, :attr:`~.Encoding.MULAW`,
                         :attr:`~.Encoding.AMR`, :attr:`~.Encoding.AMR_WB`

        :type sample_rate: int
        :param sample_rate: Sample rate in Hertz of the audio data sent in all
                            requests. Valid values are: 8000-48000. For best
                            results, set the sampling rate of the audio source
                            to 16000 Hz. If that's not possible, use the
                            native sample rate of the audio source (instead of
                            re-sampling).

        :type language_code: str
        :param language_code: (Optional) The language of the supplied audio as
                              BCP-47 language tag. Example: ``'en-GB'``.
                              If omitted, defaults to ``'en-US'``.

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

        :type speech_context: list
        :param speech_context: A list of strings (max 50) containing words and
                               phrases "hints" so that the speech recognition
                               is more likely to recognize them. This can be
                               used to improve the accuracy for specific words
                               and phrases. This can also be used to add new
                               words to the vocabulary of the recognizer.

        :rtype: `~google.cloud.speech.operation.Operation`
        :returns: ``Operation`` for asynchronous request to Google Speech API.
        """

        data = _build_request_data(content, source_uri, encoding,
                                   sample_rate, language_code,
                                   max_alternatives, profanity_filter,
                                   speech_context)

        api_response = self.connection.api_request(
            method='POST', path='speech:asyncrecognize', data=data)

        return Operation.from_api_repr(self, api_response)

    def sync_recognize(self, content, source_uri, encoding, sample_rate,
                       language_code=None, max_alternatives=None,
                       profanity_filter=None, speech_context=None):
        """Synchronous Speech Recognition.

        .. _sync_recognize: https://cloud.google.com/speech/reference/\
                            rest/v1beta1/speech/syncrecognize

        See `sync_recognize`_.

        :type content: bytes
        :param content: Byte stream of audio.

        :type source_uri: str
        :param source_uri: URI that points to a file that contains audio
                           data bytes as specified in RecognitionConfig.
                           Currently, only Google Cloud Storage URIs are
                           supported, which must be specified in the following
                           format: ``gs://bucket_name/object_name``.

        :type encoding: str
        :param encoding: encoding of audio data sent in all RecognitionAudio
                         messages, can be one of: :attr:`~.Encoding.LINEAR16`,
                         :attr:`~.Encoding.FLAC`, :attr:`~.Encoding.MULAW`,
                         :attr:`~.Encoding.AMR`, :attr:`~.Encoding.AMR_WB`

        :type sample_rate: int
        :param sample_rate: Sample rate in Hertz of the audio data sent in all
                            requests. Valid values are: 8000-48000. For best
                            results, set the sampling rate of the audio source
                            to 16000 Hz. If that's not possible, use the
                            native sample rate of the audio source (instead of
                            re-sampling).

        :type language_code: str
        :param language_code: (Optional) The language of the supplied audio as
                              BCP-47 language tag. Example: ``'en-GB'``.
                              If omitted, defaults to ``'en-US'``.

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

        :type speech_context: list
        :param speech_context: A list of strings (max 50) containing words and
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
        """

        data = _build_request_data(content, source_uri, encoding,
                                   sample_rate, language_code,
                                   max_alternatives, profanity_filter,
                                   speech_context)

        api_response = self.connection.api_request(
            method='POST', path='speech:syncrecognize', data=data)

        if len(api_response['results']) == 1:
            return api_response['results'][0]['alternatives']
        else:
            raise ValueError('result in api should have length 1')


def _build_request_data(content, source_uri, encoding, sample_rate,
                        language_code=None, max_alternatives=None,
                        profanity_filter=None, speech_context=None):
    """Builds the request data before making API request.

    :type content: bytes
    :param content: Byte stream of audio.

    :type source_uri: str
    :param source_uri: URI that points to a file that contains audio
                       data bytes as specified in RecognitionConfig.
                       Currently, only Google Cloud Storage URIs are
                       supported, which must be specified in the following
                       format: ``gs://bucket_name/object_name``.

    :type encoding: str
    :param encoding: encoding of audio data sent in all RecognitionAudio
                     messages, can be one of: :attr:`~.Encoding.LINEAR16`,
                     :attr:`~.Encoding.FLAC`, :attr:`~.Encoding.MULAW`,
                     :attr:`~.Encoding.AMR`, :attr:`~.Encoding.AMR_WB`

    :type sample_rate: int
    :param sample_rate: Sample rate in Hertz of the audio data sent in all
                        requests. Valid values are: 8000-48000. For best
                        results, set the sampling rate of the audio source
                        to 16000 Hz. If that's not possible, use the
                        native sample rate of the audio source (instead of
                        re-sampling).

    :type language_code: str
    :param language_code: (Optional) The language of the supplied audio as
                          BCP-47 language tag. Example: ``'en-GB'``.
                          If omitted, defaults to ``'en-US'``.

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

    :type speech_context: list
    :param speech_context: A list of strings (max 50) containing words and
                           phrases "hints" so that the speech recognition
                           is more likely to recognize them. This can be
                           used to improve the accuracy for specific words
                           and phrases. This can also be used to add new
                           words to the vocabulary of the recognizer.

    :rtype: dict
    :returns: Dictionary with required data for Google Speech API.
    """
    if content is None and source_uri is None:
        raise ValueError('content and source_uri cannot be both '
                         'equal to None')

    if content is not None and source_uri is not None:
        raise ValueError('content and source_uri cannot be both '
                         'different from None')

    if encoding is None:
        raise ValueError('encoding cannot be None')

    encoding_value = getattr(Encoding, encoding)

    if sample_rate is None:
        raise ValueError('sample_rate cannot be None')

    if content is not None:
        audio = {'content': b64encode(_to_bytes(content))}
    else:
        audio = {'uri': source_uri}

    config = {'encoding': encoding_value,
              'sampleRate': sample_rate}

    if language_code is not None:
        config['languageCode'] = language_code
    if max_alternatives is not None:
        config['maxAlternatives'] = max_alternatives
    if profanity_filter is not None:
        config['profanityFilter'] = profanity_filter
    if speech_context is not None:
        config['speechContext'] = {'phrases': speech_context}

    data = {
        'audio': audio,
        'config': config,
    }

    return data
