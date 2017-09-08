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

from six.moves import http_client
import unittest


class Test__error_result_to_exception(unittest.TestCase):
    def _call_fut(self, *args, **kwargs):
        from google.cloud.bigquery import job
        return job._error_result_to_exception(*args, **kwargs)

    def test_simple(self):
        error_result = {
            'reason': 'invalid',
            'message': 'bad request'
        }
        exception = self._call_fut(error_result)
        self.assertEqual(exception.code, http_client.BAD_REQUEST)
        self.assertTrue(exception.message.startswith('bad request'))
        self.assertIn(error_result, exception.errors)

    def test_missing_reason(self):
        error_result = {}
        exception = self._call_fut(error_result)
        self.assertEqual(exception.code, http_client.INTERNAL_SERVER_ERROR)


class _Base(object):
    PROJECT = 'project'
    SOURCE1 = 'http://example.com/source1.csv'
    DS_NAME = 'datset_name'
    TABLE_NAME = 'table_name'
    JOB_NAME = 'job_name'

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from google.cloud._helpers import UTC

        self.WHEN_TS = 1437767599.006
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(
            tzinfo=UTC)
        self.ETAG = 'ETAG'
        self.JOB_ID = '%s:%s' % (self.PROJECT, self.JOB_NAME)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'
        self.USER_EMAIL = 'phred@example.com'

    def _makeResource(self, started=False, ended=False):
        self._setUpConstants()
        resource = {
            'configuration': {
                self.JOB_TYPE: {
                },
            },
            'statistics': {
                'creationTime': self.WHEN_TS * 1000,
                self.JOB_TYPE: {
                }
            },
            'etag': self.ETAG,
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'selfLink': self.RESOURCE_URL,
            'user_email': self.USER_EMAIL,
        }

        if started or ended:
            resource['statistics']['startTime'] = self.WHEN_TS * 1000

        if ended:
            resource['statistics']['endTime'] = (self.WHEN_TS + 1000) * 1000

        return resource

    def _verifyInitialReadonlyProperties(self, job):
        # root elements of resource
        self.assertIsNone(job.etag)
        self.assertIsNone(job.self_link)
        self.assertIsNone(job.user_email)

        # derived from resource['statistics']
        self.assertIsNone(job.created)
        self.assertIsNone(job.started)
        self.assertIsNone(job.ended)

        # derived from resource['status']
        self.assertIsNone(job.error_result)
        self.assertIsNone(job.errors)
        self.assertIsNone(job.state)

    def _verifyReadonlyResourceProperties(self, job, resource):
        from datetime import timedelta

        statistics = resource.get('statistics', {})

        if 'creationTime' in statistics:
            self.assertEqual(job.created, self.WHEN)
        else:
            self.assertIsNone(job.created)

        if 'startTime' in statistics:
            self.assertEqual(job.started, self.WHEN)
        else:
            self.assertIsNone(job.started)

        if 'endTime' in statistics:
            self.assertEqual(job.ended, self.WHEN + timedelta(seconds=1000))
        else:
            self.assertIsNone(job.ended)

        if 'etag' in resource:
            self.assertEqual(job.etag, self.ETAG)
        else:
            self.assertIsNone(job.etag)

        if 'selfLink' in resource:
            self.assertEqual(job.self_link, self.RESOURCE_URL)
        else:
            self.assertIsNone(job.self_link)

        if 'user_email' in resource:
            self.assertEqual(job.user_email, self.USER_EMAIL)
        else:
            self.assertIsNone(job.user_email)


