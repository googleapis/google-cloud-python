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

"""Speech result representations."""

from google.cloud.speech.alternative import Alternative


class Result(object):
    """Speech recognition result representation.

    This is the object that comes back on sync or async requests
    (but not streaming requests).

    :type alternatives: list
    :param alternatives: List of
        :class:`~google.cloud.speech.alternative.Alternative`.
    """
    def __init__(self, alternatives):
        self.alternatives = alternatives

    @classmethod
    def from_pb(cls, result):
        """Factory: construct instance of ``Result``.

        :type result: :class:`~google.cloud.proto.speech.v1\
                               .cloud_speech_pb2.SpeechRecognitionResult`
        :param result: Instance of ``SpeechRecognitionResult`` protobuf.

        :rtype: :class:`~google.cloud.speech.result.Result`
        :returns: Instance of ``Result``.
        """
        alternatives = [Alternative.from_pb(alternative) for alternative
                        in result.alternatives]
        return cls(alternatives=alternatives)

    @classmethod
    def from_api_repr(cls, result):
        """Factory: construct instance of ``Result``.

        :type result: dict
        :param result: Dictionary of a :class:`~google.cloud.proto.speech.\
            v1.cloud_speech_pb2.SpeechRecognitionResult`

        :rtype: :class:`~google.cloud.speech.result.Result`
        :returns: Instance of ``Result``.
        """
        alternatives = [Alternative.from_api_repr(alternative) for alternative
                        in result['alternatives']]
        return cls(alternatives=alternatives)

    @property
    def confidence(self):
        """Return the confidence for the most probable alternative.

        :rtype: float
        :returns: Confidence value, between 0 and 1.
        """
        return self.alternatives[0].confidence

    @property
    def transcript(self):
        """Return the transcript for the most probable alternative.

        :rtype: str
        :returns: Speech transcript.
        """
        return self.alternatives[0].transcript


class StreamingSpeechResult(object):
    """Streaming speech result representation.

    :type alternatives: list
    :param alternatives: List of
                         :class:`~google.cloud.speech.alternative.Alternative`.

    :type is_final: bool
    :param is_final: Boolean indicator of results finality.

    :type stability: float
    :param stability: 0.0-1.0 stability score for the results returned.
    """
    def __init__(self, alternatives, is_final=False, stability=0.0):
        self.alternatives = alternatives
        self.is_final = is_final
        self.stability = stability

    @classmethod
    def from_pb(cls, response):
        """Factory: construct instance of ``StreamingSpeechResult``.

        :type response: :class:`~google.cloud.proto.speech.v1\
                               .cloud_speech_pb2.StreamingRecognizeResult`
        :param response: Instance of ``StreamingRecognizeResult`` protobuf.

        :rtype: :class:`~google.cloud.speech.result.StreamingSpeechResult`
        :returns: Instance of ``StreamingSpeechResult``.
        """
        alternatives = [Alternative.from_pb(result) for result
                        in response.alternatives]
        is_final = response.is_final
        stability = response.stability
        return cls(alternatives=alternatives, is_final=is_final,
                   stability=stability)

    @property
    def confidence(self):
        """Return the confidence for the most probable alternative.

        :rtype: float
        :returns: Confidence value, between 0 and 1.
        """
        return self.alternatives[0].confidence

    @property
    def transcript(self):
        """Return the transcript for the most probable alternative.

        :rtype: str
        :returns: Speech transcript.
        """
        return self.alternatives[0].transcript
