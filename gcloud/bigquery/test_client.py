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
        from gcloud.bigquery.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        from gcloud.bigquery.connection import Connection
        PROJECT = 'PROJECT'
        creds = _Credentials()
        http = object()
        client = self._makeOne(project=PROJECT, credentials=creds, http=http)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertTrue(client.connection.credentials is creds)
        self.assertTrue(client.connection.http is http)

    def test_dataset(self):
        from gcloud.bigquery.dataset import Dataset
        PROJECT = 'PROJECT'
        DATASET = 'dataset_name'
        creds = _Credentials()
        http = object()
        client = self._makeOne(project=PROJECT, credentials=creds, http=http)
        dataset = client.dataset(DATASET)
        self.assertTrue(isinstance(dataset, Dataset))
        self.assertEqual(dataset.name, DATASET)
        self.assertTrue(dataset._client is client)

    def test_list_datasets_defaults(self):
        from gcloud.bigquery.dataset import Dataset
        PROJECT = 'PROJECT'
        DATASET_1 = 'dataset_one'
        DATASET_2 = 'dataset_two'
        PATH = 'projects/%s/datasets' % PROJECT
        TOKEN = 'TOKEN'
        DATA = {
            'nextPageToken': TOKEN,
            'datasets': [
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s' % (PROJECT, DATASET_1),
                 'datasetReference': {'datasetId': DATASET_1,
                                      'projectId': PROJECT},
                 'friendlyName': None},
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s' % (PROJECT, DATASET_2),
                 'datasetReference': {'datasetId': DATASET_2,
                                      'projectId': PROJECT},
                 'friendlyName': 'Two'},
            ]
        }
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        datasets, token = client.list_datasets()

        self.assertEqual(len(datasets), len(DATA['datasets']))
        for found, expected in zip(datasets, DATA['datasets']):
            self.assertTrue(isinstance(found, Dataset))
            self.assertEqual(found.dataset_id, expected['id'])
            self.assertEqual(found.friendly_name, expected['friendlyName'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_datasets_explicit(self):
        from gcloud.bigquery.dataset import Dataset
        PROJECT = 'PROJECT'
        DATASET_1 = 'dataset_one'
        DATASET_2 = 'dataset_two'
        PATH = 'projects/%s/datasets' % PROJECT
        TOKEN = 'TOKEN'
        DATA = {
            'datasets': [
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s' % (PROJECT, DATASET_1),
                 'datasetReference': {'datasetId': DATASET_1,
                                      'projectId': PROJECT},
                 'friendlyName': None},
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s' % (PROJECT, DATASET_2),
                 'datasetReference': {'datasetId': DATASET_2,
                                      'projectId': PROJECT},
                 'friendlyName': 'Two'},
            ]
        }
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        datasets, token = client.list_datasets(
            include_all=True, max_results=3, page_token=TOKEN)

        self.assertEqual(len(datasets), len(DATA['datasets']))
        for found, expected in zip(datasets, DATA['datasets']):
            self.assertTrue(isinstance(found, Dataset))
            self.assertEqual(found.dataset_id, expected['id'])
            self.assertEqual(found.friendly_name, expected['friendlyName'])
        self.assertEqual(token, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'all': True, 'maxResults': 3, 'pageToken': TOKEN})


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
