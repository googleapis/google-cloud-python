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
    PROJECT = 'PROJECT'

    def _getTargetClass(self):
        from gcloud.search.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        from gcloud.search.connection import Connection
        creds = _Credentials()
        http = object()
        client = self._makeOne(
            project=self.PROJECT, credentials=creds, http=http)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertTrue(client.connection.credentials is creds)
        self.assertTrue(client.connection.http is http)

    def test_list_indexes_defaults(self):
        from gcloud.search.index import Index
        INDEX_1 = 'index-one'
        INDEX_2 = 'index-two'
        PATH = 'projects/%s/indexes' % self.PROJECT
        TOKEN = 'TOKEN'
        DATA = {
            'nextPageToken': TOKEN,
            'indexes': [
                {'project': self.PROJECT,
                 'indexId': INDEX_1},
                {'project': self.PROJECT,
                 'indexId': INDEX_2},
            ]
        }
        creds = _Credentials()
        client = self._makeOne(self.PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        zones, token = client.list_indexes()

        self.assertEqual(len(zones), len(DATA['indexes']))
        for found, expected in zip(zones, DATA['indexes']):
            self.assertTrue(isinstance(found, Index))
            self.assertEqual(found.name, expected['indexId'])
            self.assertEqual(found.text_fields, None)
            self.assertEqual(found.atom_fields, None)
            self.assertEqual(found.html_fields, None)
            self.assertEqual(found.date_fields, None)
            self.assertEqual(found.number_fields, None)
            self.assertEqual(found.geo_fields, None)
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_indexes_explicit(self):
        from gcloud.search.index import Index
        INDEX_1 = 'index-one'
        INDEX_2 = 'index-two'
        PATH = 'projects/%s/indexes' % self.PROJECT
        TOKEN = 'TOKEN'
        DATA = {
            'indexes': [
                {'project': self.PROJECT,
                 'indexId': INDEX_1,
                 'indexedField': {'textFields': ['text-1']}},
                {'project': self.PROJECT,
                 'indexId': INDEX_2,
                 'indexedField': {'htmlFields': ['html-1']}},
            ]
        }
        creds = _Credentials()
        client = self._makeOne(self.PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        zones, token = client.list_indexes(
            max_results=3, page_token=TOKEN, prefix='index', view='FULL')

        self.assertEqual(len(zones), len(DATA['indexes']))
        for found, expected in zip(zones, DATA['indexes']):
            self.assertTrue(isinstance(found, Index))
            self.assertEqual(found.name, expected['indexId'])
            field_info = expected['indexedField']
            self.assertEqual(found.text_fields, field_info.get('textFields'))
            self.assertEqual(found.atom_fields, field_info.get('atomFields'))
            self.assertEqual(found.html_fields, field_info.get('htmlFields'))
            self.assertEqual(found.date_fields, field_info.get('dateFields'))
            self.assertEqual(found.number_fields,
                             field_info.get('numberFields'))
            self.assertEqual(found.geo_fields, field_info.get('geoFields'))
        self.assertEqual(token, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'indexNamePrefix': 'index',
                          'pageSize': 3,
                          'pageToken': TOKEN,
                          'view': 'FULL'})

    def test_index(self):
        from gcloud.search.index import Index
        INDEX_ID = 'index-id'
        creds = _Credentials()
        http = object()
        client = self._makeOne(
            project=self.PROJECT, credentials=creds, http=http)
        index = client.index(INDEX_ID)
        self.assertTrue(isinstance(index, Index))
        self.assertEqual(index.name, INDEX_ID)
        self.assertTrue(index._client is client)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
