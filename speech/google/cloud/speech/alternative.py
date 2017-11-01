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

"""Representation of Speech Alternative for the Google Speech API."""


class Alternative(object):
    """Representation of Speech Alternative.

    :type transcript: str
    :param transcript: String of transcribed data.

    :type confidence: float
    :param confidence: The confidence estimate between 0.0 and 1.0.
    """
    def __init__(self, transcript, confidence):
        self._transcript = transcript
        self._confidence = confidence

    @classmethod
    def from_api_repr(cls, alternative):
        """Factory: construct ``Alternative`` from JSON response.

        :type alternative: dict
        :param alternative: Dictionary response from the REST API.

        :rtype: :class:`Alternative`
        :returns: Instance of ``Alternative``.
        """
        return cls(alternative['transcript'], alternative.get('confidence'))

    @classmethod
    def from_pb(cls, alternative):
        """Factory: construct ``Alternative`` from protobuf response.

        :type alternative:
            :class:`google.cloud.speech.v1.SpeechRecognitionAlternative`
        :param alternative: Instance of ``SpeechRecognitionAlternative``
                           from protobuf.

        :rtype: :class:`Alternative`
        :returns: Instance of ``Alternative``.
        """
        confidence = alternative.confidence
        if confidence == 0.0:  # In the protobof 0.0 means unset.
            confidence = None
        return cls(alternative.transcript, confidence)

    @property
    def transcript(self):
        """Transcript text from audio.

        :rtype: str
        :returns: Text detected in audio.
        """
        return self._transcript

    @property
    def confidence(self):
        """Confidence score for recognized speech.

        :rtype: float
        :returns: Confidence score of recognized speech [0-1].
        """
        return self._confidence