class TestLoadTableFromStorageJob(unittest.TestCase, _Base):
    JOB_TYPE = 'load'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import LoadTableFromStorageJob

        return LoadTableFromStorageJob

    def _setUpConstants(self):
        super(TestLoadTableFromStorageJob, self)._setUpConstants()
        self.INPUT_FILES = 2
        self.INPUT_BYTES = 12345
        self.OUTPUT_BYTES = 23456
        self.OUTPUT_ROWS = 345

    def _makeResource(self, started=False, ended=False):
        resource = super(TestLoadTableFromStorageJob, self)._makeResource(
            started, ended)
        config = resource['configuration']['load']
        config['sourceUris'] = [self.SOURCE1]
        config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_NAME,
            'tableId': self.TABLE_NAME,
        }

        if ended:
            resource['status'] = {'state': 'DONE'}
            resource['statistics']['load']['inputFiles'] = self.INPUT_FILES
            resource['statistics']['load']['inputFileBytes'] = self.INPUT_BYTES
            resource['statistics']['load']['outputBytes'] = self.OUTPUT_BYTES
            resource['statistics']['load']['outputRows'] = self.OUTPUT_ROWS

        return resource

    def _verifyBooleanConfigProperties(self, job, config):
        if 'allowJaggedRows' in config:
            self.assertEqual(job.allow_jagged_rows,
                             config['allowJaggedRows'])
        else:
            self.assertIsNone(job.allow_jagged_rows)
        if 'allowQuotedNewlines' in config:
            self.assertEqual(job.allow_quoted_newlines,
                             config['allowQuotedNewlines'])
        else:
            self.assertIsNone(job.allow_quoted_newlines)
        if 'autodetect' in config:
            self.assertEqual(
                job.autodetect, config['autodetect'])
        else:
            self.assertIsNone(job.autodetect)
        if 'ignoreUnknownValues' in config:
            self.assertEqual(job.ignore_unknown_values,
                             config['ignoreUnknownValues'])
        else:
            self.assertIsNone(job.ignore_unknown_values)

    def _verifyEnumConfigProperties(self, job, config):
        if 'createDisposition' in config:
            self.assertEqual(job.create_disposition,
                             config['createDisposition'])
        else:
            self.assertIsNone(job.create_disposition)
        if 'encoding' in config:
            self.assertEqual(job.encoding,
                             config['encoding'])
        else:
            self.assertIsNone(job.encoding)
        if 'sourceFormat' in config:
            self.assertEqual(job.source_format,
                             config['sourceFormat'])
        else:
            self.assertIsNone(job.source_format)
        if 'writeDisposition' in config:
            self.assertEqual(job.write_disposition,
                             config['writeDisposition'])
        else:
            self.assertIsNone(job.write_disposition)

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('load')

        self._verifyBooleanConfigProperties(job, config)
        self._verifyEnumConfigProperties(job, config)

        self.assertEqual(job.source_uris, config['sourceUris'])

        table_ref = config['destinationTable']
        self.assertEqual(job.destination.project, table_ref['projectId'])
        self.assertEqual(job.destination.dataset_name, table_ref['datasetId'])
        self.assertEqual(job.destination.name, table_ref['tableId'])

        if 'fieldDelimiter' in config:
            self.assertEqual(job.field_delimiter,
                             config['fieldDelimiter'])
        else:
            self.assertIsNone(job.field_delimiter)
        if 'maxBadRecords' in config:
            self.assertEqual(job.max_bad_records,
                             config['maxBadRecords'])
        else:
            self.assertIsNone(job.max_bad_records)
        if 'nullMarker' in config:
            self.assertEqual(job.null_marker,
                             config['nullMarker'])
        else:
            self.assertIsNone(job.null_marker)
        if 'quote' in config:
            self.assertEqual(job.quote_character,
                             config['quote'])
        else:
            self.assertIsNone(job.quote_character)
        if 'skipLeadingRows' in config:
            self.assertEqual(job.skip_leading_rows,
                             config['skipLeadingRows'])
        else:
            self.assertIsNone(job.skip_leading_rows)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)
        self.assertIs(job.destination, table)
        self.assertEqual(list(job.source_uris), [self.SOURCE1])
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))
        self.assertEqual(job.schema, [])

        self._verifyInitialReadonlyProperties(job)

        # derived from resource['statistics']['load']
        self.assertIsNone(job.input_file_bytes)
        self.assertIsNone(job.input_files)
        self.assertIsNone(job.output_bytes)
        self.assertIsNone(job.output_rows)

        # set/read from resource['configuration']['load']
        self.assertIsNone(job.allow_jagged_rows)
        self.assertIsNone(job.allow_quoted_newlines)
        self.assertIsNone(job.autodetect)
        self.assertIsNone(job.create_disposition)
        self.assertIsNone(job.encoding)
        self.assertIsNone(job.field_delimiter)
        self.assertIsNone(job.ignore_unknown_values)
        self.assertIsNone(job.max_bad_records)
        self.assertIsNone(job.null_marker)
        self.assertIsNone(job.quote_character)
        self.assertIsNone(job.skip_leading_rows)
        self.assertIsNone(job.source_format)
        self.assertIsNone(job.write_disposition)

    def test_ctor_w_schema(self):
        from google.cloud.bigquery.schema import SchemaField

        client = _Client(self.PROJECT)
        table = _Table()
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client,
                             schema=[full_name, age])
        self.assertEqual(job.schema, [full_name, age])

    def test_done(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)
        self.assertTrue(job.done())

    def test_result(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        result = job.result()

        self.assertIs(result, job)

    def test_result_invokes_begins(self):
        begun_resource = self._makeResource()
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _Connection(begun_resource, done_resource)
        client = _Client(self.PROJECT, connection=connection)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)

        job.result()

        self.assertEqual(len(connection._requested), 2)
        begin_request,  reload_request = connection._requested
        self.assertEqual(begin_request['method'], 'POST')
        self.assertEqual(reload_request['method'], 'GET')

    def test_schema_setter_non_list(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(TypeError):
            job.schema = object()

    def test_schema_setter_invalid_field(self):
        from google.cloud.bigquery.schema import SchemaField

        client = _Client(self.PROJECT)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        with self.assertRaises(ValueError):
            job.schema = [full_name, object()]

    def test_schema_setter(self):
        from google.cloud.bigquery.schema import SchemaField

        client = _Client(self.PROJECT)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        job.schema = [full_name, age]
        self.assertEqual(job.schema, [full_name, age])

    def test_schema_setter_w_autodetect(self):
        from google.cloud.bigquery.schema import SchemaField

        client = _Client(self.PROJECT)
        table = _Table()
        full_name = SchemaField('full_name', 'STRING')
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)
        job.autodetect = False
        job.schema = [full_name]
        self.assertEqual(job.schema, [full_name])

        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)
        job.autodetect = True
        with self.assertRaises(ValueError):
            job.schema = [full_name]

    def test_autodetect_setter_w_schema(self):
        from google.cloud.bigquery.schema import SchemaField

        client = _Client(self.PROJECT)
        table = _Table()
        full_name = SchemaField('full_name', 'STRING')
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)

        job.autodetect = True
        job.schema = []
        self.assertEqual(job.schema, [])

        job.autodetect = False
        job.schema = [full_name]
        self.assertEqual(job.autodetect, False)

        with self.assertRaises(ValueError):
            job.autodetect = True

    def test_props_set_by_server(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis

        CREATED = datetime.datetime(2015, 8, 11, 12, 13, 22, tzinfo=UTC)
        STARTED = datetime.datetime(2015, 8, 11, 13, 47, 15, tzinfo=UTC)
        ENDED = datetime.datetime(2015, 8, 11, 14, 47, 15, tzinfo=UTC)
        JOB_ID = '%s:%s' % (self.PROJECT, self.JOB_NAME)
        URL = 'http://example.com/projects/%s/jobs/%s' % (
            self.PROJECT, self.JOB_NAME)
        EMAIL = 'phred@example.com'
        ERROR_RESULT = {'debugInfo': 'DEBUG',
                        'location': 'LOCATION',
                        'message': 'MESSAGE',
                        'reason': 'REASON'}

        client = _Client(self.PROJECT)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)
        job._properties['etag'] = 'ETAG'
        job._properties['id'] = JOB_ID
        job._properties['selfLink'] = URL
        job._properties['user_email'] = EMAIL

        statistics = job._properties['statistics'] = {}
        statistics['creationTime'] = _millis(CREATED)
        statistics['startTime'] = _millis(STARTED)
        statistics['endTime'] = _millis(ENDED)
        load_stats = statistics['load'] = {}
        load_stats['inputFileBytes'] = 12345
        load_stats['inputFiles'] = 1
        load_stats['outputBytes'] = 23456
        load_stats['outputRows'] = 345

        self.assertEqual(job.etag, 'ETAG')
        self.assertEqual(job.self_link, URL)
        self.assertEqual(job.user_email, EMAIL)

        self.assertEqual(job.created, CREATED)
        self.assertEqual(job.started, STARTED)
        self.assertEqual(job.ended, ENDED)

        self.assertEqual(job.input_file_bytes, 12345)
        self.assertEqual(job.input_files, 1)
        self.assertEqual(job.output_bytes, 23456)
        self.assertEqual(job.output_rows, 345)

        status = job._properties['status'] = {}

        self.assertIsNone(job.error_result)
        self.assertIsNone(job.errors)
        self.assertIsNone(job.state)

        status['errorResult'] = ERROR_RESULT
        status['errors'] = [ERROR_RESULT]
        status['state'] = 'STATE'

        self.assertEqual(job.error_result, ERROR_RESULT)
        self.assertEqual(job.errors, [ERROR_RESULT])
        self.assertEqual(job.state, 'STATE')

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_NAME),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'load': {
                    'sourceUris': [self.SOURCE1],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.TABLE_NAME,
                    },
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        klass = self._get_target_class()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(dataset._client, client)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_begin_w_already_running(self):
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)
        job._properties['status'] = {'state': 'RUNNING'}

        with self.assertRaises(ValueError):
            job.begin()

    def test_begin_w_bound_client(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'load': {
                    'sourceUris': [self.SOURCE1],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.TABLE_NAME,
                    },
                },
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_autodetect(self):
        path = '/projects/{}/jobs'.format(self.PROJECT)
        resource = self._makeResource()
        resource['configuration']['load']['autodetect'] = True
        # Ensure None for missing server-set props
        del resource['statistics']['creationTime']
        del resource['etag']
        del resource['selfLink']
        del resource['user_email']
        conn = _Connection(resource)
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)
        job.autodetect = True
        job.begin()

        sent = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'load': {
                    'sourceUris': [self.SOURCE1],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.TABLE_NAME,
                    },
                    'autodetect': True
                },
            },
        }
        expected_request = {
            'method': 'POST',
            'path': path,
            'data': sent,
        }
        self.assertEqual(conn._requested, [expected_request])
        self._verifyResourceProperties(job, resource)

    def test_begin_w_alternate_client(self):
        from google.cloud.bigquery.schema import SchemaField

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource(ended=True)
        LOAD_CONFIGURATION = {
            'sourceUris': [self.SOURCE1],
            'destinationTable': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.TABLE_NAME,
            },
            'allowJaggedRows': True,
            'allowQuotedNewlines': True,
            'createDisposition': 'CREATE_NEVER',
            'encoding': 'ISO-8559-1',
            'fieldDelimiter': '|',
            'ignoreUnknownValues': True,
            'maxBadRecords': 100,
            'nullMarker': r'\N',
            'quote': "'",
            'skipLeadingRows': 1,
            'sourceFormat': 'CSV',
            'writeDisposition': 'WRITE_TRUNCATE',
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            ]}
        }
        RESOURCE['configuration']['load'] = LOAD_CONFIGURATION
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        table = _Table()
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client1,
                             schema=[full_name, age])

        job.allow_jagged_rows = True
        job.allow_quoted_newlines = True
        job.create_disposition = 'CREATE_NEVER'
        job.encoding = 'ISO-8559-1'
        job.field_delimiter = '|'
        job.ignore_unknown_values = True
        job.max_bad_records = 100
        job.null_marker = r'\N'
        job.quote_character = "'"
        job.skip_leading_rows = 1
        job.source_format = 'CSV'
        job.write_disposition = 'WRITE_TRUNCATE'

        job.begin(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'load': LOAD_CONFIGURATION,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)

        self.assertFalse(job.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)

        job.reload()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancel_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s/cancel' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource(ended=True)
        RESPONSE = {'job': RESOURCE}
        conn = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client)

        job.cancel()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancel_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s/cancel' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource(ended=True)
        RESPONSE = {'job': RESOURCE}
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESPONSE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        table = _Table()
        job = self._make_one(self.JOB_NAME, table, [self.SOURCE1], client1)

        job.cancel(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestCopyJob(unittest.TestCase, _Base):
    JOB_TYPE = 'copy'
    SOURCE_TABLE = 'source_table'
    DESTINATION_TABLE = 'destination_table'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import CopyJob

        return CopyJob

    def _makeResource(self, started=False, ended=False):
        resource = super(TestCopyJob, self)._makeResource(
            started, ended)
        config = resource['configuration']['copy']
        config['sourceTables'] = [{
            'projectId': self.PROJECT,
            'datasetId': self.DS_NAME,
            'tableId': self.SOURCE_TABLE,
        }]
        config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_NAME,
            'tableId': self.DESTINATION_TABLE,
        }

        return resource

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('copy')

        table_ref = config['destinationTable']
        self.assertEqual(job.destination.project, table_ref['projectId'])
        self.assertEqual(job.destination.dataset_name, table_ref['datasetId'])
        self.assertEqual(job.destination.name, table_ref['tableId'])

        sources = config.get('sourceTables')
        if sources is None:
            sources = [config['sourceTable']]
        self.assertEqual(len(sources), len(job.sources))
        for table_ref, table in zip(sources, job.sources):
            self.assertEqual(table.project, table_ref['projectId'])
            self.assertEqual(table.dataset_name, table_ref['datasetId'])
            self.assertEqual(table.name, table_ref['tableId'])

        if 'createDisposition' in config:
            self.assertEqual(job.create_disposition,
                             config['createDisposition'])
        else:
            self.assertIsNone(job.create_disposition)

        if 'writeDisposition' in config:
            self.assertEqual(job.write_disposition,
                             config['writeDisposition'])
        else:
            self.assertIsNone(job.write_disposition)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_NAME, destination, [source], client)
        self.assertIs(job.destination, destination)
        self.assertEqual(job.sources, [source])
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertIsNone(job.create_disposition)
        self.assertIsNone(job.write_disposition)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_NAME),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'copy': {
                    'sourceTables': [{
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.SOURCE_TABLE,
                    }],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.DESTINATION_TABLE,
                    },
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_sourcetable(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'copy': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.SOURCE_TABLE,
                    },
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.DESTINATION_TABLE,
                    },
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_wo_sources(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'copy': {
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.DESTINATION_TABLE,
                    },
                }
            },
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        klass = self._get_target_class()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(dataset._client, client)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_begin_w_bound_client(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_NAME, destination, [source], client)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'copy': {
                    'sourceTables': [{
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.SOURCE_TABLE
                    }],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.DESTINATION_TABLE,
                    },
                },
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_alternate_client(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource(ended=True)
        COPY_CONFIGURATION = {
            'sourceTables': [{
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.SOURCE_TABLE,
            }],
            'destinationTable': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.DESTINATION_TABLE,
            },
            'createDisposition': 'CREATE_NEVER',
            'writeDisposition': 'WRITE_TRUNCATE',
        }
        RESOURCE['configuration']['copy'] = COPY_CONFIGURATION
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_NAME, destination, [source], client1)

        job.create_disposition = 'CREATE_NEVER'
        job.write_disposition = 'WRITE_TRUNCATE'

        job.begin(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'copy': COPY_CONFIGURATION,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_NAME, destination, [source], client)

        self.assertFalse(job.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_NAME, destination, [source], client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_NAME, destination, [source], client)

        job.reload()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_NAME, destination, [source], client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestExtractTableToStorageJob(unittest.TestCase, _Base):
    JOB_TYPE = 'extract'
    SOURCE_TABLE = 'source_table'
    DESTINATION_URI = 'gs://bucket_name/object_name'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import ExtractTableToStorageJob

        return ExtractTableToStorageJob

    def _makeResource(self, started=False, ended=False):
        resource = super(TestExtractTableToStorageJob, self)._makeResource(
            started, ended)
        config = resource['configuration']['extract']
        config['sourceTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_NAME,
            'tableId': self.SOURCE_TABLE,
        }
        config['destinationUris'] = [self.DESTINATION_URI]
        return resource

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('extract')

        self.assertEqual(job.destination_uris, config['destinationUris'])

        table_ref = config['sourceTable']
        self.assertEqual(job.source.project, table_ref['projectId'])
        self.assertEqual(job.source.dataset_name, table_ref['datasetId'])
        self.assertEqual(job.source.name, table_ref['tableId'])

        if 'compression' in config:
            self.assertEqual(job.compression,
                             config['compression'])
        else:
            self.assertIsNone(job.compression)

        if 'destinationFormat' in config:
            self.assertEqual(job.destination_format,
                             config['destinationFormat'])
        else:
            self.assertIsNone(job.destination_format)

        if 'fieldDelimiter' in config:
            self.assertEqual(job.field_delimiter,
                             config['fieldDelimiter'])
        else:
            self.assertIsNone(job.field_delimiter)

        if 'printHeader' in config:
            self.assertEqual(job.print_header,
                             config['printHeader'])
        else:
            self.assertIsNone(job.print_header)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_NAME, source, [self.DESTINATION_URI],
                             client)
        self.assertEqual(job.source, source)
        self.assertEqual(job.destination_uris, [self.DESTINATION_URI])
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertIsNone(job.compression)
        self.assertIsNone(job.destination_format)
        self.assertIsNone(job.field_delimiter)
        self.assertIsNone(job.print_header)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_NAME),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.SOURCE_TABLE,
                    },
                    'destinationUris': [self.DESTINATION_URI],
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        klass = self._get_target_class()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(dataset._client, client)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_begin_w_bound_client(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_NAME, source, [self.DESTINATION_URI],
                             client)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_NAME,
                        'tableId': self.SOURCE_TABLE
                    },
                    'destinationUris': [self.DESTINATION_URI],
                },
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_alternate_client(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource(ended=True)
        EXTRACT_CONFIGURATION = {
            'sourceTable': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
                'tableId': self.SOURCE_TABLE,
            },
            'destinationUris': [self.DESTINATION_URI],
            'compression': 'GZIP',
            'destinationFormat': 'NEWLINE_DELIMITED_JSON',
            'fieldDelimiter': '|',
            'printHeader': False,
        }
        RESOURCE['configuration']['extract'] = EXTRACT_CONFIGURATION
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_NAME, source, [self.DESTINATION_URI],
                             client1)

        job.compression = 'GZIP'
        job.destination_format = 'NEWLINE_DELIMITED_JSON'
        job.field_delimiter = '|'
        job.print_header = False

        job.begin(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'extract': EXTRACT_CONFIGURATION,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_NAME, source, [self.DESTINATION_URI],
                             client)

        self.assertFalse(job.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_NAME, source, [self.DESTINATION_URI],
                             client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_NAME, source, [self.DESTINATION_URI],
                             client)

        job.reload()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_NAME, source, [self.DESTINATION_URI],
                             client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestQueryJob(unittest.TestCase, _Base):
    JOB_TYPE = 'query'
    QUERY = 'select count(*) from persons'
    DESTINATION_TABLE = 'destination_table'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import QueryJob

        return QueryJob

    def _makeResource(self, started=False, ended=False):
        resource = super(TestQueryJob, self)._makeResource(
            started, ended)
        config = resource['configuration']['query']
        config['query'] = self.QUERY

        if ended:
            resource['status'] = {'state': 'DONE'}

        return resource

    def _verifyBooleanResourceProperties(self, job, config):

        if 'allowLargeResults' in config:
            self.assertEqual(job.allow_large_results,
                             config['allowLargeResults'])
        else:
            self.assertIsNone(job.allow_large_results)
        if 'flattenResults' in config:
            self.assertEqual(job.flatten_results,
                             config['flattenResults'])
        else:
            self.assertIsNone(job.flatten_results)
        if 'useQueryCache' in config:
            self.assertEqual(job.use_query_cache,
                             config['useQueryCache'])
        else:
            self.assertIsNone(job.use_query_cache)
        if 'useLegacySql' in config:
            self.assertEqual(job.use_legacy_sql,
                             config['useLegacySql'])
        else:
            self.assertIsNone(job.use_legacy_sql)

    def _verifyIntegerResourceProperties(self, job, config):
        if 'maximumBillingTier' in config:
            self.assertEqual(job.maximum_billing_tier,
                             config['maximumBillingTier'])
        else:
            self.assertIsNone(job.maximum_billing_tier)
        if 'maximumBytesBilled' in config:
            self.assertEqual(job.maximum_bytes_billed,
                             config['maximumBytesBilled'])
        else:
            self.assertIsNone(job.maximum_bytes_billed)

    def _verify_udf_resources(self, job, config):
        udf_resources = config.get('userDefinedFunctionResources', ())
        self.assertEqual(len(job.udf_resources), len(udf_resources))
        for found, expected in zip(job.udf_resources, udf_resources):
            if 'resourceUri' in expected:
                self.assertEqual(found.udf_type, 'resourceUri')
                self.assertEqual(found.value, expected['resourceUri'])
            else:
                self.assertEqual(found.udf_type, 'inlineCode')
                self.assertEqual(found.value, expected['inlineCode'])

    def _verifyQueryParameters(self, job, config):
        query_parameters = config.get('queryParameters', ())
        self.assertEqual(len(job.query_parameters), len(query_parameters))
        for found, expected in zip(job.query_parameters, query_parameters):
            self.assertEqual(found.to_api_repr(), expected)

    def _verify_configuration_properties(self, job, configuration):
        if 'dryRun' in configuration:
            self.assertEqual(job.dry_run,
                             configuration['dryRun'])
        else:
            self.assertIsNone(job.dry_run)

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        configuration = resource.get('configuration', {})
        self._verify_configuration_properties(job, configuration)

        query_config = resource.get('configuration', {}).get('query')
        self._verifyBooleanResourceProperties(job, query_config)
        self._verifyIntegerResourceProperties(job, query_config)
        self._verify_udf_resources(job, query_config)
        self._verifyQueryParameters(job, query_config)

        self.assertEqual(job.query, query_config['query'])
        if 'createDisposition' in query_config:
            self.assertEqual(job.create_disposition,
                             query_config['createDisposition'])
        else:
            self.assertIsNone(job.create_disposition)
        if 'defaultDataset' in query_config:
            dataset = job.default_dataset
            ds_ref = {
                'projectId': dataset.project,
                'datasetId': dataset.name,
            }
            self.assertEqual(ds_ref, query_config['defaultDataset'])
        else:
            self.assertIsNone(job.default_dataset)
        if 'destinationTable' in query_config:
            table = job.destination
            tb_ref = {
                'projectId': table.project,
                'datasetId': table.dataset_name,
                'tableId': table.name
            }
            self.assertEqual(tb_ref, query_config['destinationTable'])
        else:
            self.assertIsNone(job.destination)
        if 'priority' in query_config:
            self.assertEqual(job.priority,
                             query_config['priority'])
        else:
            self.assertIsNone(job.priority)
        if 'writeDisposition' in query_config:
            self.assertEqual(job.write_disposition,
                             query_config['writeDisposition'])
        else:
            self.assertIsNone(job.write_disposition)

    def test_ctor_defaults(self):
        client = _Client(self.PROJECT)
        job = self._make_one(self.JOB_NAME, self.QUERY, client)
        self.assertEqual(job.query, self.QUERY)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertIsNone(job.allow_large_results)
        self.assertIsNone(job.create_disposition)
        self.assertIsNone(job.default_dataset)
        self.assertIsNone(job.destination)
        self.assertIsNone(job.flatten_results)
        self.assertIsNone(job.priority)
        self.assertIsNone(job.use_query_cache)
        self.assertIsNone(job.use_legacy_sql)
        self.assertIsNone(job.dry_run)
        self.assertIsNone(job.write_disposition)
        self.assertIsNone(job.maximum_billing_tier)
        self.assertIsNone(job.maximum_bytes_billed)

    def test_ctor_w_udf_resources(self):
        from google.cloud.bigquery._helpers import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        client = _Client(self.PROJECT)
        job = self._make_one(self.JOB_NAME, self.QUERY, client,
                             udf_resources=udf_resources)
        self.assertEqual(job.udf_resources, udf_resources)

    def test_ctor_w_query_parameters(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", 'INT64', 123)]
        client = _Client(self.PROJECT)
        job = self._make_one(self.JOB_NAME, self.QUERY, client,
                             query_parameters=query_parameters)
        self.assertEqual(job.query_parameters, query_parameters)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_NAME),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'query': {'query': self.QUERY}
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        RESOURCE['configuration']['query']['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_NAME,
            'tableId': self.DESTINATION_TABLE,
        }
        klass = self._get_target_class()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(dataset._client, client)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_cancelled(self):
        client = _Client(self.PROJECT)
        job = self._make_one(self.JOB_NAME, self.QUERY, client)
        job._properties['status'] = {
            'state': 'DONE',
            'errorResult': {
                'reason': 'stopped'
            }
        }

        self.assertTrue(job.cancelled())

    def test_done(self):
        client = _Client(self.PROJECT)
        resource = self._makeResource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)
        self.assertTrue(job.done())

    def test_query_results(self):
        from google.cloud.bigquery.query import QueryResults

        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
        }
        connection = _Connection(query_resource)
        client = _Client(self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_NAME, self.QUERY, client)
        results = job.query_results()
        self.assertIsInstance(results, QueryResults)

    def test_query_results_w_cached_value(self):
        from google.cloud.bigquery.query import QueryResults

        client = _Client(self.PROJECT)
        job = self._make_one(self.JOB_NAME, self.QUERY, client)
        query_results = QueryResults(None, client)
        job._query_results = query_results

        results = job.query_results()

        self.assertIs(results, query_results)

    def test_result(self):
        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
        }
        connection = _Connection(query_resource, query_resource)
        client = _Client(self.PROJECT, connection=connection)
        resource = self._makeResource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        result = job.result()

        self.assertEqual(list(result), [])

    def test_result_invokes_begins(self):
        begun_resource = self._makeResource()
        incomplete_resource = {'jobComplete': False}
        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
        }
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _Connection(
            begun_resource, incomplete_resource, query_resource, done_resource,
            query_resource)
        client = _Client(self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_NAME, self.QUERY, client)

        job.result()

        self.assertEqual(len(connection._requested), 4)
        begin_request, _, query_request, reload_request = connection._requested
        self.assertEqual(begin_request['method'], 'POST')
        self.assertEqual(query_request['method'], 'GET')
        self.assertEqual(reload_request['method'], 'GET')

    def test_result_error(self):
        from google.cloud import exceptions

        client = _Client(self.PROJECT)
        job = self._make_one(self.JOB_NAME, self.QUERY, client)
        error_result = {
            'debugInfo': 'DEBUG',
            'location': 'LOCATION',
            'message': 'MESSAGE',
            'reason': 'invalid'
        }
        job._properties['status'] = {
            'errorResult': error_result,
            'errors': [error_result],
            'state': 'DONE'
        }
        job._set_future_result()

        with self.assertRaises(exceptions.GoogleCloudError) as exc_info:
            job.result()

        self.assertIsInstance(exc_info.exception, exceptions.GoogleCloudError)
        self.assertEqual(exc_info.exception.code, http_client.BAD_REQUEST)

    def test_begin_w_bound_client(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_NAME, self.QUERY, client)

        job.begin()
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY
                },
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_alternate_client(self):
        from google.cloud.bigquery.dataset import Dataset
        from google.cloud.bigquery.dataset import Table

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        TABLE = 'TABLE'
        DS_NAME = 'DATASET'
        RESOURCE = self._makeResource(ended=True)
        QUERY_CONFIGURATION = {
            'query': self.QUERY,
            'allowLargeResults': True,
            'createDisposition': 'CREATE_NEVER',
            'defaultDataset': {
                'projectId': self.PROJECT,
                'datasetId': DS_NAME,
            },
            'destinationTable': {
                'projectId': self.PROJECT,
                'datasetId': DS_NAME,
                'tableId': TABLE,
            },
            'flattenResults': True,
            'priority': 'INTERACTIVE',
            'useQueryCache': True,
            'useLegacySql': True,
            'writeDisposition': 'WRITE_TRUNCATE',
            'maximumBillingTier': 4,
            'maximumBytesBilled': 123456
        }
        RESOURCE['configuration']['query'] = QUERY_CONFIGURATION
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        job = self._make_one(self.JOB_NAME, self.QUERY, client1)

        dataset = Dataset(DS_NAME, client1)
        table = Table(TABLE, dataset)

        job.allow_large_results = True
        job.create_disposition = 'CREATE_NEVER'
        job.default_dataset = dataset
        job.destination = table
        job.flatten_results = True
        job.priority = 'INTERACTIVE'
        job.use_query_cache = True
        job.use_legacy_sql = True
        job.dry_run = True
        RESOURCE['configuration']['dryRun'] = True
        job.write_disposition = 'WRITE_TRUNCATE'
        job.maximum_billing_tier = 4
        job.maximum_bytes_billed = 123456

        job.begin(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'dryRun': True,
                'query': QUERY_CONFIGURATION,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_udf(self):
        from google.cloud.bigquery._helpers import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        INLINE_UDF_CODE = 'var someCode = "here";'
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        RESOURCE['configuration']['query']['userDefinedFunctionResources'] = [
            {'resourceUri': RESOURCE_URI},
            {'inlineCode': INLINE_UDF_CODE},
        ]
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        udf_resources = [
            UDFResource("resourceUri", RESOURCE_URI),
            UDFResource("inlineCode", INLINE_UDF_CODE),
        ]
        job = self._make_one(self.JOB_NAME, self.QUERY, client,
                             udf_resources=udf_resources)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(job.udf_resources, udf_resources)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'userDefinedFunctionResources': [
                        {'resourceUri': RESOURCE_URI},
                        {'inlineCode': INLINE_UDF_CODE},
                    ]
                },
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_named_query_parameter(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter('foo', 'INT64', 123)]
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        config = RESOURCE['configuration']['query']
        config['parameterMode'] = 'NAMED'
        config['queryParameters'] = [
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
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_NAME, self.QUERY, client,
                             query_parameters=query_parameters)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(job.query_parameters, query_parameters)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'parameterMode': 'NAMED',
                    'queryParameters': config['queryParameters'],
                },
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_positional_query_parameter(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter.positional('INT64', 123)]
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        config = RESOURCE['configuration']['query']
        config['parameterMode'] = 'POSITIONAL'
        config['queryParameters'] = [
            {
                'parameterType': {
                    'type': 'INT64',
                },
                'parameterValue': {
                    'value': '123',
                },
            },
        ]
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_NAME, self.QUERY, client,
                             query_parameters=query_parameters)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(job.query_parameters, query_parameters)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'parameterMode': 'POSITIONAL',
                    'queryParameters': config['queryParameters'],
                },
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_dry_run_query(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_NAME, self.QUERY, client)
        job.dry_run = True
        RESOURCE['configuration']['dryRun'] = True

        job.begin()
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY
                },
                'dryRun': True,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_NAME, self.QUERY, client)

        self.assertFalse(job.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        job = self._make_one(self.JOB_NAME, self.QUERY, client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        from google.cloud.bigquery.dataset import Dataset
        from google.cloud.bigquery.dataset import Table

        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        DS_NAME = 'DATASET'
        DEST_TABLE = 'dest_table'
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_NAME, None, client)

        dataset = Dataset(DS_NAME, client)
        table = Table(DEST_TABLE, dataset)
        job.destination = table

        job.reload()

        self.assertIsNone(job.destination)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        DS_NAME = 'DATASET'
        DEST_TABLE = 'dest_table'
        RESOURCE = self._makeResource()
        q_config = RESOURCE['configuration']['query']
        q_config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': DS_NAME,
            'tableId': DEST_TABLE,
        }
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        job = self._make_one(self.JOB_NAME, self.QUERY, client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)


class _Client(object):

    def __init__(self, project='project', connection=None):
        self.project = project
        self._connection = connection

    def dataset(self, name):
        from google.cloud.bigquery.dataset import Dataset

        return Dataset(name, client=self)

    def _get_query_results(self, job_id):
        from google.cloud.bigquery.query import QueryResults

        resource = self._connection.api_request(method='GET')
        return QueryResults.from_api_repr(resource, self)


class _Table(object):

    def __init__(self, name=None):
        self._name = name

    @property
    def name(self):
        if self._name is not None:
            return self._name
        return TestLoadTableFromStorageJob.TABLE_NAME

    @property
    def project(self):
        return TestLoadTableFromStorageJob.PROJECT

    @property
    def dataset_name(self):
        return TestLoadTableFromStorageJob.DS_NAME


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from google.cloud.exceptions import NotFound

        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except IndexError:
            raise NotFound('miss')
        else:
            return response
