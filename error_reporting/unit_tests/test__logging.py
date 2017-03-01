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

import unittest

import mock


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class Test_ErrorReportingLoggingAPI(unittest.TestCase):

    PROJECT = 'PROJECT'

    def _make_one(self, project, credentials):
        from google.cloud.error_reporting._logging import (
            _ErrorReportingLoggingAPI)

        return _ErrorReportingLoggingAPI(project, credentials)

    def test_constructor(self):
        credentials = _make_credentials()
        logging_api = self._make_one(self.PROJECT, credentials)

        self.assertEqual(logging_api.logging_client._connection.credentials,
                         credentials)
        self.assertEqual(logging_api.logging_client.project, self.PROJECT)

    @mock.patch('google.cloud.logging.client.Client')
    def test_report_error_event(self, mocked_cls):
        credentials = _make_credentials()
        logging_api = self._make_one(self.PROJECT, credentials)
        mocked_cls.assert_called_once_with(self.PROJECT, credentials, None)
        self.assertIs(logging_api.logging_client, mocked_cls.return_value)

        logger = mock.Mock(spec=['log_struct'])
        logging_api.logging_client.logger.return_value = logger

        # Actually make the API call.
        error_report = {
            'message': 'The cabs are here.',
        }
        logging_api.report_error_event(error_report)

        # Check the mocks.
        logger.log_struct.assert_called_once_with(error_report)
