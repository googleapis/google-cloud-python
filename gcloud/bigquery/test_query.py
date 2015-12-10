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


class TestRunSyncQueryJob(unittest2.TestCase):
    PROJECT = 'project'
    JOB_NAME = 'job_name'
    JOB_NAME = 'test-synchronous-query'
    JOB_TYPE = 'query'
    QUERY = 'select count(*) from persons'
    TOKEN = 'TOKEN'

    def _getTargetClass(self):
        from gcloud.bigquery.query import RunSyncQueryJob
        return RunSyncQueryJob

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeResource(self, complete=False):
        resource = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'jobComplete': complete,
            'errors': [],
            'schema': {
                'fields': [
                    {'name': 'full_name', 'type': 'STRING', 'mode': 'REQURED'},
                    {'name': 'age', 'type': 'INTEGER', 'mode': 'REQURED'},
                ],
            },
        }

        if complete:
            resource['totalRows'] = 1000
            resource['rows'] = [
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
            resource['pageToken'] = self.TOKEN
            resource['totalBytesProcessed'] = 100000
            resource['cacheHit'] = False

        return resource

    def _verifySchema(self, job, resource):
        from gcloud.bigquery.table import SchemaField
        if 'schema' in resource:
            fields = resource['schema']['fields']
            self.assertEqual(len(job.schema), len(fields))
            for found, expected in zip(job.schema, fields):
                self.assertTrue(isinstance(found, SchemaField))
                self.assertEqual(found.name, expected['name'])
                self.assertEqual(found.field_type, expected['type'])
                self.assertEqual(found.mode, expected['mode'])
                self.assertEqual(found.description,
                                 expected.get('description'))
                self.assertEqual(found.fields, expected.get('fields'))
        else:
            self.assertTrue(job.schema is None)

    def _verifyRows(self, job, resource):
        expected = resource.get('rows')
        if expected is None:
            self.assertEqual(job.rows, [])
        else:
            found = job.rows
            self.assertEqual(len(found), len(expected))
            for f_row, e_row in zip(found, expected):
                self.assertEqual(f_row,
                                 tuple([cell['v'] for cell in e_row['f']]))

    def _verifyResourceProperties(self, job, resource):
        self.assertEqual(job.cache_hit, resource.get('cacheHit'))
        self.assertEqual(job.complete, resource.get('jobComplete'))
        self.assertEqual(job.errors, resource.get('errors'))
        self.assertEqual(job.page_token, resource.get('pageToken'))
        self.assertEqual(job.total_rows, resource.get('totalRows'))
        self.assertEqual(job.total_bytes_processed,
                         resource.get('totalBytesProcessed'))

        if 'jobReference' in resource:
            self.assertEqual(job.name, resource['jobReference']['jobId'])
        else:
            self.assertTrue(job.name is None)

        self._verifySchema(job, resource)
        self._verifyRows(job, resource)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        job = self._makeOne(self.QUERY, client)
        self.assertEqual(job.query, self.QUERY)
        self.assertTrue(job._client is client)

        self.assertTrue(job.cache_hit is None)
        self.assertTrue(job.complete is None)
        self.assertTrue(job.errors is None)
        self.assertTrue(job.name is None)
        self.assertTrue(job.page_token is None)
        self.assertEqual(job.rows, [])
        self.assertTrue(job.schema is None)
        self.assertTrue(job.total_rows is None)
        self.assertTrue(job.total_bytes_processed is None)

        self.assertTrue(job.default_dataset is None)
        self.assertTrue(job.max_results is None)
        self.assertTrue(job.preserve_nulls is None)
        self.assertTrue(job.use_query_cache is None)

    def test_name_setter_bad_value(self):
        client = _Client(self.PROJECT)
        job = self._makeOne(self.QUERY, client)
        with self.assertRaises(ValueError):
            job.name = 12345

    def test_name_setter(self):
        client = _Client(self.PROJECT)
        job = self._makeOne(self.QUERY, client)
        job.name = 'NAME'
        self.assertEqual(job.name, 'NAME')

    def test_schema(self):
        client = _Client(self.PROJECT)
        job = self._makeOne(self.QUERY, client)
        self._verifyResourceProperties(job, {})
        resource = {
            'schema': {
                'fields': [
                    {'name': 'full_name', 'type': 'STRING', 'mode': 'REQURED'},
                    {'name': 'age', 'type': 'INTEGER', 'mode': 'REQURED'},
                ],
            },
        }
        job._set_properties(resource)
        self._verifyResourceProperties(job, resource)

    def test_run_w_bound_client(self):
        PATH = 'projects/%s/queries' % self.PROJECT
        RESOURCE = self._makeResource(complete=False)
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._makeOne(self.QUERY, client)

        job.run()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {'query': self.QUERY}
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_run_w_alternate_client(self):
        PATH = 'projects/%s/queries' % self.PROJECT
        RESOURCE = self._makeResource(complete=True)
        DATASET = 'test_dataset'
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        job = self._makeOne(self.QUERY, client1)

        job.default_dataset = client2.dataset(DATASET)
        job.max_results = 100
        job.preserve_nulls = True
        job.timeout_ms = 20000
        job.use_query_cache = False

        job.run(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'query': self.QUERY,
            'defaultDataset': {
                'projectId': self.PROJECT,
                'datasetId': DATASET,
            },
            'maxResults': 100,
            'preserveNulls': True,
            'timeoutMs': 20000,
            'useQueryCache': False,
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_fetch_data_query_not_yet_run(self):
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._makeOne(self.QUERY, client)
        self.assertRaises(ValueError, job.fetch_data)

    def test_fetch_data_w_bound_client(self):
        PATH = 'projects/%s/queries/%s' % (self.PROJECT, self.JOB_NAME)
        BEFORE = self._makeResource(complete=False)
        AFTER = self._makeResource(complete=True)

        conn = _Connection(AFTER)
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._makeOne(self.QUERY, client)
        job._set_properties(BEFORE)
        self.assertFalse(job.complete)

        rows, total_rows, page_token = job.fetch_data()

        self.assertTrue(job.complete)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ('Phred Phlyntstone', 32))
        self.assertEqual(rows[1], ('Bharney Rhubble', 33))
        self.assertEqual(rows[2], ('Wylma Phlyntstone', 29))
        self.assertEqual(rows[3], ('Bhettye Rhubble', 27))
        self.assertEqual(total_rows, AFTER['totalRows'])
        self.assertEqual(page_token, AFTER['pageToken'])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_fetch_data_w_alternate_client(self):
        PATH = 'projects/%s/queries/%s' % (self.PROJECT, self.JOB_NAME)
        MAX = 10
        TOKEN = 'TOKEN'
        START = 2257
        TIMEOUT = 20000
        BEFORE = self._makeResource(complete=False)
        AFTER = self._makeResource(complete=True)

        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(AFTER)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        job = self._makeOne(self.QUERY, client1)
        job._set_properties(BEFORE)
        self.assertFalse(job.complete)

        rows, total_rows, page_token = job.fetch_data(client=client2,
                                                      max_results=MAX,
                                                      page_token=TOKEN,
                                                      start_index=START,
                                                      timeout_ms=TIMEOUT)

        self.assertTrue(job.complete)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ('Phred Phlyntstone', 32))
        self.assertEqual(rows[1], ('Bharney Rhubble', 33))
        self.assertEqual(rows[2], ('Wylma Phlyntstone', 29))
        self.assertEqual(rows[3], ('Bhettye Rhubble', 27))
        self.assertEqual(total_rows, AFTER['totalRows'])
        self.assertEqual(page_token, AFTER['pageToken'])

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'maxResults': MAX,
                          'pageToken': TOKEN,
                          'startIndex': START,
                          'timeoutMs': TIMEOUT})


class _Client(object):

    def __init__(self, project='project', connection=None):
        self.project = project
        self.connection = connection

    def dataset(self, name):
        from gcloud.bigquery.dataset import Dataset
        return Dataset(name, client=self)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response
