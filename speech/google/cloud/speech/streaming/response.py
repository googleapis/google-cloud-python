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

"""Representation of a GAPIC Speech API response."""

from google.cloud.speech.streaming.result import StreamingSpeechResult


class StreamingSpeechResponse(object):
    """Representation of a Speech API protobuf streaming response.

    :type error: :class:`google.grpc.Status`
    :param error: Instance of ``Status``

    :type endpointer_type: :class:`~EndpointerType`
    :param endpointer_type: Enum of endpointer event.

    :type results: list of
        :class:`google.cloud.speech.v1beta1.StreamingRecognitionResult`
    :param results: List of protobuf ``StreamingRecognitionResult``.

    :type result_index: int
    :param result_index: Index for specific result set. Used for updating with
                         ``interim_results``.
    """
    def __init__(self, error, endpointer_type, results, result_index):
        self._error = error
        self._endpointer_type = endpointer_type  # Should be enum.
        self._result_index = result_index
        self._results = [StreamingSpeechResult.from_pb(result)
                         for result in results]

    @classmethod
    def from_pb(cls, pb_response):
        """Factory: construct a ``StreamingSpeechResponse`` from protobuf.

        :type pb_response:
            :class:`google.cloud.speech.v1beta1.StreamingRecognizeResponse`
        :param pb_response: Instance of protobuf
                            ``StreamingRecognizeResponse``.
        :rtype: :class:`~StreamingSpeechResponse`
        :returns: Instance of ``StreamingSpeechResponse``.
        """
        error = pb_response.error
        endpointer_type = pb_response.endpointer_type
        results = pb_response.results
        result_index = pb_response.result_index
        return cls(error, endpointer_type, results, result_index)

    @property
    def result_index(self):
        """Result index associated with this response.

        :rtype: int
        :returns: Result index of this response.
        """
        return self._result_index

    @property
    def results(self):
        """List of results for this response.

        :rtype: list of :class:`~result.StreamingSpeechResult`
        :returns: List of ``StreamingSpeechResult`` in this response.
        """
        return self._results
