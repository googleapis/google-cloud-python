# Copyright 2014 Google Inc. All rights reserved.
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


class Test_GCloudError(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.exceptions import GCloudError
        return GCloudError

    def _makeOne(self, *args):
        return self._getTargetClass()(*args)

    def test_ctor_defaults(self):
        e = self._makeOne('Testing')
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
        e = self._makeOne('Testing', [ERROR])
        e.code = 600
        self.assertEqual(str(e), '600 Testing')
        self.assertEqual(e.message, 'Testing')
        self.assertEqual(list(e.errors), [ERROR])


class Test_make_exception(unittest2.TestCase):

    def _callFUT(self, response, content):
        from gcloud.exceptions import make_exception
        return make_exception(response, content)

    def test_hit_w_content_as_str(self):
        from gcloud.exceptions import NotFound
        response = _Response(404)
        content = b'{"error": {"message": "Not Found"}}'
        exception = self._callFUT(response, content)
        self.assertTrue(isinstance(exception, NotFound))
        self.assertEqual(exception.message, 'Not Found')
        self.assertEqual(list(exception.errors), [])

    def test_miss_w_content_as_dict(self):
        from gcloud.exceptions import GCloudError
        ERROR = {
            'domain': 'global',
            'location': 'test',
            'locationType': 'testing',
            'message': 'Testing',
            'reason': 'test',
            }
        response = _Response(600)
        content = {"error": {"message": "Unknown Error", "errors": [ERROR]}}
        exception = self._callFUT(response, content)
        self.assertTrue(isinstance(exception, GCloudError))
        self.assertEqual(exception.message, 'Unknown Error')
        self.assertEqual(list(exception.errors), [ERROR])


class _Response(object):
    def __init__(self, status):
        self.status = status
