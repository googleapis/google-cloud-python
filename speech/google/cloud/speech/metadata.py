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

"""Metadata representation from Google Speech API"""

from google.cloud._helpers import _rfc3339_to_datetime


class Metadata(object):
    """Representation of metadata from a Google Speech API Operation.

    :type last_update: datetime
    :param last_update: When the Speech operation was last updated.

    :type start_time: datetime
    :param start_time: When the Speech operation was started.

    :type progress_percent: int
    :param progress_percent: Percentage of operation that has been completed.
    """
    def __init__(self, last_update, start_time, progress_percent):
        self._last_update = last_update
        self._start_time = start_time
        self._progress_percent = progress_percent

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct representation of operation metadata.

        :type response: dict
        :param response: Dictionary containing operation metadata.

        :rtype: :class:`~google.cloud.speech.metadata.Metadata`
        :returns: Instance of operation Metadata.
        """
        last_update = _rfc3339_to_datetime(response['lastUpdateTime'])
        start_time = _rfc3339_to_datetime(response['startTime'])
        progress_percent = response['progressPercent']

        return cls(last_update, start_time, progress_percent)

    @property
    def last_update(self):
        """Last time operation was updated.

        :rtype: datetime
        :returns: Datetime when operation was last updated.
        """
        return self._last_update

    @property
    def start_time(self):
        """Start time of operation.

        :rtype: datetime
        :returns: Datetime when operation was started.
        """
        return self._start_time

    @property
    def progress_percent(self):
        """Progress percentage completed of operation.

        :rtype: int
        :returns: Percentage of operation completed.
        """
        return self._progress_percent
