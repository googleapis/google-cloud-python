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

        PROJECT = object()
        CREDENTIALS = _Credentials()

        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertTrue(client.connection.credentials is CREDENTIALS)

    def test_get_bucket_miss(self):
        from gcloud.exceptions import NotFound

        PROJECT = object()
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

        PROJECT = object()
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
        PROJECT = object()
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

        PROJECT = object()
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
