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


class Operation(object):
    """Representation of a Google API Long-Running Operation.

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

        :type response: dict
        :param response: Dictionary response from Google Speech Operations API.

        :rtype: :class:`Operation`
        :returns: Instance of `~google.cloud.speech.operations.Operation`.
        """
        last_updated = None
        progress_percent = 0
        results = None
        start_time = None

        name = response['name']
        metadata = response.get('metadata', None)

        if metadata:
            last_updated = _rfc3339_to_datetime(metadata.get('lastUpdateTime'))
            start_time = _rfc3339_to_datetime(metadata.get('startTime'))
            progress_percent = metadata.get('progressPercent')

        if response.get('response'):
            results = response.get('response').get('results')
        complete = response.get('done', False)

        return cls(client, name, complete, last_updated, progress_percent,
                   results, start_time)

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
        metadata = response['metadata']
        results = response.get('response', {}).get('results')
        self._last_updated = _rfc3339_to_datetime(metadata['lastUpdateTime'])
        self._results = results
        self._start_time = _rfc3339_to_datetime(metadata['startTime'])
        self._complete = response.get('done', False)
        self._progress_percent = metadata.get('progressPercent', 0)
