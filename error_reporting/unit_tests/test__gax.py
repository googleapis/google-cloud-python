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


class Test_make_report_error_api(unittest.TestCase):

    def test_make_report_error_api(self):
        from google.cloud.gapic.errorreporting.v1beta1 import (
            report_errors_service_client)

        from grpc._channel import Channel

        from google.cloud.error_reporting import __version__
        from google.cloud.error_reporting._gax import make_report_error_api

        client = mock.Mock(
            _credentials=mock.sentinel.credentials,
            project='prahj-ekt',
            spec=['project', '_credentials'],
        )

        # Mock out the constructor for the GAPIC client.
        ServiceClient = report_errors_service_client.ReportErrorsServiceClient
        with mock.patch.object(ServiceClient, '__init__') as resc:
            resc.return_value = None

            # Call the function being tested.
            report_error_client = make_report_error_api(client)

            # Assert that the arguments to the GAPIC constructor appear
            # to be correct.
            resc.assert_called_once()
            _, _, kwargs = resc.mock_calls[0]
            self.assertIsInstance(kwargs['channel'], Channel)
            self.assertEqual(kwargs['lib_name'], 'gccl')
            self.assertEqual(kwargs['lib_version'], __version__)

        # Assert that the final error client has the project in
        # the expected location.
        self.assertIs(report_error_client._project, client.project)


class Test_ErrorReportingGaxApi(unittest.TestCase):

    PROJECT = 'PROJECT'

    def _call_fut(self, gax_api, project):
        from google.cloud.error_reporting._gax import _ErrorReportingGaxApi

        return _ErrorReportingGaxApi(gax_api, project)

    def test_constructor(self):
        gax_api = mock.Mock()
        gax_client_wrapper = self._call_fut(gax_api, self.PROJECT)

        self.assertEqual(gax_client_wrapper._project, self.PROJECT)
        self.assertEqual(gax_client_wrapper._gax_api, gax_api)

    @mock.patch("google.cloud.error_reporting._gax.ParseDict")
    def test_report_error_event(self, _):
        gax_api = mock.Mock()
        gax_client_wrapper = self._call_fut(gax_api, self.PROJECT)

        mock_error_report = mock.Mock()
        gax_client_wrapper.report_error_event(mock_error_report)
        self.assertTrue(gax_api.report_error_event.called_with,
                        mock_error_report)
