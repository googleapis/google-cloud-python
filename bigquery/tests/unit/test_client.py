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

import copy
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
        ds = client.create_dataset(Dataset(client.dataset(DS_ID)))
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'datasetReference':
                {'projectId': PROJECT, 'datasetId': DS_ID},
            'labels': {},
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
        LABELS = {'color': 'red'}
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
            'labels': LABELS,
            'access': [
                {'role': 'OWNER', 'userByEmail': USER_EMAIL},
                {'view': VIEW}],
        }
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        conn = client._connection = _Connection(RESOURCE)
        entries = [AccessEntry('OWNER', 'userByEmail', USER_EMAIL),
                   AccessEntry(None, 'view', VIEW)]
        ds_arg = Dataset(client.dataset(DS_ID))
        ds_arg.access_entries = entries
        ds_arg.description = DESCRIPTION
        ds_arg.friendly_name = FRIENDLY_NAME
        ds_arg.default_table_expiration_ms = 3600
        ds_arg.location = LOCATION
        ds_arg.labels = LABELS
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
            'labels': LABELS,
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
        self.assertEqual(ds.labels, LABELS)

    def test_create_table_w_day_partition(self):
        from google.cloud.bigquery.table import Table

        project = 'PROJECT'
        dataset_id = 'dataset_id'
        table_id = 'table-id'
        path = 'projects/%s/datasets/%s/tables' % (
            project, dataset_id)
        creds = _make_credentials()
        client = self._make_one(project=project, credentials=creds)
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
        table = Table(table_ref, client=client)
        table.partitioning_type = 'DAY'

        got = client.create_table(table)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'timePartitioning': {'type': 'DAY'},
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(table.partitioning_type, "DAY")
        self.assertEqual(got.table_id, table_id)

    def test_create_table_w_day_partition_and_expire(self):
        from google.cloud.bigquery.table import Table

        project = 'PROJECT'
        dataset_id = 'dataset_id'
        table_id = 'table-id'
        path = 'projects/%s/datasets/%s/tables' % (
            project, dataset_id)
        creds = _make_credentials()
        client = self._make_one(project=project, credentials=creds)
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
        table = Table(table_ref, client=client)
        table.partitioning_type = 'DAY'
        table.partition_expiration = 100

        got = client.create_table(table)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'timePartitioning': {'type': 'DAY', 'expirationMs': 100},
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(table.partitioning_type, "DAY")
        self.assertEqual(table.partition_expiration, 100)
        self.assertEqual(got.table_id, table_id)

    def test_create_table_w_schema_and_query(self):
        from google.cloud.bigquery.table import Table, SchemaField

        project = 'PROJECT'
        dataset_id = 'dataset_id'
        table_id = 'table-id'
        path = 'projects/%s/datasets/%s/tables' % (
            project, dataset_id)
        query = 'SELECT * from %s:%s' % (dataset_id, table_id)
        creds = _make_credentials()
        client = self._make_one(project=project, credentials=creds)
        resource = {
            'id': '%s:%s:%s' % (project, dataset_id, table_id),
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]
            },
            'view': {'query': query},
        }
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        conn = client._connection = _Connection(resource)
        table_ref = client.dataset(dataset_id).table(table_id)
        table = Table(table_ref, schema=schema, client=client)
        table.view_query = query

        got = client.create_table(table)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]
            },
            'view': {'query': query},
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(got.table_id, table_id)
        self.assertEqual(got.project, project)
        self.assertEqual(got.dataset_id, dataset_id)
        self.assertEqual(got.schema, schema)
        self.assertEqual(got.view_query, query)

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
            client.update_dataset(Dataset(client.dataset(DS_ID)), ["foo"])

    def test_update_dataset(self):
        from google.cloud.bigquery.dataset import Dataset

        PROJECT = 'PROJECT'
        DS_ID = 'DATASET_ID'
        PATH = 'projects/%s/datasets/%s' % (PROJECT, DS_ID)
        DESCRIPTION = 'DESCRIPTION'
        FRIENDLY_NAME = 'TITLE'
        LOCATION = 'loc'
        LABELS = {'priority': 'high'}
        EXP = 17
        RESOURCE = {
            'datasetReference':
                {'projectId': PROJECT, 'datasetId': DS_ID},
            'etag': "etag",
            'description': DESCRIPTION,
            'friendlyName': FRIENDLY_NAME,
            'location': LOCATION,
            'defaultTableExpirationMs': EXP,
            'labels': LABELS,
        }
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        conn = client._connection = _Connection(RESOURCE, RESOURCE)
        ds = Dataset(client.dataset(DS_ID))
        ds.description = DESCRIPTION
        ds.friendly_name = FRIENDLY_NAME
        ds.location = LOCATION
        ds.default_table_expiration_ms = EXP
        ds.labels = LABELS
        ds2 = client.update_dataset(
            ds, ['description', 'friendly_name', 'location', 'labels'])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        SENT = {
            'description': DESCRIPTION,
            'friendlyName': FRIENDLY_NAME,
            'location': LOCATION,
            'labels': LABELS,
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(req['path'], '/' + PATH)
        self.assertIsNone(req['headers'])
        self.assertEqual(ds2.description, ds.description)
        self.assertEqual(ds2.friendly_name, ds.friendly_name)
        self.assertEqual(ds2.location, ds.location)
        self.assertEqual(ds2.labels, ds.labels)

        # ETag becomes If-Match header.
        ds._properties['etag'] = 'etag'
        client.update_dataset(ds, [])
        req = conn._requested[1]
        self.assertEqual(req['headers']['If-Match'], 'etag')

    def test_update_table(self):
        from google.cloud.bigquery.table import Table, SchemaField

        project = 'PROJECT'
        dataset_id = 'DATASET_ID'
        table_id = 'table_id'
        path = 'projects/%s/datasets/%s/tables/%s' % (
            project, dataset_id, table_id)
        description = 'description'
        title = 'title'
        resource = {
            'id': '%s:%s:%s' % (project, dataset_id, table_id),
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]
            },
            'etag': 'etag',
            'description': description,
            'friendlyName': title,
        }
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        creds = _make_credentials()
        client = self._make_one(project=project, credentials=creds)
        conn = client._connection = _Connection(resource, resource)
        table_ref = client.dataset(dataset_id).table(table_id)
        table = Table(table_ref, schema=schema, client=client)
        table.description = description
        table.friendly_name = title

        updated_table = client.update_table(
            table, ['schema', 'description', 'friendly_name'])

        sent = {
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
            'description': description,
            'friendlyName': title,
        }
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        self.assertEqual(req['data'], sent)
        self.assertEqual(req['path'], '/' + path)
        self.assertIsNone(req['headers'])
        self.assertEqual(updated_table.description, table.description)
        self.assertEqual(updated_table.friendly_name, table.friendly_name)
        self.assertEqual(updated_table.schema, table.schema)

        # ETag becomes If-Match header.
        table._properties['etag'] = 'etag'
        client.update_table(table, [])
        req = conn._requested[1]
        self.assertEqual(req['headers']['If-Match'], 'etag')

    def test_update_table_only_use_legacy_sql(self):
        from google.cloud.bigquery.table import Table

        project = 'PROJECT'
        dataset_id = 'DATASET_ID'
        table_id = 'table_id'
        path = 'projects/%s/datasets/%s/tables/%s' % (
            project, dataset_id, table_id)
        resource = {
            'id': '%s:%s:%s' % (project, dataset_id, table_id),
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'view': {'useLegacySql': True}
        }
        creds = _make_credentials()
        client = self._make_one(project=project, credentials=creds)
        conn = client._connection = _Connection(resource)
        table_ref = client.dataset(dataset_id).table(table_id)
        table = Table(table_ref, client=client)
        table.view_use_legacy_sql = True

        updated_table = client.update_table(table, ['view_use_legacy_sql'])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'view': {'useLegacySql': True}
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(
            updated_table.view_use_legacy_sql, table.view_use_legacy_sql)

    def test_update_table_w_query(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis
        from google.cloud.bigquery.table import Table, SchemaField

        project = 'PROJECT'
        dataset_id = 'DATASET_ID'
        table_id = 'table_id'
        path = 'projects/%s/datasets/%s/tables/%s' % (
            project, dataset_id, table_id)
        query = 'select fullname, age from person_ages'
        location = 'EU'
        exp_time = datetime.datetime(2015, 8, 1, 23, 59, 59, tzinfo=UTC)
        schema_resource = {'fields': [
            {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]}
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        resource = {
            'id': '%s:%s:%s' % (project, dataset_id, table_id),
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'schema': schema_resource,
            'view': {'query': query, 'useLegacySql': True},
            'location': location,
            'expirationTime': _millis(exp_time)
        }
        creds = _make_credentials()
        client = self._make_one(project=project, credentials=creds)
        conn = client._connection = _Connection(resource)
        table_ref = client.dataset(dataset_id).table(table_id)
        table = Table(table_ref, schema=schema, client=client)
        table.location = location
        table.expires = exp_time
        table.view_query = query
        table.view_use_legacy_sql = True
        updated_properties = ['schema', 'view_query', 'location',
                              'expires', 'view_use_legacy_sql']

        updated_table = client.update_table(table, updated_properties)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'view': {'query': query, 'useLegacySql': True},
            'location': location,
            'expirationTime': _millis(exp_time),
            'schema': schema_resource,
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(updated_table.schema, table.schema)
        self.assertEqual(updated_table.view_query, table.view_query)
        self.assertEqual(updated_table.location, table.location)
        self.assertEqual(updated_table.expires, table.expires)
        self.assertEqual(
            updated_table.view_use_legacy_sql, table.view_use_legacy_sql)

    def test_update_table_w_schema_None(self):
        # Simulate deleting schema:  not sure if back-end will actually
        # allow this operation, but the spec says it is optional.
        from google.cloud.bigquery.table import Table, SchemaField

        project = 'PROJECT'
        dataset_id = 'DATASET_ID'
        table_id = 'table_id'
        path = 'projects/%s/datasets/%s/tables/%s' % (
            project, dataset_id, table_id)
        resource = {
            'id': '%s:%s:%s' % (project, dataset_id, table_id),
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id},
            'schema': {'fields': []}
        }
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        creds = _make_credentials()
        client = self._make_one(project=project, credentials=creds)
        conn = client._connection = _Connection(resource)
        table_ref = client.dataset(dataset_id).table(table_id)
        table = Table(table_ref, schema=schema, client=client)
        table.schema = None

        updated_table = client.update_table(table, ['schema'])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        sent = {
            'tableReference': {
                'projectId': project,
                'datasetId': dataset_id,
                'tableId': table_id
            },
            'schema': {'fields': []}
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(req['path'], '/%s' % path)
        self.assertEqual(updated_table.schema, table.schema)

    def test_list_dataset_tables_empty(self):
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
        ds_ref = client.dataset(DS_ID)
        for arg in (ds_ref, Dataset(ds_ref)):
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

    def test_delete_table(self):
        from google.cloud.bigquery.table import Table

        project = 'PROJECT'
        dataset_id = 'dataset_id'
        table_id = 'table-id'
        path = 'projects/%s/datasets/%s/tables/%s' % (
            project, dataset_id, table_id)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=project, credentials=creds, _http=http)
        conn = client._connection = _Connection({}, {})
        table_ref = client.dataset(dataset_id).table(table_id)

        for arg in (table_ref, Table(table_ref)):
            client.delete_table(arg)
            req = conn._requested[0]
            self.assertEqual(req['method'], 'DELETE')
            self.assertEqual(req['path'], '/%s' % path)

    def test_delete_table_w_wrong_type(self):
        project = 'PROJECT'
        dataset_id = 'DATASET_ID'
        creds = _make_credentials()
        client = self._make_one(project=project, credentials=creds)
        with self.assertRaises(TypeError):
            client.delete_table(client.dataset(dataset_id))

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
        RESOURCE = {
            'jobReference': {
                'projectId': PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'load': {
                    'sourceUris': [SOURCE_URI],
                    'destinationTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': DESTINATION,
                    },
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(RESOURCE)
        destination = client.dataset(DATASET).table(DESTINATION)

        job = client.load_table_from_storage(SOURCE_URI, destination,
                                             job_id=JOB)

        # Check that load_table_from_storage actually starts the job.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/%s/jobs' % PROJECT)

        self.assertIsInstance(job, LoadJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.source_uris), [SOURCE_URI])
        self.assertIs(job.destination, destination)

        conn = client._connection = _Connection(RESOURCE)

        job = client.load_table_from_storage([SOURCE_URI], destination,
                                             job_id=JOB)
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
        RESOURCE = {
            'jobReference': {
                'projectId': PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'copy': {
                    'sourceTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': SOURCE,
                    },
                    'destinationTable': {
                        'projectId': PROJECT,
                        'datasetId': DATASET,
                        'tableId': DESTINATION,
                    },
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(RESOURCE)
        dataset = client.dataset(DATASET)
        source = dataset.table(SOURCE)
        destination = dataset.table(DESTINATION)

        job = client.copy_table(source, destination, job_id=JOB)

        # Check that copy_table actually starts the job.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/%s/jobs' % PROJECT)

        self.assertIsInstance(job, CopyJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.sources), [source])
        self.assertIs(job.destination, destination)

        conn = client._connection = _Connection(RESOURCE)
        source2 = dataset.table(SOURCE + '2')
        job = client.copy_table([source, source2], destination, job_id=JOB)
        self.assertIsInstance(job, CopyJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.sources), [source, source2])
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

    def test_query_rows_defaults(self):
        from google.api.core.page_iterator import HTTPIterator

        JOB = 'job-id'
        PROJECT = 'PROJECT'
        QUERY = 'SELECT COUNT(*) FROM persons'
        RESOURCE = {
            'jobReference': {
                'projectId': PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'query': {
                    'query': QUERY,
                },
            },
            'status': {
                'state': 'DONE',
            },
        }
        RESULTS_RESOURCE = {
            'jobReference': RESOURCE['jobReference'],
            'jobComplete': True,
            'schema': {
                'fields': [
                    {'name': 'field0', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                ]
            },
            'totalRows': '3',
            'pageToken': 'next-page',
        }
        FIRST_PAGE = copy.deepcopy(RESULTS_RESOURCE)
        FIRST_PAGE['rows'] = [
            {'f': [{'v': '1'}]},
            {'f': [{'v': '2'}]},
        ]
        LAST_PAGE = copy.deepcopy(RESULTS_RESOURCE)
        LAST_PAGE['rows'] = [
            {'f': [{'v': '3'}]},
        ]
        del LAST_PAGE['pageToken']
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(
            RESOURCE, RESULTS_RESOURCE, FIRST_PAGE, LAST_PAGE)

        rows_iter = client.query_rows(QUERY)
        rows = list(rows_iter)

        self.assertEqual(rows, [(1,), (2,), (3,)])
        self.assertIs(rows_iter.client, client)
        self.assertIsInstance(rows_iter, HTTPIterator)
        self.assertEqual(len(conn._requested), 4)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs')
        self.assertIsInstance(
            req['data']['jobReference']['jobId'], six.string_types)

    def test_query_rows_w_job_id(self):
        from google.api.core.page_iterator import HTTPIterator

        JOB = 'job-id'
        PROJECT = 'PROJECT'
        QUERY = 'SELECT COUNT(*) FROM persons'
        RESOURCE = {
            'jobReference': {
                'projectId': PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'query': {
                    'query': QUERY,
                },
            },
            'status': {
                'state': 'DONE',
            },
        }
        RESULTS_RESOURCE = {
            'jobReference': RESOURCE['jobReference'],
            'jobComplete': True,
            'schema': {
                'fields': [
                    {'name': 'field0', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                ]
            },
            'totalRows': '0',
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(
            RESOURCE, RESULTS_RESOURCE, RESULTS_RESOURCE)

        rows_iter = client.query_rows(QUERY, job_id=JOB)
        rows = list(rows_iter)

        self.assertEqual(rows, [])
        self.assertIs(rows_iter.client, client)
        self.assertIsInstance(rows_iter, HTTPIterator)
        self.assertEqual(len(conn._requested), 3)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs')
        self.assertEqual(req['data']['jobReference']['jobId'], JOB)

    def test_query_rows_w_job_config(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.api.core.page_iterator import HTTPIterator

        JOB = 'job-id'
        PROJECT = 'PROJECT'
        QUERY = 'SELECT COUNT(*) FROM persons'
        RESOURCE = {
            'jobReference': {
                'projectId': PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'query': {
                    'query': QUERY,
                    'useLegacySql': True,
                },
                'dryRun': True,
            },
            'status': {
                'state': 'DONE',
            },
        }
        RESULTS_RESOURCE = {
            'jobReference': RESOURCE['jobReference'],
            'jobComplete': True,
            'schema': {
                'fields': [
                    {'name': 'field0', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                ]
            },
            'totalRows': '0',
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(
            RESOURCE, RESULTS_RESOURCE, RESULTS_RESOURCE)

        job_config = QueryJobConfig()
        job_config.use_legacy_sql = True
        job_config.dry_run = True
        rows_iter = client.query_rows(QUERY, job_id=JOB, job_config=job_config)

        self.assertIsInstance(rows_iter, HTTPIterator)
        self.assertEqual(len(conn._requested), 2)
        req = conn._requested[0]
        configuration = req['data']['configuration']
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs')
        self.assertEqual(req['data']['jobReference']['jobId'], JOB)
        self.assertEqual(configuration['query']['useLegacySql'], True)
        self.assertEqual(configuration['dryRun'], True)

    def test_list_rows(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.table import Table, SchemaField

        PROJECT = 'PROJECT'
        DS_ID = 'DS_ID'
        TABLE_ID = 'TABLE_ID'
        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            PROJECT, DS_ID, TABLE_ID)
        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(
            tzinfo=UTC)
        WHEN_1 = WHEN + datetime.timedelta(seconds=1)
        WHEN_2 = WHEN + datetime.timedelta(seconds=2)
        ROWS = 1234
        TOKEN = 'TOKEN'

        def _bigquery_timestamp_float_repr(ts_float):
            # Preserve microsecond precision for E+09 timestamps
            return '%0.15E' % (ts_float,)

        DATA = {
            'totalRows': str(ROWS),
            'pageToken': TOKEN,
            'rows': [
                {'f': [
                    {'v': 'Phred Phlyntstone'},
                    {'v': '32'},
                    {'v': _bigquery_timestamp_float_repr(WHEN_TS)},
                ]},
                {'f': [
                    {'v': 'Bharney Rhubble'},
                    {'v': '33'},
                    {'v': _bigquery_timestamp_float_repr(WHEN_TS + 1)},
                ]},
                {'f': [
                    {'v': 'Wylma Phlyntstone'},
                    {'v': '29'},
                    {'v': _bigquery_timestamp_float_repr(WHEN_TS + 2)},
                ]},
                {'f': [
                    {'v': 'Bhettye Rhubble'},
                    {'v': None},
                    {'v': None},
                ]},
            ]
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(DATA, DATA)
        table_ref = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='NULLABLE')
        joined = SchemaField('joined', 'TIMESTAMP', mode='NULLABLE')
        table = Table(table_ref, schema=[full_name, age, joined])

        iterator = client.list_rows(table)
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ('Phred Phlyntstone', 32, WHEN))
        self.assertEqual(rows[1], ('Bharney Rhubble', 33, WHEN_1))
        self.assertEqual(rows[2], ('Wylma Phlyntstone', 29, WHEN_2))
        self.assertEqual(rows[3], ('Bhettye Rhubble', None, None))
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {})

    def test_list_rows_query_params(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.table import Table, SchemaField

        PROJECT = 'PROJECT'
        DS_ID = 'DS_ID'
        TABLE_ID = 'TABLE_ID'
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        table_ref = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)
        table = Table(table_ref,
                      schema=[SchemaField('age', 'INTEGER', mode='NULLABLE')])
        tests = [
            ({}, {}),
            ({'start_index': 1}, {'startIndex': 1}),
            ({'max_results': 2}, {'maxResults': 2}),
            ({'start_index': 1, 'max_results': 2},
             {'startIndex': 1, 'maxResults': 2}),
        ]
        conn = client._connection = _Connection(*len(tests)*[{}])
        for i, test in enumerate(tests):
            iterator = client.list_rows(table, **test[0])
            six.next(iterator.pages)
            req = conn._requested[i]
            self.assertEqual(req['query_params'], test[1],
                             'for kwargs %s' % test[0])

    def test_list_rows_repeated_fields(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.table import SchemaField

        PROJECT = 'PROJECT'
        DS_ID = 'DS_ID'
        TABLE_ID = 'TABLE_ID'
        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            PROJECT, DS_ID, TABLE_ID)
        ROWS = 1234
        TOKEN = 'TOKEN'
        DATA = {
            'totalRows': ROWS,
            'pageToken': TOKEN,
            'rows': [
                {'f': [
                    {'v': [{'v': 'red'}, {'v': 'green'}]},
                    {'v': [{
                        'v': {
                            'f': [
                                {'v': [{'v': '1'}, {'v': '2'}]},
                                {'v': [{'v': '3.1415'}, {'v': '1.414'}]},
                            ]}
                    }]},
                ]},
            ]
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(DATA)
        table_ref = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)
        color = SchemaField('color', 'STRING', mode='REPEATED')
        index = SchemaField('index', 'INTEGER', 'REPEATED')
        score = SchemaField('score', 'FLOAT', 'REPEATED')
        struct = SchemaField('struct', 'RECORD', mode='REPEATED',
                             fields=[index, score])

        iterator = client.list_rows(table_ref, selected_fields=[color, struct])
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], ['red', 'green'])
        self.assertEqual(rows[0][1], [{'index': [1, 2],
                                       'score': [3.1415, 1.414]}])
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_rows_w_record_schema(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.table import Table, SchemaField

        PROJECT = 'PROJECT'
        DS_ID = 'DS_ID'
        TABLE_ID = 'TABLE_ID'
        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            PROJECT, DS_ID, TABLE_ID)
        ROWS = 1234
        TOKEN = 'TOKEN'
        DATA = {
            'totalRows': ROWS,
            'pageToken': TOKEN,
            'rows': [
                {'f': [
                    {'v': 'Phred Phlyntstone'},
                    {'v': {'f': [{'v': '800'}, {'v': '555-1212'}, {'v': 1}]}},
                ]},
                {'f': [
                    {'v': 'Bharney Rhubble'},
                    {'v': {'f': [{'v': '877'}, {'v': '768-5309'}, {'v': 2}]}},
                ]},
                {'f': [
                    {'v': 'Wylma Phlyntstone'},
                    {'v': None},
                ]},
            ]
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection(DATA)
        table_ref = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        area_code = SchemaField('area_code', 'STRING', 'REQUIRED')
        local_number = SchemaField('local_number', 'STRING', 'REQUIRED')
        rank = SchemaField('rank', 'INTEGER', 'REQUIRED')
        phone = SchemaField('phone', 'RECORD', mode='NULLABLE',
                            fields=[area_code, local_number, rank])
        table = Table(table_ref, schema=[full_name, phone])

        iterator = client.list_rows(table)
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0][0], 'Phred Phlyntstone')
        self.assertEqual(rows[0][1], {'area_code': '800',
                                      'local_number': '555-1212',
                                      'rank': 1})
        self.assertEqual(rows[1][0], 'Bharney Rhubble')
        self.assertEqual(rows[1][1], {'area_code': '877',
                                      'local_number': '768-5309',
                                      'rank': 2})
        self.assertEqual(rows[2][0], 'Wylma Phlyntstone')
        self.assertIsNone(rows[2][1])
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_rows_errors(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.table import Table

        PROJECT = 'PROJECT'
        DS_ID = 'DS_ID'
        TABLE_ID = 'TABLE_ID'

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        table_ref = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)

        # table ref with no selected fields
        with self.assertRaises(ValueError):
            client.list_rows(table_ref)

        # table with no schema
        with self.assertRaises(ValueError):
            client.list_rows(Table(table_ref))

        # neither Table nor tableReference
        with self.assertRaises(TypeError):
            client.list_rows(1)


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
