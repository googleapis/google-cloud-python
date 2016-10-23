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

import os
from base64 import b64encode

from google.cloud._helpers import _to_bytes
from google.cloud._helpers import _bytes_to_unicode
from google.cloud import client as client_module
from google.cloud.environment_vars import DISABLE_GRPC
from google.cloud.speech.connection import Connection
from google.cloud.speech.encoding import Encoding
from google.cloud.speech.operation import Operation
from google.cloud.speech.sample import Sample
from google.cloud.speech.transcript import Transcript
from google.cloud.speech.streaming_response import StreamingSpeechResponse

try:
    from google.cloud.gapic.speech.v1beta1.speech_api import SpeechApi
    from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
        SpeechContext)
    from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
        RecognitionConfig)
    from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
        RecognitionAudio)
    from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
        StreamingRecognitionConfig)
    from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
        StreamingRecognizeRequest)
except ImportError:  # pragma: NO COVER
    _HAVE_GAX = False
else:
    _HAVE_GAX = True


_DISABLE_GAX = os.getenv(DISABLE_GRPC, False)
_USE_GAX = _HAVE_GAX and not _DISABLE_GAX


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
    _speech_api = None

    def async_recognize(self, sample, language_code=None,
                        max_alternatives=None, profanity_filter=None,
                        speech_context=None):
        """Asychronous Recognize request to Google Speech API.

        .. _async_recognize: https://cloud.google.com/speech/reference/\
                             rest/v1beta1/speech/asyncrecognize

        See `async_recognize`_.

        :type sample: :class:`~google.cloud.speech.sample.Sample`
        :param sample: Instance of ``Sample`` containing audio information.

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
        if sample.encoding is not Encoding.LINEAR16:
            raise ValueError('Only LINEAR16 encoding is supported by '
                             'asynchronous speech requests.')

        data = _build_request_data(sample, language_code, max_alternatives,
                                   profanity_filter, speech_context)

        api_response = self.connection.api_request(
            method='POST', path='speech:asyncrecognize', data=data)

        return Operation.from_api_repr(self, api_response)

    @staticmethod
    def sample(content=None, source_uri=None, stream=None, encoding=None,
               sample_rate=None):
        """Factory: construct Sample to use when making recognize requests.

        :type content: bytes
        :param content: (Optional) Byte stream of audio.

        :type source_uri: str
        :param source_uri: (Optional) URI that points to a file that contains
                           audio data bytes as specified in RecognitionConfig.
                           Currently, only Google Cloud Storage URIs are
                           supported, which must be specified in the following
                           format: ``gs://bucket_name/object_name``.

        :type stream: :class:`io.BufferedReader`
        :param stream: File like object to read audio data from.

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

        :rtype: :class:`~google.cloud.speech.sample.Sample`
        :returns: Instance of ``Sample``.
        """
        return Sample(content=content, source_uri=source_uri, stream=stream,
                      encoding=encoding, sample_rate=sample_rate)

    def sync_recognize(self, sample, language_code=None,
                       max_alternatives=None, profanity_filter=None,
                       speech_context=None):
        """Synchronous Speech Recognition.

        .. _sync_recognize: https://cloud.google.com/speech/reference/\
                            rest/v1beta1/speech/syncrecognize

        See `sync_recognize`_.

        :type sample: :class:`~google.cloud.speech.sample.Sample`
        :param sample: Instance of ``Sample`` containing audio information.

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
        if _USE_GAX:
            config = RecognitionConfig(
                encoding=sample.encoding, sample_rate=sample.sample_rate,
                language_code=language_code, max_alternatives=max_alternatives,
                profanity_filter=profanity_filter,
                speech_context=SpeechContext(phrases=speech_context))

            audio = RecognitionAudio(content=sample.content,
                                     uri=sample.source_uri)

            return self._sync_recognize(config, audio)
        else:
            data = _build_request_data(sample, language_code, max_alternatives,
                                       profanity_filter, speech_context)
            return self._sync_recognize(data=data)

    def stream_recognize(self, sample, language_code=None,
                         max_alternatives=None, profanity_filter=None,
                         speech_context=None, single_utterance=False,
                         interim_results=False):
        """Streaming speech recognition.

        .. note::
            Streaming recognition requests are limited to 1 minute of audio.

            See: https://cloud.google.com/speech/limits#content

        :type sample: :class:`~google.cloud.speech.sample.Sample`
        :param sample: Instance of ``Sample`` containing audio information.

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

        :type single_utterance: boolean
        :param single_utterance: [Optional] If false or omitted, the recognizer
                                 will perform continuous recognition
                                 (continuing to process audio even if the user
                                 pauses speaking) until the client closes the
                                 output stream (gRPC API) or when the maximum
                                 time limit has been reached. Multiple
                                 SpeechRecognitionResults with the is_final
                                 flag set to true may be returned.

                                 If true, the recognizer will detect a single
                                 spoken utterance. When it detects that the
                                 user has paused or stopped speaking, it will
                                 return an END_OF_UTTERANCE event and cease
                                 recognition. It will return no more than one
                                 SpeechRecognitionResult with the is_final flag
                                 set to true.

        :type interim_results: boolean
        :param interim_results: [Optional] If true, interim results (tentative
                                hypotheses) may be returned as they become
                                available (these interim results are indicated
                                with the is_final=false flag). If false or
                                omitted, only is_final=true result(s) are
                                returned.
        """
        if not _USE_GAX:
            raise EnvironmentError('gRPC is required to use this API.')

        requests = _make_request_stream(sample, language_code=language_code,
                                        max_alternatives=max_alternatives,
                                        profanity_filter=profanity_filter,
                                        speech_context=speech_context,
                                        single_utterance=single_utterance,
                                        interim_results=interim_results)

        for response in self.speech_api.streaming_recognize(requests):
            if hasattr(response, 'results') or interim_results:
                yield StreamingSpeechResponse.from_pb(response)

    @property
    def speech_api(self):
        """Instance of Speech API.

        :rtype: :class:`google.cloud.gapic.speech.v1beta1.speech_api.SpeechApi`
        :returns: Instance of ``SpeechApi``.
        """
        if not self._speech_api:
            self._speech_api = SpeechApi()
        return self._speech_api

    def _sync_recognize(self, config=None, audio=None, data=None):
        """Handler for sync_recognize requests with or without GAPIC.

        :type config: :class:`~RecognitionConfig
        :param config: Instance of ``RecognitionConfig`` with recognition
                       settings.

        :type audio: :class:`~RecognitionAudio`
        :param audio: Instance of ``RecognitionAudio`` with audio source data.

        :type data: dict
        :param data: Mapped configuration paramters for the request.

        :rtype: list of :class:`~transcript.Transcript`
        :returns: List of ``Transcript`` with recognition results.
        """
        if config and audio and _USE_GAX:
            api_response = self.speech_api.sync_recognize(config=config,
                                                          audio=audio)
            results = api_response.results.pop()
            alternatives = results.alternatives
            return [Transcript.from_pb(alternative)
                    for alternative in alternatives]
        elif data:
            api_response = self.connection.api_request(
                method='POST', path='speech:syncrecognize', data=data)

            return [Transcript.from_api_repr(alternative)
                    for alternative
                    in api_response['results'][0]['alternatives']]


