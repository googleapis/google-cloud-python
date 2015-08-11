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


class TestLoadFromStorageJob(unittest2.TestCase):
    PROJECT = 'project'
    SOURCE1 = 'http://example.com/source1.csv'
    DS_NAME = 'datset_name'
    TABLE_NAME = 'table_name'
    JOB_NAME = 'job_name'

    def _getTargetClass(self):
        from gcloud.bigquery.job import LoadFromStorageJob
        return LoadFromStorageJob

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from gcloud._helpers import UTC

        self.WHEN_TS = 1437767599.006
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(
            tzinfo=UTC)
        self.ETAG = 'ETAG'
        self.JOB_ID = '%s:%s' % (self.PROJECT, self.JOB_NAME)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'
        self.USER_EMAIL = 'phred@example.com'
        self.INPUT_FILES = 2
        self.INPUT_BYTES = 12345
        self.OUTPUT_BYTES = 23456
        self.OUTPUT_ROWS = 345

    def _makeResource(self, started=False, ended=False):
        self._setUpConstants()
        resource = {
            'configuration': {
                'load': {
                },
            },
            'statistics': {
                'creationTime': self.WHEN_TS * 1000,
                'load': {
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
            resource['statistics']['load']['inputFiles'] = self.INPUT_FILES
            resource['statistics']['load']['inputFileBytes'] = self.INPUT_BYTES
            resource['statistics']['load']['outputBytes'] = self.OUTPUT_BYTES
            resource['statistics']['load']['outputRows'] = self.OUTPUT_ROWS

        return resource

    def _verifyReadonlyResourceProperties(self, job, resource):
        from datetime import timedelta

        self.assertEqual(job.job_id, self.JOB_ID)

        if 'creationTime' in resource.get('statistics', {}):
            self.assertEqual(job.created, self.WHEN)
        else:
            self.assertEqual(job.created, None)
        if 'startTime' in resource.get('statistics', {}):
            self.assertEqual(job.started, self.WHEN)
        else:
            self.assertEqual(job.started, None)
        if 'endTime' in resource.get('statistics', {}):
            self.assertEqual(job.ended, self.WHEN + timedelta(seconds=1000))
        else:
            self.assertEqual(job.ended, None)
        if 'etag' in resource:
            self.assertEqual(job.etag, self.ETAG)
        else:
            self.assertEqual(job.etag, None)
        if 'selfLink' in resource:
            self.assertEqual(job.self_link, self.RESOURCE_URL)
        else:
            self.assertEqual(job.self_link, None)
        if 'user_email' in resource:
            self.assertEqual(job.user_email, self.USER_EMAIL)
        else:
            self.assertEqual(job.user_email, None)

    def _verifyBooleanConfigProperties(self, job, config):
        if 'allowJaggedRows' in config:
            self.assertEqual(job.allow_jagged_rows,
                             config['allowJaggedRows'])
        else:
            self.assertTrue(job.allow_jagged_rows is None)
        if 'allowQuotedNewlines' in config:
            self.assertEqual(job.allow_quoted_newlines,
                             config['allowQuotedNewlines'])
        else:
            self.assertTrue(job.allow_quoted_newlines is None)
        if 'ignoreUnknownValues' in config:
            self.assertEqual(job.ignore_unknown_values,
                             config['ignoreUnknownValues'])
        else:
            self.assertTrue(job.ignore_unknown_values is None)

    def _verifyEnumConfigProperties(self, job, config):
        if 'createDisposition' in config:
            self.assertEqual(job.create_disposition,
                             config['createDisposition'])
        else:
            self.assertTrue(job.create_disposition is None)
        if 'encoding' in config:
            self.assertEqual(job.encoding,
                             config['encoding'])
        else:
            self.assertTrue(job.encoding is None)
        if 'sourceFormat' in config:
            self.assertEqual(job.source_format,
                             config['sourceFormat'])
        else:
            self.assertTrue(job.source_format is None)
        if 'writeDisposition' in config:
            self.assertEqual(job.write_disposition,
                             config['writeDisposition'])
        else:
            self.assertTrue(job.write_disposition is None)

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('load')

        self._verifyBooleanConfigProperties(job, config)
        self._verifyEnumConfigProperties(job, config)

        if 'fieldDelimiter' in config:
            self.assertEqual(job.field_delimiter,
                             config['fieldDelimiter'])
        else:
            self.assertTrue(job.field_delimiter is None)
        if 'maxBadRecords' in config:
            self.assertEqual(job.max_bad_records,
                             config['maxBadRecords'])
        else:
            self.assertTrue(job.max_bad_records is None)
        if 'quote' in config:
            self.assertEqual(job.quote_character,
                             config['quote'])
        else:
            self.assertTrue(job.quote_character is None)
        if 'skipLeadingRows' in config:
            self.assertEqual(job.skip_leading_rows,
                             config['skipLeadingRows'])
        else:
            self.assertTrue(job.skip_leading_rows is None)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        self.assertTrue(job.destination is table)
        self.assertEqual(list(job.source_uris), [self.SOURCE1])
        self.assertTrue(job._client is client)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))
        self.assertEqual(job.schema, [])
        self.assertTrue(job.allow_jagged_rows is None)
        self.assertTrue(job.allow_quoted_newlines is None)
        self.assertTrue(job.create_disposition is None)
        self.assertTrue(job.encoding is None)
        self.assertTrue(job.field_delimiter is None)
        self.assertTrue(job.ignore_unknown_values is None)
        self.assertTrue(job.max_bad_records is None)
        self.assertTrue(job.quote_character is None)
        self.assertTrue(job.skip_leading_rows is None)
        self.assertTrue(job.source_format is None)
        self.assertTrue(job.write_disposition is None)

        # root elements of resource
        self.assertEqual(job.etag, None)
        self.assertEqual(job.job_id, None)
        self.assertEqual(job.self_link, None)
        self.assertEqual(job.user_email, None)

        # derived from resource['statistics']
        self.assertEqual(job.created, None)
        self.assertEqual(job.started, None)
        self.assertEqual(job.ended, None)

        # derived from resource['statistics']['load']
        self.assertEqual(job.input_file_bytes, None)
        self.assertEqual(job.input_files, None)
        self.assertEqual(job.output_bytes, None)
        self.assertEqual(job.output_rows, None)

        # derived from resource['status']
        self.assertEqual(job.error_result, None)
        self.assertEqual(job.errors, None)
        self.assertEqual(job.state, None)

    def test_ctor_w_schema(self):
        from gcloud.bigquery.table import SchemaField
        client = _Client(self.PROJECT)
        table = _Table()
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client,
                            schema=[full_name, age])
        self.assertEqual(job.schema, [full_name, age])

    def test_schema_setter_non_list(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(TypeError):
            job.schema = object()

    def test_schema_setter_invalid_field(self):
        from gcloud.bigquery.table import SchemaField
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        with self.assertRaises(ValueError):
            job.schema = [full_name, object()]

    def test_schema_setter(self):
        from gcloud.bigquery.table import SchemaField
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        job.schema = [full_name, age]
        self.assertEqual(job.schema, [full_name, age])

    def test_props_set_by_server(self):
        import datetime
        from gcloud._helpers import UTC
        from gcloud.bigquery._helpers import _millis

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
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
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

        status = job._properties['status'] = {}
        status['errorResult'] = ERROR_RESULT
        status['errors'] = [ERROR_RESULT]
        status['state'] = 'STATE'

        self.assertEqual(job.etag, 'ETAG')
        self.assertEqual(job.job_id, JOB_ID)
        self.assertEqual(job.self_link, URL)
        self.assertEqual(job.user_email, EMAIL)

        self.assertEqual(job.created, CREATED)
        self.assertEqual(job.started, STARTED)
        self.assertEqual(job.ended, ENDED)

        self.assertEqual(job.input_file_bytes, 12345)
        self.assertEqual(job.input_files, 1)
        self.assertEqual(job.output_bytes, 23456)
        self.assertEqual(job.output_rows, 345)

        self.assertEqual(job.error_result, ERROR_RESULT)
        self.assertEqual(job.errors, [ERROR_RESULT])
        self.assertEqual(job.state, 'STATE')

    def test_allow_jagged_rows_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.allow_jagged_rows = object()

    def test_allow_jagged_rows_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.allow_jagged_rows = True
        self.assertTrue(job.allow_jagged_rows)
        del job.allow_jagged_rows
        self.assertTrue(job.allow_jagged_rows is None)

    def test_allow_quoted_newlines_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.allow_quoted_newlines = object()

    def test_allow_quoted_newlines_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.allow_quoted_newlines = True
        self.assertTrue(job.allow_quoted_newlines)
        del job.allow_quoted_newlines
        self.assertTrue(job.allow_quoted_newlines is None)

    def test_create_disposition_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.create_disposition = 'BOGUS'

    def test_create_disposition_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.create_disposition = 'CREATE_IF_NEEDED'
        self.assertEqual(job.create_disposition, 'CREATE_IF_NEEDED')
        del job.create_disposition
        self.assertTrue(job.create_disposition is None)

    def test_encoding_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.encoding = 'BOGUS'

    def test_encoding_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.encoding = 'ISO-8559-1'
        self.assertEqual(job.encoding, 'ISO-8559-1')
        del job.encoding
        self.assertTrue(job.encoding is None)

    def test_field_delimiter_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.field_delimiter = object()

    def test_field_delimiter_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.field_delimiter = '|'
        self.assertEqual(job.field_delimiter, '|')
        del job.field_delimiter
        self.assertTrue(job.field_delimiter is None)

    def test_ignore_unknown_values_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.ignore_unknown_values = object()

    def test_ignore_unknown_values_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.ignore_unknown_values = True
        self.assertTrue(job.ignore_unknown_values)
        del job.ignore_unknown_values
        self.assertTrue(job.ignore_unknown_values is None)

    def test_max_bad_records_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.max_bad_records = object()

    def test_max_bad_records_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.max_bad_records = 100
        self.assertEqual(job.max_bad_records, 100)
        del job.max_bad_records
        self.assertTrue(job.max_bad_records is None)

    def test_quote_character_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.quote_character = object()

    def test_quote_character_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.quote_character = "'"
        self.assertEqual(job.quote_character, "'")
        del job.quote_character
        self.assertTrue(job.quote_character is None)

    def test_skip_leading_rows_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.skip_leading_rows = object()

    def test_skip_leading_rows_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.skip_leading_rows = 2
        self.assertEqual(job.skip_leading_rows, 2)
        del job.skip_leading_rows
        self.assertTrue(job.skip_leading_rows is None)

    def test_source_format_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.source_format = 'BOGUS'

    def test_source_format_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.source_format = 'NEWLINE_DELIMITED_JSON'
        self.assertEqual(job.source_format, 'NEWLINE_DELIMITED_JSON')
        del job.source_format
        self.assertTrue(job.source_format is None)

    def test_write_disposition_setter_bad_value(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        with self.assertRaises(ValueError):
            job.write_disposition = 'BOGUS'

    def test_write_disposition_setter_deleter(self):
        client = _Client(self.PROJECT)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)
        job.write_disposition = 'WRITE_TRUNCATE'
        self.assertEqual(job.write_disposition, 'WRITE_TRUNCATE')
        del job.write_disposition
        self.assertTrue(job.write_disposition is None)

    def test_begin_w_bound_client(self):
        PATH = 'projects/%s/jobs' % self.PROJECT
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'sourceUris': [self.SOURCE1],
                'destinationTable': {
                    'projectId': self.PROJECT,
                    'datasetId': self.DS_NAME,
                    'tableId': self.TABLE_NAME,
                },
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_alternate_client(self):
        from gcloud.bigquery.table import SchemaField
        PATH = 'projects/%s/jobs' % self.PROJECT
        RESOURCE = self._makeResource(ended=True)
        LOAD_CONFIGURATION = {
            'allowJaggedRows': True,
            'allowQuotedNewlines': True,
            'createDisposition': 'CREATE_NEVER',
            'encoding': 'ISO-8559-1',
            'fieldDelimiter': '|',
            'ignoreUnknownValues': True,
            'maxBadRecords': 100,
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
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client1,
                            schema=[full_name, age])

        job.allow_jagged_rows = True
        job.allow_quoted_newlines = True
        job.create_disposition = 'CREATE_NEVER'
        job.encoding = 'ISO-8559-1'
        job.field_delimiter = '|'
        job.ignore_unknown_values = True
        job.max_bad_records = 100
        job.quote_character = "'"
        job.skip_leading_rows = 1
        job.source_format = 'CSV'
        job.write_disposition = 'WRITE_TRUNCATE'

        job.begin(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_NAME,
            },
            'configuration': {
                'sourceUris': [self.SOURCE1],
                'destinationTable': {
                    'projectId': self.PROJECT,
                    'datasetId': self.DS_NAME,
                    'tableId': self.TABLE_NAME,
                },
                'load': LOAD_CONFIGURATION,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = 'projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)

        self.assertFalse(job.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = 'projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = 'projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)

        job.reload()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = 'projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(job, RESOURCE)


class _Client(object):

    def __init__(self, project='project', connection=None):
        self.project = project
        self.connection = connection


class _Table(object):

    def __init__(self):
        pass

    @property
    def name(self):
        return TestLoadFromStorageJob.TABLE_NAME

    @property
    def project(self):
        return TestLoadFromStorageJob.PROJECT

    @property
    def dataset_name(self):
        return TestLoadFromStorageJob.DS_NAME


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
