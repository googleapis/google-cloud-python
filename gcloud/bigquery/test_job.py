# pylint: disable=C0302
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


class Test_ConfigurationProperty(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigquery.job import _ConfigurationProperty
        return _ConfigurationProperty

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_it(self):

        class Configuration(object):
            _attr = None

        class Wrapper(object):
            attr = self._makeOne('attr')

            def __init__(self):
                self._configuration = Configuration()

        self.assertEqual(Wrapper.attr.name, 'attr')

        wrapper = Wrapper()
        self.assertEqual(wrapper.attr, None)

        value = object()
        wrapper.attr = value
        self.assertTrue(wrapper.attr is value)
        self.assertTrue(wrapper._configuration._attr is value)

        del wrapper.attr
        self.assertEqual(wrapper.attr, None)
        self.assertEqual(wrapper._configuration._attr, None)


class Test_TypedProperty(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigquery.job import _TypedProperty
        return _TypedProperty

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_it(self):

        class Configuration(object):
            _attr = None

        class Wrapper(object):
            attr = self._makeOne('attr', int)

            def __init__(self):
                self._configuration = Configuration()

        wrapper = Wrapper()
        with self.assertRaises(ValueError):
            wrapper.attr = 'BOGUS'

        wrapper.attr = 42
        self.assertEqual(wrapper.attr, 42)
        self.assertEqual(wrapper._configuration._attr, 42)

        del wrapper.attr
        self.assertEqual(wrapper.attr, None)
        self.assertEqual(wrapper._configuration._attr, None)


class Test_EnumProperty(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigquery.job import _EnumProperty
        return _EnumProperty

    def test_it(self):

        class Sub(self._getTargetClass()):
            ALLOWED = ('FOO', 'BAR', 'BAZ')

        class Configuration(object):
            _attr = None

        class Wrapper(object):
            attr = Sub('attr')

            def __init__(self):
                self._configuration = Configuration()

        wrapper = Wrapper()
        with self.assertRaises(ValueError):
            wrapper.attr = 'BOGUS'

        wrapper.attr = 'FOO'
        self.assertEqual(wrapper.attr, 'FOO')
        self.assertEqual(wrapper._configuration._attr, 'FOO')

        del wrapper.attr
        self.assertEqual(wrapper.attr, None)
        self.assertEqual(wrapper._configuration._attr, None)


class _Base(object):
    PROJECT = 'project'
    SOURCE1 = 'http://example.com/source1.csv'
    DS_NAME = 'datset_name'
    TABLE_NAME = 'table_name'
    JOB_NAME = 'job_name'

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
        self.assertEqual(job.etag, None)
        self.assertEqual(job.job_id, None)
        self.assertEqual(job.self_link, None)
        self.assertEqual(job.user_email, None)

        # derived from resource['statistics']
        self.assertEqual(job.created, None)
        self.assertEqual(job.started, None)
        self.assertEqual(job.ended, None)

        # derived from resource['status']
        self.assertEqual(job.error_result, None)
        self.assertEqual(job.errors, None)
        self.assertEqual(job.state, None)

    def _verifyReadonlyResourceProperties(self, job, resource):
        from datetime import timedelta

        self.assertEqual(job.job_id, self.JOB_ID)

        statistics = resource.get('statistics', {})

        if 'creationTime' in statistics:
            self.assertEqual(job.created, self.WHEN)
        else:
            self.assertEqual(job.created, None)

        if 'startTime' in statistics:
            self.assertEqual(job.started, self.WHEN)
        else:
            self.assertEqual(job.started, None)

        if 'endTime' in statistics:
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


class TestLoadTableFromStorageJob(unittest2.TestCase, _Base):
    JOB_TYPE = 'load'

    def _getTargetClass(self):
        from gcloud.bigquery.job import LoadTableFromStorageJob
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

        if ended:
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

        self._verifyInitialReadonlyProperties(job)

        # derived from resource['statistics']['load']
        self.assertEqual(job.input_file_bytes, None)
        self.assertEqual(job.input_files, None)
        self.assertEqual(job.output_bytes, None)
        self.assertEqual(job.output_rows, None)

        # set/read from resource['configuration']['load']
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
        from gcloud._helpers import _millis

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

        status = job._properties['status'] = {}

        self.assertEqual(job.error_result, None)
        self.assertEqual(job.errors, None)
        self.assertEqual(job.state, None)

        status['errorResult'] = ERROR_RESULT
        status['errors'] = [ERROR_RESULT]
        status['state'] = 'STATE'

        self.assertEqual(job.error_result, ERROR_RESULT)
        self.assertEqual(job.errors, [ERROR_RESULT])
        self.assertEqual(job.state, 'STATE')

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

    def test_begin_w_alternate_client(self):
        from gcloud.bigquery.table import SchemaField
        PATH = 'projects/%s/jobs' % self.PROJECT
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

    def test_cancel_w_bound_client(self):
        PATH = 'projects/%s/jobs/%s/cancel' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client)

        job.cancel()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancel_w_alternate_client(self):
        PATH = 'projects/%s/jobs/%s/cancel' % (self.PROJECT, self.JOB_NAME)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        table = _Table()
        job = self._makeOne(self.JOB_NAME, table, [self.SOURCE1], client1)

        job.cancel(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestCopyJob(unittest2.TestCase, _Base):
    JOB_TYPE = 'copy'
    SOURCE_TABLE = 'source_table'
    DESTINATION_TABLE = 'destination_table'

    def _getTargetClass(self):
        from gcloud.bigquery.job import CopyJob
        return CopyJob

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('copy')

        if 'createDisposition' in config:
            self.assertEqual(job.create_disposition,
                             config['createDisposition'])
        else:
            self.assertTrue(job.create_disposition is None)

        if 'writeDisposition' in config:
            self.assertEqual(job.write_disposition,
                             config['writeDisposition'])
        else:
            self.assertTrue(job.write_disposition is None)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._makeOne(self.JOB_NAME, destination, [source], client)
        self.assertTrue(job.destination is destination)
        self.assertEqual(job.sources, [source])
        self.assertTrue(job._client is client)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertTrue(job.create_disposition is None)
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
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._makeOne(self.JOB_NAME, destination, [source], client)

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
        PATH = 'projects/%s/jobs' % self.PROJECT
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
        job = self._makeOne(self.JOB_NAME, destination, [source], client1)

        job.create_disposition = 'CREATE_NEVER'
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
                'copy': COPY_CONFIGURATION,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = 'projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._makeOne(self.JOB_NAME, destination, [source], client)

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
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._makeOne(self.JOB_NAME, destination, [source], client1)

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
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._makeOne(self.JOB_NAME, destination, [source], client)

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
        source = _Table(self.SOURCE_TABLE)
        destination = _Table(self.DESTINATION_TABLE)
        job = self._makeOne(self.JOB_NAME, destination, [source], client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestExtractTableToStorageJob(unittest2.TestCase, _Base):
    JOB_TYPE = 'extract'
    SOURCE_TABLE = 'source_table'
    DESTINATION_URI = 'gs://bucket_name/object_name'

    def _getTargetClass(self):
        from gcloud.bigquery.job import ExtractTableToStorageJob
        return ExtractTableToStorageJob

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('extract')

        if 'compression' in config:
            self.assertEqual(job.compression,
                             config['compression'])
        else:
            self.assertTrue(job.compression is None)

        if 'destinationFormat' in config:
            self.assertEqual(job.destination_format,
                             config['destinationFormat'])
        else:
            self.assertTrue(job.destination_format is None)

        if 'fieldDelimiter' in config:
            self.assertEqual(job.field_delimiter,
                             config['fieldDelimiter'])
        else:
            self.assertTrue(job.field_delimiter is None)

        if 'printHeader' in config:
            self.assertEqual(job.print_header,
                             config['printHeader'])
        else:
            self.assertTrue(job.print_header is None)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        source = _Table(self.SOURCE_TABLE)
        job = self._makeOne(self.JOB_NAME, source, [self.DESTINATION_URI],
                            client)
        self.assertEqual(job.source, source)
        self.assertEqual(job.destination_uris, [self.DESTINATION_URI])
        self.assertTrue(job._client is client)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertTrue(job.compression is None)
        self.assertTrue(job.destination_format is None)
        self.assertTrue(job.field_delimiter is None)
        self.assertTrue(job.print_header is None)

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
        source = _Table(self.SOURCE_TABLE)
        job = self._makeOne(self.JOB_NAME, source, [self.DESTINATION_URI],
                            client)

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
        PATH = 'projects/%s/jobs' % self.PROJECT
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
        job = self._makeOne(self.JOB_NAME, source, [self.DESTINATION_URI],
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
        self.assertEqual(req['path'], '/%s' % PATH)
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
        PATH = 'projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        source = _Table(self.SOURCE_TABLE)
        job = self._makeOne(self.JOB_NAME, source, [self.DESTINATION_URI],
                            client)

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
        source = _Table(self.SOURCE_TABLE)
        job = self._makeOne(self.JOB_NAME, source, [self.DESTINATION_URI],
                            client1)

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
        source = _Table(self.SOURCE_TABLE)
        job = self._makeOne(self.JOB_NAME, source, [self.DESTINATION_URI],
                            client)

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
        source = _Table(self.SOURCE_TABLE)
        job = self._makeOne(self.JOB_NAME, source, [self.DESTINATION_URI],
                            client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestRunAsyncQueryJob(unittest2.TestCase, _Base):
    JOB_TYPE = 'query'
    QUERY = 'select count(*) from persons'

    def _getTargetClass(self):
        from gcloud.bigquery.job import RunAsyncQueryJob
        return RunAsyncQueryJob

    def _verifyBooleanResourceProperties(self, job, config):

        if 'allowLargeResults' in config:
            self.assertEqual(job.allow_large_results,
                             config['allowLargeResults'])
        else:
            self.assertTrue(job.allow_large_results is None)
        if 'flattenResults' in config:
            self.assertEqual(job.flatten_results,
                             config['flattenResults'])
        else:
            self.assertTrue(job.flatten_results is None)
        if 'useQueryCache' in config:
            self.assertEqual(job.use_query_cache,
                             config['useQueryCache'])
        else:
            self.assertTrue(job.use_query_cache is None)

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('query')
        self._verifyBooleanResourceProperties(job, config)

        if 'createDisposition' in config:
            self.assertEqual(job.create_disposition,
                             config['createDisposition'])
        else:
            self.assertTrue(job.create_disposition is None)
        if 'defaultDataset' in config:
            dataset = job.default_dataset
            ds_ref = {
                'projectId': dataset.project,
                'datasetId': dataset.name,
            }
            self.assertEqual(ds_ref, config['defaultDataset'])
        else:
            self.assertTrue(job.default_dataset is None)
        if 'destinationTable' in config:
            table = job.destination_table
            tb_ref = {
                'projectId': table.project,
                'datasetId': table.dataset_name,
                'tableId': table.name
            }
            self.assertEqual(tb_ref, config['destinationTable'])
        else:
            self.assertTrue(job.destination_table is None)
        if 'priority' in config:
            self.assertEqual(job.priority,
                             config['priority'])
        else:
            self.assertTrue(job.priority is None)
        if 'writeDisposition' in config:
            self.assertEqual(job.write_disposition,
                             config['writeDisposition'])
        else:
            self.assertTrue(job.write_disposition is None)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        job = self._makeOne(self.JOB_NAME, self.QUERY, client)
        self.assertEqual(job.query, self.QUERY)
        self.assertTrue(job._client is client)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertTrue(job.allow_large_results is None)
        self.assertTrue(job.create_disposition is None)
        self.assertTrue(job.default_dataset is None)
        self.assertTrue(job.destination_table is None)
        self.assertTrue(job.flatten_results is None)
        self.assertTrue(job.priority is None)
        self.assertTrue(job.use_query_cache is None)
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
        job = self._makeOne(self.JOB_NAME, self.QUERY, client)

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
                'query': {
                    'query': self.QUERY,
                },
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_alternate_client(self):
        from gcloud.bigquery.dataset import Dataset
        from gcloud.bigquery.dataset import Table
        PATH = 'projects/%s/jobs' % self.PROJECT
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
            'writeDisposition': 'WRITE_TRUNCATE',
        }
        RESOURCE['configuration']['query'] = QUERY_CONFIGURATION
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        job = self._makeOne(self.JOB_NAME, self.QUERY, client1)

        dataset = Dataset(DS_NAME, client1)
        table = Table(TABLE, dataset)

        job.allow_large_results = True
        job.create_disposition = 'CREATE_NEVER'
        job.default_dataset = dataset
        job.destination_table = table
        job.flatten_results = True
        job.priority = 'INTERACTIVE'
        job.use_query_cache = True
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
                'query': QUERY_CONFIGURATION,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = 'projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._makeOne(self.JOB_NAME, self.QUERY, client)

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
        job = self._makeOne(self.JOB_NAME, self.QUERY, client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        from gcloud.bigquery.dataset import Dataset
        from gcloud.bigquery.dataset import Table
        PATH = 'projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
        DS_NAME = 'DATASET'
        DEST_TABLE = 'dest_table'
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        job = self._makeOne(self.JOB_NAME, self.QUERY, client)

        dataset = Dataset(DS_NAME, client)
        table = Table(DEST_TABLE, dataset)
        job.destination_table = table

        job.reload()

        self.assertEqual(job.destination_table, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = 'projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME)
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
        job = self._makeOne(self.JOB_NAME, self.QUERY, client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestRunSyncQueryJob(unittest2.TestCase, _Base):
    JOB_NAME = 'test-synchronous-query'
    JOB_TYPE = 'query'
    QUERY = 'select count(*) from persons'
    TOKEN = 'TOKEN'

    def _getTargetClass(self):
        from gcloud.bigquery.job import RunSyncQueryJob
        return RunSyncQueryJob

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
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response
