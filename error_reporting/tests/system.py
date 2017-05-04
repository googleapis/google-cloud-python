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

import time
import unittest

from google.cloud import error_reporting
from google.cloud.gapic.errorreporting.v1beta1 import (
    error_stats_service_client)
from google.cloud.proto.devtools.clouderrorreporting.v1beta1 import (
    error_stats_service_pb2)
from google.protobuf.duration_pb2 import Duration


ERROR_NAME = 'Stackdriver Error Reporting System Test'

def setUpModule():
    Config.CLIENT = error_reporting.Client()


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None


def _list_groups(project):
    """List Error Groups from the last 60 seconds.

    This class provides a wrapper around making calls to the GAX
    API. It's used by the system tests to find the appropriate error group
    to verify the error was successfully reported.

    :type project: str
    :param project: Google Cloud Project ID
    """
    gax_api = error_stats_service_client.ErrorStatsServiceClient(
        credentials=Config.CLIENT._credentials)
    project_name = gax_api.project_path(project)

    time_range = error_stats_service_pb2.QueryTimeRange()
    time_range.period = error_stats_service_pb2.QueryTimeRange.PERIOD_1_HOUR

    duration = Duration(seconds=60*60)

    return gax_api.list_group_stats(
        project_name, time_range, timed_count_duration=duration)


def _simulate_exception():
    """Simulates an exception to verify it was reported."""
    try:
        raise RuntimeError(ERROR_NAME)
    except RuntimeError:
        Config.CLIENT.report_exception()


class TestErrorReporting(unittest.TestCase):

    def _get_error_count(self):
        """Counts the number of errors in the group of the test exception."""
        groups = _list_groups(Config.CLIENT.project)
        for group in groups:
            if ERROR_NAME in group.representative.message:
                return group.count

    def test_report_exception(self):
        # If test has never run, group won't exist until we report first
        # exception, so first simulate it just to create the group
        _simulate_exception()
        time.sleep(2)

        initial_count = self._get_error_count()
        _simulate_exception()

        time.sleep(2)
        new_count = self._get_error_count()

        self.assertEqual(new_count, initial_count + 1)
