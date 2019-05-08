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
    @staticmethod
    def _call_fut(client):
        from google.cloud.error_reporting._gapic import make_report_error_api

        return make_report_error_api(client)

    def test_make_report_error_api(self):
        client = mock.Mock(spec=["project", "_credentials", "_client_info"])

        # Call the function being tested.
        patch = mock.patch(
            "google.cloud.errorreporting_v1beta1."
            "gapic.report_errors_service_client.ReportErrorsServiceClient"
        )

        with patch as patched:
            report_error_client = self._call_fut(client)

        # Assert that the final error client has the project in
        # the expected location.
        self.assertIs(report_error_client._project, client.project)
        self.assertIs(report_error_client._gapic_api, patched.return_value)
        patched.assert_called_once_with(
            credentials=client._credentials, client_info=client._client_info
        )


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
