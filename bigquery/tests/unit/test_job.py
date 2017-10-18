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

from google.cloud.bigquery.job import ExtractJobConfig, CopyJobConfig
from google.cloud.bigquery.job import LoadJobConfig
from google.cloud.bigquery.dataset import DatasetReference

import mock


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project='test-project', connection=None):
    from google.cloud.bigquery.client import Client

    if connection is None:
        connection = _Connection()

    client = Client(
        project=project, credentials=_make_credentials(), _http=object())
    client._connection = connection
    return client


class Test__int_or_none(unittest.TestCase):

    def _call_fut(self, *args, **kwargs):
        from google.cloud.bigquery import job

        return job._int_or_none(*args, **kwargs)

    def test_w_int(self):
        self.assertEqual(self._call_fut(13), 13)

    def test_w_none(self):
        self.assertIsNone(self._call_fut(None))

    def test_w_str(self):
        self.assertEqual(self._call_fut('13'), 13)


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
    from google.cloud.bigquery.dataset import DatasetReference
    from google.cloud.bigquery.table import TableReference

    PROJECT = 'project'
    SOURCE1 = 'http://example.com/source1.csv'
    DS_ID = 'datset_id'
    DS_REF = DatasetReference(PROJECT, DS_ID)
    TABLE_ID = 'table_id'
    TABLE_REF = TableReference(DS_REF, TABLE_ID)
    JOB_ID = 'JOB_ID'

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from google.cloud._helpers import UTC

        self.WHEN_TS = 1437767599.006
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(
            tzinfo=UTC)
        self.ETAG = 'ETAG'
        self.FULL_JOB_ID = '%s:%s' % (self.PROJECT, self.JOB_ID)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'
        self.USER_EMAIL = 'phred@example.com'

    def _table_ref(self, table_id):
        from google.cloud.bigquery.table import TableReference

        return TableReference(self.DS_REF, table_id)

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
            'id': self.FULL_JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'selfLink': self.RESOURCE_URL,
            'user_email': self.USER_EMAIL,
        }

        if started or ended:
            resource['statistics']['startTime'] = self.WHEN_TS * 1000

        if ended:
            resource['statistics']['endTime'] = (self.WHEN_TS + 1000) * 1000

        if self.JOB_TYPE == 'query':
            resource['configuration']['query']['destinationTable'] = {
                'projectId': self.PROJECT,
                'datasetId': '_temp_dataset',
                'tableId': '_temp_table',
            }

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


