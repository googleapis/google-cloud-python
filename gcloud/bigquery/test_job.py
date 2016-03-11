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
        config = resource['configuration']['load']
        config['sourceUris'] = [self.SOURCE1]
        config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_NAME,
            'tableId': self.TABLE_NAME,
        }

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

        self.assertEqual(job.source_uris, config['sourceUris'])

        table_ref = config['destinationTable']
        self.assertEqual(job.destination.project, table_ref['projectId'])
        self.assertEqual(job.destination.dataset_name, table_ref['datasetId'])
        self.assertEqual(job.destination.name, table_ref['tableId'])

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
        self.assertEqual(job.job_type, self.JOB_TYPE)
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

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._getTargetClass()
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
        klass = self._getTargetClass()
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
        klass = self._getTargetClass()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(job._client is client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        klass = self._getTargetClass()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(dataset._client is client)
        self._verifyResourceProperties(dataset, RESOURCE)

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

        sources = config['sourceTables']
        self.assertEqual(len(sources), len(job.sources))
        for table_ref, table in zip(sources, job.sources):
            self.assertEqual(table.project, table_ref['projectId'])
            self.assertEqual(table.dataset_name, table_ref['datasetId'])
            self.assertEqual(table.name, table_ref['tableId'])

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
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertTrue(job.create_disposition is None)
        self.assertTrue(job.write_disposition is None)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._getTargetClass()
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
        klass = self._getTargetClass()
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
        klass = self._getTargetClass()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(job._client is client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        klass = self._getTargetClass()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(dataset._client is client)
        self._verifyResourceProperties(dataset, RESOURCE)

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
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertTrue(job.compression is None)
        self.assertTrue(job.destination_format is None)
        self.assertTrue(job.field_delimiter is None)
        self.assertTrue(job.print_header is None)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._getTargetClass()
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
        klass = self._getTargetClass()
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
        klass = self._getTargetClass()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(job._client is client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        klass = self._getTargetClass()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(dataset._client is client)
        self._verifyResourceProperties(dataset, RESOURCE)

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


class TestQueryJob(unittest2.TestCase, _Base):
    JOB_TYPE = 'query'
    QUERY = 'select count(*) from persons'
    DESTINATION_TABLE = 'destination_table'

    def _getTargetClass(self):
        from gcloud.bigquery.job import QueryJob
        return QueryJob

    def _makeResource(self, started=False, ended=False):
        resource = super(TestQueryJob, self)._makeResource(
            started, ended)
        config = resource['configuration']['query']
        config['query'] = self.QUERY
        return resource

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
            table = job.destination
            tb_ref = {
                'projectId': table.project,
                'datasetId': table.dataset_name,
                'tableId': table.name
            }
            self.assertEqual(tb_ref, config['destinationTable'])
        else:
            self.assertTrue(job.destination is None)
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
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_NAME))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertTrue(job.allow_large_results is None)
        self.assertTrue(job.create_disposition is None)
        self.assertTrue(job.default_dataset is None)
        self.assertTrue(job.destination is None)
        self.assertTrue(job.flatten_results is None)
        self.assertTrue(job.priority is None)
        self.assertTrue(job.use_query_cache is None)
        self.assertTrue(job.write_disposition is None)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._getTargetClass()
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
        klass = self._getTargetClass()
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
        klass = self._getTargetClass()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(job._client is client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        RESOURCE['configuration']['query']['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_NAME,
            'tableId': self.DESTINATION_TABLE,
        }
        klass = self._getTargetClass()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(dataset._client is client)
        self._verifyResourceProperties(dataset, RESOURCE)

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
        job.destination = table
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
        job.destination = table

        job.reload()

        self.assertEqual(job.destination, None)

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
