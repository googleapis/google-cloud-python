# Copyright 2015 Google Inc.
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

import mock


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.client import Client

        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        from google.cloud.bigquery._http import Connection

        PROJECT = 'PROJECT'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)

    def test_list_projects_defaults(self):
        import six
        from google.cloud.bigquery.client import Project

        PROJECT_1 = 'PROJECT_ONE'
        PROJECT_2 = 'PROJECT_TWO'
        PATH = 'projects'
        TOKEN = 'TOKEN'
        DATA = {
            'nextPageToken': TOKEN,
            'projects': [
                {'kind': 'bigquery#project',
                 'id': PROJECT_1,
                 'numericId': 1,
                 'projectReference': {'projectId': PROJECT_1},
                 'friendlyName': 'One'},
                {'kind': 'bigquery#project',
                 'id': PROJECT_2,
                 'numericId': 2,
                 'projectReference': {'projectId': PROJECT_2},
                 'friendlyName': 'Two'},
            ]
        }
        creds = _make_credentials()
        client = self._make_one(PROJECT_1, creds)
        conn = client._connection = _Connection(DATA)

        iterator = client.list_projects()
        page = six.next(iterator.pages)
        projects = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(projects), len(DATA['projects']))
        for found, expected in zip(projects, DATA['projects']):
            self.assertIsInstance(found, Project)
            self.assertEqual(found.project_id, expected['id'])
            self.assertEqual(found.numeric_id, expected['numericId'])
            self.assertEqual(found.friendly_name, expected['friendlyName'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_projects_explicit_response_missing_projects_key(self):
        import six

        PROJECT = 'PROJECT'
        PATH = 'projects'
        TOKEN = 'TOKEN'
        DATA = {}
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        conn = client._connection = _Connection(DATA)

        iterator = client.list_projects(max_results=3, page_token=TOKEN)
        page = six.next(iterator.pages)
        projects = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(projects), 0)
        self.assertIsNone(token)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'maxResults': 3, 'pageToken': TOKEN})

    def test_list_datasets_defaults(self):
        import six
        from google.cloud.bigquery.dataset import Dataset

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
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        conn = client._connection = _Connection(DATA)

        iterator = client.list_datasets()
        page = six.next(iterator.pages)
        datasets = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(datasets), len(DATA['datasets']))
        for found, expected in zip(datasets, DATA['datasets']):
            self.assertIsInstance(found, Dataset)
            self.assertEqual(found.dataset_id, expected['id'])
            self.assertEqual(found.friendly_name, expected['friendlyName'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_datasets_explicit_response_missing_datasets_key(self):
        import six

        PROJECT = 'PROJECT'
        PATH = 'projects/%s/datasets' % PROJECT
        TOKEN = 'TOKEN'
        DATA = {}
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        conn = client._connection = _Connection(DATA)

        iterator = client.list_datasets(
            include_all=True, max_results=3, page_token=TOKEN)
        page = six.next(iterator.pages)
        datasets = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(datasets), 0)
        self.assertIsNone(token)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'all': True, 'maxResults': 3, 'pageToken': TOKEN})

    def test_dataset(self):
        from google.cloud.bigquery.dataset import Dataset

        PROJECT = 'PROJECT'
        DATASET = 'dataset_name'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        dataset = client.dataset(DATASET)
        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.name, DATASET)
        self.assertIs(dataset._client, client)

    def test_job_from_resource_unknown_type(self):
        PROJECT = 'PROJECT'
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        with self.assertRaises(ValueError):
            client.job_from_resource({'configuration': {'nonesuch': {}}})

    def test_list_jobs_defaults(self):
        import six
        from google.cloud.bigquery.job import LoadTableFromStorageJob
        from google.cloud.bigquery.job import CopyJob
        from google.cloud.bigquery.job import ExtractTableToStorageJob
        from google.cloud.bigquery.job import QueryJob

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
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        conn = client._connection = _Connection(DATA)

        iterator = client.list_jobs()
        page = six.next(iterator.pages)
        jobs = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(jobs), len(DATA['jobs']))
        for found, expected in zip(jobs, DATA['jobs']):
            name = expected['jobReference']['jobId']
            self.assertIsInstance(found, JOB_TYPES[name])
            self.assertEqual(found.name, name)
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'projection': 'full'})

    def test_list_jobs_load_job_wo_sourceUris(self):
        import six
        from google.cloud.bigquery.job import LoadTableFromStorageJob

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
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        conn = client._connection = _Connection(DATA)

        iterator = client.list_jobs()
        page = six.next(iterator.pages)
        jobs = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(jobs), len(DATA['jobs']))
        for found, expected in zip(jobs, DATA['jobs']):
            name = expected['jobReference']['jobId']
            self.assertIsInstance(found, JOB_TYPES[name])
            self.assertEqual(found.name, name)
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'projection': 'full'})

    def test_list_jobs_explicit_missing(self):
        import six

        PROJECT = 'PROJECT'
        PATH = 'projects/%s/jobs' % PROJECT
        DATA = {}
        TOKEN = 'TOKEN'
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        conn = client._connection = _Connection(DATA)

        iterator = client.list_jobs(max_results=1000, page_token=TOKEN,
                                    all_users=True, state_filter='done')
        page = six.next(iterator.pages)
        jobs = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(jobs), 0)
        self.assertIsNone(token)

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
        from google.cloud.bigquery.job import LoadTableFromStorageJob

        PROJECT = 'PROJECT'
        JOB = 'job_name'
        DATASET = 'dataset_name'
        DESTINATION = 'destination_table'
        SOURCE_URI = 'http://example.com/source.csv'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        dataset = client.dataset(DATASET)
        destination = dataset.table(DESTINATION)
        job = client.load_table_from_storage(JOB, destination, SOURCE_URI)
        self.assertIsInstance(job, LoadTableFromStorageJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(list(job.source_uris), [SOURCE_URI])
        self.assertIs(job.destination, destination)

    def test_copy_table(self):
        from google.cloud.bigquery.job import CopyJob

        PROJECT = 'PROJECT'
        JOB = 'job_name'
        DATASET = 'dataset_name'
        SOURCE = 'source_table'
        DESTINATION = 'destination_table'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        dataset = client.dataset(DATASET)
        source = dataset.table(SOURCE)
        destination = dataset.table(DESTINATION)
        job = client.copy_table(JOB, destination, source)
        self.assertIsInstance(job, CopyJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(list(job.sources), [source])
        self.assertIs(job.destination, destination)

    def test_extract_table_to_storage(self):
        from google.cloud.bigquery.job import ExtractTableToStorageJob

        PROJECT = 'PROJECT'
        JOB = 'job_name'
        DATASET = 'dataset_name'
        SOURCE = 'source_table'
        DESTINATION = 'gs://bucket_name/object_name'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        dataset = client.dataset(DATASET)
        source = dataset.table(SOURCE)
        job = client.extract_table_to_storage(JOB, source, DESTINATION)
        self.assertIsInstance(job, ExtractTableToStorageJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(job.source, source)
        self.assertEqual(list(job.destination_uris), [DESTINATION])

    def test_run_async_query_defaults(self):
        from google.cloud.bigquery.job import QueryJob

        PROJECT = 'PROJECT'
        JOB = 'job_name'
        QUERY = 'select count(*) from persons'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        job = client.run_async_query(JOB, QUERY)
        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(job.query_parameters, [])

    def test_run_async_w_udf_resources(self):
        from google.cloud.bigquery._helpers import UDFResource
        from google.cloud.bigquery.job import QueryJob

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        PROJECT = 'PROJECT'
        JOB = 'job_name'
        QUERY = 'select count(*) from persons'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        job = client.run_async_query(JOB, QUERY, udf_resources=udf_resources)
        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, udf_resources)
        self.assertEqual(job.query_parameters, [])

    def test_run_async_w_query_parameters(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter
        from google.cloud.bigquery.job import QueryJob

        PROJECT = 'PROJECT'
        JOB = 'job_name'
        QUERY = 'select count(*) from persons'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        query_parameters = [ScalarQueryParameter('foo', 'INT64', 123)]
        job = client.run_async_query(JOB, QUERY,
                                     query_parameters=query_parameters)
        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.name, JOB)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(job.query_parameters, query_parameters)

    def test_run_sync_query_defaults(self):
        from google.cloud.bigquery.query import QueryResults

        PROJECT = 'PROJECT'
        QUERY = 'select count(*) from persons'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        query = client.run_sync_query(QUERY)
        self.assertIsInstance(query, QueryResults)
        self.assertIs(query._client, client)
        self.assertIsNone(query.name)
        self.assertEqual(query.query, QUERY)
        self.assertEqual(query.udf_resources, [])
        self.assertEqual(query.query_parameters, [])

    def test_run_sync_query_w_udf_resources(self):
        from google.cloud.bigquery._helpers import UDFResource
        from google.cloud.bigquery.query import QueryResults

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        PROJECT = 'PROJECT'
        QUERY = 'select count(*) from persons'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        query = client.run_sync_query(QUERY, udf_resources=udf_resources)
        self.assertIsInstance(query, QueryResults)
        self.assertIs(query._client, client)
        self.assertIsNone(query.name)
        self.assertEqual(query.query, QUERY)
        self.assertEqual(query.udf_resources, udf_resources)
        self.assertEqual(query.query_parameters, [])

    def test_run_sync_query_w_query_parameters(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter
        from google.cloud.bigquery.query import QueryResults

        PROJECT = 'PROJECT'
        QUERY = 'select count(*) from persons'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, http=http)
        query_parameters = [ScalarQueryParameter('foo', 'INT64', 123)]
        query = client.run_sync_query(QUERY, query_parameters=query_parameters)
        self.assertIsInstance(query, QueryResults)
        self.assertIs(query._client, client)
        self.assertIsNone(query.name)
        self.assertEqual(query.query, QUERY)
        self.assertEqual(query.udf_resources, [])
        self.assertEqual(query.query_parameters, query_parameters)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
