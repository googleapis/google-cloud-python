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

from google.cloud._helpers import _rfc3339_to_datetime
from google.cloud import operation


class Operation(operation.Operation):
    """Representation of a Google API Long-Running Operation.

    :type client: :class:`~google.cloud.speech.client.Client`
    :param client: Instance of speech client.

    :type name: int
    :param name: ID assigned to an operation.

    :type complete: bool
    :param complete: True if operation is complete, else False.

    :type last_updated: datetime
    :param last_updated: The last time the operation was updated.

    :type progress_percent: int
    :param progress_percent: Percentage of operation that has been completed.

    :type results: dict
    :param results: Dictionary with transcript and score of operation.

    :type start_time: datetime
    :param start_time: Datetime when operation was started.
    """
    def __init__(self, client, name, complete=False, last_updated=None,
                 progress_percent=0, results=None, start_time=None):
        self.client = client
        self.name = name
        self._complete = complete
        self._last_updated = last_updated
        self._progress_percent = progress_percent
        self._results = results
        self._start_time = start_time

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
    def last_updated(self):
        """Operation last updated time.

        :rtype: datetime
        :returns: RFC3339 last updated time of the operation.
        """
        return self._last_updated

    @property
    def progress_percent(self):
        """Progress percentage of operation.

        :rtype: int
        :returns: Percentage of operation completed. [0-100]
        """
        return self._progress_percent

    @property
    def results(self):
        """Results dictionary with transcript information.

        :rtype: dict
        :returns: Dictionary with transcript and confidence score.
        """
        return self._results

    @property
    def start_time(self):
        """Operation start time.

        :rtype: datetime
        :returns: RFC3339 start time of the operation.
        """
        return self._start_time

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
                results.append(Transcript(result))
        if metadata:
            self._last_updated = _rfc3339_to_datetime(
                metadata['lastUpdateTime'])
            self._start_time = _rfc3339_to_datetime(metadata['startTime'])
            self._progress_percent = metadata.get('progressPercent', 0)

        self._results = results
        self._complete = response.get('done', False)


class Transcript(object):
    """Representation of Speech Transcripts

    :type result: dict
    :param result: Dictionary of transcript and confidence of recognition.
    """
    def __init__(self, result):
        self._transcript = result.get('transcript')
        self._confidence = result.get('confidence')

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
