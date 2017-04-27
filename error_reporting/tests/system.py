# Copyright 2017 Google Inc.
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

import functools
import unittest

from google.cloud import error_reporting
from google.cloud.gapic.errorreporting.v1beta1 import (
    error_stats_service_client)
from google.cloud.proto.devtools.clouderrorreporting.v1beta1 import (
    error_stats_service_pb2)
from google.protobuf.duration_pb2 import Duration

from test_utils.retry import RetryResult


class _ErrorStatsGaxApi(object):
    """Helper mapping Error Reporting-related APIs

    This class provides a small wrapper around making calls to the GAX
    API. It's used by the system tests to find the appropriate error group
    to verify the error was successfully reported.

    :type project: str
    :param project: Google Cloud Project ID
    """
    def __init__(self, project):
        self._project = project
        self._gax_api = error_stats_service_client.ErrorStatsServiceClient()

    def list_groups(self):
        """Helper to list the groups that have had errors in the last hour."""
        project_name = self._gax_api.project_path(self._project)
        time_range = error_stats_service_pb2.QueryTimeRange()
        time_range.period = (
            error_stats_service_pb2.QueryTimeRange.PERIOD_1_HOUR
        )

        duration = Duration()
        duration.seconds = 60 * 60

        return self._gax_api.list_group_stats(
            project_name, time_range, timed_count_duration=duration)


def _is_incremented(initial, new):
    """Helper to retry until new error is counted."""
    return new == initial + 1


class TestErrorReporting(unittest.TestCase):

    def setUp(self):
        self._client = error_reporting.Client()
        self._error_name = 'Stackdriver Error Reporting System Test'

    def _simulate_exception(self):
        """Simulates an exception to verify it was reported."""
        try:
            raise RuntimeError(self._error_name)
        except RuntimeError:
            self._client.report_exception()

    def _get_error_count(self):
        """Counts the number of errors in the group of the test exception."""
        error_stats_api = _ErrorStatsGaxApi(self._client.project)
        groups = error_stats_api.list_groups()
        for group in groups:
            if self._error_name in group.representative.message:
                return group.count

    def test_report_exception(self):
        """Verifies the exception reported increases the group count by one."""
        # If test has never run, group won't exist until we report first
        # exception, so first simulate it just to create the group
        self._simulate_exception()

        initial_count = self._get_error_count()
        self._simulate_exception()

        is_incremented = functools.partial(_is_incremented, initial_count)
        retry_get_count = RetryResult(is_incremented)(self._get_error_count)
        new_count = retry_get_count()

        self.assertEqual(new_count, initial_count + 1)
