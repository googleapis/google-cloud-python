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

"""Speech result representations."""

from google.cloud.speech.alternative import Alternative


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

        :type response: :class:`~google.cloud.grpc.speech.v1beta1\
                               .cloud_speech_pb2.StreamingRecognizeResult`
        :param response: Instance of ``StreamingRecognizeResult`` protobuf.

        :rtype: :class:`~google.cloud.speech.result.StreamingSpeechResult`
        :returns: Instance of ``StreamingSpeechResult``.
        """
        alternatives = [Alternative.from_pb(alternative)
                        for alternative in response.alternatives]
        is_final = response.is_final
        stability = response.stability
        return cls(alternatives=alternatives, is_final=is_final,
                   stability=stability)
