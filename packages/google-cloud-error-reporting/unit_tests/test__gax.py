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
        from google.cloud.error_reporting._gax import make_report_error_api

        client = mock.Mock()
        client.project = mock.Mock()
        report_error_client = make_report_error_api(client)
        self.assertEqual(report_error_client._project, client.project)


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
