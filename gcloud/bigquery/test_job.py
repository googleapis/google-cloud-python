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
    JOB_NAME = 'job_name'

    def _getTargetClass(self):
        from gcloud.bigquery.job import LoadFromStorageJob
        return LoadFromStorageJob

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

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


class _Client(object):

    def __init__(self, project='project', connection=None):
        self.project = project
        self.connection = connection


class _Table(object):

    def __init__(self):
        pass
