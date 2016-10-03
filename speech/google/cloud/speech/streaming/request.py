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

"""Helper to make Speech requests from IO stream"""

from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import RecognitionConfig
from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
    StreamingRecognitionConfig)
from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
    StreamingRecognizeRequest)


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

    buff = b''
    for data in sample.stream:
        # Optimize the request data size to around 100ms.
        if len(buff) + len(data) >= sample.chunk_size:
            yield StreamingRecognizeRequest(audio_content=buff)
            buff = data
        else:
            buff += data

    # Clear final contents of buffer.
    yield StreamingRecognizeRequest(audio_content=buff)


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
