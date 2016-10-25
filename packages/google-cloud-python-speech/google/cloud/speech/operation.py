# Copyright 2016 Google Inc. All rights reserved.
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

"""Long running operation representation for Google Speech API"""

from google.cloud.speech.metadata import Metadata
from google.cloud.speech.transcript import Transcript
from google.cloud import operation


class Operation(operation.Operation):
    """Representation of a Google API Long-Running Operation.

    :type client: :class:`~google.cloud.speech.client.Client`
    :param client: Instance of speech client.

    :type name: int
    :param name: ID assigned to an operation.

    :type complete: bool
    :param complete: True if operation is complete, else False.

    :type metadata: :class:`~google.cloud.speech.metadata.Metadata`
    :param metadata: Instance of ``Metadata`` with operation information.

    :type results: dict
    :param results: Dictionary with transcript and score of operation.
    """
    def __init__(self, client, name, complete=False, metadata=None,
                 results=None):
        self.client = client
        self.name = name
        self._complete = complete
        self._metadata = metadata
        self._results = results

    @classmethod
    def from_api_repr(cls, client, response):
        """Factory:  construct an instance from Google Speech API.

        :type client: :class:`~google.cloud.speech.client.Client`
        :param client: Instance of speech client.

        :type response: dict
        :param response: Dictionary response from Google Speech Operations API.

        :rtype: :class:`Operation`
        :returns: Instance of `~google.cloud.speech.operations.Operation`.
        """
        name = response['name']
        complete = response.get('done', False)

        operation_instance = cls(client, name, complete)
        operation_instance._update(response)
        return operation_instance

    @property
    def complete(self):
        """Completion state of the `Operation`.

        :rtype: bool
        :returns: True if already completed, else false.
        """
        return self._complete

    @property
    def metadata(self):
        """Metadata of operation.

        :rtype: :class:`~google.cloud.speech.metadata.Metadata`
        :returns: Instance of ``Metadata``.
        """
        return self._metadata

    @property
    def results(self):
        """Results dictionary with transcript information.

        :rtype: dict
        :returns: Dictionary with transcript and confidence score.
        """
        return self._results

    def poll(self):
        """Check if the operation has finished.

        :rtype: bool
        :returns: A boolean indicating if the current operation has completed.
        :raises: :class:`ValueError <exceptions.ValueError>` if the operation
                 has already completed.
        """
        if self.complete:
            raise ValueError('The operation has completed.')

        path = 'operations/%s' % (self.name,)
        api_response = self.client.connection.api_request(method='GET',
                                                          path=path)
        self._update(api_response)
        return self.complete

    def _update(self, response):
        """Update Operation instance with latest data from Speech API.

        .. _speech_operations: https://cloud.google.com/speech/reference/\
                               rest/v1beta1/operations

        :type response: dict
        :param response: Response from Speech API Operations endpoint.
                         See: `speech_operations`_.
        """
        metadata = response.get('metadata', None)
        raw_results = response.get('response', {}).get('results', None)
        results = []
        if raw_results:
            for result in raw_results[0]['alternatives']:
                results.append(Transcript.from_api_repr(result))
        if metadata:
            self._metadata = Metadata.from_api_repr(metadata)

        self._results = results
        self._complete = response.get('done', False)
