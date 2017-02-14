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


class TestQueryResults(unittest.TestCase):
    PROJECT = 'project'
    JOB_NAME = 'job_name'
    JOB_NAME = 'test-synchronous-query'
    JOB_TYPE = 'query'
    QUERY = 'select count(*) from persons'
    TOKEN = 'TOKEN'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.query import QueryResults

        return QueryResults

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

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
            resource['totalRows'] = '1000'
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
                self.assertEqual(found.fields, expected.get('fields'))
        else:
            self.assertIsNone(query.schema)

    def _verifyRows(self, query, resource):
        expected = resource.get('rows')
        if expected is None:
            self.assertEqual(query.rows, [])
        else:
            found = query.rows
            self.assertEqual(len(found), len(expected))
            for f_row, e_row in zip(found, expected):
                self.assertEqual(f_row,
                                 tuple([cell['v'] for cell in e_row['f']]))

    def _verify_udf_resources(self, query, resource):
        udf_resources = resource.get('userDefinedFunctionResources', ())
        self.assertEqual(len(query.udf_resources), len(udf_resources))
        for found, expected in zip(query.udf_resources, udf_resources):
            if 'resourceUri' in expected:
                self.assertEqual(found.udf_type, 'resourceUri')
                self.assertEqual(found.value, expected['resourceUri'])
            else:
                self.assertEqual(found.udf_type, 'inlineCode')
                self.assertEqual(found.value, expected['inlineCode'])

    def _verifyQueryParameters(self, query, resource):
        query_parameters = resource.get('queryParameters', ())
        self.assertEqual(len(query.query_parameters), len(query_parameters))
        for found, expected in zip(query.query_parameters, query_parameters):
            self.assertEqual(found.to_api_repr(), expected)

    def _verifyResourceProperties(self, query, resource):
        self.assertEqual(query.cache_hit, resource.get('cacheHit'))
        self.assertEqual(query.complete, resource.get('jobComplete'))
        self.assertEqual(query.errors, resource.get('errors'))
        self.assertEqual(query.page_token, resource.get('pageToken'))
        if 'totalRows' in resource:
            self.assertEqual(query.total_rows, int(resource['totalRows']))
        else:
            self.assertIsNone(query.total_rows)
        if 'totalBytesProcessed' in resource:
            self.assertEqual(query.total_bytes_processed,
                             int(resource['totalBytesProcessed']))
        else:
            self.assertIsNone(query.total_bytes_processed)

        if 'jobReference' in resource:
            self.assertEqual(query.name, resource['jobReference']['jobId'])
        else:
            self.assertIsNone(query.name)

        self._verify_udf_resources(query, resource)
        self._verifyQueryParameters(query, resource)
        self._verifySchema(query, resource)
        self._verifyRows(query, resource)

    def test_ctor_defaults(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self.assertEqual(query.query, self.QUERY)
        self.assertIs(query._client, client)

        self.assertIsNone(query.cache_hit)
        self.assertIsNone(query.complete)
        self.assertIsNone(query.errors)
        self.assertIsNone(query.name)
        self.assertIsNone(query.page_token)
        self.assertEqual(query.query_parameters, [])
        self.assertEqual(query.rows, [])
        self.assertIsNone(query.schema)
        self.assertIsNone(query.total_rows)
        self.assertIsNone(query.total_bytes_processed)
        self.assertEqual(query.udf_resources, [])

        self.assertIsNone(query.default_dataset)
        self.assertIsNone(query.max_results)
        self.assertIsNone(query.preserve_nulls)
        self.assertIsNone(query.use_query_cache)
        self.assertIsNone(query.use_legacy_sql)

    def test_ctor_w_udf_resources(self):
        from google.cloud.bigquery._helpers import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client, udf_resources=udf_resources)
        self.assertEqual(query.udf_resources, udf_resources)

    def test_ctor_w_query_parameters(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", 'INT64', 123)]
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client,
                               query_parameters=query_parameters)
        self.assertEqual(query.query_parameters, query_parameters)

    def test_from_query_job(self):
        from google.cloud.bigquery.dataset import Dataset
        from google.cloud.bigquery.job import QueryJob
        from google.cloud.bigquery._helpers import UDFResource

        DS_NAME = 'DATASET'
        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        client = _Client(self.PROJECT)
        job = QueryJob(
            self.JOB_NAME, self.QUERY, client,
            udf_resources=[UDFResource("resourceUri", RESOURCE_URI)])
        dataset = job.default_dataset = Dataset(DS_NAME, client)
        job.use_query_cache = True
        job.use_legacy_sql = True
        klass = self._get_target_class()

        query = klass.from_query_job(job)

        self.assertEqual(query.name, self.JOB_NAME)
        self.assertEqual(query.query, self.QUERY)
        self.assertIs(query._client, client)
        self.assertIs(query._job, job)
        self.assertEqual(query.udf_resources, job.udf_resources)
        self.assertIs(query.default_dataset, dataset)
        self.assertTrue(query.use_query_cache)
        self.assertTrue(query.use_legacy_sql)

    def test_from_query_job_wo_default_dataset(self):
        from google.cloud.bigquery.job import QueryJob
        from google.cloud.bigquery._helpers import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        client = _Client(self.PROJECT)
        job = QueryJob(
            self.JOB_NAME, self.QUERY, client,
            udf_resources=[UDFResource("resourceUri", RESOURCE_URI)])
        klass = self._get_target_class()

        query = klass.from_query_job(job)

        self.assertEqual(query.query, self.QUERY)
        self.assertIs(query._client, client)
        self.assertIs(query._job, job)
        self.assertEqual(query.udf_resources, job.udf_resources)
        self.assertIsNone(query.default_dataset)
        self.assertIsNone(query.use_query_cache)
        self.assertIsNone(query.use_legacy_sql)

    def test_job_wo_jobid(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self.assertIsNone(query.job)

    def test_job_w_jobid(self):
        from google.cloud.bigquery.job import QueryJob

        SERVER_GENERATED = 'SERVER_GENERATED'
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        query._properties['jobReference'] = {
            'projectId': self.PROJECT,
            'jobId': SERVER_GENERATED,
        }
        job = query.job
        self.assertIsInstance(job, QueryJob)
        self.assertEqual(job.query, self.QUERY)
        self.assertIs(job._client, client)
        self.assertEqual(job.name, SERVER_GENERATED)
        fetched_later = query.job
        self.assertIs(fetched_later, job)

    def test_cache_hit_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self.assertIsNone(query.cache_hit)

    def test_cache_hit_present(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'cacheHit': True}
        query._set_properties(resource)
        self.assertTrue(query.cache_hit)

    def test_complete_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self.assertIsNone(query.complete)

    def test_complete_present(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'jobComplete': True}
        query._set_properties(resource)
        self.assertTrue(query.complete)

    def test_errors_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self.assertIsNone(query.errors)

    def test_errors_present(self):
        ERRORS = [
            {'reason': 'testing'},
        ]
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'errors': ERRORS}
        query._set_properties(resource)
        self.assertEqual(query.errors, ERRORS)

    def test_name_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self.assertIsNone(query.name)

    def test_name_broken_job_reference(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'jobReference': {'bogus': 'BOGUS'}}
        query._set_properties(resource)
        self.assertIsNone(query.name)

    def test_name_present(self):
        JOB_ID = 'JOB_ID'
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'jobReference': {'jobId': JOB_ID}}
        query._set_properties(resource)
        self.assertEqual(query.name, JOB_ID)

    def test_page_token_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self.assertIsNone(query.page_token)

    def test_page_token_present(self):
        TOKEN = 'TOKEN'
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'pageToken': TOKEN}
        query._set_properties(resource)
        self.assertEqual(query.page_token, TOKEN)

    def test_total_rows_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self.assertIsNone(query.total_rows)

    def test_total_rows_present_integer(self):
        TOTAL_ROWS = 42
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'totalRows': TOTAL_ROWS}
        query._set_properties(resource)
        self.assertEqual(query.total_rows, TOTAL_ROWS)

    def test_total_rows_present_string(self):
        TOTAL_ROWS = 42
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'totalRows': str(TOTAL_ROWS)}
        query._set_properties(resource)
        self.assertEqual(query.total_rows, TOTAL_ROWS)

    def test_total_bytes_processed_missing(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self.assertIsNone(query.total_bytes_processed)

    def test_total_bytes_processed_present_integer(self):
        TOTAL_BYTES_PROCESSED = 123456
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'totalBytesProcessed': TOTAL_BYTES_PROCESSED}
        query._set_properties(resource)
        self.assertEqual(query.total_bytes_processed, TOTAL_BYTES_PROCESSED)

    def test_total_bytes_processed_present_string(self):
        TOTAL_BYTES_PROCESSED = 123456
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        resource = {'totalBytesProcessed': str(TOTAL_BYTES_PROCESSED)}
        query._set_properties(resource)
        self.assertEqual(query.total_bytes_processed, TOTAL_BYTES_PROCESSED)

    def test_schema(self):
        client = _Client(self.PROJECT)
        query = self._make_one(self.QUERY, client)
        self._verifyResourceProperties(query, {})
        resource = {
            'schema': {
                'fields': [
                    {'name': 'full_name', 'type': 'STRING', 'mode': 'REQURED'},
                    {'name': 'age', 'type': 'INTEGER', 'mode': 'REQURED'},
                ],
            },
        }
        query._set_properties(resource)
        self._verifyResourceProperties(query, resource)

    def test_run_w_already_has_job(self):
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client)
        query._job = object()  # simulate already running
        with self.assertRaises(ValueError):
            query.run()

    def test_run_w_already_has_job_in_properties(self):
        JOB_ID = 'JOB_ID'
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client)
        query._properties['jobReference'] = {'jobId': JOB_ID}
        with self.assertRaises(ValueError):
            query.run()

    def test_run_w_bound_client(self):
        PATH = 'projects/%s/queries' % self.PROJECT
        RESOURCE = self._makeResource(complete=False)
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client)
        self.assertEqual(query.udf_resources, [])
        query.run()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {'query': self.QUERY}
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(query, RESOURCE)

    def test_run_w_alternate_client(self):
        PATH = 'projects/%s/queries' % self.PROJECT
        RESOURCE = self._makeResource(complete=True)
        DATASET = 'test_dataset'
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        query = self._make_one(self.QUERY, client1)

        query.default_dataset = client2.dataset(DATASET)
        query.max_results = 100
        query.preserve_nulls = True
        query.timeout_ms = 20000
        query.use_query_cache = False
        query.use_legacy_sql = True
        query.dry_run = True

        query.run(client=client2)

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
            'dryRun': True,
            'maxResults': 100,
            'preserveNulls': True,
            'timeoutMs': 20000,
            'useQueryCache': False,
            'useLegacySql': True,
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(query, RESOURCE)

    def test_run_w_inline_udf(self):
        from google.cloud.bigquery._helpers import UDFResource

        INLINE_UDF_CODE = 'var someCode = "here";'
        PATH = 'projects/%s/queries' % self.PROJECT
        RESOURCE = self._makeResource(complete=False)
        RESOURCE['userDefinedFunctionResources'] = [
            {'inlineCode': INLINE_UDF_CODE},
        ]
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client)
        query.udf_resources = [UDFResource("inlineCode", INLINE_UDF_CODE)]

        query.run()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {'query': self.QUERY,
                'userDefinedFunctionResources':
                [{'inlineCode': INLINE_UDF_CODE}]}
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(query, RESOURCE)

    def test_run_w_udf_resource_uri(self):
        from google.cloud.bigquery._helpers import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        PATH = 'projects/%s/queries' % self.PROJECT
        RESOURCE = self._makeResource(complete=False)
        RESOURCE['userDefinedFunctionResources'] = [
            {'resourceUri': RESOURCE_URI},
        ]
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client)
        query.udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]

        query.run()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {'query': self.QUERY,
                'userDefinedFunctionResources':
                [{'resourceUri': RESOURCE_URI}]}
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(query, RESOURCE)

    def test_run_w_mixed_udfs(self):
        from google.cloud.bigquery._helpers import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        INLINE_UDF_CODE = 'var someCode = "here";'
        PATH = 'projects/%s/queries' % self.PROJECT
        RESOURCE = self._makeResource(complete=False)
        RESOURCE['userDefinedFunctionResources'] = [
            {'resourceUri': RESOURCE_URI},
            {'inlineCode': INLINE_UDF_CODE},
        ]
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client)
        query.udf_resources = [UDFResource("resourceUri", RESOURCE_URI),
                               UDFResource("inlineCode", INLINE_UDF_CODE)]

        query.run()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(query.udf_resources,
                         [UDFResource("resourceUri", RESOURCE_URI),
                          UDFResource("inlineCode", INLINE_UDF_CODE)])
        SENT = {'query': self.QUERY,
                'userDefinedFunctionResources': [
                    {'resourceUri': RESOURCE_URI},
                    {"inlineCode": INLINE_UDF_CODE}]}
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(query, RESOURCE)

    def test_run_w_named_query_paramter(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        PATH = 'projects/%s/queries' % self.PROJECT
        RESOURCE = self._makeResource(complete=False)
        RESOURCE['parameterMode'] = 'NAMED'
        RESOURCE['queryParameters'] = [
            {
                'name': 'foo',
                'parameterType': {
                    'type': 'INT64',
                },
                'parameterValue': {
                    'value': '123',
                },
            },
        ]
        query_parameters = [ScalarQueryParameter('foo', 'INT64', 123)]
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client,
                               query_parameters=query_parameters)
        query.run()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'query': self.QUERY,
            'parameterMode': 'NAMED',
            'queryParameters': RESOURCE['queryParameters'],
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(query, RESOURCE)

    def test_run_w_positional_query_paramter(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        PATH = 'projects/%s/queries' % self.PROJECT
        RESOURCE = self._makeResource(complete=False)
        RESOURCE['parameterMode'] = 'POSITIONAL'
        RESOURCE['queryParameters'] = [
            {
                'parameterType': {
                    'type': 'INT64',
                },
                'parameterValue': {
                    'value': '123',
                },
            },
        ]
        query_parameters = [ScalarQueryParameter.positional('INT64', 123)]
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client,
                               query_parameters=query_parameters)
        query.run()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'query': self.QUERY,
            'parameterMode': 'POSITIONAL',
            'queryParameters': RESOURCE['queryParameters'],
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(query, RESOURCE)

    def test_fetch_data_query_not_yet_run(self):
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client)
        self.assertRaises(ValueError, query.fetch_data)

    def test_fetch_data_w_bound_client(self):
        PATH = 'projects/%s/queries/%s' % (self.PROJECT, self.JOB_NAME)
        BEFORE = self._makeResource(complete=False)
        AFTER = self._makeResource(complete=True)
        del AFTER['totalRows']

        conn = _Connection(AFTER)
        client = _Client(project=self.PROJECT, connection=conn)
        query = self._make_one(self.QUERY, client)
        query._set_properties(BEFORE)
        self.assertFalse(query.complete)

        rows, total_rows, page_token = query.fetch_data()

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
        query = self._make_one(self.QUERY, client1)
        query._set_properties(BEFORE)
        self.assertFalse(query.complete)

        rows, total_rows, page_token = query.fetch_data(
            client=client2, max_results=MAX, page_token=TOKEN,
            start_index=START, timeout_ms=TIMEOUT)

        self.assertTrue(query.complete)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ('Phred Phlyntstone', 32))
        self.assertEqual(rows[1], ('Bharney Rhubble', 33))
        self.assertEqual(rows[2], ('Wylma Phlyntstone', 29))
        self.assertEqual(rows[3], ('Bhettye Rhubble', 27))
        self.assertEqual(total_rows, int(AFTER['totalRows']))
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
        self._connection = connection

    def dataset(self, name):
        from google.cloud.bigquery.dataset import Dataset

        return Dataset(name, client=self)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
