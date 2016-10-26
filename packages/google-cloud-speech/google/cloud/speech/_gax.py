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

"""GAX/GAPIC module for managing Speech API requests."""

from google.cloud.gapic.speech.v1beta1.speech_api import SpeechApi
from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import SpeechContext
from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import RecognitionConfig
from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import RecognitionAudio

from google.cloud.speech.transcript import Transcript


class GAPICSpeechAPI(object):
    """Manage calls through GAPIC wrappers to the Speech API."""
    def __init__(self):
        self._gapic_api = SpeechApi()

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

        :raises NotImplementedError: Always.
        """
        raise NotImplementedError

    def sync_recognize(self, sample, language_code=None, max_alternatives=None,
                       profanity_filter=None, speech_context=None):
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

        :raises: ValueError if more than one result is returned or no results.
        """
        config = RecognitionConfig(
            encoding=sample.encoding, sample_rate=sample.sample_rate,
            language_code=language_code, max_alternatives=max_alternatives,
            profanity_filter=profanity_filter,
            speech_context=SpeechContext(phrases=speech_context))

        audio = RecognitionAudio(content=sample.content,
                                 uri=sample.source_uri)
        api = self._gapic_api
        api_response = api.sync_recognize(config=config, audio=audio)
        if len(api_response.results) == 1:
            results = api_response.results.pop()
            alternatives = results.alternatives
            return [Transcript.from_pb(alternative)
                    for alternative in alternatives]
        else:
            raise ValueError('More than one result or none returned from API.')
