# Copyright 2016 Google Inc. All Rights Reserved.
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


import unittest2


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.error_reporting.client import Client
        return Client

    def _getHttpContext(self):
        from gcloud.error_reporting.client import HTTPContext
        return HTTPContext

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeHTTP(self, *args, **kw):
        return self._getHttpContext()(*args, **kw)

    PROJECT = 'PROJECT'
    SERVICE = 'SERVICE'
    VERSION = 'myversion'

    def test_ctor_default(self):
        CREDENTIALS = _Credentials()
        target = self._makeOne(project=self.PROJECT,
                               credentials=CREDENTIALS)
        self.assertEquals(target.service, target.DEFAULT_SERVICE)
        self.assertEquals(target.version, None)

    def test_ctor_params(self):
        CREDENTIALS = _Credentials()
        target = self._makeOne(project=self.PROJECT,
                               credentials=CREDENTIALS,
                               service=self.SERVICE,
                               version=self.VERSION)
        self.assertEquals(target.service, self.SERVICE)
        self.assertEquals(target.version, self.VERSION)

    def test_report_exception(self):
        CREDENTIALS = _Credentials()
        target = self._makeOne(project=self.PROJECT,
                               credentials=CREDENTIALS)

        logger = _Logger()
        target.logging_client.logger = lambda _: logger

        try:
            raise NameError
        except NameError:
            target.report_exception()

        payload = logger.log_struct_called_with
        self.assertEquals(payload['serviceContext'], {
            'service': target.DEFAULT_SERVICE,
        })
        self.assertIn('test_report', payload['message'])
        self.assertIn('test_client.py', payload['message'])

    def test_report_exception_with_service_version_in_constructor(self):
        CREDENTIALS = _Credentials()
        SERVICE = "notdefault"
        VERSION = "notdefaultversion"
        target = self._makeOne(project=self.PROJECT,
                               credentials=CREDENTIALS,
                               service=SERVICE,
                               version=VERSION)

        logger = _Logger()
        target.logging_client.logger = lambda _: logger

        http_context = self._makeHTTP(method="GET", response_status_code=500)
        USER = "user@gmail.com"

        try:
            raise NameError
        except NameError:
            target.report_exception(http_context=http_context, user=USER)

        payload = logger.log_struct_called_with
        self.assertEquals(payload['serviceContext'], {
            'service': SERVICE,
            'version': VERSION
        })
        self.assertIn(
            'test_report_exception_with_service_version_in_constructor',
            payload['message'])
        self.assertIn('test_client.py', payload['message'])
        self.assertEquals(
            payload['context']['httpContext']['responseStatusCode'], 500)
        self.assertEquals(
            payload['context']['httpContext']['method'], 'GET')
        self.assertEquals(payload['context']['user'], USER)

    def test_report(self):
        CREDENTIALS = _Credentials()
        target = self._makeOne(project=self.PROJECT,
                               credentials=CREDENTIALS)

        logger = _Logger()
        target.logging_client.logger = lambda _: logger

        MESSAGE = 'this is an error'
        target.report(MESSAGE)

        payload = logger.log_struct_called_with
        self.assertEquals(payload['message'], MESSAGE)
        report_location = payload['context']['reportLocation']
        self.assertIn('test_client.py', report_location['filePath'])
        self.assertEqual(report_location['functionName'], 'test_report')
        self.assertGreater(report_location['lineNumber'], 100)
        self.assertLess(report_location['lineNumber'], 150)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Logger(object):

    def log_struct(self, payload,  # pylint: disable=unused-argument
                   client=None,  # pylint: disable=unused-argument
                   labels=None,   # pylint: disable=unused-argument
                   insert_id=None,   # pylint: disable=unused-argument
                   severity=None,   # pylint: disable=unused-argument
                   http_request=None):  # pylint: disable=unused-argument
        self.log_struct_called_with = payload
