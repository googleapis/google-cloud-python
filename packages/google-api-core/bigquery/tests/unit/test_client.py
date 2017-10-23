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
import email
import io
import json
import unittest

import mock
import six
from six.moves import http_client
import pytest

from google.cloud.bigquery.dataset import DatasetReference


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):

    PROJECT = 'PROJECT'
    DS_ID = 'DATASET_ID'
    TABLE_ID = 'TABLE_ID'
    TABLE_REF = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.client import Client

        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        from google.cloud.bigquery._http import Connection

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)

    def test__get_query_results_miss_w_explicit_project_and_timeout(self):
        from google.cloud.exceptions import NotFound

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = _Connection()

        with self.assertRaises(NotFound):
            client._get_query_results(
                'nothere', None, project='other-project', timeout_ms=500)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(
            req['path'], '/projects/other-project/queries/nothere')
        self.assertEqual(
            req['query_params'], {'maxResults': 0, 'timeoutMs': 500})

    def test__get_query_results_hit(self):
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
                'projectId': self.PROJECT,
                'jobId': job_id,
            },
            'totalRows': '10',
            'totalBytesProcessed': '2464625',
            'jobComplete': True,
            'cacheHit': False,
        }

        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        client._connection = _Connection(data)
        query_results = client._get_query_results(job_id, None)

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
        PATH = 'projects'
        TOKEN = 'TOKEN'
        DATA = {}
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
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

        DATASET_1 = 'dataset_one'
        DATASET_2 = 'dataset_two'
        PATH = 'projects/%s/datasets' % self.PROJECT
        TOKEN = 'TOKEN'
        DATA = {
            'nextPageToken': TOKEN,
            'datasets': [
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s' % (self.PROJECT, DATASET_1),
                 'datasetReference': {'datasetId': DATASET_1,
                                      'projectId': self.PROJECT},
                 'friendlyName': None},
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s' % (self.PROJECT, DATASET_2),
                 'datasetReference': {'datasetId': DATASET_2,
                                      'projectId': self.PROJECT},
                 'friendlyName': 'Two'},
            ]
        }
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
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
        PATH = 'projects/%s/datasets' % self.PROJECT
        TOKEN = 'TOKEN'
        FILTER = 'FILTER'
        DATA = {}
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        conn = client._connection = _Connection(DATA)

        iterator = client.list_datasets(
            include_all=True, filter=FILTER,
            max_results=3, page_token=TOKEN)
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
                         {'all': True, 'filter': FILTER,
                          'maxResults': 3, 'pageToken': TOKEN})

    def test_dataset_with_specified_project(self):
        from google.cloud.bigquery.dataset import DatasetReference

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        dataset = client.dataset(self.DS_ID, self.PROJECT)
        self.assertIsInstance(dataset, DatasetReference)
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)

    def test_dataset_with_default_project(self):
        from google.cloud.bigquery.dataset import DatasetReference

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        dataset = client.dataset(self.DS_ID)
        self.assertIsInstance(dataset, DatasetReference)
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)

    def test_get_dataset(self):
        from google.cloud.exceptions import ServerError

        path = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        resource = {
            'id': '%s:%s' % (self.PROJECT, self.DS_ID),
            'datasetReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
            },
        }
        conn = client._connection = _Connection(resource)
        dataset_ref = client.dataset(self.DS_ID)

        dataset = client.get_dataset(dataset_ref)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % path)
        self.assertEqual(dataset.dataset_id, self.DS_ID)

        # Test retry.

        # Not a cloud API exception (missing 'errors' field).
        client._connection = _Connection(Exception(''), resource)
        with self.assertRaises(Exception):
            client.get_dataset(dataset_ref)

        # Zero-length errors field.
        client._connection = _Connection(ServerError(''), resource)
        with self.assertRaises(ServerError):
            client.get_dataset(dataset_ref)

        # Non-retryable reason.
        client._connection = _Connection(
            ServerError('', errors=[{'reason': 'serious'}]),
            resource)
        with self.assertRaises(ServerError):
            client.get_dataset(dataset_ref)

        # Retryable reason, but retry is disabled.
        client._connection = _Connection(
            ServerError('', errors=[{'reason': 'backendError'}]),
            resource)
        with self.assertRaises(ServerError):
            client.get_dataset(dataset_ref, retry=None)

        # Retryable reason, default retry: success.
        client._connection = _Connection(
            ServerError('', errors=[{'reason': 'backendError'}]),
            resource)
        dataset = client.get_dataset(dataset_ref)
        self.assertEqual(dataset.dataset_id, self.DS_ID)

    def test_create_dataset_minimal(self):
        from google.cloud.bigquery.dataset import Dataset

        PATH = 'projects/%s/datasets' % self.PROJECT
        RESOURCE = {
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_ID},
            'etag': "etag",
            'id': "%s:%s" % (self.PROJECT, self.DS_ID),
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(RESOURCE)
        ds = client.create_dataset(Dataset(client.dataset(self.DS_ID)))
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_ID},
            'labels': {},
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(ds.dataset_id, self.DS_ID)
        self.assertEqual(ds.project, self.PROJECT)
        self.assertEqual(ds.etag, RESOURCE['etag'])
        self.assertEqual(ds.full_dataset_id, RESOURCE['id'])

    def test_create_dataset_w_attrs(self):
        from google.cloud.bigquery.dataset import Dataset, AccessEntry

        PATH = 'projects/%s/datasets' % self.PROJECT
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
                {'projectId': self.PROJECT, 'datasetId': self.DS_ID},
            'etag': "etag",
            'id': "%s:%s" % (self.PROJECT, self.DS_ID),
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
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(RESOURCE)
        entries = [AccessEntry('OWNER', 'userByEmail', USER_EMAIL),
                   AccessEntry(None, 'view', VIEW)]
        ds_arg = Dataset(client.dataset(self.DS_ID))
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
                {'projectId': self.PROJECT, 'datasetId': self.DS_ID},
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
        self.assertEqual(ds.dataset_id, self.DS_ID)
        self.assertEqual(ds.project, self.PROJECT)
        self.assertEqual(ds.etag, RESOURCE['etag'])
        self.assertEqual(ds.full_dataset_id, RESOURCE['id'])
        self.assertEqual(ds.description, DESCRIPTION)
        self.assertEqual(ds.friendly_name, FRIENDLY_NAME)
        self.assertEqual(ds.location, LOCATION)
        self.assertEqual(ds.default_table_expiration_ms, 3600)
        self.assertEqual(ds.labels, LABELS)

    def test_create_table_w_day_partition(self):
        from google.cloud.bigquery.table import Table

        path = 'projects/%s/datasets/%s/tables' % (
            self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
        }
        conn = client._connection = _Connection(resource)
        table = Table(self.TABLE_REF)
        table.partitioning_type = 'DAY'

        got = client.create_table(table)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'timePartitioning': {'type': 'DAY'},
            'labels': {},
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(table.partitioning_type, "DAY")
        self.assertEqual(got.table_id, self.TABLE_ID)

    def test_create_table_w_day_partition_and_expire(self):
        from google.cloud.bigquery.table import Table

        path = 'projects/%s/datasets/%s/tables' % (
            self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
        }
        conn = client._connection = _Connection(resource)
        table = Table(self.TABLE_REF)
        table.partitioning_type = 'DAY'
        table.partition_expiration = 100

        got = client.create_table(table)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'timePartitioning': {'type': 'DAY', 'expirationMs': 100},
            'labels': {},
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(table.partitioning_type, "DAY")
        self.assertEqual(table.partition_expiration, 100)
        self.assertEqual(got.table_id, self.TABLE_ID)

    def test_create_table_w_schema_and_query(self):
        from google.cloud.bigquery.table import Table, SchemaField

        path = 'projects/%s/datasets/%s/tables' % (
            self.PROJECT, self.DS_ID)
        query = 'SELECT * from %s:%s' % (self.DS_ID, self.TABLE_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
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
        table = Table(self.TABLE_REF, schema=schema)
        table.view_query = query

        got = client.create_table(table)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID,
            },
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]
            },
            'view': {'query': query, 'useLegacySql': False},
            'labels': {},
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(got.table_id, self.TABLE_ID)
        self.assertEqual(got.project, self.PROJECT)
        self.assertEqual(got.dataset_id, self.DS_ID)
        self.assertEqual(got.schema, schema)
        self.assertEqual(got.view_query, query)

    def test_create_table_w_external(self):
        from google.cloud.bigquery.table import Table
        from google.cloud.bigquery.external_config import ExternalConfig

        path = 'projects/%s/datasets/%s/tables' % (
            self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        resource = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'externalDataConfiguration': {
                'sourceFormat': 'CSV',
                'autodetect': True,
            },
        }
        conn = client._connection = _Connection(resource)
        table = Table(self.TABLE_REF)
        ec = ExternalConfig('CSV')
        ec.autodetect = True
        table.external_data_configuration = ec

        got = client.create_table(table)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID,
            },
            'externalDataConfiguration': {
                'sourceFormat': 'CSV',
                'autodetect': True,
            },
            'labels': {},
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(got.table_id, self.TABLE_ID)
        self.assertEqual(got.project, self.PROJECT)
        self.assertEqual(got.dataset_id, self.DS_ID)
        self.assertEqual(got.external_data_configuration.source_format, 'CSV')
        self.assertEqual(got.external_data_configuration.autodetect, True)

    def test_get_table(self):
        path = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        resource = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID,
            },
        }
        conn = client._connection = _Connection(resource)
        table = client.get_table(self.TABLE_REF)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % path)
        self.assertEqual(table.table_id, self.TABLE_ID)

    def test_update_dataset_w_invalid_field(self):
        from google.cloud.bigquery.dataset import Dataset

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(ValueError):
            client.update_dataset(Dataset(client.dataset(self.DS_ID)), ["foo"])

    def test_update_dataset(self):
        from google.cloud.bigquery.dataset import Dataset, AccessEntry

        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_ID)
        DESCRIPTION = 'DESCRIPTION'
        FRIENDLY_NAME = 'TITLE'
        LOCATION = 'loc'
        LABELS = {'priority': 'high'}
        ACCESS = [
                {'role': 'OWNER', 'userByEmail': 'phred@example.com'},
        ]
        EXP = 17
        RESOURCE = {
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_ID},
            'etag': "etag",
            'description': DESCRIPTION,
            'friendlyName': FRIENDLY_NAME,
            'location': LOCATION,
            'defaultTableExpirationMs': EXP,
            'labels': LABELS,
            'access': ACCESS,
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(RESOURCE, RESOURCE)
        ds = Dataset(client.dataset(self.DS_ID))
        ds.description = DESCRIPTION
        ds.friendly_name = FRIENDLY_NAME
        ds.location = LOCATION
        ds.default_table_expiration_ms = EXP
        ds.labels = LABELS
        ds.access_entries = [
            AccessEntry('OWNER', 'userByEmail', 'phred@example.com')]
        ds2 = client.update_dataset(
            ds, ['description', 'friendly_name', 'location', 'labels',
                 'access_entries'])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        SENT = {
            'description': DESCRIPTION,
            'friendlyName': FRIENDLY_NAME,
            'location': LOCATION,
            'labels': LABELS,
            'access': ACCESS,
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(req['path'], '/' + PATH)
        self.assertIsNone(req['headers'])
        self.assertEqual(ds2.description, ds.description)
        self.assertEqual(ds2.friendly_name, ds.friendly_name)
        self.assertEqual(ds2.location, ds.location)
        self.assertEqual(ds2.labels, ds.labels)
        self.assertEqual(ds2.access_entries, ds.access_entries)

        # ETag becomes If-Match header.
        ds._properties['etag'] = 'etag'
        client.update_dataset(ds, [])
        req = conn._requested[1]
        self.assertEqual(req['headers']['If-Match'], 'etag')

    def test_update_table(self):
        from google.cloud.bigquery.table import Table, SchemaField

        path = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        description = 'description'
        title = 'title'
        resource = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]
            },
            'etag': 'etag',
            'description': description,
            'friendlyName': title,
            'labels': {'x': 'y'},
        }
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED')
        ]
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(resource, resource)
        table = Table(self.TABLE_REF, schema=schema)
        table.description = description
        table.friendly_name = title
        table.labels = {'x': 'y'}

        updated_table = client.update_table(
            table, ['schema', 'description', 'friendly_name', 'labels'])

        sent = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]},
            'description': description,
            'friendlyName': title,
            'labels': {'x': 'y'},
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
        self.assertEqual(updated_table.labels, table.labels)

        # ETag becomes If-Match header.
        table._properties['etag'] = 'etag'
        client.update_table(table, [])
        req = conn._requested[1]
        self.assertEqual(req['headers']['If-Match'], 'etag')

    def test_update_table_only_use_legacy_sql(self):
        from google.cloud.bigquery.table import Table

        path = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        resource = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'view': {'useLegacySql': True}
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(resource)
        table = Table(self.TABLE_REF)
        table.view_use_legacy_sql = True

        updated_table = client.update_table(table, ['view_use_legacy_sql'])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
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

        path = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
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
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'schema': schema_resource,
            'view': {'query': query, 'useLegacySql': True},
            'location': location,
            'expirationTime': _millis(exp_time)
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(resource)
        table = Table(self.TABLE_REF, schema=schema)
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
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
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
        path = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        resource1 = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID},
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}]}
        }
        resource2 = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID},
            'schema': {'fields': []},
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(resource1, resource2)
        table = client.get_table(self.TABLE_REF)
        table.schema = None

        updated_table = client.update_table(table, ['schema'])

        self.assertEqual(len(conn._requested), 2)
        req = conn._requested[1]
        self.assertEqual(req['method'], 'PATCH')
        sent = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'schema': None
        }
        self.assertEqual(req['data'], sent)
        self.assertEqual(req['path'], '/%s' % path)
        self.assertEqual(updated_table.schema, table.schema)

    def test_update_table_delete_property(self):
        from google.cloud.bigquery.table import Table

        description = 'description'
        title = 'title'
        path = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        resource1 = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'description': description,
            'friendlyName': title,
        }
        resource2 = {
            'id': '%s:%s:%s' % (self.PROJECT, self.DS_ID, self.TABLE_ID),
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'description': None,
        }
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(resource1, resource2)
        table = Table(self.TABLE_REF)
        table.description = description
        table.friendly_name = title
        table2 = client.update_table(table, ['description', 'friendly_name'])
        self.assertEqual(table2.description, table.description)
        table2.description = None

        table3 = client.update_table(table2, ['description'])
        self.assertEqual(len(conn._requested), 2)
        req = conn._requested[1]
        self.assertEqual(req['method'], 'PATCH')
        self.assertEqual(req['path'], '/%s' % path)
        sent = {
            'tableReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID
            },
            'description': None,
        }
        self.assertEqual(req['data'], sent)
        self.assertIsNone(table3.description)

    def test_list_dataset_tables_empty(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection({})

        dataset = client.dataset(self.DS_ID)
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
        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_ID)
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_dataset_tables_defaults(self):
        from google.cloud.bigquery.table import Table

        TABLE_1 = 'table_one'
        TABLE_2 = 'table_two'
        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_ID)
        TOKEN = 'TOKEN'
        DATA = {
            'nextPageToken': TOKEN,
            'tables': [
                {'kind': 'bigquery#table',
                 'id': '%s:%s.%s' % (self.PROJECT, self.DS_ID, TABLE_1),
                 'tableReference': {'tableId': TABLE_1,
                                    'datasetId': self.DS_ID,
                                    'projectId': self.PROJECT},
                 'type': 'TABLE'},
                {'kind': 'bigquery#table',
                 'id': '%s:%s.%s' % (self.PROJECT, self.DS_ID, TABLE_2),
                 'tableReference': {'tableId': TABLE_2,
                                    'datasetId': self.DS_ID,
                                    'projectId': self.PROJECT},
                 'type': 'TABLE'},
            ]
        }

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(DATA)
        dataset = client.dataset(self.DS_ID)

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

        TABLE_1 = 'table_one'
        TABLE_2 = 'table_two'
        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_ID)
        TOKEN = 'TOKEN'
        DATA = {
            'tables': [
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s.%s' % (self.PROJECT, self.DS_ID, TABLE_1),
                 'tableReference': {'tableId': TABLE_1,
                                    'datasetId': self.DS_ID,
                                    'projectId': self.PROJECT},
                 'type': 'TABLE'},
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s.%s' % (self.PROJECT, self.DS_ID, TABLE_2),
                 'tableReference': {'tableId': TABLE_2,
                                    'datasetId': self.DS_ID,
                                    'projectId': self.PROJECT},
                 'type': 'TABLE'},
            ]
        }

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection(DATA)
        dataset = client.dataset(self.DS_ID)

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
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.list_dataset_tables(client.dataset(self.DS_ID).table("foo"))

    def test_delete_dataset(self):
        from google.cloud.bigquery.dataset import Dataset

        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_ID)
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection({}, {})
        ds_ref = client.dataset(self.DS_ID)
        for arg in (ds_ref, Dataset(ds_ref)):
            client.delete_dataset(arg)
            req = conn._requested[0]
            self.assertEqual(req['method'], 'DELETE')
            self.assertEqual(req['path'], '/%s' % PATH)

    def test_delete_dataset_wrong_type(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.delete_dataset(client.dataset(self.DS_ID).table("foo"))

    def test_delete_table(self):
        from google.cloud.bigquery.table import Table

        path = 'projects/%s/datasets/%s/tables/%s' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection({}, {})

        for arg in (self.TABLE_REF, Table(self.TABLE_REF)):
            client.delete_table(arg)
            req = conn._requested[0]
            self.assertEqual(req['method'], 'DELETE')
            self.assertEqual(req['path'], '/%s' % path)

    def test_delete_table_w_wrong_type(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        with self.assertRaises(TypeError):
            client.delete_table(client.dataset(self.DS_ID))

    def test_job_from_resource_unknown_type(self):
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
        with self.assertRaises(ValueError):
            client.job_from_resource({'configuration': {'nonesuch': {}}})

    def test_get_job_miss_w_explict_project(self):
        from google.cloud.exceptions import NotFound

        OTHER_PROJECT = 'OTHER_PROJECT'
        JOB_ID = 'NONESUCH'
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
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

        JOB_ID = 'query_job'
        QUERY_DESTINATION_TABLE = 'query_destination_table'
        QUERY = 'SELECT * from test_dataset:test_table'
        ASYNC_QUERY_DATA = {
            'id': '{}:{}'.format(self.PROJECT, JOB_ID),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': 'query_job',
            },
            'state': 'DONE',
            'configuration': {
                'query': {
                    'query': QUERY,
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': QUERY_DESTINATION_TABLE,
                    },
                    'createDisposition': 'CREATE_IF_NEEDED',
                    'writeDisposition': 'WRITE_TRUNCATE',
                }
            },
        }
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
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
        PATH = 'projects/%s/jobs' % self.PROJECT
        TOKEN = 'TOKEN'
        QUERY = 'SELECT * from test_dataset:test_table'
        ASYNC_QUERY_DATA = {
            'id': '%s:%s' % (self.PROJECT, 'query_job'),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': 'query_job',
            },
            'state': 'DONE',
            'configuration': {
                'query': {
                    'query': QUERY,
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': QUERY_DESTINATION_TABLE,
                    },
                    'createDisposition': 'CREATE_IF_NEEDED',
                    'writeDisposition': 'WRITE_TRUNCATE',
                }
            },
        }
        EXTRACT_DATA = {
            'id': '%s:%s' % (self.PROJECT, 'extract_job'),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': 'extract_job',
            },
            'state': 'DONE',
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': SOURCE_TABLE,
                    },
                    'destinationUris': [DESTINATION_URI],
                }
            },
        }
        COPY_DATA = {
            'id': '%s:%s' % (self.PROJECT, 'copy_job'),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': 'copy_job',
            },
            'state': 'DONE',
            'configuration': {
                'copy': {
                    'sourceTables': [{
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': SOURCE_TABLE,
                    }],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': DESTINATION_TABLE,
                    },
                }
            },
        }
        LOAD_DATA = {
            'id': '%s:%s' % (self.PROJECT, 'load_job'),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': 'load_job',
            },
            'state': 'DONE',
            'configuration': {
                'load': {
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
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
        client = self._make_one(self.PROJECT, creds)
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

        SOURCE_TABLE = 'source_table'
        JOB_TYPES = {
            'load_job': LoadJob,
        }
        PATH = 'projects/%s/jobs' % self.PROJECT
        TOKEN = 'TOKEN'
        LOAD_DATA = {
            'id': '%s:%s' % (self.PROJECT, 'load_job'),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': 'load_job',
            },
            'state': 'DONE',
            'configuration': {
                'load': {
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
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
        client = self._make_one(self.PROJECT, creds)
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
        PATH = 'projects/%s/jobs' % self.PROJECT
        DATA = {}
        TOKEN = 'TOKEN'
        creds = _make_credentials()
        client = self._make_one(self.PROJECT, creds)
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

    def test_load_table_from_uri(self):
        from google.cloud.bigquery.job import LoadJob

        JOB = 'job_name'
        DESTINATION = 'destination_table'
        SOURCE_URI = 'http://example.com/source.csv'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'load': {
                    'sourceUris': [SOURCE_URI],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': DESTINATION,
                    },
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(RESOURCE)
        destination = client.dataset(self.DS_ID).table(DESTINATION)

        job = client.load_table_from_uri(SOURCE_URI, destination, job_id=JOB)

        # Check that load_table_from_uri actually starts the job.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/%s/jobs' % self.PROJECT)

        self.assertIsInstance(job, LoadJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.source_uris), [SOURCE_URI])
        self.assertIs(job.destination, destination)

        conn = client._connection = _Connection(RESOURCE)

        job = client.load_table_from_uri([SOURCE_URI], destination, job_id=JOB)
        self.assertIsInstance(job, LoadJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(list(job.source_uris), [SOURCE_URI])
        self.assertIs(job.destination, destination)

    @staticmethod
    def _mock_requests_response(status_code, headers, content=b''):
        return mock.Mock(
            content=content, headers=headers, status_code=status_code,
            spec=['content', 'headers', 'status_code'])

    def _mock_transport(self, status_code, headers, content=b''):
        fake_transport = mock.Mock(spec=['request'])
        fake_response = self._mock_requests_response(
            status_code, headers, content=content)
        fake_transport.request.return_value = fake_response
        return fake_transport

    def _initiate_resumable_upload_helper(self, num_retries=None):
        from google.resumable_media.requests import ResumableUpload
        from google.cloud.bigquery.client import _DEFAULT_CHUNKSIZE
        from google.cloud.bigquery.client import _GENERIC_CONTENT_TYPE
        from google.cloud.bigquery.client import _get_upload_headers
        from google.cloud.bigquery.job import LoadJob, LoadJobConfig

        # Create mocks to be checked for doing transport.
        resumable_url = 'http://test.invalid?upload_id=hey-you'
        response_headers = {'location': resumable_url}
        fake_transport = self._mock_transport(
            http_client.OK, response_headers)
        client = self._make_one(project=self.PROJECT, _http=fake_transport)
        conn = client._connection = _Connection()

        # Create some mock arguments and call the method under test.
        data = b'goodbye gudbi gootbee'
        stream = io.BytesIO(data)
        config = LoadJobConfig()
        config.source_format = 'CSV'
        job = LoadJob(None, None, self.TABLE_REF, client, job_config=config)
        metadata = job._build_resource()
        upload, transport = client._initiate_resumable_upload(
            stream, metadata, num_retries)

        # Check the returned values.
        self.assertIsInstance(upload, ResumableUpload)
        upload_url = (
            'https://www.googleapis.com/upload/bigquery/v2/projects/' +
            self.PROJECT +
            '/jobs?uploadType=resumable')
        self.assertEqual(upload.upload_url, upload_url)
        expected_headers = _get_upload_headers(conn.USER_AGENT)
        self.assertEqual(upload._headers, expected_headers)
        self.assertFalse(upload.finished)
        self.assertEqual(upload._chunk_size, _DEFAULT_CHUNKSIZE)
        self.assertIs(upload._stream, stream)
        self.assertIsNone(upload._total_bytes)
        self.assertEqual(upload._content_type, _GENERIC_CONTENT_TYPE)
        self.assertEqual(upload.resumable_url, resumable_url)

        retry_strategy = upload._retry_strategy
        self.assertEqual(retry_strategy.max_sleep, 64.0)
        if num_retries is None:
            self.assertEqual(retry_strategy.max_cumulative_retry, 600.0)
            self.assertIsNone(retry_strategy.max_retries)
        else:
            self.assertIsNone(retry_strategy.max_cumulative_retry)
            self.assertEqual(retry_strategy.max_retries, num_retries)
        self.assertIs(transport, fake_transport)
        # Make sure we never read from the stream.
        self.assertEqual(stream.tell(), 0)

        # Check the mocks.
        request_headers = expected_headers.copy()
        request_headers['x-upload-content-type'] = _GENERIC_CONTENT_TYPE
        fake_transport.request.assert_called_once_with(
            'POST',
            upload_url,
            data=json.dumps(metadata).encode('utf-8'),
            headers=request_headers,
        )

    def test__initiate_resumable_upload(self):
        self._initiate_resumable_upload_helper()

    def test__initiate_resumable_upload_with_retry(self):
        self._initiate_resumable_upload_helper(num_retries=11)

    def _do_multipart_upload_success_helper(
            self, get_boundary, num_retries=None):
        from google.cloud.bigquery.client import _get_upload_headers
        from google.cloud.bigquery.job import LoadJob, LoadJobConfig

        fake_transport = self._mock_transport(http_client.OK, {})
        client = self._make_one(project=self.PROJECT, _http=fake_transport)
        conn = client._connection = _Connection()

        # Create some mock arguments.
        data = b'Bzzzz-zap \x00\x01\xf4'
        stream = io.BytesIO(data)
        config = LoadJobConfig()
        config.source_format = 'CSV'
        job = LoadJob(None, None, self.TABLE_REF, client, job_config=config)
        metadata = job._build_resource()
        size = len(data)
        response = client._do_multipart_upload(
            stream, metadata, size, num_retries)

        # Check the mocks and the returned value.
        self.assertIs(response, fake_transport.request.return_value)
        self.assertEqual(stream.tell(), size)
        get_boundary.assert_called_once_with()

        upload_url = (
            'https://www.googleapis.com/upload/bigquery/v2/projects/' +
            self.PROJECT +
            '/jobs?uploadType=multipart')
        payload = (
            b'--==0==\r\n' +
            b'content-type: application/json; charset=UTF-8\r\n\r\n' +
            json.dumps(metadata).encode('utf-8') + b'\r\n' +
            b'--==0==\r\n' +
            b'content-type: */*\r\n\r\n' +
            data + b'\r\n' +
            b'--==0==--')
        headers = _get_upload_headers(conn.USER_AGENT)
        headers['content-type'] = b'multipart/related; boundary="==0=="'
        fake_transport.request.assert_called_once_with(
            'POST',
            upload_url,
            data=payload,
            headers=headers,
        )

    @mock.patch(u'google.resumable_media._upload.get_boundary',
                return_value=b'==0==')
    def test__do_multipart_upload(self, get_boundary):
        self._do_multipart_upload_success_helper(get_boundary)

    @mock.patch(u'google.resumable_media._upload.get_boundary',
                return_value=b'==0==')
    def test__do_multipart_upload_with_retry(self, get_boundary):
        self._do_multipart_upload_success_helper(get_boundary, num_retries=8)

    def test_copy_table(self):
        from google.cloud.bigquery.job import CopyJob

        JOB = 'job_name'
        SOURCE = 'source_table'
        DESTINATION = 'destination_table'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'copy': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': SOURCE,
                    },
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': DESTINATION,
                    },
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(RESOURCE)
        dataset = client.dataset(self.DS_ID)
        source = dataset.table(SOURCE)
        destination = dataset.table(DESTINATION)

        job = client.copy_table(source, destination, job_id=JOB)

        # Check that copy_table actually starts the job.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/%s/jobs' % self.PROJECT)

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

        JOB = 'job_id'
        SOURCE = 'source_table'
        DESTINATION = 'gs://bucket_name/object_name'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': SOURCE,
                    },
                    'destinationUris': [DESTINATION],
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(RESOURCE)
        dataset = client.dataset(self.DS_ID)
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

        JOB = 'job_id'
        SOURCE = 'source_table'
        DESTINATION = 'gs://bucket_name/object_name'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': SOURCE,
                    },
                    'destinationUris': [DESTINATION],
                    'destinationFormat': 'NEWLINE_DELIMITED_JSON',
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(RESOURCE)
        dataset = client.dataset(self.DS_ID)
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

    def test_extract_table_w_destination_uris(self):
        from google.cloud.bigquery.job import ExtractJob

        JOB = 'job_id'
        SOURCE = 'source_table'
        DESTINATION1 = 'gs://bucket_name/object_one'
        DESTINATION2 = 'gs://bucket_name/object_two'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': SOURCE,
                    },
                    'destinationUris': [
                        DESTINATION1,
                        DESTINATION2,
                    ],
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(RESOURCE)
        dataset = client.dataset(self.DS_ID)
        source = dataset.table(SOURCE)

        job = client.extract_table(
            source, [DESTINATION1, DESTINATION2], job_id=JOB)

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
        self.assertEqual(
            list(job.destination_uris), [DESTINATION1, DESTINATION2])

    def test_query_defaults(self):
        from google.cloud.bigquery.job import QueryJob

        QUERY = 'select count(*) from persons'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': 'some-random-id',
            },
            'configuration': {
                'query': {
                    'query': QUERY,
                    'useLegacySql': False,
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(RESOURCE)

        job = client.query(QUERY)

        self.assertIsInstance(job, QueryJob)
        self.assertIsInstance(job.job_id, six.string_types)
        self.assertIs(job._client, client)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(job.query_parameters, [])

        # Check that query actually starts the job.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs')
        sent = req['data']
        self.assertIsInstance(
            sent['jobReference']['jobId'], six.string_types)
        sent_config = sent['configuration']['query']
        self.assertEqual(sent_config['query'], QUERY)
        self.assertFalse(sent_config['useLegacySql'])

    def test_query_w_udf_resources(self):
        from google.cloud.bigquery.job import QueryJob
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        JOB = 'job_name'
        QUERY = 'select count(*) from persons'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'query': {
                    'query': QUERY,
                    'useLegacySql': True,
                    'userDefinedFunctionResources': [
                        {'resourceUri': RESOURCE_URI},
                    ],
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(RESOURCE)
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        config = QueryJobConfig()
        config.udf_resources = udf_resources
        config.use_legacy_sql = True

        job = client.query(QUERY, job_config=config, job_id=JOB)

        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, udf_resources)
        self.assertEqual(job.query_parameters, [])

        # Check that query actually starts the job.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs')
        sent = req['data']
        self.assertIsInstance(
            sent['jobReference']['jobId'], six.string_types)
        sent_config = sent['configuration']['query']
        self.assertEqual(sent_config['query'], QUERY)
        self.assertTrue(sent_config['useLegacySql'])
        self.assertEqual(
            sent_config['userDefinedFunctionResources'][0],
            {'resourceUri': RESOURCE_URI})

    def test_query_w_query_parameters(self):
        from google.cloud.bigquery.job import QueryJob
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

        JOB = 'job_name'
        QUERY = 'select count(*) from persons'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'query': {
                    'query': QUERY,
                    'useLegacySql': False,
                    'queryParameters': [
                        {
                            'name': 'foo',
                            'parameterType': {'type': 'INT64'},
                            'parameterValue': {'value': '123'}
                        },
                    ],
                },
            },
        }
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(RESOURCE)
        query_parameters = [ScalarQueryParameter('foo', 'INT64', 123)]
        config = QueryJobConfig()
        config.query_parameters = query_parameters

        job = client.query(QUERY, job_config=config, job_id=JOB)

        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, JOB)
        self.assertEqual(job.query, QUERY)
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(job.query_parameters, query_parameters)

        # Check that query actually starts the job.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs')
        sent = req['data']
        self.assertEqual(sent['jobReference']['jobId'], JOB)
        sent_config = sent['configuration']['query']
        self.assertEqual(sent_config['query'], QUERY)
        self.assertFalse(sent_config['useLegacySql'])
        self.assertEqual(
            sent_config['queryParameters'][0],
            {
                'name': 'foo',
                'parameterType': {'type': 'INT64'},
                'parameterValue': {'value': '123'}
            })

    def test_create_rows_wo_schema(self):
        from google.cloud.bigquery.table import Table, _TABLE_HAS_NO_SCHEMA

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        table = Table(self.TABLE_REF)
        ROWS = [
            ('Phred Phlyntstone', 32),
            ('Bharney Rhubble', 33),
            ('Wylma Phlyntstone', 29),
            ('Bhettye Rhubble', 27),
        ]

        with self.assertRaises(ValueError) as exc:
            client.create_rows(table, ROWS)

        self.assertEqual(exc.exception.args, (_TABLE_HAS_NO_SCHEMA,))

    def test_create_rows_w_schema(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_rfc3339
        from google.cloud._helpers import _microseconds_from_datetime
        from google.cloud.bigquery.table import Table, SchemaField

        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(
            tzinfo=UTC)
        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection({})
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED'),
            SchemaField('joined', 'TIMESTAMP', mode='NULLABLE'),
        ]
        table = Table(self.TABLE_REF, schema=schema)
        ROWS = [
            ('Phred Phlyntstone', 32, _datetime_to_rfc3339(WHEN)),
            ('Bharney Rhubble', 33, WHEN + datetime.timedelta(seconds=1)),
            ('Wylma Phlyntstone', 29, WHEN + datetime.timedelta(seconds=2)),
            ('Bhettye Rhubble', 27, None),
        ]

        def _row_data(row):
            joined = row[2]
            if isinstance(row[2], datetime.datetime):
                joined = _microseconds_from_datetime(joined) * 1e-6
            return {'full_name': row[0],
                    'age': str(row[1]),
                    'joined': joined}

        SENT = {
            'rows': [{
                'json': _row_data(row),
                'insertId': str(i),
            } for i, row in enumerate(ROWS)],
        }

        with mock.patch('uuid.uuid4', side_effect=map(str, range(len(ROWS)))):
            errors = client.create_rows(table, ROWS)

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_create_rows_w_list_of_dictionaries(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_rfc3339
        from google.cloud._helpers import _microseconds_from_datetime
        from google.cloud.bigquery.table import Table, SchemaField

        WHEN_TS = 1437767599.006
        WHEN = datetime.datetime.utcfromtimestamp(WHEN_TS).replace(
            tzinfo=UTC)
        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection({})
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED'),
            SchemaField('joined', 'TIMESTAMP', mode='NULLABLE'),
        ]
        table = Table(self.TABLE_REF, schema=schema)
        ROWS = [
            {
                'full_name': 'Phred Phlyntstone', 'age': 32,
                'joined': _datetime_to_rfc3339(WHEN)
            },
            {
                'full_name': 'Bharney Rhubble', 'age': 33,
                'joined': WHEN + datetime.timedelta(seconds=1)
            },
            {
                'full_name': 'Wylma Phlyntstone', 'age': 29,
                'joined': WHEN + datetime.timedelta(seconds=2)
            },
            {
                'full_name': 'Bhettye Rhubble', 'age': 27, 'joined': None
            },
        ]

        def _row_data(row):
            joined = row['joined']
            if isinstance(joined, datetime.datetime):
                row['joined'] = _microseconds_from_datetime(joined) * 1e-6
            row['age'] = str(row['age'])
            return row

        SENT = {
            'rows': [{
                'json': _row_data(row),
                'insertId': str(i),
            } for i, row in enumerate(ROWS)],
        }

        with mock.patch('uuid.uuid4', side_effect=map(str, range(len(ROWS)))):
            errors = client.create_rows(table, ROWS)

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_create_rows_w_list_of_Rows(self):
        from google.cloud.bigquery._helpers import Row
        from google.cloud.bigquery.table import Table, SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection({})
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED'),
        ]
        table = Table(self.TABLE_REF, schema=schema)
        f2i = {'full_name': 0, 'age': 1}
        ROWS = [
            Row(('Phred Phlyntstone', 32), f2i),
            Row(('Bharney Rhubble', 33), f2i),
            Row(('Wylma Phlyntstone', 29), f2i),
            Row(('Bhettye Rhubble', 27), f2i),
        ]

        def _row_data(row):
            return {'full_name': row[0], 'age': str(row[1])}

        SENT = {
            'rows': [{
                'json': _row_data(row),
                'insertId': str(i),
            } for i, row in enumerate(ROWS)],
        }

        with mock.patch('uuid.uuid4', side_effect=map(str, range(len(ROWS)))):
            errors = client.create_rows(table, ROWS)

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_create_rows_w_skip_invalid_and_ignore_unknown(self):
        from google.cloud.bigquery.table import Table, SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        RESPONSE = {
            'insertErrors': [
                {'index': 1,
                 'errors': [
                     {'reason': 'REASON',
                      'location': 'LOCATION',
                      'debugInfo': 'INFO',
                      'message': 'MESSAGE'}
                 ]},
            ]}
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(RESPONSE)
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED'),
            SchemaField('voter', 'BOOLEAN', mode='NULLABLE'),
        ]
        table = Table(self.TABLE_REF, schema=schema)
        ROWS = [
            ('Phred Phlyntstone', 32, True),
            ('Bharney Rhubble', 33, False),
            ('Wylma Phlyntstone', 29, True),
            ('Bhettye Rhubble', 27, True),
        ]

        def _row_data(row):
            return {
                'full_name': row[0],
                'age': str(row[1]),
                'voter': row[2] and 'true' or 'false',
            }

        SENT = {
            'skipInvalidRows': True,
            'ignoreUnknownValues': True,
            'templateSuffix': '20160303',
            'rows': [{'insertId': index, 'json': _row_data(row)}
                     for index, row in enumerate(ROWS)],
        }

        errors = client.create_rows(
            table,
            ROWS,
            row_ids=[index for index, _ in enumerate(ROWS)],
            skip_invalid_rows=True,
            ignore_unknown_values=True,
            template_suffix='20160303',
        )

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['index'], 1)
        self.assertEqual(len(errors[0]['errors']), 1)
        self.assertEqual(errors[0]['errors'][0],
                         RESPONSE['insertErrors'][0]['errors'][0])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_create_rows_w_repeated_fields(self):
        from google.cloud.bigquery.table import Table, SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection({})
        full_name = SchemaField('color', 'STRING', mode='REPEATED')
        index = SchemaField('index', 'INTEGER', 'REPEATED')
        score = SchemaField('score', 'FLOAT', 'REPEATED')
        struct = SchemaField('struct', 'RECORD', mode='REPEATED',
                             fields=[index, score])
        table = Table(self.TABLE_REF, schema=[full_name, struct])
        ROWS = [
            (['red', 'green'], [{'index': [1, 2], 'score': [3.1415, 1.414]}]),
        ]

        def _row_data(row):
            return {'color': row[0],
                    'struct': row[1]}

        SENT = {
            'rows': [{
                'json': _row_data(row),
                'insertId': str(i),
            } for i, row in enumerate(ROWS)],
        }

        with mock.patch('uuid.uuid4', side_effect=map(str, range(len(ROWS)))):
            errors = client.create_rows(table, ROWS)

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_create_rows_w_record_schema(self):
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection({})
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        area_code = SchemaField('area_code', 'STRING', 'REQUIRED')
        local_number = SchemaField('local_number', 'STRING', 'REQUIRED')
        rank = SchemaField('rank', 'INTEGER', 'REQUIRED')
        phone = SchemaField('phone', 'RECORD', mode='NULLABLE',
                            fields=[area_code, local_number, rank])
        ROWS = [
            ('Phred Phlyntstone', {'area_code': '800',
                                   'local_number': '555-1212',
                                   'rank': 1}),
            ('Bharney Rhubble', {'area_code': '877',
                                 'local_number': '768-5309',
                                 'rank': 2}),
            ('Wylma Phlyntstone', None),
        ]

        def _row_data(row):
            return {'full_name': row[0],
                    'phone': row[1]}

        SENT = {
            'rows': [{
                'json': _row_data(row),
                'insertId': str(i),
            } for i, row in enumerate(ROWS)],
        }

        with mock.patch('uuid.uuid4', side_effect=map(str, range(len(ROWS)))):
            errors = client.create_rows(self.TABLE_REF, ROWS,
                                        selected_fields=[full_name, phone])

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_create_rows_errors(self):
        from google.cloud.bigquery.table import Table

        ROWS = [
            ('Phred Phlyntstone', 32, True),
            ('Bharney Rhubble', 33, False),
            ('Wylma Phlyntstone', 29, True),
            ('Bhettye Rhubble', 27, True),
        ]
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)

        # table ref with no selected fields
        with self.assertRaises(ValueError):
            client.create_rows(self.TABLE_REF, ROWS)

        # table with no schema
        with self.assertRaises(ValueError):
            client.create_rows(Table(self.TABLE_REF), ROWS)

        # neither Table nor tableReference
        with self.assertRaises(TypeError):
            client.create_rows(1, ROWS)

    def test_create_rows_json(self):
        from google.cloud.bigquery.table import Table, SchemaField
        from google.cloud.bigquery.dataset import DatasetReference

        PROJECT = 'PROJECT'
        DS_ID = 'DS_ID'
        TABLE_ID = 'TABLE_ID'
        PATH = 'projects/%s/datasets/%s/tables/%s/insertAll' % (
            PROJECT, DS_ID, TABLE_ID)
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=PROJECT, credentials=creds, _http=http)
        conn = client._connection = _Connection({})
        table_ref = DatasetReference(PROJECT, DS_ID).table(TABLE_ID)
        schema = [
            SchemaField('full_name', 'STRING', mode='REQUIRED'),
            SchemaField('age', 'INTEGER', mode='REQUIRED'),
            SchemaField('joined', 'TIMESTAMP', mode='NULLABLE'),
        ]
        table = Table(table_ref, schema=schema)
        ROWS = [
            {
                'full_name': 'Phred Phlyntstone', 'age': '32',
                'joined': '2015-07-24T19:53:19.006000Z'
            },
            {
                'full_name': 'Bharney Rhubble', 'age': '33',
                'joined': 1437767600.006
            },
            {
                'full_name': 'Wylma Phlyntstone', 'age': '29',
                'joined': 1437767601.006
            },
            {
                'full_name': 'Bhettye Rhubble', 'age': '27', 'joined': None
            },
        ]

        SENT = {
            'rows': [{
                'json': row,
                'insertId': str(i),
            } for i, row in enumerate(ROWS)],
        }

        with mock.patch('uuid.uuid4', side_effect=map(str, range(len(ROWS)))):
            errors = client.create_rows_json(table, ROWS)

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], SENT)

    def test_query_rows_defaults(self):
        from google.api_core.page_iterator import HTTPIterator
        from google.cloud.bigquery._helpers import Row

        JOB = 'job-id'
        QUERY = 'SELECT COUNT(*) FROM persons'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'query': {
                    'query': QUERY,
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': '_temp_dataset',
                        'tableId': '_temp_table',
                    },
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
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(
            RESOURCE, RESULTS_RESOURCE, FIRST_PAGE, LAST_PAGE)

        rows_iter = client.query_rows(QUERY)
        rows = list(rows_iter)

        self.assertEqual(rows, [Row((i,), {'field0': 0}) for i in (1, 2, 3)])
        self.assertIs(rows_iter.client, client)
        self.assertIsInstance(rows_iter, HTTPIterator)
        self.assertEqual(len(conn._requested), 4)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/projects/PROJECT/jobs')
        self.assertIsInstance(
            req['data']['jobReference']['jobId'], six.string_types)

    def test_query_rows_w_job_id(self):
        from google.api_core.page_iterator import HTTPIterator

        JOB = 'job-id'
        QUERY = 'SELECT COUNT(*) FROM persons'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'query': {
                    'query': QUERY,
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': '_temp_dataset',
                        'tableId': '_temp_table',
                    },
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
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
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
        from google.api_core.page_iterator import HTTPIterator

        JOB = 'job-id'
        QUERY = 'SELECT COUNT(*) FROM persons'
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': JOB,
            },
            'configuration': {
                'query': {
                    'query': QUERY,
                    'useLegacySql': True,
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': '_temp_dataset',
                        'tableId': '_temp_table',
                    },
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
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
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
        from google.cloud.bigquery.table import Table, SchemaField
        from google.cloud.bigquery._helpers import Row

        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
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
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(DATA, DATA)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='NULLABLE')
        joined = SchemaField('joined', 'TIMESTAMP', mode='NULLABLE')
        table = Table(self.TABLE_REF, schema=[full_name, age, joined])

        iterator = client.list_rows(table)
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        f2i = {'full_name': 0, 'age': 1, 'joined': 2}
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], Row(('Phred Phlyntstone', 32, WHEN), f2i))
        self.assertEqual(rows[1], Row(('Bharney Rhubble', 33, WHEN_1), f2i))
        self.assertEqual(rows[2], Row(('Wylma Phlyntstone', 29, WHEN_2), f2i))
        self.assertEqual(rows[3], Row(('Bhettye Rhubble', None, None), f2i))
        self.assertEqual(total_rows, ROWS)
        self.assertEqual(page_token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {})

    def test_list_rows_query_params(self):
        from google.cloud.bigquery.table import Table, SchemaField

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        table = Table(self.TABLE_REF,
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
        from google.cloud.bigquery.table import SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
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
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(DATA)
        color = SchemaField('color', 'STRING', mode='REPEATED')
        index = SchemaField('index', 'INTEGER', 'REPEATED')
        score = SchemaField('score', 'FLOAT', 'REPEATED')
        struct = SchemaField('struct', 'RECORD', mode='REPEATED',
                             fields=[index, score])

        iterator = client.list_rows(self.TABLE_REF,
                                    selected_fields=[color, struct])
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
        from google.cloud.bigquery.table import Table, SchemaField

        PATH = 'projects/%s/datasets/%s/tables/%s/data' % (
            self.PROJECT, self.DS_ID, self.TABLE_ID)
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
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        conn = client._connection = _Connection(DATA)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        area_code = SchemaField('area_code', 'STRING', 'REQUIRED')
        local_number = SchemaField('local_number', 'STRING', 'REQUIRED')
        rank = SchemaField('rank', 'INTEGER', 'REQUIRED')
        phone = SchemaField('phone', 'RECORD', mode='NULLABLE',
                            fields=[area_code, local_number, rank])
        table = Table(self.TABLE_REF, schema=[full_name, phone])

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
        from google.cloud.bigquery.table import Table

        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)

        # table ref with no selected fields
        with self.assertRaises(ValueError):
            client.list_rows(self.TABLE_REF)

        # table with no schema
        with self.assertRaises(ValueError):
            client.list_rows(Table(self.TABLE_REF))

        # neither Table nor tableReference
        with self.assertRaises(TypeError):
            client.list_rows(1)

    def test_list_partitions(self):
        RESOURCE = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': 'JOB_ID',
            },
            'configuration': {
                'query': {
                    'query': 'q',
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': 'DS_ID',
                        'tableId': 'TABLE_ID',
                    },
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
                    {'name': 'partition_id', 'type': 'INTEGER',
                     'mode': 'REQUIRED'},
                ]
            },
            'totalRows': '2',
            'pageToken': 'next-page',
        }
        FIRST_PAGE = copy.deepcopy(RESULTS_RESOURCE)
        FIRST_PAGE['rows'] = [
            {'f': [{'v': 20160804}]},
            {'f': [{'v': 20160805}]},
        ]
        del FIRST_PAGE['pageToken']
        creds = _make_credentials()
        http = object()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _http=http)
        client._connection = _Connection(
            RESOURCE, RESULTS_RESOURCE, FIRST_PAGE)
        self.assertEqual(client.list_partitions(self.TABLE_REF),
                         [20160804, 20160805])


