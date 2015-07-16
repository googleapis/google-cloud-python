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
        from gcloud.search.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_explicit(self):
        from gcloud.search import SCOPE
        from gcloud.search.connection import Connection

        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        client_obj = self._makeOne(project=PROJECT, credentials=CREDS)

        self.assertEqual(client_obj.project, PROJECT)
        self.assertTrue(isinstance(client_obj.connection, Connection))
        self.assertTrue(client_obj.connection._credentials is CREDS)
        self.assertEqual(CREDS._scopes, SCOPE)

    def test_list_indexes_no_paging(self):
        from gcloud.search.index import Index
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)
        INDEX_ID = 'my-index-id'
        INDEX_PATH = '/projects/%s/indexes/%s' % (PROJECT, INDEX_ID)

        RETURNED = {'indexes': [{'indexId': INDEX_ID}]}
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        indexes = list(CLIENT_OBJ.list_indexes())
        # Test values are correct.
        self.assertEqual(len(indexes), 1)
        self.assertTrue(isinstance(indexes[0], Index))
        self.assertEqual(indexes[0].path, INDEX_PATH)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/indexes' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_list_indexes_with_paging(self):
        from gcloud.search.index import Index
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        INDEX_ID1 = 'index-id-1'
        INDEX_ID2 = 'index-id-2'
        TOKEN = 'TOKEN'
        SIZE = 1
        RETURNED = [{'indexes': [{'indexId': INDEX_ID1}],
                     'nextPageToken': TOKEN},
                    {'indexes': [{'indexId': INDEX_ID2}]}]
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(*RETURNED)

        # Execute request.
        indexes = list(CLIENT_OBJ.list_indexes(page_size=SIZE))
        # Test values are correct.
        self.assertEqual(len(indexes), 2)
        self.assertTrue(isinstance(indexes[0], Index))
        self.assertEqual(indexes[0].index_id, INDEX_ID1)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 2)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/indexes' % PROJECT)
        self.assertEqual(req['query_params'], {'pageSize': SIZE})
        req2 = CLIENT_OBJ.connection._requested[1]
        self.assertEqual(req2['method'], 'GET')
        self.assertEqual(req2['path'], '/projects/%s/indexes' % PROJECT)
        self.assertEqual(req2['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN})

    def test_index(self):
        PROJECT = 'PROJECT'
        INDEX_ID = 'index-id'
        CREDS = _Credentials()

        client_obj = self._makeOne(project=PROJECT, credentials=CREDS)
        new_index = client_obj.index(INDEX_ID)
        self.assertEqual(new_index.index_id, INDEX_ID)
        self.assertTrue(new_index.client is client_obj)
        self.assertEqual(new_index.project, PROJECT)
        self.assertEqual(new_index.full_name,
                         'projects/%s/indexes/%s' % (PROJECT, INDEX_ID))


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
