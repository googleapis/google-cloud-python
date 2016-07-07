# Copyright 2016 Google Inc. All rights reserved.
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


class TestLogger(unittest2.TestCase):

    PROJECT = 'test-project'
    LOGGER_NAME = 'logger-name'

    def _getTargetClass(self):
        from gcloud.logging.logger import Logger
        return Logger

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        conn = object()
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)
        self.assertEqual(logger.full_name, 'projects/%s/logs/%s'
                         % (self.PROJECT, self.LOGGER_NAME))
        self.assertEqual(logger.path, '/projects/%s/logs/%s'
                         % (self.PROJECT, self.LOGGER_NAME))
        self.assertEqual(logger.labels, None)

    def test_ctor_explicit(self):
        LABELS = {'foo': 'bar', 'baz': 'qux'}
        conn = object()
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client, labels=LABELS)
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)
        self.assertEqual(logger.full_name, 'projects/%s/logs/%s'
                         % (self.PROJECT, self.LOGGER_NAME))
        self.assertEqual(logger.path, '/projects/%s/logs/%s'
                         % (self.PROJECT, self.LOGGER_NAME))
        self.assertEqual(logger.labels, LABELS)

    def test_batch_w_bound_client(self):
        from gcloud.logging.logger import Batch
        conn = object()
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        batch = logger.batch()
        self.assertTrue(isinstance(batch, Batch))
        self.assertTrue(batch.logger is logger)
        self.assertTrue(batch.client is client)

    def test_batch_w_alternate_client(self):
        from gcloud.logging.logger import Batch
        conn1 = object()
        conn2 = object()
        client1 = _Client(self.PROJECT, conn1)
        client2 = _Client(self.PROJECT, conn2)
        logger = self._makeOne(self.LOGGER_NAME, client=client1)
        batch = logger.batch(client2)
        self.assertTrue(isinstance(batch, Batch))
        self.assertTrue(batch.logger is logger)
        self.assertTrue(batch.client is client2)

    def test_log_text_w_str_implicit_client(self):
        TEXT = 'TEXT'
        ENTRIES = [{
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
            'textPayload': TEXT,
            'resource': {
                'type': 'global',
            },
        }]
        client = _Client(self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client)

        logger.log_text(TEXT)

        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, None, None, None))

    def test_log_text_w_default_labels(self):
        TEXT = 'TEXT'
        DEFAULT_LABELS = {'foo': 'spam'}
        ENTRIES = [{
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
            'textPayload': TEXT,
            'resource': {
                'type': 'global',
            },
            'labels': DEFAULT_LABELS,
        }]
        client = _Client(self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client,
                               labels=DEFAULT_LABELS)

        logger.log_text(TEXT)

        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, None, None, None))

    def test_log_text_w_unicode_explicit_client_labels_severity_httpreq(self):
        TEXT = u'TEXT'
        DEFAULT_LABELS = {'foo': 'spam'}
        LABELS = {'foo': 'bar', 'baz': 'qux'}
        IID = 'IID'
        SEVERITY = 'CRITICAL'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = '500'
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        ENTRIES = [{
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
            'textPayload': TEXT,
            'resource': {
                'type': 'global',
            },
            'labels': LABELS,
            'insertId': IID,
            'severity': SEVERITY,
            'httpRequest': REQUEST,
        }]
        client1 = _Client(self.PROJECT)
        client2 = _Client(self.PROJECT)
        api = client2.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client1,
                               labels=DEFAULT_LABELS)

        logger.log_text(TEXT, client=client2, labels=LABELS,
                        insert_id=IID, severity=SEVERITY, http_request=REQUEST)

        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, None, None, None))

    def test_log_struct_w_implicit_client(self):
        STRUCT = {'message': 'MESSAGE', 'weather': 'cloudy'}
        ENTRIES = [{
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
            'jsonPayload': STRUCT,
            'resource': {
                'type': 'global',
            },
        }]
        client = _Client(self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client)

        logger.log_struct(STRUCT)

        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, None, None, None))

    def test_log_struct_w_default_labels(self):
        STRUCT = {'message': 'MESSAGE', 'weather': 'cloudy'}
        DEFAULT_LABELS = {'foo': 'spam'}
        ENTRIES = [{
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
            'jsonPayload': STRUCT,
            'resource': {
                'type': 'global',
            },
            'labels': DEFAULT_LABELS,
        }]
        client = _Client(self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client,
                               labels=DEFAULT_LABELS)

        logger.log_struct(STRUCT)

        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, None, None, None))

    def test_log_struct_w_explicit_client_labels_severity_httpreq(self):
        STRUCT = {'message': 'MESSAGE', 'weather': 'cloudy'}
        DEFAULT_LABELS = {'foo': 'spam'}
        LABELS = {'foo': 'bar', 'baz': 'qux'}
        IID = 'IID'
        SEVERITY = 'CRITICAL'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = '500'
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        ENTRIES = [{
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
            'jsonPayload': STRUCT,
            'resource': {
                'type': 'global',
            },
            'labels': LABELS,
            'insertId': IID,
            'severity': SEVERITY,
            'httpRequest': REQUEST,
        }]
        client1 = _Client(self.PROJECT)
        client2 = _Client(self.PROJECT)
        api = client2.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client1,
                               labels=DEFAULT_LABELS)

        logger.log_struct(STRUCT, client=client2, labels=LABELS,
                          insert_id=IID, severity=SEVERITY,
                          http_request=REQUEST)

        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, None, None, None))

    def test_log_proto_w_implicit_client(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        ENTRIES = [{
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
            'protoPayload': json.loads(MessageToJson(message)),
            'resource': {
                'type': 'global',
            },
        }]
        client = _Client(self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client)

        logger.log_proto(message)

        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, None, None, None))

    def test_log_proto_w_default_labels(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        DEFAULT_LABELS = {'foo': 'spam'}
        ENTRIES = [{
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
            'protoPayload': json.loads(MessageToJson(message)),
            'resource': {
                'type': 'global',
            },
            'labels': DEFAULT_LABELS,
        }]
        client = _Client(self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client,
                               labels=DEFAULT_LABELS)

        logger.log_proto(message)

        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, None, None, None))

    def test_log_proto_w_explicit_client_labels_severity_httpreq(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        DEFAULT_LABELS = {'foo': 'spam'}
        LABELS = {'foo': 'bar', 'baz': 'qux'}
        IID = 'IID'
        SEVERITY = 'CRITICAL'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = '500'
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        ENTRIES = [{
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
            'protoPayload': json.loads(MessageToJson(message)),
            'resource': {
                'type': 'global',
            },
            'labels': LABELS,
            'insertId': IID,
            'severity': SEVERITY,
            'httpRequest': REQUEST,
        }]
        client1 = _Client(self.PROJECT)
        client2 = _Client(self.PROJECT)
        api = client2.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client1,
                               labels=DEFAULT_LABELS)

        logger.log_proto(message, client=client2, labels=LABELS,
                         insert_id=IID, severity=SEVERITY,
                         http_request=REQUEST)

        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, None, None, None))

    def test_delete_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client)

        logger.delete()

        self.assertEqual(api._logger_delete_called_with,
                         (self.PROJECT, self.LOGGER_NAME))

    def test_delete_w_alternate_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.logging_api = _DummyLoggingAPI()
        logger = self._makeOne(self.LOGGER_NAME, client=client1)

        logger.delete(client=client2)

        self.assertEqual(api._logger_delete_called_with,
                         (self.PROJECT, self.LOGGER_NAME))

    def test_list_entries_defaults(self):
        LISTED = {
            'projects': None,
            'filter_': 'logName=projects/%s/logs/%s' %
                       (self.PROJECT, self.LOGGER_NAME),
            'order_by': None,
            'page_size': None,
            'page_token': None,
        }
        TOKEN = 'TOKEN'
        client = _Client(self.PROJECT)
        client._token = TOKEN
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        entries, token = logger.list_entries()
        self.assertEqual(len(entries), 0)
        self.assertEqual(token, TOKEN)
        self.assertEqual(client._listed, LISTED)

    def test_list_entries_explicit(self):
        from gcloud.logging import DESCENDING
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        FILTER = 'resource.type:global'
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        LISTED = {
            'projects': ['PROJECT1', 'PROJECT2'],
            'filter_': '%s AND logName=projects/%s/logs/%s' %
                       (FILTER, self.PROJECT, self.LOGGER_NAME),
            'order_by': DESCENDING,
            'page_size': PAGE_SIZE,
            'page_token': TOKEN,
        }
        client = _Client(self.PROJECT)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        entries, token = logger.list_entries(
            projects=[PROJECT1, PROJECT2], filter_=FILTER, order_by=DESCENDING,
            page_size=PAGE_SIZE, page_token=TOKEN)
        self.assertEqual(len(entries), 0)
        self.assertEqual(token, None)
        self.assertEqual(client._listed, LISTED)


