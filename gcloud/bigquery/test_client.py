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

    def test_list_datasets_explicit_response_missing_datasets_key(self):
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/datasets' % PROJECT
        TOKEN = 'TOKEN'
        DATA = {}
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        datasets, token = client.list_datasets(
            include_all=True, max_results=3, page_token=TOKEN)

        self.assertEqual(len(datasets), 0)
        self.assertEqual(token, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'all': True, 'maxResults': 3, 'pageToken': TOKEN})

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

    def test_job_from_resource_unknown_type(self):
        PROJECT = 'PROJECT'
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        with self.assertRaises(ValueError):
            client.job_from_resource({'configuration': {'nonesuch': {}}})

    def test_list_jobs_defaults(self):
        from gcloud.bigquery.job import LoadTableFromStorageJob
        from gcloud.bigquery.job import CopyJob
        from gcloud.bigquery.job import ExtractTableToStorageJob
        from gcloud.bigquery.job import QueryJob
        PROJECT = 'PROJECT'
        DATASET = 'test_dataset'
        SOURCE_TABLE = 'source_table'
        DESTINATION_TABLE = 'destination_table'
        QUERY_DESTINATION_TABLE = 'query_destination_table'
        SOURCE_URI = 'gs://test_bucket/src_object*'
        DESTINATION_URI = 'gs://test_bucket/dst_object*'
        JOB_TYPES = {
            'load_job': LoadTableFromStorageJob,
            'copy_job': CopyJob,
            'extract_job': ExtractTableToStorageJob,
            'query_job': QueryJob,
        }
        PATH = 'projects/%s/jobs' % PROJECT
        TOKEN = 'TOKEN'
        QUERY = 'SELECT * from test_dataset:test_table'
        ASYNC_QUERY_DATA = {
            'id': '%s:%s' % (PROJECT, 'query_job'),
            'jobReference': {
                'projectId': PROJECT,
                'jobId': 'query_job',
            },
            'state': 'DONE',
            'configuration': {
                'query': {
                    'query': QUERY,
                    'destinationTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': QUERY_DESTINATION_TABLE,
                    },
                    'createDisposition': 'CREATE_IF_NEEDED',
                    'writeDisposition': 'WRITE_TRUNCATE',
                }
            },
        }
        EXTRACT_DATA = {
            'id': '%s:%s' % (PROJECT, 'extract_job'),
            'jobReference': {
                'projectId': PROJECT,
                'jobId': 'extract_job',
            },
            'state': 'DONE',
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': SOURCE_TABLE,
                    },
                    'destinationUris': [DESTINATION_URI],
                }
            },
        }
        COPY_DATA = {
            'id': '%s:%s' % (PROJECT, 'copy_job'),
            'jobReference': {
                'projectId': PROJECT,
                'jobId': 'copy_job',
            },
            'state': 'DONE',
            'configuration': {
                'copy': {
                    'sourceTables': [{
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': SOURCE_TABLE,
                    }],
                    'destinationTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': DESTINATION_TABLE,
                    },
                }
            },
        }
        LOAD_DATA = {
            'id': '%s:%s' % (PROJECT, 'load_job'),
            'jobReference': {
                'projectId': PROJECT,
                'jobId': 'load_job',
            },
            'state': 'DONE',
            'configuration': {
                'load': {
                    'destinationTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': SOURCE_TABLE,
                    },
                    'sourceUris': [SOURCE_URI],
                }
            },
        }
        DATA = {
            'nextPageToken': TOKEN,
            'jobs': [
                ASYNC_QUERY_DATA,
                EXTRACT_DATA,
                COPY_DATA,
                LOAD_DATA,
            ]
        }
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        jobs, token = client.list_jobs()

        self.assertEqual(len(jobs), len(DATA['jobs']))
        for found, expected in zip(jobs, DATA['jobs']):
            name = expected['jobReference']['jobId']
            self.assertTrue(isinstance(found, JOB_TYPES[name]))
            self.assertEqual(found.name, name)
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'projection': 'full'})

    def test_list_jobs_load_job_wo_sourceUris(self):
        from gcloud.bigquery.job import LoadTableFromStorageJob
        PROJECT = 'PROJECT'
        DATASET = 'test_dataset'
        SOURCE_TABLE = 'source_table'
        JOB_TYPES = {
            'load_job': LoadTableFromStorageJob,
        }
        PATH = 'projects/%s/jobs' % PROJECT
        TOKEN = 'TOKEN'
        LOAD_DATA = {
            'id': '%s:%s' % (PROJECT, 'load_job'),
            'jobReference': {
                'projectId': PROJECT,
                'jobId': 'load_job',
            },
            'state': 'DONE',
            'configuration': {
                'load': {
                    'destinationTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': SOURCE_TABLE,
                    },
                }
            },
        }
        DATA = {
            'nextPageToken': TOKEN,
            'jobs': [
                LOAD_DATA,
            ]
        }
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        jobs, token = client.list_jobs()

        self.assertEqual(len(jobs), len(DATA['jobs']))
        for found, expected in zip(jobs, DATA['jobs']):
            name = expected['jobReference']['jobId']
            self.assertTrue(isinstance(found, JOB_TYPES[name]))
            self.assertEqual(found.name, name)
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'projection': 'full'})

    def test_list_jobs_explicit_missing(self):
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/jobs' % PROJECT
        DATA = {}
        TOKEN = 'TOKEN'
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        jobs, token = client.list_jobs(max_results=1000, page_token=TOKEN,
                                       all_users=True, state_filter='done')

        self.assertEqual(len(jobs), 0)
        self.assertEqual(token, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'projection': 'full',
                          'maxResults': 1000,
                          'pageToken': TOKEN,
                          'allUsers': True,
                          'stateFilter': 'done'})

    def test_load_table_from_storage(self):
        from gcloud.bigquery.job import LoadTableFromStorageJob
        PROJECT = 'PROJECT'
        JOB = 'job_name'
        DATASET = 'dataset_name'
        DESTINATION = 'destination_table'
        SOURCE_URI = 'http://example.com/source.csv'
        creds = _Credentials()
        http = object()
        client = self._makeOne(project=PROJECT, credentials=creds, http=http)
        dataset = client.dataset(DATASET)
        destination = dataset.table(DESTINATION)
        job = client.load_table_from_storage(JOB, destination, SOURCE_URI)
        self.assertTrue(isinstance(job, LoadTableFromStorageJob))
        self.assertTrue(job._client is client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(list(job.source_uris), [SOURCE_URI])
        self.assertTrue(job.destination is destination)

    def test_copy_table(self):
        from gcloud.bigquery.job import CopyJob
        PROJECT = 'PROJECT'
        JOB = 'job_name'
        DATASET = 'dataset_name'
        SOURCE = 'source_table'
        DESTINATION = 'destination_table'
        creds = _Credentials()
        http = object()
        client = self._makeOne(project=PROJECT, credentials=creds, http=http)
        dataset = client.dataset(DATASET)
        source = dataset.table(SOURCE)
        destination = dataset.table(DESTINATION)
        job = client.copy_table(JOB, destination, source)
        self.assertTrue(isinstance(job, CopyJob))
        self.assertTrue(job._client is client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(list(job.sources), [source])
        self.assertTrue(job.destination is destination)

    def test_extract_table_to_storage(self):
        from gcloud.bigquery.job import ExtractTableToStorageJob
        PROJECT = 'PROJECT'
        JOB = 'job_name'
        DATASET = 'dataset_name'
        SOURCE = 'source_table'
        DESTINATION = 'gs://bucket_name/object_name'
        creds = _Credentials()
        http = object()
        client = self._makeOne(project=PROJECT, credentials=creds, http=http)
        dataset = client.dataset(DATASET)
        source = dataset.table(SOURCE)
        job = client.extract_table_to_storage(JOB, source, DESTINATION)
        self.assertTrue(isinstance(job, ExtractTableToStorageJob))
        self.assertTrue(job._client is client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(job.source, source)
        self.assertEqual(list(job.destination_uris), [DESTINATION])

    def test_run_async_query(self):
        from gcloud.bigquery.job import QueryJob
        PROJECT = 'PROJECT'
        JOB = 'job_name'
        QUERY = 'select count(*) from persons'
        creds = _Credentials()
        http = object()
        client = self._makeOne(project=PROJECT, credentials=creds, http=http)
        job = client.run_async_query(JOB, QUERY)
        self.assertTrue(isinstance(job, QueryJob))
        self.assertTrue(job._client is client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(job.query, QUERY)

    def test_run_sync_query(self):
        from gcloud.bigquery.query import QueryResults
        PROJECT = 'PROJECT'
        QUERY = 'select count(*) from persons'
        creds = _Credentials()
        http = object()
        client = self._makeOne(project=PROJECT, credentials=creds, http=http)
        job = client.run_sync_query(QUERY)
        self.assertTrue(isinstance(job, QueryResults))
        self.assertTrue(job._client is client)
        self.assertEqual(job.name, None)
        self.assertEqual(job.query, QUERY)


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
