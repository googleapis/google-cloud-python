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


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_connection_type(self):
        from gcloud.storage.connection import Connection

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()

        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)
        self.assertEqual(client.project, PROJECT)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertTrue(client.connection.credentials is CREDENTIALS)
        self.assertTrue(client.current_batch is None)
        self.assertEqual(list(client._batch_stack), [])

    def test__push_batch_and__pop_batch(self):
        from gcloud.storage.batch import Batch

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()

        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)
        batch1 = Batch(client)
        batch2 = Batch(client)
        client._push_batch(batch1)
        self.assertEqual(list(client._batch_stack), [batch1])
        self.assertTrue(client.current_batch is batch1)
        client._push_batch(batch2)
        self.assertTrue(client.current_batch is batch2)
        # list(_LocalStack) returns in reverse order.
        self.assertEqual(list(client._batch_stack), [batch2, batch1])
        self.assertTrue(client._pop_batch() is batch2)
        self.assertEqual(list(client._batch_stack), [batch1])
        self.assertTrue(client._pop_batch() is batch1)
        self.assertEqual(list(client._batch_stack), [])

    def test_connection_setter(self):
        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)
        client._connection = None  # Unset the value from the constructor
        client.connection = connection = object()
        self.assertTrue(client._connection is connection)

    def test_connection_setter_when_set(self):
        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)
        self.assertRaises(ValueError, setattr, client, 'connection', None)

    def test_connection_getter_no_batch(self):
        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)
        self.assertTrue(client.connection is client._connection)
        self.assertTrue(client.current_batch is None)

    def test_connection_getter_with_batch(self):
        from gcloud.storage.batch import Batch
        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)
        batch = Batch(client)
        client._push_batch(batch)
        self.assertTrue(client.connection is not client._connection)
        self.assertTrue(client.connection is batch)
        self.assertTrue(client.current_batch is batch)

    def test_bucket(self):
        from gcloud.storage.bucket import Bucket

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        BUCKET_NAME = 'BUCKET_NAME'

        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)
        bucket = client.bucket(BUCKET_NAME)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.client is client)
        self.assertEqual(bucket.name, BUCKET_NAME)

    def test_batch(self):
        from gcloud.storage.batch import Batch

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()

        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)
        batch = client.batch()
        self.assertTrue(isinstance(batch, Batch))
        self.assertTrue(batch._client is client)

    def test_get_bucket_miss(self):
        from gcloud.exceptions import NotFound

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        NONESUCH = 'nonesuch'
        URI = '/'.join([
            client.connection.API_BASE_URL,
            'storage',
            client.connection.API_VERSION,
            'b',
            'nonesuch?projection=noAcl',
        ])
        http = client.connection._http = _Http(
            {'status': '404', 'content-type': 'application/json'},
            b'{}',
        )
        self.assertRaises(NotFound, client.get_bucket, NONESUCH)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_get_bucket_hit(self):
        from gcloud.storage.bucket import Bucket

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        BLOB_NAME = 'blob-name'
        URI = '/'.join([
            client.connection.API_BASE_URL,
            'storage',
            client.connection.API_VERSION,
            'b',
            '%s?projection=noAcl' % (BLOB_NAME,),
        ])
        http = client.connection._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            '{{"name": "{0}"}}'.format(BLOB_NAME).encode('utf-8'),
        )

        bucket = client.get_bucket(BLOB_NAME)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertEqual(bucket.name, BLOB_NAME)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_lookup_bucket_miss(self):
        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        NONESUCH = 'nonesuch'
        URI = '/'.join([
            client.connection.API_BASE_URL,
            'storage',
            client.connection.API_VERSION,
            'b',
            'nonesuch?projection=noAcl',
        ])
        http = client.connection._http = _Http(
            {'status': '404', 'content-type': 'application/json'},
            b'{}',
        )
        bucket = client.lookup_bucket(NONESUCH)
        self.assertEqual(bucket, None)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_lookup_bucket_hit(self):
        from gcloud.storage.bucket import Bucket

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        BLOB_NAME = 'blob-name'
        URI = '/'.join([
            client.connection.API_BASE_URL,
            'storage',
            client.connection.API_VERSION,
            'b',
            '%s?projection=noAcl' % (BLOB_NAME,),
        ])
        http = client.connection._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            '{{"name": "{0}"}}'.format(BLOB_NAME).encode('utf-8'),
        )

        bucket = client.lookup_bucket(BLOB_NAME)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertEqual(bucket.name, BLOB_NAME)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_create_bucket_conflict(self):
        from gcloud.exceptions import Conflict

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        BLOB_NAME = 'blob-name'
        URI = '/'.join([
            client.connection.API_BASE_URL,
            'storage',
            client.connection.API_VERSION,
            'b?project=%s' % (PROJECT,),
        ])
        http = client.connection._http = _Http(
            {'status': '409', 'content-type': 'application/json'},
            '{"error": {"message": "Conflict"}}',
        )

        self.assertRaises(Conflict, client.create_bucket, BLOB_NAME)
        self.assertEqual(http._called_with['method'], 'POST')
        self.assertEqual(http._called_with['uri'], URI)

    def test_create_bucket_success(self):
        from gcloud.storage.bucket import Bucket

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        BLOB_NAME = 'blob-name'
        URI = '/'.join([
            client.connection.API_BASE_URL,
            'storage',
            client.connection.API_VERSION,
            'b?project=%s' % (PROJECT,),
        ])
        http = client.connection._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            '{{"name": "{0}"}}'.format(BLOB_NAME).encode('utf-8'),
        )

        bucket = client.create_bucket(BLOB_NAME)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertEqual(bucket.name, BLOB_NAME)
        self.assertEqual(http._called_with['method'], 'POST')
        self.assertEqual(http._called_with['uri'], URI)

    def test_list_buckets_empty(self):
        from six.moves.urllib.parse import parse_qs
        from six.moves.urllib.parse import urlparse

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        EXPECTED_QUERY = {
            'project': [PROJECT],
            'projection': ['noAcl'],
        }
        http = client.connection._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
        buckets = list(client.list_buckets())
        self.assertEqual(len(buckets), 0)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['body'], None)

        BASE_URI = '/'.join([
            client.connection.API_BASE_URL,
            'storage',
            client.connection.API_VERSION,
            'b',
        ])
        URI = http._called_with['uri']
        self.assertTrue(URI.startswith(BASE_URI))
        uri_parts = urlparse(URI)
        self.assertEqual(parse_qs(uri_parts.query), EXPECTED_QUERY)

    def test_list_buckets_non_empty(self):
        from six.moves.urllib.parse import parse_qs
        from six.moves.urllib.parse import urlencode
        from six.moves.urllib.parse import urlparse
        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        BUCKET_NAME = 'bucket-name'
        query_params = urlencode({'project': PROJECT, 'projection': 'noAcl'})
        BASE_URI = '/'.join([
            client.connection.API_BASE_URL,
            'storage',
            client.connection.API_VERSION,
        ])
        URI = '/'.join([BASE_URI, 'b?%s' % (query_params,)])
        http = client.connection._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            '{{"items": [{{"name": "{0}"}}]}}'.format(BUCKET_NAME)
            .encode('utf-8'),
        )
        buckets = list(client.list_buckets())
        self.assertEqual(len(buckets), 1)
        self.assertEqual(buckets[0].name, BUCKET_NAME)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertTrue(http._called_with['uri'].startswith(BASE_URI))
        self.assertEqual(parse_qs(urlparse(http._called_with['uri']).query),
                         parse_qs(urlparse(URI).query))

    def test_list_buckets_all_arguments(self):
        from six.moves.urllib.parse import parse_qs
        from six.moves.urllib.parse import urlparse

        PROJECT = 'foo-bar'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        MAX_RESULTS = 10
        PAGE_TOKEN = 'ABCD'
        PREFIX = 'subfolder'
        PROJECTION = 'full'
        FIELDS = 'items/id,nextPageToken'
        EXPECTED_QUERY = {
            'project': [PROJECT],
            'maxResults': [str(MAX_RESULTS)],
            'pageToken': [PAGE_TOKEN],
            'prefix': [PREFIX],
            'projection': [PROJECTION],
            'fields': [FIELDS],
        }

        http = client.connection._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            '{"items": []}',
        )
        iterator = client.list_buckets(
            max_results=MAX_RESULTS,
            page_token=PAGE_TOKEN,
            prefix=PREFIX,
            projection=PROJECTION,
            fields=FIELDS,
        )
        buckets = list(iterator)
        self.assertEqual(buckets, [])
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['body'], None)

        BASE_URI = '/'.join([
            client.connection.API_BASE_URL,
            'storage',
            client.connection.API_VERSION,
            'b'
        ])
        URI = http._called_with['uri']
        self.assertTrue(URI.startswith(BASE_URI))
        uri_parts = urlparse(URI)
        self.assertEqual(parse_qs(uri_parts.query), EXPECTED_QUERY)


class Test__BucketIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.client import _BucketIterator
        return _BucketIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = object()
        client = _Client(connection)
        iterator = self._makeOne(client)
        self.assertEqual(iterator.path, '/b')
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)
        self.assertTrue(iterator.client is client)

    def test_get_items_from_response_empty(self):
        connection = object()
        client = _Client(connection)
        iterator = self._makeOne(client)
        self.assertEqual(list(iterator.get_items_from_response({})), [])

    def test_get_items_from_response_non_empty(self):
        from gcloud.storage.bucket import Bucket
        BLOB_NAME = 'blob-name'
        response = {'items': [{'name': BLOB_NAME}]}
        connection = object()
        client = _Client(connection)
        iterator = self._makeOne(client)
        buckets = list(iterator.get_items_from_response(response))
        self.assertEqual(len(buckets), 1)
        bucket = buckets[0]
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertEqual(bucket.name, BLOB_NAME)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content


class _Client(object):

    def __init__(self, connection):
        self.connection = connection
