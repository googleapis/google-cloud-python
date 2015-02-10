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


class TestConnection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.connection import Connection
        return Connection

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        self.assertEqual(conn.project, PROJECT)
        self.assertEqual(conn.credentials, None)

    def test_ctor_explicit(self):
        PROJECT = 'project'
        creds = object()
        conn = self._makeOne(PROJECT, creds)
        self.assertEqual(conn.project, PROJECT)
        self.assertTrue(conn.credentials is creds)

    def test_http_w_existing(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        conn._http = http = object()
        self.assertTrue(conn.http is http)

    def test_http_wo_creds(self):
        import httplib2
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        self.assertTrue(isinstance(conn.http, httplib2.Http))

    def test_http_w_creds(self):
        import httplib2
        PROJECT = 'project'
        authorized = object()

        class Creds(object):
            def authorize(self, http):
                self._called_with = http
                return authorized
        creds = Creds()
        conn = self._makeOne(PROJECT, creds)
        self.assertTrue(conn.http is authorized)
        self.assertTrue(isinstance(creds._called_with, httplib2.Http))

    def test_build_api_url_no_extra_query_params(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'storage',
            conn.API_VERSION,
            'foo?project=%s' % PROJECT,
        ])
        self.assertEqual(conn.build_api_url('/foo'), URI)

    def test_build_api_url_w_extra_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        uri = conn.build_api_url('/foo', {'bar': 'baz'})
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        self.assertEqual(path,
                         '/'.join(['', 'storage', conn.API_VERSION, 'foo']))
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['project'], PROJECT)
        self.assertEqual(parms['bar'], 'baz')

    def test_build_api_url_w_upload(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'upload',
            'storage',
            conn.API_VERSION,
            'foo?project=%s' % PROJECT,
        ])
        self.assertEqual(conn.build_api_url('/foo', upload=True), URI)

    def test__make_request_no_data_no_content_type_no_headers(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = 'http://example.com/test'
        http = conn._http = Http(
            {'status': '200', 'content-type': 'text/plain'},
            '',
        )
        headers, content = conn._make_request('GET', URI)
        self.assertEqual(headers['status'], '200')
        self.assertEqual(headers['content-type'], 'text/plain')
        self.assertEqual(content, '')
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test__make_request_w_data_no_extra_headers(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = 'http://example.com/test'
        http = conn._http = Http(
            {'status': '200', 'content-type': 'text/plain'},
            '',
        )
        conn._make_request('GET', URI, {}, 'application/json')
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], {})
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'Content-Type': 'application/json',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test__make_request_w_extra_headers(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = 'http://example.com/test'
        http = conn._http = Http(
            {'status': '200', 'content-type': 'text/plain'},
            '',
        )
        conn._make_request('GET', URI, headers={'X-Foo': 'foo'})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'X-Foo': 'foo',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_defaults(self):
        PROJECT = 'project'
        PATH = '/path/required'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'storage',
            '%s%s?project=%s' % (conn.API_VERSION, PATH, PROJECT),
        ])
        http = conn._http = Http(
            {'status': '200', 'content-type': 'application/json'},
            '{}',
        )
        self.assertEqual(conn.api_request('GET', PATH), {})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_non_json_response(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        conn._http = Http(
            {'status': '200', 'content-type': 'text/plain'},
            'CONTENT',
        )

        self.assertRaises(TypeError, conn.api_request, 'GET', '/')

    def test_api_request_wo_json_expected(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        conn._http = Http(
            {'status': '200', 'content-type': 'text/plain'},
            'CONTENT',
        )
        self.assertEqual(conn.api_request('GET', '/', expect_json=False),
                         'CONTENT')

    def test_api_request_w_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        http = conn._http = Http(
            {'status': '200', 'content-type': 'application/json'},
            '{}',
        )
        self.assertEqual(conn.api_request('GET', '/', {'foo': 'bar'}), {})
        self.assertEqual(http._called_with['method'], 'GET')
        uri = http._called_with['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        self.assertEqual(path,
                         '/'.join(['', 'storage', conn.API_VERSION, '']))
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['project'], PROJECT)
        self.assertEqual(parms['foo'], 'bar')
        self.assertEqual(http._called_with['body'], None)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_data(self):
        import json
        PROJECT = 'project'
        DATA = {'foo': 'bar'}
        DATAJ = json.dumps(DATA)
        conn = self._makeOne(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'storage',
            conn.API_VERSION,
            '?project=%s' % PROJECT,
        ])
        http = conn._http = Http(
            {'status': '200', 'content-type': 'application/json'},
            '{}',
        )
        self.assertEqual(conn.api_request('POST', '/', data=DATA), {})
        self.assertEqual(http._called_with['method'], 'POST')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], DATAJ)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': len(DATAJ),
            'Content-Type': 'application/json',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_404(self):
        from gcloud.exceptions import NotFound
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        conn._http = Http(
            {'status': '404', 'content-type': 'text/plain'},
            '{}'
        )
        self.assertRaises(NotFound, conn.api_request, 'GET', '/')

    def test_api_request_w_500(self):
        from gcloud.exceptions import InternalServerError
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        conn._http = Http(
            {'status': '500', 'content-type': 'text/plain'},
            '{}',
        )
        self.assertRaises(InternalServerError, conn.api_request, 'GET', '/')

    def test_get_all_buckets_empty(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
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
        buckets = list(conn.get_all_buckets())
        self.assertEqual(len(buckets), 0)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_get_all_buckets_non_empty(self):
        PROJECT = 'project'
        BUCKET_NAME = 'bucket-name'
        conn = self._makeOne(PROJECT)
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
        buckets = list(conn.get_all_buckets())
        self.assertEqual(len(buckets), 1)
        self.assertEqual(buckets[0].name, BUCKET_NAME)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_get_bucket_miss(self):
        from gcloud.exceptions import NotFound
        PROJECT = 'project'
        NONESUCH = 'nonesuch'
        conn = self._makeOne(PROJECT)
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
        self.assertRaises(NotFound, conn.get_bucket, NONESUCH)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_get_bucket_hit(self):
        from gcloud.storage.bucket import Bucket
        PROJECT = 'project'
        BLOB_NAME = 'blob-name'
        conn = self._makeOne(PROJECT)
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
        bucket = conn.get_bucket(BLOB_NAME)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is conn)
        self.assertEqual(bucket.name, BLOB_NAME)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_create_bucket_ok(self):
        from gcloud.storage.bucket import Bucket
        PROJECT = 'project'
        BLOB_NAME = 'blob-name'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'storage',
            conn.API_VERSION,
            'b?project=%s' % PROJECT,
            ])
        http = conn._http = Http(
            {'status': '200', 'content-type': 'application/json'},
            '{"name": "%s"}' % BLOB_NAME,
        )
        bucket = conn.create_bucket(BLOB_NAME)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is conn)
        self.assertEqual(bucket.name, BLOB_NAME)
        self.assertEqual(http._called_with['method'], 'POST')
        self.assertEqual(http._called_with['uri'], URI)

    def test_delete_bucket_defaults_miss(self):
        _deleted_blobs = []

        PROJECT = 'project'
        BLOB_NAME = 'blob-name'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([
            conn.API_BASE_URL,
            'storage',
            conn.API_VERSION,
            'b',
            '%s?project=%s' % (BLOB_NAME, PROJECT),
        ])
        http = conn._http = Http(
            {'status': '200', 'content-type': 'application/json'},
            '{}',
        )

        self.assertEqual(conn.delete_bucket(BLOB_NAME), None)
        self.assertEqual(_deleted_blobs, [])
        self.assertEqual(http._called_with['method'], 'DELETE')
        self.assertEqual(http._called_with['uri'], URI)


class Test__BucketIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.connection import _BucketIterator
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
