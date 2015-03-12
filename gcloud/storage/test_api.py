# Copyright 2015 Google Inc. All rights reserved.
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


class Test_lookup_bucket(unittest2.TestCase):

    def _callFUT(self, bucket_name, connection=None):
        from gcloud.storage.api import lookup_bucket
        return lookup_bucket(bucket_name, connection=connection)

    def test_lookup_bucket_miss(self):
        from gcloud.storage.connection import Connection
        PROJECT = 'project'
        NONESUCH = 'nonesuch'
        conn = Connection(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'storage',
            conn.API_VERSION,
            'b',
            'nonesuch?project=%s' % PROJECT,
        ])
        http = conn._http = Http(
            {'status': '404', 'content-type': 'application/json'},
            '{}',
        )
        bucket = self._callFUT(NONESUCH, connection=conn)
        self.assertEqual(bucket, None)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def _lookup_bucket_hit_helper(self, use_default=False):
        from gcloud.storage._testing import _monkey_defaults
        from gcloud.storage.bucket import Bucket
        from gcloud.storage.connection import Connection
        PROJECT = 'project'
        BLOB_NAME = 'blob-name'
        conn = Connection(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'storage',
            conn.API_VERSION,
            'b',
            '%s?project=%s' % (BLOB_NAME, PROJECT),
        ])
        http = conn._http = Http(
            {'status': '200', 'content-type': 'application/json'},
            '{"name": "%s"}' % BLOB_NAME,
        )

        if use_default:
            with _monkey_defaults(connection=conn):
                bucket = self._callFUT(BLOB_NAME)
        else:
            bucket = self._callFUT(BLOB_NAME, connection=conn)

        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is conn)
        self.assertEqual(bucket.name, BLOB_NAME)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_lookup_bucket_hit(self):
        self._lookup_bucket_hit_helper(use_default=False)

    def test_lookup_bucket_use_default(self):
        self._lookup_bucket_hit_helper(use_default=True)


class Test_get_all_buckets(unittest2.TestCase):

    def _callFUT(self, connection=None):
        from gcloud.storage.api import get_all_buckets
        return get_all_buckets(connection=connection)

    def test_empty(self):
        from gcloud.storage.connection import Connection
        PROJECT = 'project'
        conn = Connection(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'storage',
            conn.API_VERSION,
            'b?project=%s' % PROJECT,
        ])
        http = conn._http = Http(
            {'status': '200', 'content-type': 'application/json'},
            '{}',
        )
        buckets = list(self._callFUT(conn))
        self.assertEqual(len(buckets), 0)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def _get_all_buckets_non_empty_helper(self, use_default=False):
        from gcloud.storage._testing import _monkey_defaults
        from gcloud.storage.connection import Connection
        PROJECT = 'project'
        BUCKET_NAME = 'bucket-name'
        conn = Connection(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'storage',
            conn.API_VERSION,
            'b?project=%s' % PROJECT,
        ])
        http = conn._http = Http(
            {'status': '200', 'content-type': 'application/json'},
            '{"items": [{"name": "%s"}]}' % BUCKET_NAME,
        )

        if use_default:
            with _monkey_defaults(connection=conn):
                buckets = list(self._callFUT())
        else:
            buckets = list(self._callFUT(conn))

        self.assertEqual(len(buckets), 1)
        self.assertEqual(buckets[0].name, BUCKET_NAME)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_non_empty(self):
        self._get_all_buckets_non_empty_helper(use_default=False)

    def test_non_use_default(self):
        self._get_all_buckets_non_empty_helper(use_default=True)


class Test__BucketIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.api import _BucketIterator
        return _BucketIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = object()
        iterator = self._makeOne(connection)
        self.assertTrue(iterator.connection is connection)
        self.assertEqual(iterator.path, '/b')
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)

    def test_get_items_from_response_empty(self):
        connection = object()
        iterator = self._makeOne(connection)
        self.assertEqual(list(iterator.get_items_from_response({})), [])

    def test_get_items_from_response_non_empty(self):
        from gcloud.storage.bucket import Bucket
        BLOB_NAME = 'blob-name'
        response = {'items': [{'name': BLOB_NAME}]}
        connection = object()
        iterator = self._makeOne(connection)
        buckets = list(iterator.get_items_from_response(response))
        self.assertEqual(len(buckets), 1)
        bucket = buckets[0]
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is connection)
        self.assertEqual(bucket.name, BLOB_NAME)


class Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content
