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

"""Representation of Speech GAPIC API result."""

from google.cloud.speech.transcript import Transcript


class StreamingSpeechResult(object):
    """Factory: contruct streaming speech result.

    :type alternatives:
        :class:`google.cloud.speech.v1beta1.SpeechRecognitionAlternative`
    :param alternatives: List of ``SpeechRecognitionAlternative``.

    :type is_final: bool
    :param is_final: Indicates if the transcription is complete.

    :type stability: float
    :param stability: An estimate of the probability that the recognizer will
                      not change its guess about this interim result.
    """

    def __init__(self, alternatives, is_final, stability):
        self._alternatives = [Transcript.from_pb(alternative)
                              for alternative in alternatives]
        self._is_final = is_final
        self._stability = stability

    @classmethod
    def from_pb(cls, pb_response):
        """Factory: construct StreamingSpeechResult from protobuf response.

        :type pb_response:
            :class:`google.cloud.speech.v1beta1.StreamingRecognitionResult`
        :param pb_response: Instance of ``StreamingRecognitionResult``.

        :rtype: :class:`~result.StreamingSpeechResult`
        :returns: Instance of ``StreamingSpeechResult``.
        """
        alternatives = pb_response.alternatives
        is_final = pb_response.is_final
        stability = pb_response.stability
        return cls(alternatives, is_final, stability)

    @property
    def alternatives(self):
        """List of alternative transcripts.

        :rtype: list of :class:`~google.cloud.speech.transcript.Transcript`
        :returns: List of ``Transcript`` objects.
        """
        return self._alternatives

    @property
    def is_final(self):
        """Represents an interim result that may change.

        :rtype: bool
        :returns: True if the result has completed it's processing.
        """
        return bool(self._is_final)
