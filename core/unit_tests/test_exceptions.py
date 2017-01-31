# Copyright 2014 Google Inc.
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


class Test_GoogleCloudError(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.exceptions import GoogleCloudError

        return GoogleCloudError

    def _make_one(self, message, errors=()):
        return self._get_target_class()(message, errors=errors)

    def test_ctor_defaults(self):
        e = self._make_one('Testing')
        e.code = 600
        self.assertEqual(str(e), '600 Testing')
        self.assertEqual(e.message, 'Testing')
        self.assertEqual(list(e.errors), [])

    def test_ctor_explicit(self):
        ERROR = {
            'domain': 'global',
            'location': 'test',
            'locationType': 'testing',
            'message': 'Testing',
            'reason': 'test',
        }
        e = self._make_one('Testing', [ERROR])
        e.code = 600
        self.assertEqual(str(e), '600 Testing')
        self.assertEqual(e.message, 'Testing')
        self.assertEqual(list(e.errors), [ERROR])


class Test_make_exception(unittest.TestCase):

    def _call_fut(self, response, content, error_info=None, use_json=True):
        from google.cloud.exceptions import make_exception

        return make_exception(response, content, error_info=error_info,
                              use_json=use_json)

    def test_hit_w_content_as_str(self):
        from google.cloud.exceptions import NotFound

        response = _Response(404)
        content = b'{"error": {"message": "Not Found"}}'
        exception = self._call_fut(response, content)
        self.assertIsInstance(exception, NotFound)
        self.assertEqual(exception.message, 'Not Found')
        self.assertEqual(list(exception.errors), [])

    def test_hit_w_content_as_unicode(self):
        import six
        from google.cloud._helpers import _to_bytes
        from google.cloud.exceptions import NotFound

        error_message = u'That\u2019s not found.'
        expected = u'404 %s' % (error_message,)

        response = _Response(404)
        content = u'{"error": {"message": "%s" }}' % (error_message,)

        exception = self._call_fut(response, content)
        if six.PY2:
            self.assertEqual(str(exception),
                             _to_bytes(expected, encoding='utf-8'))
        else:  # pragma: NO COVER
            self.assertEqual(str(exception), expected)

        self.assertIsInstance(exception, NotFound)
        self.assertEqual(exception.message, error_message)
        self.assertEqual(list(exception.errors), [])

    def test_hit_w_content_as_unicode_as_py3(self):
        import six
        from google.cloud._testing import _Monkey
        from google.cloud.exceptions import NotFound

        error_message = u'That is not found.'
        expected = u'404 %s' % (error_message,)

        with _Monkey(six, PY2=False):
            response = _Response(404)
            content = u'{"error": {"message": "%s" }}' % (error_message,)
            exception = self._call_fut(response, content)

            self.assertIsInstance(exception, NotFound)
            self.assertEqual(exception.message, error_message)
            self.assertEqual(list(exception.errors), [])
            self.assertEqual(str(exception), expected)

    def test_miss_w_content_as_dict(self):
        from google.cloud.exceptions import GoogleCloudError

        ERROR = {
            'domain': 'global',
            'location': 'test',
            'locationType': 'testing',
            'message': 'Testing',
            'reason': 'test',
        }
        response = _Response(600)
        content = {"error": {"message": "Unknown Error", "errors": [ERROR]}}
        exception = self._call_fut(response, content)
        self.assertIsInstance(exception, GoogleCloudError)
        self.assertEqual(exception.message, 'Unknown Error')
        self.assertEqual(list(exception.errors), [ERROR])

    def test_html_when_json_expected(self):
        from google.cloud.exceptions import NotFound

        response = _Response(NotFound.code)
        content = '<html><body>404 Not Found</body></html>'
        exception = self._call_fut(response, content, use_json=True)
        self.assertIsInstance(exception, NotFound)
        self.assertEqual(exception.message, content)
        self.assertEqual(list(exception.errors), [])

    def test_without_use_json(self):
        from google.cloud.exceptions import TooManyRequests

        content = u'error-content'
        response = _Response(TooManyRequests.code)
        exception = self._call_fut(response, content, use_json=False)

        self.assertIsInstance(exception, TooManyRequests)
        self.assertEqual(exception.message, content)
        self.assertEqual(list(exception.errors), [])


class _Response(object):
    def __init__(self, status):
        self.status = status
