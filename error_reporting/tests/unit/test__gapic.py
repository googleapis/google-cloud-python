# Copyright 2017 Google LLC
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
        from google.cloud.errorreporting_v1beta1.gapic import (
            report_errors_service_client,
        )

        from google.cloud.error_reporting._gapic import make_report_error_api

        client = mock.Mock(
            _credentials=mock.sentinel.credentials,
            project="prahj-ekt",
            spec=["project", "_credentials"],
        )

        # Mock out the constructor for the GAPIC client.
        ServiceClient = report_errors_service_client.ReportErrorsServiceClient
        with mock.patch.object(ServiceClient, "__init__") as resc:
            resc.return_value = None

            # Call the function being tested.
            report_error_client = make_report_error_api(client)

            # Assert that the arguments to the GAPIC constructor appear
            # to be correct.
            resc.assert_called_once()
            _, _, kwargs = resc.mock_calls[0]
            self.assertEqual(kwargs["credentials"], mock.sentinel.credentials)
            self.assertIsNotNone(kwargs["client_info"])

        # Assert that the final error client has the project in
        # the expected location.
        self.assertIs(report_error_client._project, client.project)


class Test_ErrorReportingGapicApi(unittest.TestCase):

    PROJECT = "PROJECT"

    def _make_one(self, gapic_api, project):
        from google.cloud.error_reporting._gapic import _ErrorReportingGapicApi

        return _ErrorReportingGapicApi(gapic_api, project)

    def test_constructor(self):
        gapic_api = mock.Mock(spec=[])
        gapic_client_wrapper = self._make_one(gapic_api, self.PROJECT)

        self.assertEqual(gapic_client_wrapper._project, self.PROJECT)
        self.assertEqual(gapic_client_wrapper._gapic_api, gapic_api)

    def test_report_error_event(self):
        from google.cloud.errorreporting_v1beta1.proto import report_errors_service_pb2

        gapic_api = mock.Mock(spec=["project_path", "report_error_event"])
        gapic_client_wrapper = self._make_one(gapic_api, self.PROJECT)

        error_report = {"message": "The cabs are here."}
        gapic_client_wrapper.report_error_event(error_report)

        gapic_api.project_path.assert_called_once_with(self.PROJECT)
        project_name = gapic_api.project_path.return_value
        error_pb = report_errors_service_pb2.ReportedErrorEvent(
            message=error_report["message"]
        )
        gapic_api.report_error_event.assert_called_once_with(project_name, error_pb)