class Test_make_job_id(unittest.TestCase):
    def _call_fut(self, job_id, prefix=None):
        from google.cloud.bigquery.client import _make_job_id

        return _make_job_id(job_id, prefix=prefix)

    def test__make_job_id_wo_suffix(self):
        job_id = self._call_fut('job_id')

        self.assertEqual(job_id, 'job_id')

    def test__make_job_id_w_suffix(self):
        with mock.patch('uuid.uuid4', side_effect=['212345']):
            job_id = self._call_fut(None, prefix='job_id')

        self.assertEqual(job_id, 'job_id212345')

    def test__make_random_job_id(self):
        with mock.patch('uuid.uuid4', side_effect=['212345']):
            job_id = self._call_fut(None)

        self.assertEqual(job_id, '212345')

    def test__make_job_id_w_job_id_overrides_prefix(self):
        job_id = self._call_fut('job_id', prefix='unused_prefix')

        self.assertEqual(job_id, 'job_id')


class TestClientUpload(object):
    # NOTE: This is a "partner" to `TestClient` meant to test some of the
    #       "load_table_from_file" portions of `Client`. It also uses
    #       `pytest`-style tests rather than `unittest`-style.

    TABLE_REF = DatasetReference(
        'project_id', 'test_dataset').table('test_table')

    @staticmethod
    def _make_client(transport=None):
        from google.cloud.bigquery import _http
        from google.cloud.bigquery import client

        cl = client.Client(project='project_id',
                           credentials=_make_credentials(),
                           _http=transport)
        cl._connection = mock.create_autospec(_http.Connection, instance=True)
        return cl

    @staticmethod
    def _make_response(status_code, content='', headers={}):
        """Make a mock HTTP response."""
        import requests
        response = requests.Response()
        response.request = requests.Request(
            'POST', 'http://example.com').prepare()
        response._content = content.encode('utf-8')
        response.headers.update(headers)
        response.status_code = status_code
        return response

    @classmethod
    def _make_do_upload_patch(cls, client, method,
                              resource={}, side_effect=None):
        """Patches the low-level upload helpers."""
        if side_effect is None:
            side_effect = [cls._make_response(
                http_client.OK,
                json.dumps(resource),
                {'Content-Type': 'application/json'})]
        return mock.patch.object(
            client, method, side_effect=side_effect, autospec=True)

    EXPECTED_CONFIGURATION = {
        'jobReference': {'projectId': 'project_id', 'jobId': 'job_id'},
        'configuration': {
            'load': {
                'sourceFormat': 'CSV',
                'destinationTable': {
                    'projectId': 'project_id',
                    'datasetId': 'test_dataset',
                    'tableId': 'test_table'
                }
            }
        }
    }

    @staticmethod
    def _make_file_obj():
        return io.BytesIO(b'hello, is it me you\'re looking for?')

    @staticmethod
    def _make_config():
        from google.cloud.bigquery.job import LoadJobConfig

        config = LoadJobConfig()
        config.source_format = 'CSV'
        return config

    # High-level tests

    def test_load_table_from_file_resumable(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES

        client = self._make_client()
        file_obj = self._make_file_obj()

        do_upload_patch = self._make_do_upload_patch(
            client, '_do_resumable_upload', self.EXPECTED_CONFIGURATION)
        with do_upload_patch as do_upload:
            client.load_table_from_file(file_obj, self.TABLE_REF,
                                        job_id='job_id',
                                        job_config=self._make_config())

        do_upload.assert_called_once_with(
            file_obj,
            self.EXPECTED_CONFIGURATION,
            _DEFAULT_NUM_RETRIES)

    def test_load_table_from_file_resumable_metadata(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES

        client = self._make_client()
        file_obj = self._make_file_obj()

        config = self._make_config()
        config.allow_jagged_rows = False
        config.allow_quoted_newlines = False
        config.create_disposition = 'CREATE_IF_NEEDED'
        config.encoding = 'utf8'
        config.field_delimiter = ','
        config.ignore_unknown_values = False
        config.max_bad_records = 0
        config.quote_character = '"'
        config.skip_leading_rows = 1
        config.write_disposition = 'WRITE_APPEND'
        config.null_marker = r'\N'

        expected_config = {
            'jobReference': {'projectId': 'project_id', 'jobId': 'job_id'},
            'configuration': {
                'load': {
                    'destinationTable': {
                        'projectId': self.TABLE_REF.project,
                        'datasetId': self.TABLE_REF.dataset_id,
                        'tableId': self.TABLE_REF.table_id,
                    },
                    'sourceFormat': config.source_format,
                    'allowJaggedRows': config.allow_jagged_rows,
                    'allowQuotedNewlines': config.allow_quoted_newlines,
                    'createDisposition': config.create_disposition,
                    'encoding': config.encoding,
                    'fieldDelimiter': config.field_delimiter,
                    'ignoreUnknownValues': config.ignore_unknown_values,
                    'maxBadRecords': config.max_bad_records,
                    'quote': config.quote_character,
                    'skipLeadingRows': str(config.skip_leading_rows),
                    'writeDisposition': config.write_disposition,
                    'nullMarker': config.null_marker,
                },
            },
        }

        do_upload_patch = self._make_do_upload_patch(
            client, '_do_resumable_upload', expected_config)
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                file_obj, self.TABLE_REF, job_id='job_id', job_config=config)

        do_upload.assert_called_once_with(
            file_obj,
            expected_config,
            _DEFAULT_NUM_RETRIES)

    def test_load_table_from_file_multipart(self):
        from google.cloud.bigquery.client import _DEFAULT_NUM_RETRIES

        client = self._make_client()
        file_obj = self._make_file_obj()
        file_obj_size = 10
        config = self._make_config()

        do_upload_patch = self._make_do_upload_patch(
            client, '_do_multipart_upload', self.EXPECTED_CONFIGURATION)
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                file_obj, self.TABLE_REF, job_id='job_id', job_config=config,
                size=file_obj_size)

        do_upload.assert_called_once_with(
            file_obj,
            self.EXPECTED_CONFIGURATION,
            file_obj_size,
            _DEFAULT_NUM_RETRIES)

    def test_load_table_from_file_with_retries(self):
        client = self._make_client()
        file_obj = self._make_file_obj()
        num_retries = 20

        do_upload_patch = self._make_do_upload_patch(
            client, '_do_resumable_upload', self.EXPECTED_CONFIGURATION)
        with do_upload_patch as do_upload:
            client.load_table_from_file(
                file_obj, self.TABLE_REF, num_retries=num_retries,
                job_id='job_id', job_config=self._make_config())

        do_upload.assert_called_once_with(
            file_obj,
            self.EXPECTED_CONFIGURATION,
            num_retries)

    def test_load_table_from_file_with_rewind(self):
        client = self._make_client()
        file_obj = self._make_file_obj()
        file_obj.seek(2)

        with self._make_do_upload_patch(
                client, '_do_resumable_upload', self.EXPECTED_CONFIGURATION):
            client.load_table_from_file(
                file_obj, self.TABLE_REF, rewind=True)

        assert file_obj.tell() == 0

    def test_load_table_from_file_failure(self):
        from google.resumable_media import InvalidResponse
        from google.cloud import exceptions

        client = self._make_client()
        file_obj = self._make_file_obj()

        response = self._make_response(
            content='Someone is already in this spot.',
            status_code=http_client.CONFLICT)

        do_upload_patch = self._make_do_upload_patch(
            client, '_do_resumable_upload',
            side_effect=InvalidResponse(response))

        with do_upload_patch, pytest.raises(exceptions.Conflict) as exc_info:
            client.load_table_from_file(
                file_obj, self.TABLE_REF, rewind=True)

        assert response.text in exc_info.value.message
        assert exc_info.value.errors == []

    def test_load_table_from_file_bad_mode(self):
        client = self._make_client()
        file_obj = mock.Mock(spec=['mode'])
        file_obj.mode = 'x'

        with pytest.raises(ValueError):
            client.load_table_from_file(file_obj, self.TABLE_REF)

    # Low-level tests

    @classmethod
    def _make_resumable_upload_responses(cls, size):
        """Make a series of responses for a successful resumable upload."""
        from google import resumable_media

        resumable_url = 'http://test.invalid?upload_id=and-then-there-was-1'
        initial_response = cls._make_response(
            http_client.OK, '', {'location': resumable_url})
        data_response = cls._make_response(
            resumable_media.PERMANENT_REDIRECT,
            '', {'range': 'bytes=0-{:d}'.format(size - 1)})
        final_response = cls._make_response(
            http_client.OK,
            json.dumps({'size': size}),
            {'Content-Type': 'application/json'})
        return [initial_response, data_response, final_response]

    @staticmethod
    def _make_transport(responses=None):
        import google.auth.transport.requests

        transport = mock.create_autospec(
            google.auth.transport.requests.AuthorizedSession, instance=True)
        transport.request.side_effect = responses
        return transport

    def test__do_resumable_upload(self):
        file_obj = self._make_file_obj()
        file_obj_len = len(file_obj.getvalue())
        transport = self._make_transport(
            self._make_resumable_upload_responses(file_obj_len))
        client = self._make_client(transport)

        result = client._do_resumable_upload(
            file_obj,
            self.EXPECTED_CONFIGURATION,
            None)

        content = result.content.decode('utf-8')
        assert json.loads(content) == {'size': file_obj_len}

        # Verify that configuration data was passed in with the initial
        # request.
        transport.request.assert_any_call(
            'POST',
            mock.ANY,
            data=json.dumps(self.EXPECTED_CONFIGURATION).encode('utf-8'),
            headers=mock.ANY)

    def test__do_multipart_upload(self):
        transport = self._make_transport([self._make_response(http_client.OK)])
        client = self._make_client(transport)
        file_obj = self._make_file_obj()
        file_obj_len = len(file_obj.getvalue())

        client._do_multipart_upload(
            file_obj,
            self.EXPECTED_CONFIGURATION,
            file_obj_len,
            None)

        # Verify that configuration data was passed in with the initial
        # request.
        request_args = transport.request.mock_calls[0][2]
        request_data = request_args['data'].decode('utf-8')
        request_headers = request_args['headers']

        request_content = email.message_from_string(
            'Content-Type: {}\r\n{}'.format(
                request_headers['content-type'].decode('utf-8'),
                request_data))

        # There should be two payloads: the configuration and the binary daya.
        configuration_data = request_content.get_payload(0).get_payload()
        binary_data = request_content.get_payload(1).get_payload()

        assert json.loads(configuration_data) == self.EXPECTED_CONFIGURATION
        assert binary_data.encode('utf-8') == file_obj.getvalue()

    def test__do_multipart_upload_wrong_size(self):
        client = self._make_client()
        file_obj = self._make_file_obj()
        file_obj_len = len(file_obj.getvalue())

        with pytest.raises(ValueError):
            client._do_multipart_upload(
                file_obj,
                {},
                file_obj_len+1,
                None)


class _Connection(object):

    USER_AGENT = 'testing 1.2.3'

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from google.cloud.exceptions import NotFound
        self._requested.append(kw)

        if len(self._responses) == 0:
            raise NotFound('miss')

        response, self._responses = self._responses[0], self._responses[1:]
        if isinstance(response, Exception):
            raise response
        return response
