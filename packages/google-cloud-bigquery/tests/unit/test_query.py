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

from google.cloud.bigquery import Client


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestQueryResults(unittest.TestCase):
    PROJECT = 'project'
    JOB_ID = 'test-synchronous-query'
    TOKEN = 'TOKEN'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.query import QueryResults

        return QueryResults

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _makeResource(self):
        return {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
        }

    def _verifySchema(self, query, resource):
        from google.cloud.bigquery.schema import SchemaField

        if 'schema' in resource:
            fields = resource['schema']['fields']
            self.assertEqual(len(query.schema), len(fields))
            for found, expected in zip(query.schema, fields):
                self.assertIsInstance(found, SchemaField)
                self.assertEqual(found.name, expected['name'])
                self.assertEqual(found.field_type, expected['type'])
                self.assertEqual(found.mode, expected['mode'])
                self.assertEqual(found.description,
                                 expected.get('description'))
                self.assertEqual(found.fields, expected.get('fields', ()))
        else:
            self.assertEqual(query.schema, ())

    def test_ctor_defaults(self):
        client = _Client(self.PROJECT)
        query = self._make_one(client, self._makeResource())
        self.assertIs(query._client, client)
        self.assertIsNone(query.cache_hit)
        self.assertIsNone(query.complete)
        self.assertIsNone(query.errors)
        self.assertIsNone(query.page_token)
        self.assertEqual(query.project, self.PROJECT)
        self.assertEqual(query.rows, [])
        self.assertEqual(query.schema, ())
        self.assertIsNone(query.total_rows)
        self.assertIsNone(query.total_bytes_processed)

    def test_job_w_jobid(self):
        from google.cloud.bigquery.job import QueryJob

        SERVER_GENERATED = 'SERVER_GENERATED'
        job_resource = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': SERVER_GENERATED,
            },
            'configuration': {'query': {'query': 'SELECT 1'}},
        }
        query_resource = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': SERVER_GENERATED,
            },
        }
        conn = _Connection(job_resource)
        client = _Client(self.PROJECT, conn)
        query = self._make_one(client, query_resource)
        job = query.job()
        self.assertIsInstance(job, QueryJob)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_id, SERVER_GENERATED)
        fetched_later = query.job()
        self.assertIs(fetched_later, job)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(
            req['path'],
            '/projects/{}/jobs/{}'.format(self.PROJECT, SERVER_GENERATED))

    def test_cache_hit_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(client, self._makeResource())
        self.assertIsNone(query.cache_hit)

    def test_cache_hit_present(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['cacheHit'] = True
        query = self._make_one(client, resource)
        self.assertTrue(query.cache_hit)

    def test_complete_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(client, self._makeResource())
        self.assertIsNone(query.complete)

    def test_complete_present(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['jobComplete'] = True
        query = self._make_one(client, resource)
        self.assertTrue(query.complete)

    def test_errors_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(client, self._makeResource())
        self.assertIsNone(query.errors)

    def test_errors_present(self):
        ERRORS = [
            {'reason': 'testing'},
        ]
        resource = self._makeResource()
        resource['errors'] = ERRORS
        client = _Client(self.PROJECT)
        query = self._make_one(client, resource)
        self.assertEqual(query.errors, ERRORS)

    def test_job_id_missing(self):
        client = _Client(self.PROJECT)
        with self.assertRaises(ValueError):
            self._make_one(client, {})

    def test_job_id_broken_job_reference(self):
        client = _Client(self.PROJECT)
        resource = {'jobReference': {'bogus': 'BOGUS'}}
        with self.assertRaises(ValueError):
            self._make_one(client, resource)

    def test_job_id_present(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['jobReference']['jobId'] = 'custom-job'
        query = self._make_one(client, resource)
        self.assertEqual(query.job_id, 'custom-job')

    def test_page_token_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(client, self._makeResource())
        self.assertIsNone(query.page_token)

    def test_page_token_present(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['pageToken'] = 'TOKEN'
        query = self._make_one(client, resource)
        self.assertEqual(query.page_token, 'TOKEN')

    def test_total_rows_present_integer(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['totalRows'] = 42
        query = self._make_one(client, resource)
        self.assertEqual(query.total_rows, 42)

    def test_total_rows_present_string(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['totalRows'] = '42'
        query = self._make_one(client, resource)
        self.assertEqual(query.total_rows, 42)

    def test_total_bytes_processed_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(client, self._makeResource())
        self.assertIsNone(query.total_bytes_processed)

    def test_total_bytes_processed_present_integer(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['totalBytesProcessed'] = 123456
        query = self._make_one(client, resource)
        self.assertEqual(query.total_bytes_processed, 123456)

    def test_total_bytes_processed_present_string(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['totalBytesProcessed'] = '123456'
        query = self._make_one(client, resource)
        self.assertEqual(query.total_bytes_processed, 123456)

    def test_num_dml_affected_rows_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(client, self._makeResource())
        self.assertIsNone(query.num_dml_affected_rows)

    def test_num_dml_affected_rows_present_integer(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['numDmlAffectedRows'] = 123456
        query = self._make_one(client, resource)
        self.assertEqual(query.num_dml_affected_rows, 123456)

    def test_num_dml_affected_rows_present_string(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource()
        resource['numDmlAffectedRows'] = '123456'
        query = self._make_one(client, resource)
        self.assertEqual(query.num_dml_affected_rows, 123456)

    def test_schema(self):
        client = _Client(self.PROJECT)
        query = self._make_one(client, self._makeResource())
        self._verifySchema(query, self._makeResource())
        resource = self._makeResource()
        resource['schema'] = {
            'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQURED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQURED'},
            ],
        }
        query._set_properties(resource)
        self._verifySchema(query, resource)

    def test_fetch_data_w_bound_client(self):
        import six

        PATH = 'projects/%s/queries/%s' % (self.PROJECT, self.JOB_ID)
        schema = {
            'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQURED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQURED'},
            ],
        }
        BEFORE = self._makeResource()
        BEFORE['jobComplete'] = False
        BEFORE['schema'] = schema
        AFTER = self._makeResource()
        AFTER['rows'] = [
            {'f': [
                {'v': 'Phred Phlyntstone'},
                {'v': 32},
            ]},
            {'f': [
                {'v': 'Bharney Rhubble'},
                {'v': 33},
            ]},
            {'f': [
                {'v': 'Wylma Phlyntstone'},
                {'v': 29},
            ]},
            {'f': [
                {'v': 'Bhettye Rhubble'},
                {'v': 27},
            ]},
        ]
        AFTER['cacheHit'] = False
        AFTER['jobComplete'] = True
        AFTER['numDmlAffectedRows'] = 123
        AFTER['pageToken'] = self.TOKEN
        AFTER['schema'] = schema
        AFTER['totalBytesProcessed'] = 100000

        conn = _Connection(AFTER)
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(client, BEFORE)
        self.assertFalse(query.complete)

        iterator = query.fetch_data()
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertTrue(query.complete)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ('Phred Phlyntstone', 32))
        self.assertEqual(rows[1], ('Bharney Rhubble', 33))
        self.assertEqual(rows[2], ('Wylma Phlyntstone', 29))
        self.assertEqual(rows[3], ('Bhettye Rhubble', 27))
        self.assertIsNone(total_rows)
        self.assertEqual(page_token, AFTER['pageToken'])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_fetch_data_w_alternate_client(self):
        import six

        PATH = 'projects/%s/queries/%s' % (self.PROJECT, self.JOB_ID)
        MAX = 10
        START = 2257
        TIMEOUT = 20000

        schema = {
            'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQURED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQURED'},
            ],
        }
        BEFORE = self._makeResource()
        BEFORE['jobComplete'] = False
        BEFORE['schema'] = schema
        AFTER = self._makeResource()
        AFTER['rows'] = [
            {'f': [
                {'v': 'Phred Phlyntstone'},
                {'v': 32},
            ]},
            {'f': [
                {'v': 'Bharney Rhubble'},
                {'v': 33},
            ]},
            {'f': [
                {'v': 'Wylma Phlyntstone'},
                {'v': 29},
            ]},
            {'f': [
                {'v': 'Bhettye Rhubble'},
                {'v': 27},
            ]},
        ]
        AFTER['cacheHit'] = False
        AFTER['jobComplete'] = True
        AFTER['numDmlAffectedRows'] = 123
        AFTER['pageToken'] = self.TOKEN
        AFTER['schema'] = schema
        AFTER['totalBytesProcessed'] = 100000

        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(AFTER)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        query = self._make_one(client1, BEFORE)
        self.assertFalse(query.complete)

        iterator = query.fetch_data(
            client=client2, max_results=MAX, page_token=self.TOKEN,
            start_index=START, timeout_ms=TIMEOUT)
        page = six.next(iterator.pages)
        rows = list(page)
        total_rows = iterator.total_rows
        page_token = iterator.next_page_token

        self.assertTrue(query.complete)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ('Phred Phlyntstone', 32))
        self.assertEqual(rows[1], ('Bharney Rhubble', 33))
        self.assertEqual(rows[2], ('Wylma Phlyntstone', 29))
        self.assertEqual(rows[3], ('Bhettye Rhubble', 27))
        self.assertIsNone(total_rows)
        self.assertEqual(page_token, AFTER['pageToken'])

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'maxResults': MAX,
                          'pageToken': self.TOKEN,
                          'startIndex': START,
                          'timeoutMs': TIMEOUT})


class _Client(Client):

    def __init__(self, project='project', connection=None):
        creds = _make_credentials()
        http = object()
        super(_Client, self).__init__(
            project=project, credentials=creds, _http=http)

        if connection is None:
            connection = _Connection()
        self._connection = connection


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
