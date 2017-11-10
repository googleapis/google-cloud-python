# Copyright 2016 Google LLC
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

"""GAX/GAPIC module for managing Speech API requests."""

from google.cloud.gapic.speech.v1.speech_client import SpeechClient
from google.cloud.proto.speech.v1.cloud_speech_pb2 import RecognitionAudio
from google.cloud.proto.speech.v1.cloud_speech_pb2 import (
    RecognitionConfig)
from google.cloud.proto.speech.v1.cloud_speech_pb2 import (
    SpeechContext)
from google.cloud.proto.speech.v1.cloud_speech_pb2 import (
    StreamingRecognitionConfig)
from google.cloud.proto.speech.v1.cloud_speech_pb2 import (
    StreamingRecognizeRequest)
from google.longrunning import operations_grpc

from google.cloud import _helpers
from google.cloud._http import DEFAULT_USER_AGENT

from google.cloud.speech import __version__
from google.cloud.speech.operation import Operation
from google.cloud.speech.result import Result

OPERATIONS_API_HOST = 'speech.googleapis.com'


class GAPICSpeechAPI(object):
    """Manage calls through GAPIC wrappers to the Speech API.

    :type client: `~google.cloud.core.client.Client`
    :param client: Instance of ``Client``.
    """
    def __init__(self, client=None):
        self._client = client
        credentials = self._client._credentials
        channel = _helpers.make_secure_channel(
            credentials, DEFAULT_USER_AGENT,
            SpeechClient.SERVICE_ADDRESS)
        self._gapic_api = SpeechClient(
            channel=channel,
            lib_name='gccl',
            lib_version=__version__,
        )
        self._operations_stub = _helpers.make_secure_stub(
            credentials,
            DEFAULT_USER_AGENT,
            operations_grpc.OperationsStub,
            OPERATIONS_API_HOST,
        )

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
        :returns: Instance of ``Operation`` to poll for results.
        """
        config = RecognitionConfig(
            encoding=sample.encoding,
            language_code=language_code,
            max_alternatives=max_alternatives,
            profanity_filter=profanity_filter,
            sample_rate_hertz=sample.sample_rate_hertz,
            speech_contexts=[SpeechContext(phrases=speech_contexts)],
        )

        audio = RecognitionAudio(content=sample.content,
                                 uri=sample.source_uri)
        api = self._gapic_api
        operation_future = api.long_running_recognize(
            audio=audio,
            config=config,
        )

        return Operation.from_pb(operation_future.last_operation_data(), self)

    def streaming_recognize(self, sample, language_code,
                            max_alternatives=None, profanity_filter=None,
                            speech_contexts=(), single_utterance=False,
                            interim_results=False):
        """Streaming speech recognition.

        .. note::

            Streaming recognition requests are limited to 1 minute of audio.
            See https://cloud.google.com/speech/limits#content

        Yields :class:`~streaming_response.StreamingSpeechResponse` containing
        results and metadata from the streaming request.

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

        :type single_utterance: bool
        :param single_utterance: (Optional) If false or omitted, the recognizer
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

        :type interim_results: bool
        :param interim_results: (Optional) If true, interim results (tentative
                                hypotheses) may be returned as they become
                                available (these interim results are indicated
                                with the is_final=false flag). If false or
                                omitted, only is_final=true result(s) are
                                returned.

        :raises: :class:`ValueError` if sample.content is not a file-like
                 object. :class:`ValueError` if stream has closed.

        :rtype: :class:`~google.cloud.grpc.speech.v1\
                       .cloud_speech_pb2.StreamingRecognizeResponse`
        :returns: ``StreamingRecognizeResponse`` instances.
        """
        if sample.stream.closed:
            raise ValueError('Stream is closed.')

        requests = _stream_requests(sample, language_code=language_code,
                                    max_alternatives=max_alternatives,
                                    profanity_filter=profanity_filter,
                                    speech_contexts=speech_contexts,
                                    single_utterance=single_utterance,
                                    interim_results=interim_results)
        api = self._gapic_api
        responses = api.streaming_recognize(requests)
        return responses

    def recognize(self, sample, language_code, max_alternatives=None,
                  profanity_filter=None, speech_contexts=()):
        """Synchronous Speech Recognition.

        .. _recognize: https://cloud.google.com/speech/reference/\
                       rest/v1/speech/recognize

        See `recognize`_.

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

        :rtype: list
        :returns: List of :class:`google.cloud.speech.result.Result` objects.

        :raises: ValueError if there are no results.
        """
        config = RecognitionConfig(
            encoding=sample.encoding,
            language_code=language_code,
            max_alternatives=max_alternatives,
            profanity_filter=profanity_filter,
            sample_rate_hertz=sample.sample_rate_hertz,
            speech_contexts=[SpeechContext(phrases=speech_contexts)],
        )
        audio = RecognitionAudio(content=sample.content,
                                 uri=sample.source_uri)
        api = self._gapic_api
        api_response = api.recognize(config=config, audio=audio)

        # Sanity check: If we got no results back, raise an error.
        if len(api_response.results) == 0:
            raise ValueError('No results returned from the Speech API.')

        # Iterate over any results that came back.
        return [Result.from_pb(result) for result in api_response.results]


def _stream_requests(sample, language_code, max_alternatives=None,
                     profanity_filter=None, speech_contexts=(),
                     single_utterance=None, interim_results=None):
    """Generate stream of requests from sample.

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
    :param profanity_filter: (Optional) If True, the server will attempt to
                             filter out profanities, replacing all but the
                             initial character in each filtered word with
                             asterisks, e.g. ``'f***'``. If False or
                             omitted, profanities won't be filtered out.

    :type speech_contexts: list
    :param speech_contexts: (Optional) A list of strings (max 50) containing
                            words and phrases "hints" so that the speech
                            recognition is more likely to recognize them.
                            This can be used to improve the accuracy for
                            specific words and phrases. This can also be used
                            to add new words to the vocabulary of the
                            recognizer.

    :type single_utterance: bool
    :param single_utterance: (Optional) If false or omitted, the recognizer
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

    :type interim_results: bool
    :param interim_results: (Optional) If true, interim results (tentative
                            hypotheses) may be returned as they become
                            available (these interim results are indicated
                            with the is_final=false flag). If false or
                            omitted, only is_final=true result(s) are
                            returned.
    """
    config_request = _make_streaming_request(
        sample, language_code=language_code, max_alternatives=max_alternatives,
        profanity_filter=profanity_filter,
        speech_contexts=[SpeechContext(phrases=speech_contexts)],
        single_utterance=single_utterance, interim_results=interim_results)

    # The config request MUST go first and not contain any audio data.
    yield config_request

    while True:
        data = sample.stream.read(sample.chunk_size)
        if not data:
            break
        yield StreamingRecognizeRequest(audio_content=data)


def _make_streaming_request(sample, language_code,
                            max_alternatives, profanity_filter,
                            speech_contexts, single_utterance,
                            interim_results):
    """Build streaming request.

    :type sample: :class:`~google.cloud.speech.sample.Sample`
    :param sample: Instance of ``Sample`` containing audio information.

    :type language_code: str
    :param language_code: The language of the supplied audio as
                          BCP-47 language tag. Example: ``'en-GB'``.
                          If omitted, defaults to ``'en-US'``.

    :type max_alternatives: int
    :param max_alternatives: Maximum number of recognition
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

    :type single_utterance: bool
    :param single_utterance: If false or omitted, the recognizer
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

    :type interim_results: bool
    :param interim_results: If true, interim results (tentative
                            hypotheses) may be returned as they become
                            available (these interim results are indicated
                            with the is_final=false flag). If false or
                            omitted, only is_final=true result(s) are
                            returned.

    :rtype:
        :class:`~grpc.speech.v1.cloud_speech_pb2.StreamingRecognizeRequest`
    :returns: Instance of ``StreamingRecognizeRequest``.
    """
    config = RecognitionConfig(
        encoding=sample.encoding,
        language_code=language_code,
        max_alternatives=max_alternatives,
        profanity_filter=profanity_filter,
        sample_rate_hertz=sample.sample_rate_hertz,
        speech_contexts=speech_contexts,
    )

    streaming_config = StreamingRecognitionConfig(
        config=config, single_utterance=single_utterance,
        interim_results=interim_results)

    config_request = StreamingRecognizeRequest(
        streaming_config=streaming_config)

    return config_request