def _build_request_data(sample, language_code=None, max_alternatives=None,
                        profanity_filter=None, speech_context=None):
    """Builds the request data before making API request.

    :type sample: :class:`~google.cloud.speech.sample.Sample`
    :param sample: Instance of ``Sample`` containing audio information.

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
    if sample.content is not None:
        audio = {'content':
                 _bytes_to_unicode(b64encode(_to_bytes(sample.content)))}
    else:
        audio = {'uri': sample.source_uri}

    config = {'encoding': sample.encoding,
              'sampleRate': sample.sample_rate}

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


def _make_request_stream(sample, language_code=None, max_alternatives=None,
                         profanity_filter=None, speech_context=None,
                         single_utterance=None, interim_results=None):
    """Generate stream of requests from sample.

    :type sample: :class:`~google.cloud.speech.sample.Sample`
    :param sample: Instance of ``Sample`` containing audio information.

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

    :type single_utterance: boolean
    :param single_utterance: [Optional] If false or omitted, the recognizer
                             will perform continuous recognition
                             (continuing to process audio even if the user
                             pauses speaking) until the client closes the
                             output stream (gRPC API) or when the maximum
                             time limit has been reached. Multiple
                             SpeechRecognitionResults with the is_final
                             flag set to true may be returned.

                             If true, the recognizer will detect a single
                             spoken utterance. When it detects that the
                             user has paused or stopped speaking, it will
                             return an END_OF_UTTERANCE event and cease
                             recognition. It will return no more than one
                             SpeechRecognitionResult with the is_final flag
                             set to true.

    :type interim_results: boolean
    :param interim_results: [Optional] If true, interim results (tentative
                            hypotheses) may be returned as they become
                            available (these interim results are indicated
                            with the is_final=false flag). If false or
                            omitted, only is_final=true result(s) are
                            returned.
    """
    config_request = _make_streaming_config(
        sample, language_code=language_code, max_alternatives=max_alternatives,
        profanity_filter=profanity_filter, speech_context=speech_context,
        single_utterance=single_utterance, interim_results=interim_results)

    # The config request MUST go first and not contain any audio data.
    yield config_request

    while True:
        data = sample.stream.read(sample.chunk_size)
        if not data:
            break
        # Optimize the request data size to around 100ms.
        yield StreamingRecognizeRequest(audio_content=data)


def _make_streaming_config(sample, language_code,
                           max_alternatives, profanity_filter,
                           speech_context, single_utterance,
                           interim_results):
    """Build streaming configuration.

    :type sample: :class:`~google.cloud.speech.sample.Sample`
    :param sample: Instance of ``Sample`` containing audio information.

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

    :type single_utterance: boolean
    :param single_utterance: [Optional] If false or omitted, the recognizer
                             will perform continuous recognition
                             (continuing to process audio even if the user
                             pauses speaking) until the client closes the
                             output stream (gRPC API) or when the maximum
                             time limit has been reached. Multiple
                             SpeechRecognitionResults with the is_final
                             flag set to true may be returned.

                             If true, the recognizer will detect a single
                             spoken utterance. When it detects that the
                             user has paused or stopped speaking, it will
                             return an END_OF_UTTERANCE event and cease
                             recognition. It will return no more than one
                             SpeechRecognitionResult with the is_final flag
                             set to true.

    :type interim_results: boolean
    :param interim_results: [Optional] If true, interim results (tentative
                            hypotheses) may be returned as they become
                            available (these interim results are indicated
                            with the is_final=false flag). If false or
                            omitted, only is_final=true result(s) are
                            returned.

    :rtype: :class:`~StreamingRecognitionConfig`
    :returns: Instance of ``StreamingRecognitionConfig``.
    """
    config = RecognitionConfig(
        encoding=sample.encoding, sample_rate=sample.sample_rate,
        language_code=language_code, max_alternatives=max_alternatives,
        profanity_filter=profanity_filter, speech_context=speech_context)

    streaming_config = StreamingRecognitionConfig(
        config=config, single_utterance=single_utterance,
        interim_results=interim_results)

    config_request = StreamingRecognizeRequest(
        streaming_config=streaming_config)

    return config_request
