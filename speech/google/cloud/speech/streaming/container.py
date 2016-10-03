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

"""Representation of a group of GAPIC Speech API responses."""

from google.cloud.speech.streaming.response import StreamingSpeechResponse


class StreamingResponseContainer(object):
    """Response container to help manage streaming responses.

    :type responses: list of :class:`~response.StreamingSpeechResponse`
    :param responses: List of ``StreamingSpeechResponse`` objects.
    """
    def __init__(self, responses=None):
        self._responses = responses or {}

    def add_response(self, response):
        """Add/update response based on the ``result_index``.

        :type response: :class:`~response.StreamingSpeechResponse`
        :param response: Instance of ``StreamingSpeechResponse``.
        """
        self._responses.update({response.result_index:
                                StreamingSpeechResponse.from_pb(response)})

    @property
    def responses(self):
        """All responses held in container.

        :rtype: list of :class:`~response.StreamingSpeechResponse`
        :returns: List of ``StreamingSpeechResponse`` objects.
        """
        return self._responses

    @property
    def is_finished(self):
        """Helper property to determin if all resuls are final.

        :rtype: bool
        :returns: True of all captured results are final.
        """
        finished = []
        for response in self.responses.values():
            for result in response.results:
                finished.append(result.is_final)
        return all(finished)

    def get_full_text(self):
        """Parse together all transcript results to form complete text.

        :rtype: str
        :returns: Complete transcription.
        """
        text = None
        if self.is_finished:
            text = ''
            for response in self.responses.values():
                for result in response.results:
                    text += result.alternatives[0].transcript
        return text
