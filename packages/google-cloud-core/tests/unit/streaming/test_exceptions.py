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


class Test_HttpError(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.streaming.exceptions import HttpError

        return HttpError

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        RESPONSE = {'status': '404'}
        CONTENT = b'CONTENT'
        URL = 'http://www.example.com'
        exception = self._make_one(RESPONSE, CONTENT, URL)
        self.assertEqual(exception.response, RESPONSE)
        self.assertEqual(exception.content, CONTENT)
        self.assertEqual(exception.url, URL)
        self.assertEqual(exception.status_code, 404)
        self.assertEqual(
            str(exception),
            "HttpError accessing <http://www.example.com>: "
            "response: <{'status': '404'}>, content <CONTENT>")

    def test_from_response(self):
        RESPONSE = {'status': '404'}
        CONTENT = b'CONTENT'
        URL = 'http://www.example.com'

        class _Response(object):
            info = RESPONSE
            content = CONTENT
            request_url = URL

        klass = self._get_target_class()
        exception = klass.from_response(_Response())
        self.assertIsInstance(exception, klass)
        self.assertEqual(exception.response, RESPONSE)
        self.assertEqual(exception.content, CONTENT)
        self.assertEqual(exception.url, URL)


class Test_RetryAfterError(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.streaming.exceptions import RetryAfterError

        return RetryAfterError

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        RESPONSE = {'status': '404'}
        CONTENT = b'CONTENT'
        URL = 'http://www.example.com'
        RETRY_AFTER = 60
        exception = self._make_one(RESPONSE, CONTENT, URL, RETRY_AFTER)
        self.assertEqual(exception.response, RESPONSE)
        self.assertEqual(exception.content, CONTENT)
        self.assertEqual(exception.url, URL)
        self.assertEqual(exception.retry_after, RETRY_AFTER)
        self.assertEqual(
            str(exception),
            "HttpError accessing <http://www.example.com>: "
            "response: <{'status': '404'}>, content <CONTENT>")

    def test_from_response(self):
        RESPONSE = {'status': '404'}
        CONTENT = b'CONTENT'
        URL = 'http://www.example.com'
        RETRY_AFTER = 60

        class _Response(object):
            info = RESPONSE
            content = CONTENT
            request_url = URL
            retry_after = RETRY_AFTER

        klass = self._get_target_class()
        exception = klass.from_response(_Response())
        self.assertIsInstance(exception, klass)
        self.assertEqual(exception.response, RESPONSE)
        self.assertEqual(exception.content, CONTENT)
        self.assertEqual(exception.url, URL)
        self.assertEqual(exception.retry_after, RETRY_AFTER)