class TestBatch(unittest2.TestCase):

    PROJECT = 'test-project'

    def _getTargetClass(self):
        from gcloud.logging.logger import Batch
        return Batch

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        logger = _Logger()
        client = _Client(project=self.PROJECT)
        batch = self._makeOne(logger, client)
        self.assertTrue(batch.logger is logger)
        self.assertTrue(batch.client is client)
        self.assertEqual(len(batch.entries), 0)

    def test_log_text_defaults(self):
        TEXT = 'This is the entry text'
        client = _Client(project=self.PROJECT, connection=object())
        logger = _Logger()
        batch = self._makeOne(logger, client=client)
        batch.log_text(TEXT)
        self.assertEqual(batch.entries,
                         [('text', TEXT, None, None, None, None)])

    def test_log_text_explicit(self):
        TEXT = 'This is the entry text'
        LABELS = {'foo': 'bar', 'baz': 'qux'}
        IID = 'IID'
        SEVERITY = 'CRITICAL'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = '500'
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        client = _Client(project=self.PROJECT, connection=object())
        logger = _Logger()
        batch = self._makeOne(logger, client=client)
        batch.log_text(TEXT, labels=LABELS, insert_id=IID, severity=SEVERITY,
                       http_request=REQUEST)
        self.assertEqual(batch.entries,
                         [('text', TEXT, LABELS, IID, SEVERITY, REQUEST)])

    def test_log_struct_defaults(self):
        STRUCT = {'message': 'Message text', 'weather': 'partly cloudy'}
        client = _Client(project=self.PROJECT, connection=object())
        logger = _Logger()
        batch = self._makeOne(logger, client=client)
        batch.log_struct(STRUCT)
        self.assertEqual(batch.entries,
                         [('struct', STRUCT, None, None, None, None)])

    def test_log_struct_explicit(self):
        STRUCT = {'message': 'Message text', 'weather': 'partly cloudy'}
        LABELS = {'foo': 'bar', 'baz': 'qux'}
        IID = 'IID'
        SEVERITY = 'CRITICAL'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = '500'
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        client = _Client(project=self.PROJECT, connection=object())
        logger = _Logger()
        batch = self._makeOne(logger, client=client)
        batch.log_struct(STRUCT, labels=LABELS, insert_id=IID,
                         severity=SEVERITY, http_request=REQUEST)
        self.assertEqual(batch.entries,
                         [('struct', STRUCT, LABELS, IID, SEVERITY, REQUEST)])

    def test_log_proto_defaults(self):
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        client = _Client(project=self.PROJECT, connection=object())
        logger = _Logger()
        batch = self._makeOne(logger, client=client)
        batch.log_proto(message)
        self.assertEqual(batch.entries,
                         [('proto', message, None, None, None, None)])

    def test_log_proto_explicit(self):
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        LABELS = {'foo': 'bar', 'baz': 'qux'}
        IID = 'IID'
        SEVERITY = 'CRITICAL'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = '500'
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        client = _Client(project=self.PROJECT, connection=object())
        logger = _Logger()
        batch = self._makeOne(logger, client=client)
        batch.log_proto(message, labels=LABELS, insert_id=IID,
                        severity=SEVERITY, http_request=REQUEST)
        self.assertEqual(batch.entries,
                         [('proto', message, LABELS, IID, SEVERITY, REQUEST)])

    def test_commit_w_invalid_entry_type(self):
        logger = _Logger()
        client = _Client(project=self.PROJECT, connection=object())
        batch = self._makeOne(logger, client)
        batch.entries.append(('bogus', 'BOGUS', None, None, None, None))
        with self.assertRaises(ValueError):
            batch.commit()

    def test_commit_w_bound_client(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        TEXT = 'This is the entry text'
        STRUCT = {'message': TEXT, 'weather': 'partly cloudy'}
        message = Struct(fields={'foo': Value(bool_value=True)})
        IID1 = 'IID1'
        IID2 = 'IID2'
        IID3 = 'IID3'
        RESOURCE = {
            'type': 'global',
        }
        ENTRIES = [
            {'textPayload': TEXT, 'insertId': IID1},
            {'jsonPayload': STRUCT, 'insertId': IID2},
            {'protoPayload': json.loads(MessageToJson(message)),
             'insertId': IID3},
        ]
        client = _Client(project=self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = _Logger()
        batch = self._makeOne(logger, client=client)

        batch.log_text(TEXT, insert_id=IID1)
        batch.log_struct(STRUCT, insert_id=IID2)
        batch.log_proto(message, insert_id=IID3)
        batch.commit()

        self.assertEqual(list(batch.entries), [])
        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, logger.path, RESOURCE, None))

    def test_commit_w_alternate_client(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        from gcloud.logging.logger import Logger
        TEXT = 'This is the entry text'
        STRUCT = {'message': TEXT, 'weather': 'partly cloudy'}
        message = Struct(fields={'foo': Value(bool_value=True)})
        DEFAULT_LABELS = {'foo': 'spam'}
        LABELS = {
            'foo': 'bar',
            'baz': 'qux',
        }
        SEVERITY = 'CRITICAL'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = '500'
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.logging_api = _DummyLoggingAPI()
        logger = Logger('logger_name', client1, labels=DEFAULT_LABELS)
        RESOURCE = {'type': 'global'}
        ENTRIES = [
            {'textPayload': TEXT, 'labels': LABELS},
            {'jsonPayload': STRUCT, 'severity': SEVERITY},
            {'protoPayload': json.loads(MessageToJson(message)),
             'httpRequest': REQUEST},
        ]
        batch = self._makeOne(logger, client=client1)

        batch.log_text(TEXT, labels=LABELS)
        batch.log_struct(STRUCT, severity=SEVERITY)
        batch.log_proto(message, http_request=REQUEST)
        batch.commit(client=client2)

        self.assertEqual(list(batch.entries), [])
        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, logger.path, RESOURCE, DEFAULT_LABELS))

    def test_context_mgr_success(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        from gcloud.logging.logger import Logger
        TEXT = 'This is the entry text'
        STRUCT = {'message': TEXT, 'weather': 'partly cloudy'}
        message = Struct(fields={'foo': Value(bool_value=True)})
        DEFAULT_LABELS = {'foo': 'spam'}
        LABELS = {'foo': 'bar', 'baz': 'qux'}
        SEVERITY = 'CRITICAL'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = '500'
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        client = _Client(project=self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = Logger('logger_name', client, labels=DEFAULT_LABELS)
        RESOURCE = {
            'type': 'global',
        }
        ENTRIES = [
            {'textPayload': TEXT, 'httpRequest': REQUEST},
            {'jsonPayload': STRUCT, 'labels': LABELS},
            {'protoPayload': json.loads(MessageToJson(message)),
             'severity': SEVERITY},
        ]
        batch = self._makeOne(logger, client=client)

        with batch as other:
            other.log_text(TEXT, http_request=REQUEST)
            other.log_struct(STRUCT, labels=LABELS)
            other.log_proto(message, severity=SEVERITY)

        self.assertEqual(list(batch.entries), [])
        self.assertEqual(api._write_entries_called_with,
                         (ENTRIES, logger.path, RESOURCE, DEFAULT_LABELS))

    def test_context_mgr_failure(self):
        from google.protobuf.struct_pb2 import Struct, Value
        TEXT = 'This is the entry text'
        STRUCT = {'message': TEXT, 'weather': 'partly cloudy'}
        LABELS = {'foo': 'bar', 'baz': 'qux'}
        IID = 'IID'
        SEVERITY = 'CRITICAL'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = '500'
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        message = Struct(fields={'foo': Value(bool_value=True)})
        client = _Client(project=self.PROJECT)
        api = client.logging_api = _DummyLoggingAPI()
        logger = _Logger()
        UNSENT = [
            ('text', TEXT, None, IID, None, None),
            ('struct', STRUCT, None, None, SEVERITY, None),
            ('proto', message, LABELS, None, None, REQUEST),
        ]
        batch = self._makeOne(logger, client=client)

        try:
            with batch as other:
                other.log_text(TEXT, insert_id=IID)
                other.log_struct(STRUCT, severity=SEVERITY)
                other.log_proto(message, labels=LABELS, http_request=REQUEST)
                raise _Bugout()
        except _Bugout:
            pass

        self.assertEqual(list(batch.entries), UNSENT)
        self.assertEqual(api._write_entries_called_with, None)


class _Logger(object):

    labels = None

    def __init__(self, name="NAME", project="PROJECT"):
        self.path = '/projects/%s/logs/%s' % (project, name)


class _DummyLoggingAPI(object):

    _write_entries_called_with = None

    def write_entries(self, entries, logger_name=None, resource=None,
                      labels=None):
        self._write_entries_called_with = (
            entries, logger_name, resource, labels)

    def logger_delete(self, project, logger_name):
        self._logger_delete_called_with = (project, logger_name)


class _Client(object):

    _listed = _token = None
    _entries = ()

    def __init__(self, project, connection=None):
        self.project = project
        self.connection = connection

    def list_entries(self, **kw):
        self._listed = kw
        return self._entries, self._token


class _Bugout(Exception):
    pass