class TestLoadJob(unittest.TestCase, _Base):
    JOB_TYPE = 'load'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import LoadJob

        return LoadJob

    def _setUpConstants(self):
        super(TestLoadJob, self)._setUpConstants()
        self.INPUT_FILES = 2
        self.INPUT_BYTES = 12345
        self.OUTPUT_BYTES = 23456
        self.OUTPUT_ROWS = 345

    def _makeResource(self, started=False, ended=False):
        resource = super(TestLoadJob, self)._makeResource(
            started, ended)
        config = resource['configuration']['load']
        config['sourceUris'] = [self.SOURCE1]
        config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
            'tableId': self.TABLE_ID,
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
        self.assertEqual(job.destination.dataset_id, table_ref['datasetId'])
        self.assertEqual(job.destination.table_id, table_ref['tableId'])

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
            self.assertEqual(str(job.skip_leading_rows),
                             config['skipLeadingRows'])
        else:
            self.assertIsNone(job.skip_leading_rows)

    def test_ctor(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client)
        self.assertIs(job.destination, self.TABLE_REF)
        self.assertEqual(list(job.source_uris), [self.SOURCE1])
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID))
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

    def test_ctor_w_config(self):
        from google.cloud.bigquery.schema import SchemaField

        client = _make_client(project=self.PROJECT)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        config = LoadJobConfig()
        config.schema = [full_name, age]
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client, config)
        self.assertEqual(job.schema, [full_name, age])

    def test_done(self):
        client = _make_client(project=self.PROJECT)
        resource = self._makeResource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)
        self.assertTrue(job.done())

    def test_result(self):
        client = _make_client(project=self.PROJECT)
        resource = self._makeResource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        result = job.result()

        self.assertIs(result, job)

    def test_result_invokes_begin(self):
        begun_resource = self._makeResource()
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _Connection(begun_resource, done_resource)
        client = _make_client(self.PROJECT)
        client._connection = connection

        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client)
        job.result()

        self.assertEqual(len(connection._requested), 2)
        begin_request,  reload_request = connection._requested
        self.assertEqual(begin_request['method'], 'POST')
        self.assertEqual(reload_request['method'], 'GET')

    def test_schema_setter_non_list(self):
        config = LoadJobConfig()
        with self.assertRaises(TypeError):
            config.schema = object()

    def test_schema_setter_invalid_field(self):
        from google.cloud.bigquery.schema import SchemaField

        config = LoadJobConfig()
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        with self.assertRaises(ValueError):
            config.schema = [full_name, object()]

    def test_schema_setter(self):
        from google.cloud.bigquery.schema import SchemaField

        config = LoadJobConfig()
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        config.schema = [full_name, age]
        self.assertEqual(config.schema, [full_name, age])

    def test_props_set_by_server(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis

        CREATED = datetime.datetime(2015, 8, 11, 12, 13, 22, tzinfo=UTC)
        STARTED = datetime.datetime(2015, 8, 11, 13, 47, 15, tzinfo=UTC)
        ENDED = datetime.datetime(2015, 8, 11, 14, 47, 15, tzinfo=UTC)
        FULL_JOB_ID = '%s:%s' % (self.PROJECT, self.JOB_ID)
        URL = 'http://example.com/projects/%s/jobs/%s' % (
            self.PROJECT, self.JOB_ID)
        EMAIL = 'phred@example.com'
        ERROR_RESULT = {'debugInfo': 'DEBUG',
                        'location': 'LOCATION',
                        'message': 'MESSAGE',
                        'reason': 'REASON'}

        client = _make_client(project=self.PROJECT)
        table = _Table()
        job = self._make_one(self.JOB_ID, [self.SOURCE1], table, client)
        job._properties['etag'] = 'ETAG'
        job._properties['id'] = FULL_JOB_ID
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
        client = _make_client(project=self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.JOB_ID),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.FULL_JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'load': {
                    'sourceUris': [self.SOURCE1],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.TABLE_ID,
                    },
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _make_client(project=self.PROJECT)
        RESOURCE = self._makeResource()
        load_config = RESOURCE['configuration']['load']
        load_config['createDisposition'] = 'CREATE_IF_NEEDED'
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_already_running(self):
        conn = _Connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client)
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
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'load': {
                    'sourceUris': [self.SOURCE1],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.TABLE_ID,
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
        client = _make_client(project=self.PROJECT, connection=conn)
        config = LoadJobConfig()
        config.autodetect = True
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client, config)
        job.begin()

        sent = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'load': {
                    'sourceUris': [self.SOURCE1],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.TABLE_ID,
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
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID,
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
            'skipLeadingRows': '1',
            'sourceFormat': 'CSV',
            'writeDisposition': 'WRITE_TRUNCATE',
            'schema': {'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            ]}
        }
        RESOURCE['configuration']['load'] = LOAD_CONFIGURATION
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        config = LoadJobConfig()
        config.schema = [full_name, age]
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client1, config)
        config.allow_jagged_rows = True
        config.allow_quoted_newlines = True
        config.create_disposition = 'CREATE_NEVER'
        config.encoding = 'ISO-8559-1'
        config.field_delimiter = '|'
        config.ignore_unknown_values = True
        config.max_bad_records = 100
        config.null_marker = r'\N'
        config.quote_character = "'"
        config.skip_leading_rows = 1
        config.source_format = 'CSV'
        config.write_disposition = 'WRITE_TRUNCATE'

        job.begin(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'load': LOAD_CONFIGURATION,
            },
        }
        self.maxDiff = None
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn = _Connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._make_one(self.JOB_ID, [self.SOURCE1], table, client)

        self.assertFalse(job.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        table = _Table()
        job = self._make_one(self.JOB_ID, [self.SOURCE1], table, client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._make_one(self.JOB_ID, [self.SOURCE1], table, client)

        job.reload()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        table = _Table()
        job = self._make_one(self.JOB_ID, [self.SOURCE1], table, client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancel_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s/cancel' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._makeResource(ended=True)
        RESPONSE = {'job': RESOURCE}
        conn = _Connection(RESPONSE)
        client = _make_client(project=self.PROJECT, connection=conn)
        table = _Table()
        job = self._make_one(self.JOB_ID, [self.SOURCE1], table, client)

        job.cancel()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancel_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s/cancel' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._makeResource(ended=True)
        RESPONSE = {'job': RESOURCE}
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESPONSE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        table = _Table()
        job = self._make_one(self.JOB_ID, [self.SOURCE1], table, client1)

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
            'datasetId': self.DS_ID,
            'tableId': self.SOURCE_TABLE,
        }]
        config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
            'tableId': self.DESTINATION_TABLE,
        }

        return resource

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('copy')

        table_ref = config['destinationTable']
        self.assertEqual(job.destination.project, table_ref['projectId'])
        self.assertEqual(job.destination.dataset_id, table_ref['datasetId'])
        self.assertEqual(job.destination.table_id, table_ref['tableId'])

        sources = config.get('sourceTables')
        if sources is None:
            sources = [config['sourceTable']]
        self.assertEqual(len(sources), len(job.sources))
        for table_ref, table in zip(sources, job.sources):
            self.assertEqual(table.project, table_ref['projectId'])
            self.assertEqual(table.dataset_id, table_ref['datasetId'])
            self.assertEqual(table.table_id, table_ref['tableId'])

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
        client = _make_client(project=self.PROJECT)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client)
        self.assertIs(job.destination, destination)
        self.assertEqual(job.sources, [source])
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertIsNone(job.create_disposition)
        self.assertIsNone(job.write_disposition)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_ID),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'copy': {
                    'sourceTables': [{
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.SOURCE_TABLE,
                    }],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
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
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'copy': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.SOURCE_TABLE,
                    },
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
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
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'copy': {
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.DESTINATION_TABLE,
                    },
                }
            },
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_w_properties(self):
        client = _make_client(project=self.PROJECT)
        RESOURCE = self._makeResource()
        copy_config = RESOURCE['configuration']['copy']
        copy_config['createDisposition'] = 'CREATE_IF_NEEDED'
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_bound_client(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _Connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'copy': {
                    'sourceTables': [{
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.SOURCE_TABLE
                    }],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
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
                'datasetId': self.DS_ID,
                'tableId': self.SOURCE_TABLE,
            }],
            'destinationTable': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.DESTINATION_TABLE,
            },
            'createDisposition': 'CREATE_NEVER',
            'writeDisposition': 'WRITE_TRUNCATE',
        }
        RESOURCE['configuration']['copy'] = COPY_CONFIGURATION
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        config = CopyJobConfig()
        config.create_disposition = 'CREATE_NEVER'
        config.write_disposition = 'WRITE_TRUNCATE'
        job = self._make_one(self.JOB_ID, [source], destination, client1,
                             config)
        job.begin(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'copy': COPY_CONFIGURATION,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn = _Connection()
        client = _make_client(project=self.PROJECT, connection=conn)

        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client)

        self.assertFalse(job.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client)

        job.reload()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestExtractJob(unittest.TestCase, _Base):
    JOB_TYPE = 'extract'
    SOURCE_TABLE = 'source_table'
    DESTINATION_URI = 'gs://bucket_name/object_name'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import ExtractJob

        return ExtractJob

    def _makeResource(self, started=False, ended=False):
        resource = super(TestExtractJob, self)._makeResource(
            started, ended)
        config = resource['configuration']['extract']
        config['sourceTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
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
        self.assertEqual(job.source.dataset_id, table_ref['datasetId'])
        self.assertEqual(job.source.table_id, table_ref['tableId'])

        if 'compression' in config:
            self.assertEqual(
                job.compression, config['compression'])
        else:
            self.assertIsNone(job.compression)

        if 'destinationFormat' in config:
            self.assertEqual(
                job.destination_format, config['destinationFormat'])
        else:
            self.assertIsNone(job.destination_format)

        if 'fieldDelimiter' in config:
            self.assertEqual(
                job.field_delimiter, config['fieldDelimiter'])
        else:
            self.assertIsNone(job.field_delimiter)

        if 'printHeader' in config:
            self.assertEqual(
                job.print_header, config['printHeader'])
        else:
            self.assertIsNone(job.print_header)

    def test_ctor(self):
        client = _make_client(project=self.PROJECT)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client)
        self.assertEqual(job.source, source)
        self.assertEqual(job.destination_uris, [self.DESTINATION_URI])
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['extract']
        self.assertIsNone(job.compression)
        self.assertIsNone(job.destination_format)
        self.assertIsNone(job.field_delimiter)
        self.assertIsNone(job.print_header)

    def test_destination_uri_file_counts(self):
        file_counts = 23
        client = _make_client(project=self.PROJECT)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client)
        self.assertIsNone(job.destination_uri_file_counts)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.destination_uri_file_counts)

        extract_stats = statistics['extract'] = {}
        self.assertIsNone(job.destination_uri_file_counts)

        extract_stats['destinationUriFileCounts'] = str(file_counts)
        self.assertEqual(job.destination_uri_file_counts, file_counts)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_ID),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
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
        client = _make_client(project=self.PROJECT)
        RESOURCE = self._makeResource()
        extract_config = RESOURCE['configuration']['extract']
        extract_config['compression'] = 'GZIP'
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_bound_client(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _Connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        source_dataset = DatasetReference(self.PROJECT, self.DS_ID)
        source = source_dataset.table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
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
                'datasetId': self.DS_ID,
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
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source_dataset = DatasetReference(self.PROJECT, self.DS_ID)
        source = source_dataset.table(self.SOURCE_TABLE)
        job_config = ExtractJobConfig()
        job_config.compression = 'GZIP'
        job_config.destination_format = 'NEWLINE_DELIMITED_JSON'
        job_config.field_delimiter = '|'
        job_config.print_header = False
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client1, job_config)

        job.begin(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'extract': EXTRACT_CONFIGURATION,
            },
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn = _Connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client)

        self.assertFalse(job.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source = _Table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        source_dataset = DatasetReference(self.PROJECT, self.DS_ID)
        source = source_dataset.table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client)

        job.reload()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source_dataset = DatasetReference(self.PROJECT, self.DS_ID)
        source = source_dataset.table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestQueryJobConfig(unittest.TestCase, _Base):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import QueryJobConfig

        return QueryJobConfig

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        config = self._make_one()
        self.assertEqual(config._properties, {})

    def test_from_api_repr_empty(self):
        klass = self._get_target_class()
        config = klass.from_api_repr({})
        self.assertIsNone(config.dry_run)
        self.assertIsNone(config.use_legacy_sql)
        self.assertIsNone(config.default_dataset)

    def test_from_api_repr_normal(self):
        resource = {
            'useLegacySql': True,
            'query': 'no property for me',
            'defaultDataset': {
                'projectId': 'someproject',
                'datasetId': 'somedataset',
            },
            'someNewProperty': 'I should be saved, too.',
        }
        klass = self._get_target_class()

        config = klass.from_api_repr(resource)

        self.assertTrue(config.use_legacy_sql)
        self.assertEqual(
            config.default_dataset,
            DatasetReference('someproject', 'somedataset'))
        # Make sure unknown properties propagate.
        self.assertEqual(config._properties['query'], 'no property for me')
        self.assertEqual(
            config._properties['someNewProperty'], 'I should be saved, too.')

    def test_to_api_repr_normal(self):
        config = self._make_one()
        config.use_legacy_sql = True
        config.default_dataset = DatasetReference(
            'someproject', 'somedataset')
        config._properties['someNewProperty'] = 'Woohoo, alpha stuff.'

        resource = config.to_api_repr()

        self.assertTrue(resource['useLegacySql'])
        self.assertEqual(
            resource['defaultDataset']['projectId'], 'someproject')
        self.assertEqual(
            resource['defaultDataset']['datasetId'], 'somedataset')
        # Make sure unknown properties propagate.
        self.assertEqual(
            config._properties['someNewProperty'], 'Woohoo, alpha stuff.')


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
            self.assertEqual(
                job.maximum_billing_tier, config['maximumBillingTier'])
        else:
            self.assertIsNone(job.maximum_billing_tier)
        if 'maximumBytesBilled' in config:
            self.assertEqual(
                str(job.maximum_bytes_billed), config['maximumBytesBilled'])
            self.assertIsInstance(job.maximum_bytes_billed, int)
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

    def _verify_table_definitions(self, job, config):
        table_defs = config.get('tableDefinitions')
        if job.table_definitions is None:
            self.assertIsNone(table_defs)
        else:
            self.assertEqual(len(job.table_definitions), len(table_defs))
            for found_key, found_ec in job.table_definitions.items():
                expected_ec = table_defs.get(found_key)
                self.assertIsNotNone(expected_ec)
                self.assertEqual(found_ec.to_api_repr(), expected_ec)

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
        self._verify_table_definitions(job, query_config)

        self.assertEqual(job.query, query_config['query'])
        if 'createDisposition' in query_config:
            self.assertEqual(job.create_disposition,
                             query_config['createDisposition'])
        else:
            self.assertIsNone(job.create_disposition)
        if 'defaultDataset' in query_config:
            ds_ref = job.default_dataset
            ds_ref = {
                'projectId': ds_ref.project,
                'datasetId': ds_ref.dataset_id,
            }
            self.assertEqual(ds_ref, query_config['defaultDataset'])
        else:
            self.assertIsNone(job.default_dataset)
        if 'destinationTable' in query_config:
            table = job.destination
            tb_ref = {
                'projectId': table.project,
                'datasetId': table.dataset_id,
                'tableId': table.table_id
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
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.query, self.QUERY)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID))

        self._verifyInitialReadonlyProperties(job)

        self.assertFalse(job.use_legacy_sql)

        # set/read from resource['configuration']['query']
        self.assertIsNone(job.allow_large_results)
        self.assertIsNone(job.create_disposition)
        self.assertIsNone(job.default_dataset)
        self.assertIsNone(job.destination)
        self.assertIsNone(job.flatten_results)
        self.assertIsNone(job.priority)
        self.assertIsNone(job.use_query_cache)
        self.assertIsNone(job.dry_run)
        self.assertIsNone(job.write_disposition)
        self.assertIsNone(job.maximum_billing_tier)
        self.assertIsNone(job.maximum_bytes_billed)
        self.assertIsNone(job.table_definitions)

    def test_ctor_w_udf_resources(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        client = _make_client(project=self.PROJECT)
        config = QueryJobConfig()
        config.udf_resources = udf_resources
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)
        self.assertEqual(job.udf_resources, udf_resources)

    def test_ctor_w_query_parameters(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", 'INT64', 123)]
        client = _make_client(project=self.PROJECT)
        config = QueryJobConfig()
        config.query_parameters = query_parameters
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)
        self.assertEqual(job.query_parameters, query_parameters)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_ID),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'query': {'query': self.QUERY},
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _make_client(project=self.PROJECT)
        RESOURCE = self._makeResource()
        query_config = RESOURCE['configuration']['query']
        query_config['createDisposition'] = 'CREATE_IF_NEEDED'
        query_config['writeDisposition'] = 'WRITE_TRUNCATE'
        query_config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
            'tableId': self.DESTINATION_TABLE,
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancelled(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        job._properties['status'] = {
            'state': 'DONE',
            'errorResult': {
                'reason': 'stopped'
            }
        }

        self.assertTrue(job.cancelled())

    def test_done(self):
        client = _make_client(project=self.PROJECT)
        resource = self._makeResource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)
        self.assertTrue(job.done())

    def test_query_plan(self):
        from google.cloud.bigquery.job import QueryPlanEntry
        from google.cloud.bigquery.job import QueryPlanEntryStep

        plan_entries = [{
            'name': 'NAME',
            'id': 1234,
            'waitRatioAvg': 2.71828,
            'waitRatioMax': 3.14159,
            'readRatioAvg': 1.41421,
            'readRatioMax': 1.73205,
            'computeRatioAvg': 0.69315,
            'computeRatioMax': 1.09861,
            'writeRatioAvg': 3.32193,
            'writeRatioMax': 2.30258,
            'recordsRead': '100',
            'recordsWritten': '1',
            'status': 'STATUS',
            'steps': [{
                'kind': 'KIND',
                'substeps': ['SUBSTEP1', 'SUBSTEP2'],
            }],
        }]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.query_plan, [])

        statistics = job._properties['statistics'] = {}
        self.assertEqual(job.query_plan, [])

        query_stats = statistics['query'] = {}
        self.assertEqual(job.query_plan, [])

        query_stats['queryPlan'] = plan_entries

        self.assertEqual(len(job.query_plan), len(plan_entries))
        for found, expected in zip(job.query_plan, plan_entries):
            self.assertIsInstance(found, QueryPlanEntry)
            self.assertEqual(found.name, expected['name'])
            self.assertEqual(found.entry_id, expected['id'])
            self.assertEqual(found.wait_ratio_avg, expected['waitRatioAvg'])
            self.assertEqual(found.wait_ratio_max, expected['waitRatioMax'])
            self.assertEqual(found.read_ratio_avg, expected['readRatioAvg'])
            self.assertEqual(found.read_ratio_max, expected['readRatioMax'])
            self.assertEqual(
                found.compute_ratio_avg, expected['computeRatioAvg'])
            self.assertEqual(
                found.compute_ratio_max, expected['computeRatioMax'])
            self.assertEqual(found.write_ratio_avg, expected['writeRatioAvg'])
            self.assertEqual(found.write_ratio_max, expected['writeRatioMax'])
            self.assertEqual(
                found.records_read, int(expected['recordsRead']))
            self.assertEqual(
                found.records_written, int(expected['recordsWritten']))
            self.assertEqual(found.status, expected['status'])

            self.assertEqual(len(found.steps), len(expected['steps']))
            for f_step, e_step in zip(found.steps, expected['steps']):
                self.assertIsInstance(f_step, QueryPlanEntryStep)
                self.assertEqual(f_step.kind, e_step['kind'])
                self.assertEqual(f_step.substeps, e_step['substeps'])

    def test_total_bytes_processed(self):
        total_bytes = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.total_bytes_processed)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.total_bytes_processed)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.total_bytes_processed)

        query_stats['totalBytesProcessed'] = str(total_bytes)
        self.assertEqual(job.total_bytes_processed, total_bytes)

    def test_total_bytes_billed(self):
        total_bytes = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.total_bytes_billed)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.total_bytes_billed)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.total_bytes_billed)

        query_stats['totalBytesBilled'] = str(total_bytes)
        self.assertEqual(job.total_bytes_billed, total_bytes)

    def test_billing_tier(self):
        billing_tier = 1
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.billing_tier)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.billing_tier)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.billing_tier)

        query_stats['billingTier'] = billing_tier
        self.assertEqual(job.billing_tier, billing_tier)

    def test_cache_hit(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.cache_hit)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.cache_hit)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.cache_hit)

        query_stats['cacheHit'] = True
        self.assertTrue(job.cache_hit)

    def test_num_dml_affected_rows(self):
        num_rows = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.num_dml_affected_rows)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.num_dml_affected_rows)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.num_dml_affected_rows)

        query_stats['numDmlAffectedRows'] = str(num_rows)
        self.assertEqual(job.num_dml_affected_rows, num_rows)

    def test_statement_type(self):
        statement_type = 'SELECT'
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.statement_type)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.statement_type)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.statement_type)

        query_stats['statementType'] = statement_type
        self.assertEqual(job.statement_type, statement_type)

    def test_referenced_tables(self):
        from google.cloud.bigquery.table import TableReference

        ref_tables_resource = [{
            'projectId': self.PROJECT,
            'datasetId': 'dataset',
            'tableId': 'local1',
        }, {

            'projectId': self.PROJECT,
            'datasetId': 'dataset',
            'tableId': 'local2',
        }, {

            'projectId': 'other-project-123',
            'datasetId': 'other-dataset',
            'tableId': 'other-table',
        }]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.referenced_tables, [])

        statistics = job._properties['statistics'] = {}
        self.assertEqual(job.referenced_tables, [])

        query_stats = statistics['query'] = {}
        self.assertEqual(job.referenced_tables, [])

        query_stats['referencedTables'] = ref_tables_resource

        local1, local2, remote = job.referenced_tables

        self.assertIsInstance(local1, TableReference)
        self.assertEqual(local1.table_id, 'local1')
        self.assertEqual(local1.dataset_id, 'dataset')
        self.assertEqual(local1.project, self.PROJECT)

        self.assertIsInstance(local2, TableReference)
        self.assertEqual(local2.table_id, 'local2')
        self.assertEqual(local2.dataset_id, 'dataset')
        self.assertEqual(local2.project, self.PROJECT)

        self.assertIsInstance(remote, TableReference)
        self.assertEqual(remote.table_id, 'other-table')
        self.assertEqual(remote.dataset_id, 'other-dataset')
        self.assertEqual(remote.project, 'other-project-123')

    def test_undeclared_query_paramters(self):
        from google.cloud.bigquery.query import ArrayQueryParameter
        from google.cloud.bigquery.query import ScalarQueryParameter
        from google.cloud.bigquery.query import StructQueryParameter

        undeclared = [{
            'name': 'my_scalar',
            'parameterType': {
                'type': 'STRING',
            },
            'parameterValue': {
                'value': 'value',
            },
        }, {
            'name': 'my_array',
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {
                    'type': 'INT64',
                },
            },
            'parameterValue': {
                'arrayValues': [
                    {'value': '1066'},
                    {'value': '1745'},
                ],
            },
        }, {
            'name': 'my_struct',
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [{
                    'name': 'count',
                    'type': {
                        'type': 'INT64',
                    }
                }],
            },
            'parameterValue': {
                'structValues': {
                    'count': {
                        'value': '123',
                    },
                }
            },
        }]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.undeclared_query_paramters, [])

        statistics = job._properties['statistics'] = {}
        self.assertEqual(job.undeclared_query_paramters, [])

        query_stats = statistics['query'] = {}
        self.assertEqual(job.undeclared_query_paramters, [])

        query_stats['undeclaredQueryParamters'] = undeclared

        scalar, array, struct = job.undeclared_query_paramters

        self.assertIsInstance(scalar, ScalarQueryParameter)
        self.assertEqual(scalar.name, 'my_scalar')
        self.assertEqual(scalar.type_, 'STRING')
        self.assertEqual(scalar.value, 'value')

        self.assertIsInstance(array, ArrayQueryParameter)
        self.assertEqual(array.name, 'my_array')
        self.assertEqual(array.array_type, 'INT64')
        self.assertEqual(array.values, [1066, 1745])

        self.assertIsInstance(struct, StructQueryParameter)
        self.assertEqual(struct.name, 'my_struct')
        self.assertEqual(struct.struct_types, {'count': 'INT64'})
        self.assertEqual(struct.struct_values, {'count': 123})

    def test_query_results(self):
        from google.cloud.bigquery.query import QueryResults

        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
        }
        connection = _Connection(query_resource)
        client = _make_client(self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        results = job.query_results()
        self.assertIsInstance(results, QueryResults)

    def test_query_results_w_cached_value(self):
        from google.cloud.bigquery.query import QueryResults

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        resource = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
        }
        query_results = QueryResults(resource)
        job._query_results = query_results

        results = job.query_results()

        self.assertIs(results, query_results)

    def test_result(self):
        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
        }
        connection = _Connection(query_resource, query_resource)
        client = _make_client(self.PROJECT, connection=connection)
        resource = self._makeResource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        result = job.result()

        self.assertEqual(list(result), [])

    def test_result_invokes_begins(self):
        begun_resource = self._makeResource()
        incomplete_resource = {
            'jobComplete': False,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
        }
        query_resource = copy.deepcopy(incomplete_resource)
        query_resource['jobComplete'] = True
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _Connection(
            begun_resource, incomplete_resource, query_resource, done_resource,
            query_resource)
        client = _make_client(project=self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        job.result()

        self.assertEqual(len(connection._requested), 4)
        begin_request, _, query_request, reload_request = connection._requested
        self.assertEqual(begin_request['method'], 'POST')
        self.assertEqual(query_request['method'], 'GET')
        self.assertEqual(reload_request['method'], 'GET')

    def test_result_w_timeout(self):
        begun_resource = self._makeResource()
        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
        }
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _Connection(
            begun_resource, query_resource, done_resource)
        client = _make_client(project=self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        job.result(timeout=1.0)

        self.assertEqual(len(connection._requested), 3)
        begin_request, query_request, reload_request = connection._requested
        self.assertEqual(begin_request['method'], 'POST')
        self.assertEqual(query_request['method'], 'GET')
        self.assertEqual(
            query_request['path'],
            '/projects/{}/queries/{}'.format(self.PROJECT, self.JOB_ID))
        self.assertEqual(query_request['query_params']['timeoutMs'], 900)
        self.assertEqual(reload_request['method'], 'GET')

    def test_result_error(self):
        from google.cloud import exceptions

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
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
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        DS_ID = 'DATASET'
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _Connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)

        config = QueryJobConfig()
        config.default_dataset = DatasetReference(self.PROJECT, DS_ID)
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)

        job.begin()

        self.assertIsNone(job.default_dataset)
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'useLegacySql': False,
                    'defaultDataset': {
                        'projectId': self.PROJECT,
                        'datasetId': DS_ID,
                    },
                },
            },
        }
        self._verifyResourceProperties(job, RESOURCE)
        self.assertEqual(req['data'], SENT)

    def test_begin_w_alternate_client(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        TABLE = 'TABLE'
        DS_ID = 'DATASET'
        RESOURCE = self._makeResource(ended=True)
        QUERY_CONFIGURATION = {
            'query': self.QUERY,
            'allowLargeResults': True,
            'createDisposition': 'CREATE_NEVER',
            'defaultDataset': {
                'projectId': self.PROJECT,
                'datasetId': DS_ID,
            },
            'destinationTable': {
                'projectId': self.PROJECT,
                'datasetId': DS_ID,
                'tableId': TABLE,
            },
            'flattenResults': True,
            'priority': 'INTERACTIVE',
            'useQueryCache': True,
            'useLegacySql': True,
            'writeDisposition': 'WRITE_TRUNCATE',
            'maximumBillingTier': 4,
            'maximumBytesBilled': '123456'
        }
        RESOURCE['configuration']['query'] = QUERY_CONFIGURATION
        RESOURCE['configuration']['dryRun'] = True
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        dataset_ref = DatasetReference(self.PROJECT, DS_ID)
        table_ref = dataset_ref.table(TABLE)

        config = QueryJobConfig()
        config.allow_large_results = True
        config.create_disposition = 'CREATE_NEVER'
        config.default_dataset = dataset_ref
        config.destination = table_ref
        config.dry_run = True
        config.flatten_results = True
        config.maximum_billing_tier = 4
        config.priority = 'INTERACTIVE'
        config.use_legacy_sql = True
        config.use_query_cache = True
        config.write_disposition = 'WRITE_TRUNCATE'
        config.maximum_bytes_billed = 123456
        job = self._make_one(
            self.JOB_ID, self.QUERY, client1, job_config=config)

        job.begin(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'dryRun': True,
                'query': QUERY_CONFIGURATION,
            },
        }
        self._verifyResourceProperties(job, RESOURCE)
        self.assertEqual(req['data'], SENT)

    def test_begin_w_udf(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import UDFResource

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
        client = _make_client(project=self.PROJECT, connection=conn)
        udf_resources = [
            UDFResource("resourceUri", RESOURCE_URI),
            UDFResource("inlineCode", INLINE_UDF_CODE),
        ]
        config = QueryJobConfig()
        config.udf_resources = udf_resources
        config.use_legacy_sql = True
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(job.udf_resources, udf_resources)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'useLegacySql': True,
                    'userDefinedFunctionResources': [
                        {'resourceUri': RESOURCE_URI},
                        {'inlineCode': INLINE_UDF_CODE},
                    ]
                },
            },
        }
        self._verifyResourceProperties(job, RESOURCE)
        self.assertEqual(req['data'], SENT)

    def test_begin_w_named_query_parameter(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

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
        client = _make_client(project=self.PROJECT, connection=conn)
        jconfig = QueryJobConfig()
        jconfig.query_parameters = query_parameters
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=jconfig)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(job.query_parameters, query_parameters)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'useLegacySql': False,
                    'parameterMode': 'NAMED',
                    'queryParameters': config['queryParameters'],
                },
            },
        }
        self._verifyResourceProperties(job, RESOURCE)
        self.assertEqual(req['data'], SENT)

    def test_begin_w_positional_query_parameter(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

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
        client = _make_client(project=self.PROJECT, connection=conn)
        jconfig = QueryJobConfig()
        jconfig.query_parameters = query_parameters
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=jconfig)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(job.query_parameters, query_parameters)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'useLegacySql': False,
                    'parameterMode': 'POSITIONAL',
                    'queryParameters': config['queryParameters'],
                },
            },
        }
        self._verifyResourceProperties(job, RESOURCE)
        self.assertEqual(req['data'], SENT)

    def test_begin_w_table_defs(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.external_config import ExternalConfig
        from google.cloud.bigquery.external_config import BigtableColumn
        from google.cloud.bigquery.external_config import BigtableColumnFamily

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']

        bt_config = ExternalConfig('BIGTABLE')
        bt_config.ignore_unknown_values = True
        bt_config.options.read_rowkey_as_string = True
        cf = BigtableColumnFamily()
        cf.family_id = 'cf'
        col = BigtableColumn()
        col.field_name = 'fn'
        cf.columns = [col]
        bt_config.options.column_families = [cf]
        BT_CONFIG_RESOURCE = {
            'sourceFormat': 'BIGTABLE',
            'ignoreUnknownValues': True,
            'bigtableOptions': {
                'readRowkeyAsString': True,
                'columnFamilies': [{
                    'familyId': 'cf',
                    'columns': [{'fieldName': 'fn'}],
                }],
            },
        }
        CSV_CONFIG_RESOURCE = {
            'sourceFormat': 'CSV',
            'maxBadRecords': 8,
            'csvOptions': {
                'allowJaggedRows': True,
            },
        }
        csv_config = ExternalConfig('CSV')
        csv_config.max_bad_records = 8
        csv_config.options.allow_jagged_rows = True
        bt_table = 'bigtable-table'
        csv_table = 'csv-table'
        RESOURCE['configuration']['query']['tableDefinitions'] = {
            bt_table: BT_CONFIG_RESOURCE,
            csv_table: CSV_CONFIG_RESOURCE,
        }
        want_resource = copy.deepcopy(RESOURCE)
        conn = _Connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        config = QueryJobConfig()
        config.table_definitions = {
            bt_table: bt_config,
            csv_table: csv_config,
        }
        config.use_legacy_sql = True
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)

        job.begin()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'useLegacySql': True,
                    'tableDefinitions': {
                        bt_table: BT_CONFIG_RESOURCE,
                        csv_table: CSV_CONFIG_RESOURCE,
                    },
                },
            },
        }
        self._verifyResourceProperties(job, want_resource)
        self.assertEqual(req['data'], SENT)

    def test_dry_run_query(self):
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        RESOURCE['configuration']['dryRun'] = True
        conn = _Connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        config = QueryJobConfig()
        config.dry_run = True
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)

        job.begin()
        self.assertEqual(job.udf_resources, [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'useLegacySql': False,
                },
                'dryRun': True,
            },
        }
        self._verifyResourceProperties(job, RESOURCE)
        self.assertEqual(req['data'], SENT)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn = _Connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        self.assertFalse(job.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(self.JOB_ID, self.QUERY, client1)

        self.assertTrue(job.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        DS_ID = 'DATASET'
        DEST_TABLE = 'dest_table'
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        dataset_ref = DatasetReference(self.PROJECT, DS_ID)
        table_ref = dataset_ref.table(DEST_TABLE)
        config = QueryJobConfig()
        config.destination = table_ref
        job = self._make_one(self.JOB_ID, None, client, job_config=config)

        job.reload()

        self.assertNotEqual(job.destination, table_ref)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        DS_ID = 'DATASET'
        DEST_TABLE = 'dest_table'
        RESOURCE = self._makeResource()
        q_config = RESOURCE['configuration']['query']
        q_config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': DS_ID,
            'tableId': DEST_TABLE,
        }
        conn1 = _Connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(self.JOB_ID, self.QUERY, client1)

        job.reload(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self._verifyResourceProperties(job, RESOURCE)


class TestQueryPlanEntryStep(unittest.TestCase, _Base):
    KIND = 'KIND'
    SUBSTEPS = ('SUB1', 'SUB2')

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import QueryPlanEntryStep

        return QueryPlanEntryStep

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        self.assertEqual(step.kind, self.KIND)
        self.assertEqual(step.substeps, list(self.SUBSTEPS))

    def test_from_api_repr_empty(self):
        klass = self._get_target_class()
        step = klass.from_api_repr({})
        self.assertIsNone(step.kind)
        self.assertEqual(step.substeps, [])

    def test_from_api_repr_normal(self):
        resource = {
            'kind': self.KIND,
            'substeps': self.SUBSTEPS,
        }
        klass = self._get_target_class()
        step = klass.from_api_repr(resource)
        self.assertEqual(step.kind, self.KIND)
        self.assertEqual(step.substeps, list(self.SUBSTEPS))

    def test___eq___mismatched_type(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        self.assertNotEqual(step, object())

    def test___eq___mismatch_kind(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        other = self._make_one('OTHER', self.SUBSTEPS)
        self.assertNotEqual(step, other)

    def test___eq___mismatch_substeps(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        other = self._make_one(self.KIND, ())
        self.assertNotEqual(step, other)

    def test___eq___hit(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        other = self._make_one(self.KIND, self.SUBSTEPS)
        self.assertEqual(step, other)


class TestQueryPlanEntry(unittest.TestCase, _Base):
    NAME = 'NAME'
    ENTRY_ID = 1234
    WAIT_RATIO_AVG = 2.71828
    WAIT_RATIO_MAX = 3.14159
    READ_RATIO_AVG = 1.41421
    READ_RATIO_MAX = 1.73205
    COMPUTE_RATIO_AVG = 0.69315
    COMPUTE_RATIO_MAX = 1.09861
    WRITE_RATIO_AVG = 3.32193
    WRITE_RATIO_MAX = 2.30258
    RECORDS_READ = 100
    RECORDS_WRITTEN = 1
    STATUS = 'STATUS'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import QueryPlanEntry

        return QueryPlanEntry

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        from google.cloud.bigquery.job import QueryPlanEntryStep

        steps = [QueryPlanEntryStep(
            kind=TestQueryPlanEntryStep.KIND,
            substeps=TestQueryPlanEntryStep.SUBSTEPS)]
        entry = self._make_one(
            name=self.NAME,
            entry_id=self.ENTRY_ID,
            wait_ratio_avg=self.WAIT_RATIO_AVG,
            wait_ratio_max=self.WAIT_RATIO_MAX,
            read_ratio_avg=self.READ_RATIO_AVG,
            read_ratio_max=self.READ_RATIO_MAX,
            compute_ratio_avg=self.COMPUTE_RATIO_AVG,
            compute_ratio_max=self.COMPUTE_RATIO_MAX,
            write_ratio_avg=self.WRITE_RATIO_AVG,
            write_ratio_max=self.WRITE_RATIO_MAX,
            records_read=self.RECORDS_READ,
            records_written=self.RECORDS_WRITTEN,
            status=self.STATUS,
            steps=steps,
        )
        self.assertEqual(entry.name, self.NAME)
        self.assertEqual(entry.entry_id, self.ENTRY_ID)
        self.assertEqual(entry.wait_ratio_avg, self.WAIT_RATIO_AVG)
        self.assertEqual(entry.wait_ratio_max, self.WAIT_RATIO_MAX)
        self.assertEqual(entry.read_ratio_avg, self.READ_RATIO_AVG)
        self.assertEqual(entry.read_ratio_max, self.READ_RATIO_MAX)
        self.assertEqual(entry.compute_ratio_avg, self.COMPUTE_RATIO_AVG)
        self.assertEqual(entry.compute_ratio_max, self.COMPUTE_RATIO_MAX)
        self.assertEqual(entry.write_ratio_avg, self.WRITE_RATIO_AVG)
        self.assertEqual(entry.write_ratio_max, self.WRITE_RATIO_MAX)
        self.assertEqual(entry.records_read, self.RECORDS_READ)
        self.assertEqual(entry.records_written, self.RECORDS_WRITTEN)
        self.assertEqual(entry.status, self.STATUS)
        self.assertEqual(entry.steps, steps)

    def test_from_api_repr_empty(self):
        klass = self._get_target_class()

        entry = klass.from_api_repr({})

        self.assertIsNone(entry.name)
        self.assertIsNone(entry.entry_id)
        self.assertIsNone(entry.wait_ratio_avg)
        self.assertIsNone(entry.wait_ratio_max)
        self.assertIsNone(entry.read_ratio_avg)
        self.assertIsNone(entry.read_ratio_max)
        self.assertIsNone(entry.compute_ratio_avg)
        self.assertIsNone(entry.compute_ratio_max)
        self.assertIsNone(entry.write_ratio_avg)
        self.assertIsNone(entry.write_ratio_max)
        self.assertIsNone(entry.records_read)
        self.assertIsNone(entry.records_written)
        self.assertIsNone(entry.status)
        self.assertEqual(entry.steps, [])

    def test_from_api_repr_normal(self):
        from google.cloud.bigquery.job import QueryPlanEntryStep

        steps = [QueryPlanEntryStep(
            kind=TestQueryPlanEntryStep.KIND,
            substeps=TestQueryPlanEntryStep.SUBSTEPS)]
        resource = {
            'name': self.NAME,
            'id': self.ENTRY_ID,
            'waitRatioAvg': self.WAIT_RATIO_AVG,
            'waitRatioMax': self.WAIT_RATIO_MAX,
            'readRatioAvg': self.READ_RATIO_AVG,
            'readRatioMax': self.READ_RATIO_MAX,
            'computeRatioAvg': self.COMPUTE_RATIO_AVG,
            'computeRatioMax': self.COMPUTE_RATIO_MAX,
            'writeRatioAvg': self.WRITE_RATIO_AVG,
            'writeRatioMax': self.WRITE_RATIO_MAX,
            'recordsRead': str(self.RECORDS_READ),
            'recordsWritten': str(self.RECORDS_WRITTEN),
            'status': self.STATUS,
            'steps': [{
                'kind': TestQueryPlanEntryStep.KIND,
                'substeps': TestQueryPlanEntryStep.SUBSTEPS,
            }]
        }
        klass = self._get_target_class()

        entry = klass.from_api_repr(resource)
        self.assertEqual(entry.name, self.NAME)
        self.assertEqual(entry.entry_id, self.ENTRY_ID)
        self.assertEqual(entry.wait_ratio_avg, self.WAIT_RATIO_AVG)
        self.assertEqual(entry.wait_ratio_max, self.WAIT_RATIO_MAX)
        self.assertEqual(entry.read_ratio_avg, self.READ_RATIO_AVG)
        self.assertEqual(entry.read_ratio_max, self.READ_RATIO_MAX)
        self.assertEqual(entry.compute_ratio_avg, self.COMPUTE_RATIO_AVG)
        self.assertEqual(entry.compute_ratio_max, self.COMPUTE_RATIO_MAX)
        self.assertEqual(entry.write_ratio_avg, self.WRITE_RATIO_AVG)
        self.assertEqual(entry.write_ratio_max, self.WRITE_RATIO_MAX)
        self.assertEqual(entry.records_read, self.RECORDS_READ)
        self.assertEqual(entry.records_written, self.RECORDS_WRITTEN)
        self.assertEqual(entry.status, self.STATUS)
        self.assertEqual(entry.steps, steps)


class _Table(object):

    def __init__(self, table_id=None):
        self._table_id = table_id

    @property
    def table_id(self):
        return TestLoadJob.TABLE_ID

    @property
    def project(self):
        return TestLoadJob.PROJECT

    @property
    def dataset_id(self):
        return TestLoadJob.DS_ID


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
