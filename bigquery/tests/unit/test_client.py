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
import six


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
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)

    def test__get_query_results_miss_w_explicit_project_and_timeout(self):
        from google.cloud.exceptions import NotFound

        project = 'PROJECT'
        creds = _make_credentials()
        client = self._make_one(project, creds)
        conn = client._connection = _Connection()

        with self.assertRaises(NotFound):
            client._get_query_results(
                'nothere', project='other-project', timeout_ms=500)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(
            req['path'], '/projects/other-project/queries/nothere')
        self.assertEqual(
            req['query_params'], {'maxResults': 0, 'timeoutMs': 500})

    def test__get_query_results_hit(self):
        project = 'PROJECT'
        job_id = 'query_job'
        data = {
            'kind': 'bigquery#getQueryResultsResponse',
            'etag': 'some-tag',
            'schema': {
                'fields': [
                    {
                        'name': 'title',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'name': 'unique_words',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE'
                    }
                ]
            },
            'jobReference': {
                'projectId': project,
                'jobId': job_id,
            },
            'totalRows': '10',
            'totalBytesProcessed': '2464625',
            'jobComplete': True,
            'cacheHit': False,
        }

        creds = _make_credentials()
        client = self._make_one(project, creds)
        client._connection = _Connection(data)
        query_results = client._get_query_results(job_id)

        self.assertEqual(query_results.total_rows, 10)
        self.assertTrue(query_results.complete)

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
            self.assertEqual(found.full_dataset_id, expected['id'])
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

    def test_dataset_with_specified_project(self):
        from google.cloud.bigquery.dataset import DatasetReference

        PROJECT = 'PROJECT'
        DATASET = 'dataset_name'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        dataset = client.dataset(DATASET, PROJECT)
        self.assertIsInstance(dataset, DatasetReference)
        self.assertEqual(dataset.dataset_id, DATASET)
        self.assertEqual(dataset.project, PROJECT)

    def test_dataset_with_default_project(self):
        from google.cloud.bigquery.dataset import DatasetReference

        PROJECT = 'PROJECT'
        DATASET = 'dataset_name'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        dataset = client.dataset(DATASET)
        self.assertIsInstance(dataset, DatasetReference)
        self.assertEqual(dataset.dataset_id, DATASET)
        self.assertEqual(dataset.project, PROJECT)

    def test_get_dataset(self):
        project = 'PROJECT'
        dataset_id = 'dataset_id'
        path = 'projects/%s/datasets/%s' % (project, dataset_id)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=project, credentials=creds, _http=http)
        resource = {
            'id': '%s:%s' % (project, dataset_id),
            'datasetReference': {
                'projectId': project,
                'datasetId': dataset_id,
            },
        }
        conn = client._connection = _Connection(resource)
        dataset_ref = client.dataset(dataset_id)

        dataset = client.get_dataset(dataset_ref)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % path)
        self.assertEqual(dataset.dataset_id, dataset_id)

    def test_create_dataset_minimal(self):
        from google.cloud.bigquery.dataset import Dataset

        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        PATH = 'projects/%s/datasets' % PROJECT
        RESOURCE = {
            'datasetReference':
                {'projectId': PROJECT, 'datasetId': DS_ID},
            'etag': "etag",
            'id': "%s:%s" % (PROJECT, DS_ID),
        }
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        conn = client._connection = _Connection(RESOURCE)
        ds = client.create_dataset(Dataset(DS_ID))
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'datasetReference':
                {'projectId': PROJECT, 'datasetId': DS_ID},
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(ds.dataset_id, DS_ID)
        self.assertEqual(ds.project, PROJECT)
        self.assertEqual(ds.etag, RESOURCE['etag'])
        self.assertEqual(ds.full_dataset_id, RESOURCE['id'])

    def test_create_dataset_w_attrs(self):
        from google.cloud.bigquery.dataset import Dataset, AccessEntry

        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        PATH = 'projects/%s/datasets' % PROJECT
        DESCRIPTION = 'DESC'
        FRIENDLY_NAME = 'FN'
        LOCATION = 'US'
        USER_EMAIL = 'phred@example.com'
        VIEW = {
            'projectId': 'my-proj',
            'datasetId': 'starry-skies',
            'tableId': 'northern-hemisphere',
        }
        RESOURCE = {
            'datasetReference':
                {'projectId': PROJECT, 'datasetId': DS_ID},
            'etag': "etag",
            'id': "%s:%s" % (PROJECT, DS_ID),
            'description': DESCRIPTION,
            'friendlyName': FRIENDLY_NAME,
            'location': LOCATION,
            'defaultTableExpirationMs': 3600,
            'access': [
                {'role': 'OWNER', 'userByEmail': USER_EMAIL},
                {'view': VIEW}],
        }
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        conn = client._connection = _Connection(RESOURCE)
        entries = [AccessEntry('OWNER', 'userByEmail', USER_EMAIL),
                   AccessEntry(None, 'view', VIEW)]
        ds_arg = Dataset(DS_ID, project=PROJECT, access_entries=entries)
        ds_arg.description = DESCRIPTION
        ds_arg.friendly_name = FRIENDLY_NAME
        ds_arg.default_table_expiration_ms = 3600
        ds_arg.location = LOCATION
        ds = client.create_dataset(ds_arg)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'datasetReference':
                {'projectId': PROJECT, 'datasetId': DS_ID},
            'description': DESCRIPTION,
            'friendlyName': FRIENDLY_NAME,
            'location': LOCATION,
            'defaultTableExpirationMs': 3600,
            'access': [
                {'role': 'OWNER', 'userByEmail': USER_EMAIL},
                {'view': VIEW}],
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(ds.dataset_id, DS_ID)
        self.assertEqual(ds.project, PROJECT)
        self.assertEqual(ds.etag, RESOURCE['etag'])
        self.assertEqual(ds.full_dataset_id, RESOURCE['id'])
        self.assertEqual(ds.description, DESCRIPTION)
        self.assertEqual(ds.friendly_name, FRIENDLY_NAME)
        self.assertEqual(ds.location, LOCATION)
        self.assertEqual(ds.default_table_expiration_ms, 3600)

    def test_get_table(self):
        project = 'PROJECT'
        dataset_id = 'dataset_id'
        table_id = 'table-id'
        path = 'projects/%s/datasets/%s/tables/%s' % (
            project, dataset_id, table_id)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=project, credentials=creds, _http=http)
        resource = {
            'id': '%s:%s:%s' % (project, dataset_id, table_id),
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
        }
        conn = client._connection = _Connection(resource)
        table_ref = client.dataset(dataset_id).table(table_id)

        table = client.get_table(table_ref)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % path)
        self.assertEqual(table.table_id, table_id)

    def test_update_dataset_w_invalid_field(self):
        from google.cloud.bigquery.dataset import Dataset

        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        with self.assertRaises(ValueError):
            client.update_dataset(Dataset(DS_ID), ["foo"])

    def test_update_dataset(self):
        from google.cloud.bigquery.dataset import Dataset

        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        PATH = 'projects/%s/datasets/%s' % (PROJECT, DS_ID)
        DESCRIPTION = 'DESCRIPTION'
        FRIENDLY_NAME = 'TITLE'
        LOCATION = 'loc'
        EXP = 17
        RESOURCE = {
            'datasetReference':
                {'projectId': PROJECT, 'datasetId': DS_ID},
            'etag': "etag",
            'description': DESCRIPTION,
            'friendlyName': FRIENDLY_NAME,
            'location': LOCATION,
            'defaultTableExpirationMs': EXP,
        }
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        conn = client._connection = _Connection(RESOURCE, RESOURCE)
        ds = Dataset(DS_ID, project=PROJECT)
        ds.description = DESCRIPTION
        ds.friendly_name = FRIENDLY_NAME
        ds.location = LOCATION
        ds.default_table_expiration_ms = EXP
        ds2 = client.update_dataset(
            ds, ['description', 'friendly_name', 'location'])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        SENT = {
            'description': DESCRIPTION,
            'friendlyName': FRIENDLY_NAME,
            'location': LOCATION,
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(req['path'], '/' + PATH)
        self.assertIsNone(req['headers'])
        self.assertEqual(ds2.description, ds.description)
        self.assertEqual(ds2.friendly_name, ds.friendly_name)
        self.assertEqual(ds2.location, ds.location)

        # ETag becomes If-Match header.
        ds._properties['etag'] = 'etag'
        client.update_dataset(ds, [])
        req = conn._requested[1]
        self.assertEqual(req['headers']['If-Match'], 'etag')

    def test_list_dataset_tables_empty(self):
        import six

        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        conn = client._connection = _Connection({})

        dataset = client.dataset(DS_ID)
        iterator = client.list_dataset_tables(dataset)
        self.assertIs(iterator.dataset, dataset)
        page = six.next(iterator.pages)
        tables = list(page)
        token = iterator.next_page_token

        self.assertEqual(tables, [])
        self.assertIsNone(token)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        PATH = 'projects/%s/datasets/%s/tables' % (PROJECT, DS_ID)
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_dataset_tables_defaults(self):
        import six
        from google.cloud.bigquery.table import Table

        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        TABLE_1 = 'table_one'
        TABLE_2 = 'table_two'
        PATH = 'projects/%s/datasets/%s/tables' % (PROJECT, DS_ID)
        TOKEN = 'TOKEN'
        DATA = {
            'nextPageToken': TOKEN,
            'tables': [
                {'kind': 'bigquery#table',
                 'id': '%s:%s.%s' % (PROJECT, DS_ID, TABLE_1),
                 'tableReference': {'tableId': TABLE_1,
                                    'datasetId': DS_ID,
                                    'projectId': PROJECT},
                 'type': 'TABLE'},
                {'kind': 'bigquery#table',
                 'id': '%s:%s.%s' % (PROJECT, DS_ID, TABLE_2),
                 'tableReference': {'tableId': TABLE_2,
                                    'datasetId': DS_ID,
                                    'projectId': PROJECT},
                 'type': 'TABLE'},
            ]
        }

        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        conn = client._connection = _Connection(DATA)
        dataset = client.dataset(DS_ID)

        iterator = client.list_dataset_tables(dataset)
        self.assertIs(iterator.dataset, dataset)
        page = six.next(iterator.pages)
        tables = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(tables), len(DATA['tables']))
        for found, expected in zip(tables, DATA['tables']):
            self.assertIsInstance(found, Table)
            self.assertEqual(found.full_table_id, expected['id'])
            self.assertEqual(found.table_type, expected['type'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_dataset_tables_explicit(self):
        import six
        from google.cloud.bigquery.table import Table

        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        TABLE_1 = 'table_one'
        TABLE_2 = 'table_two'
        PATH = 'projects/%s/datasets/%s/tables' % (PROJECT, DS_ID)
        TOKEN = 'TOKEN'
        DATA = {
            'tables': [
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s.%s' % (PROJECT, DS_ID, TABLE_1),
                 'tableReference': {'tableId': TABLE_1,
                                    'datasetId': DS_ID,
                                    'projectId': PROJECT},
                 'type': 'TABLE'},
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s.%s' % (PROJECT, DS_ID, TABLE_2),
                 'tableReference': {'tableId': TABLE_2,
                                    'datasetId': DS_ID,
                                    'projectId': PROJECT},
                 'type': 'TABLE'},
            ]
        }

        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        conn = client._connection = _Connection(DATA)
        dataset = client.dataset(DS_ID)

        iterator = client.list_dataset_tables(
            dataset, max_results=3, page_token=TOKEN)
        self.assertIs(iterator.dataset, dataset)
        page = six.next(iterator.pages)
        tables = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(tables), len(DATA['tables']))
        for found, expected in zip(tables, DATA['tables']):
            self.assertIsInstance(found, Table)
            self.assertEqual(found.full_table_id, expected['id'])
            self.assertEqual(found.table_type, expected['type'])
        self.assertIsNone(token)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'maxResults': 3, 'pageToken': TOKEN})

    def test_list_dataset_tables_wrong_type(self):
        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.list_dataset_tables(client.dataset(DS_ID).table("foo"))

    def test_delete_dataset(self):
        from google.cloud.bigquery.dataset import Dataset

        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        PATH = 'projects/%s/datasets/%s' % (PROJECT, DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        conn = client._connection = _Connection({}, {})
        for arg in (client.dataset(DS_ID), Dataset(DS_ID, project=PROJECT)):
            client.delete_dataset(arg)
            req = conn._requested[0]
            self.assertEqual(req['method'], 'DELETE')
            self.assertEqual(req['path'], '/%s' % PATH)

    def test_delete_dataset_wrong_type(self):
        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.delete_dataset(client.dataset(DS_ID).table("foo"))

    def test_job_from_resource_unknown_type(self):
        PROJECT = 'PROJECT'
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        with self.assertRaises(ValueError):
            client.job_from_resource({'configuration': {'nonesuch': {}}})

    def test_get_job_miss_w_explict_project(self):
        from google.cloud.exceptions import NotFound

        PROJECT = 'PROJECT'
        OTHER_PROJECT = 'OTHER_PROJECT'
        JOB_ID = 'NONESUCH'
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        conn = client._connection = _Connection()

        with self.assertRaises(NotFound):
            client.get_job(JOB_ID, project=OTHER_PROJECT)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/OTHER_PROJECT/jobs/NONESUCH')
        self.assertEqual(req['query_params'], {'projection': 'full'})

    def test_get_job_hit(self):
        from google.cloud.bigquery.job import QueryJob

        PROJECT = 'PROJECT'
        JOB_ID = 'query_job'
        DATASET = 'test_dataset'
        QUERY_DESTINATION_TABLE = 'query_destination_table'
        QUERY = 'SELECT * from test_dataset:test_table'
        ASYNC_QUERY_DATA = {
            'id': '{}:{}'.format(PROJECT, JOB_ID),
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
        creds = _make_credentials()
        client = self._make_one(PROJECT, creds)
        conn = client._connection = _Connection(ASYNC_QUERY_DATA)

        job = client.get_job(JOB_ID)

        self.assertIsInstance(job, QueryJob)
        self.assertEqual(job.job_id, JOB_ID)
        self.assertEqual(job.create_disposition, 'CREATE_IF_NEEDED')
        self.assertEqual(job.write_disposition, 'WRITE_TRUNCATE')

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs/query_job')
        self.assertEqual(req['query_params'], {'projection': 'full'})

    def test_list_jobs_defaults(self):
        import six
        from google.cloud.bigquery.job import LoadJob
        from google.cloud.bigquery.job import CopyJob
        from google.cloud.bigquery.job import ExtractJob
        from google.cloud.bigquery.job import QueryJob

        PROJECT = 'PROJECT'
        DATASET = 'test_dataset'
        SOURCE_TABLE = 'source_table'
        DESTINATION_TABLE = 'destination_table'
        QUERY_DESTINATION_TABLE = 'query_destination_table'
        SOURCE_URI = 'gs://test_bucket/src_object*'
        DESTINATION_URI = 'gs://test_bucket/dst_object*'
        JOB_TYPES = {
            'load_job': LoadJob,
            'copy_job': CopyJob,
            'extract_job': ExtractJob,
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
            self.assertEqual(found.job_id, name)
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'projection': 'full'})

    def test_list_jobs_load_job_wo_sourceUris(self):
        import six
        from google.cloud.bigquery.job import LoadJob

        PROJECT = 'PROJECT'
        DATASET = 'test_dataset'
        SOURCE_TABLE = 'source_table'
        JOB_TYPES = {
            'load_job': LoadJob,
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
            self.assertEqual(found.job_id, name)
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
        from google.cloud.bigquery.job import LoadJob

        PROJECT = 'PROJECT'
        JOB = 'job_name'
        DATASET = 'dataset_name'
        DESTINATION = 'destination_table'
        SOURCE_URI = 'http://example.com/source.csv'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        dataset = client.dataset(DATASET)
        destination = dataset.table(DESTINATION)
        job = client.load_table_from_storage(JOB, destination, SOURCE_URI)
        self.assertIsInstance(job, LoadJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
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
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        dataset = client.dataset(DATASET)
        source = dataset.table(SOURCE)
        destination = dataset.table(DESTINATION)
        job = client.copy_table(JOB, destination, source)
        self.assertIsInstance(job, CopyJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.sources), [source])
        self.assertIs(job.destination, destination)

    def test_extract_table(self):
        from google.cloud.bigquery.job import ExtractJob

        PROJECT = 'PROJECT'
        JOB = 'job_id'
        DATASET = 'dataset_id'
        SOURCE = 'source_table'
        DESTINATION = 'gs://bucket_name/object_name'
        RESOURCE = {
            'jobReference': {
                'projectId': PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': SOURCE,
                    },
                    'destinationUris': [DESTINATION],
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(RESOURCE)
        dataset = client.dataset(DATASET)
        source = dataset.table(SOURCE)

        job = client.extract_table(source, DESTINATION, job_id=JOB)

        # Check that extract_table actually starts the job.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs')

        # Check the job resource.
        self.assertIsInstance(job, ExtractJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(job.source, source)
        self.assertEqual(list(job.destination_uris), [DESTINATION])

    def test_extract_table_generated_job_id(self):
        from google.cloud.bigquery.job import ExtractJob
        from google.cloud.bigquery.job import ExtractJobConfig
        from google.cloud.bigquery.job import DestinationFormat

        PROJECT = 'PROJECT'
        JOB = 'job_id'
        DATASET = 'dataset_id'
        SOURCE = 'source_table'
        DESTINATION = 'gs://bucket_name/object_name'
        RESOURCE = {
            'jobReference': {
                'projectId': PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': SOURCE,
                    },
                    'destinationUris': [DESTINATION],
                    'destinationFormat': 'NEWLINE_DELIMITED_JSON',
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(RESOURCE)
        dataset = client.dataset(DATASET)
        source = dataset.table(SOURCE)
        job_config = ExtractJobConfig()
        job_config.destination_format = (
            DestinationFormat.NEWLINE_DELIMITED_JSON)

        job = client.extract_table(source, DESTINATION, job_config=job_config)

        # Check that extract_table actually starts the job.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs')
        self.assertIsInstance(
            req['data']['jobReference']['jobId'], six.string_types)

        # Check the job resource.
        self.assertIsInstance(job, ExtractJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.source, source)
        self.assertEqual(list(job.destination_uris), [DESTINATION])

    def test_run_async_query_defaults(self):
        from google.cloud.bigquery.job import QueryJob

        PROJECT = 'PROJECT'
        JOB = 'job_name'
        QUERY = 'select count(*) from persons'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        job = client.run_async_query(JOB, QUERY)
        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
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
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        job = client.run_async_query(JOB, QUERY, udf_resources=udf_resources)
        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
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
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        query_parameters = [ScalarQueryParameter('foo', 'INT64', 123)]
        job = client.run_async_query(JOB, QUERY,
                                     query_parameters=query_parameters)
        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(job.query_parameters, query_parameters)

    def test_run_sync_query_defaults(self):
        from google.cloud.bigquery.query import QueryResults

        PROJECT = 'PROJECT'
        QUERY = 'select count(*) from persons'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
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
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
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
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
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
        from google.cloud.exceptions import NotFound
        self._requested.append(kw)

        if len(self._responses) == 0:
            raise NotFound('miss')

        response, self._responses = self._responses[0], self._responses[1:]
        return response
