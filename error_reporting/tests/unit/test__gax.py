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

    def _make_one(self, gax_api, project):
        from google.cloud.error_reporting._gax import _ErrorReportingGaxApi

        return _ErrorReportingGaxApi(gax_api, project)

    def test_constructor(self):
        gax_api = mock.Mock(spec=[])
        gax_client_wrapper = self._make_one(gax_api, self.PROJECT)

        self.assertEqual(gax_client_wrapper._project, self.PROJECT)
        self.assertEqual(gax_client_wrapper._gax_api, gax_api)

    def test_report_error_event(self):
        from google.cloud.proto.devtools.clouderrorreporting.v1beta1 import (
            report_errors_service_pb2)

        gax_api = mock.Mock(spec=['project_path', 'report_error_event'])
        gax_client_wrapper = self._make_one(gax_api, self.PROJECT)

        error_report = {
            'message': 'The cabs are here.',
        }
        gax_client_wrapper.report_error_event(error_report)

        gax_api.project_path.assert_called_once_with(self.PROJECT)
        project_name = gax_api.project_path.return_value
        error_pb = report_errors_service_pb2.ReportedErrorEvent(
            message=error_report['message'],
        )
        gax_api.report_error_event.assert_called_once_with(
            project_name, error_pb)
