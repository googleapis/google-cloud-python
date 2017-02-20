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


import unittest

import mock


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.error_reporting.client import Client

        return Client

    def _getHttpContext(self):
        from google.cloud.error_reporting.client import HTTPContext

        return HTTPContext

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _makeHTTP(self, *args, **kw):
        return self._getHttpContext()(*args, **kw)

    PROJECT = 'PROJECT'
    SERVICE = 'SERVICE'
    VERSION = 'myversion'

    @mock.patch(
        'google.cloud.error_reporting.client._determine_default_project')
    def test_ctor_default(self, _):
        CREDENTIALS = _make_credentials()
        target = self._make_one(credentials=CREDENTIALS)
        self.assertEqual(target.service, target.DEFAULT_SERVICE)
        self.assertEqual(target.version, None)

    def test_ctor_params(self):
        CREDENTIALS = _make_credentials()
        target = self._make_one(project=self.PROJECT,
                                credentials=CREDENTIALS,
                                service=self.SERVICE,
                                version=self.VERSION)
        self.assertEqual(target.service, self.SERVICE)
        self.assertEqual(target.version, self.VERSION)

    def test_report_exception_with_gax(self):
        CREDENTIALS = _make_credentials()
        target = self._make_one(project=self.PROJECT,
                                credentials=CREDENTIALS)

        patch = mock.patch(
            'google.cloud.error_reporting.client.make_report_error_api')
        with patch as make_api:
            try:
                raise NameError
            except NameError:
                target.report_exception()
            payload = make_api.return_value.report_error_event.call_args[0][0]
        self.assertEqual(payload['serviceContext'], {
            'service': target.DEFAULT_SERVICE,
        })
        self.assertIn('test_report', payload['message'])
        self.assertIn('test_client.py', payload['message'])

    def test_report_exception_wo_gax(self):
        CREDENTIALS = _make_credentials()
        target = self._make_one(project=self.PROJECT,
                                credentials=CREDENTIALS,
                                use_gax=False)
        patch = mock.patch(
            'google.cloud.error_reporting.client._ErrorReportingLoggingAPI'
        )
        with patch as _error_api:
            try:
                raise NameError
            except NameError:
                target.report_exception()
            mock_report = _error_api.return_value.report_error_event
            payload = mock_report.call_args[0][0]

        self.assertEqual(payload['serviceContext'], {
            'service': target.DEFAULT_SERVICE,
        })
        self.assertIn('test_report', payload['message'])
        self.assertIn('test_client.py', payload['message'])
        self.assertIsNotNone(target.report_errors_api)

    @mock.patch('google.cloud.error_reporting.client.make_report_error_api')
    def test_report_exception_with_service_version_in_constructor(
            self, make_client):
        CREDENTIALS = _make_credentials()
        SERVICE = "notdefault"
        VERSION = "notdefaultversion"
        target = self._make_one(project=self.PROJECT,
                                credentials=CREDENTIALS,
                                service=SERVICE,
                                version=VERSION)

        http_context = self._makeHTTP(method="GET", response_status_code=500)
        USER = "user@gmail.com"

        client = mock.Mock()
        make_client.return_value = client

        try:
            raise NameError
        except NameError:
            target.report_exception(http_context=http_context, user=USER)

        payload = client.report_error_event.call_args[0][0]
        self.assertEqual(payload['serviceContext'], {
            'service': SERVICE,
            'version': VERSION
        })
        self.assertIn(
            'test_report_exception_with_service_version_in_constructor',
            payload['message'])
        self.assertIn('test_client.py', payload['message'])
        self.assertEqual(
            payload['context']['httpContext']['responseStatusCode'], 500)
        self.assertEqual(
            payload['context']['httpContext']['method'], 'GET')
        self.assertEqual(payload['context']['user'], USER)

    @mock.patch('google.cloud.error_reporting.client.make_report_error_api')
    def test_report(self, make_client):
        CREDENTIALS = _make_credentials()
        target = self._make_one(project=self.PROJECT,
                                credentials=CREDENTIALS)

        client = mock.Mock()
        make_client.return_value = client

        MESSAGE = 'this is an error'
        target.report(MESSAGE)

        payload = client.report_error_event.call_args[0][0]

        self.assertEqual(payload['message'], MESSAGE)
        report_location = payload['context']['reportLocation']
        self.assertIn('test_client.py', report_location['filePath'])
        self.assertEqual(report_location['functionName'], 'test_report')
        self.assertGreater(report_location['lineNumber'], 100)
        self.assertLess(report_location['lineNumber'], 250)
