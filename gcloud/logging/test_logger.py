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
        conn = _Connection()
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
        conn = _Connection()
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
        conn = _Connection()
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        batch = logger.batch()
        self.assertTrue(isinstance(batch, Batch))
        self.assertTrue(batch.logger is logger)
        self.assertTrue(batch.client is client)

    def test_batch_w_alternate_client(self):
        from gcloud.logging.logger import Batch
        conn1 = _Connection()
        conn2 = _Connection()
        client1 = _Client(self.PROJECT, conn1)
        client2 = _Client(self.PROJECT, conn2)
        logger = self._makeOne(self.LOGGER_NAME, client=client1)
        batch = logger.batch(client2)
        self.assertTrue(isinstance(batch, Batch))
        self.assertTrue(batch.logger is logger)
        self.assertTrue(batch.client is client2)

    def test_log_text_w_str_implicit_client(self):
        TEXT = 'TEXT'
        conn = _Connection({})
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        logger.log_text(TEXT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'textPayload': TEXT,
                'resource': {
                    'type': 'global',
                },
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_log_text_w_default_labels(self):
        TEXT = 'TEXT'
        DEFAULT_LABELS = {'foo': 'spam'}
        conn = _Connection({})
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client,
                               labels=DEFAULT_LABELS)
        logger.log_text(TEXT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'textPayload': TEXT,
                'resource': {
                    'type': 'global',
                },
                'labels': DEFAULT_LABELS,
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

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
        conn = _Connection({})
        client1 = _Client(self.PROJECT, object())
        client2 = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client1,
                               labels=DEFAULT_LABELS)
        logger.log_text(TEXT, client=client2, labels=LABELS,
                        insert_id=IID, severity=SEVERITY, http_request=REQUEST)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
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
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_log_struct_w_implicit_client(self):
        STRUCT = {'message': 'MESSAGE', 'weather': 'cloudy'}
        conn = _Connection({})
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        logger.log_struct(STRUCT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'jsonPayload': STRUCT,
                'resource': {
                    'type': 'global',
                },
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_log_struct_w_default_labels(self):
        STRUCT = {'message': 'MESSAGE', 'weather': 'cloudy'}
        DEFAULT_LABELS = {'foo': 'spam'}
        conn = _Connection({})
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client,
                               labels=DEFAULT_LABELS)
        logger.log_struct(STRUCT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'jsonPayload': STRUCT,
                'resource': {
                    'type': 'global',
                },
                'labels': DEFAULT_LABELS,
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

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
        conn = _Connection({})
        client1 = _Client(self.PROJECT, object())
        client2 = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client1,
                               labels=DEFAULT_LABELS)
        logger.log_struct(STRUCT, client=client2, labels=LABELS,
                          insert_id=IID, severity=SEVERITY,
                          http_request=REQUEST)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
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
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_log_proto_w_implicit_client(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        conn = _Connection({})
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        logger.log_proto(message)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'protoPayload': json.loads(MessageToJson(message)),
                'resource': {
                    'type': 'global',
                },
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_log_proto_w_default_labels(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        DEFAULT_LABELS = {'foo': 'spam'}
        conn = _Connection({})
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client,
                               labels=DEFAULT_LABELS)
        logger.log_proto(message)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'protoPayload': json.loads(MessageToJson(message)),
                'resource': {
                    'type': 'global',
                },
                'labels': DEFAULT_LABELS,
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

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
        conn = _Connection({})
        client1 = _Client(self.PROJECT, object())
        client2 = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client1,
                               labels=DEFAULT_LABELS)
        logger.log_proto(message, client=client2, labels=LABELS,
                         insert_id=IID, severity=SEVERITY,
                         http_request=REQUEST)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
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
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_delete_w_bound_client(self):
        PATH = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        logger = self._makeOne(self.LOGGER_NAME, client=CLIENT)
        logger.delete()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_delete_w_alternate_client(self):
        PATH = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        conn1 = _Connection({})
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        logger = self._makeOne(self.LOGGER_NAME, client=CLIENT1)
        logger.delete(client=CLIENT2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_entries_defaults(self):
        LISTED = {
            'projects': None,
            'filter_': 'logName:%s' % (self.LOGGER_NAME),
            'order_by': None,
            'page_size': None,
            'page_token': None,
        }
        TOKEN = 'TOKEN'
        conn = _Connection()
        client = _Client(self.PROJECT, conn)
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
            'filter_': '%s AND logName:%s' % (FILTER, self.LOGGER_NAME),
            'order_by': DESCENDING,
            'page_size': PAGE_SIZE,
            'page_token': TOKEN,
        }
        conn = _Connection()
        client = _Client(self.PROJECT, conn)
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
        CLIENT = _Client(project=self.PROJECT)
        batch = self._makeOne(logger, CLIENT)
        self.assertTrue(batch.logger is logger)
        self.assertTrue(batch.client is CLIENT)
        self.assertEqual(len(batch.entries), 0)

    def test_log_text_defaults(self):
        TEXT = 'This is the entry text'
        connection = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=connection)
        logger = _Logger()
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_text(TEXT)
        self.assertEqual(len(connection._requested), 0)
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
        connection = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=connection)
        logger = _Logger()
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_text(TEXT, labels=LABELS, insert_id=IID, severity=SEVERITY,
                       http_request=REQUEST)
        self.assertEqual(len(connection._requested), 0)
        self.assertEqual(batch.entries,
                         [('text', TEXT, LABELS, IID, SEVERITY, REQUEST)])

    def test_log_struct_defaults(self):
        STRUCT = {'message': 'Message text', 'weather': 'partly cloudy'}
        connection = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=connection)
        logger = _Logger()
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_struct(STRUCT)
        self.assertEqual(len(connection._requested), 0)
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
        connection = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=connection)
        logger = _Logger()
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_struct(STRUCT, labels=LABELS, insert_id=IID,
                         severity=SEVERITY, http_request=REQUEST)
        self.assertEqual(len(connection._requested), 0)
        self.assertEqual(batch.entries,
                         [('struct', STRUCT, LABELS, IID, SEVERITY, REQUEST)])

    def test_log_proto_defaults(self):
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        connection = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=connection)
        logger = _Logger()
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_proto(message)
        self.assertEqual(len(connection._requested), 0)
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
        connection = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=connection)
        logger = _Logger()
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_proto(message, labels=LABELS, insert_id=IID,
                        severity=SEVERITY, http_request=REQUEST)
        self.assertEqual(len(connection._requested), 0)
        self.assertEqual(batch.entries,
                         [('proto', message, LABELS, IID, SEVERITY, REQUEST)])

    def test_commit_w_invalid_entry_type(self):
        logger = _Logger()
        conn = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        batch = self._makeOne(logger, CLIENT)
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
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        logger = _Logger()
        SENT = {
            'logName': logger.path,
            'resource': {
                'type': 'global',
            },
            'entries': [
                {'textPayload': TEXT, 'insertId': IID1},
                {'jsonPayload': STRUCT, 'insertId': IID2},
                {'protoPayload': json.loads(MessageToJson(message)),
                 'insertId': IID3},
            ],
        }
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_text(TEXT, insert_id=IID1)
        batch.log_struct(STRUCT, insert_id=IID2)
        batch.log_proto(message, insert_id=IID3)
        batch.commit()
        self.assertEqual(list(batch.entries), [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_commit_w_alternate_client(self):
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
        conn1 = _Connection()
        conn2 = _Connection({})
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        logger = Logger('logger_name', CLIENT1, labels=DEFAULT_LABELS)
        SENT = {
            'logName': logger.path,
            'resource': {'type': 'global'},
            'labels': DEFAULT_LABELS,
            'entries': [
                {'textPayload': TEXT, 'labels': LABELS},
                {'jsonPayload': STRUCT, 'severity': SEVERITY},
                {'protoPayload': json.loads(MessageToJson(message)),
                 'httpRequest': REQUEST},
            ],
        }
        batch = self._makeOne(logger, client=CLIENT1)
        batch.log_text(TEXT, labels=LABELS)
        batch.log_struct(STRUCT, severity=SEVERITY)
        batch.log_proto(message, http_request=REQUEST)
        batch.commit(client=CLIENT2)
        self.assertEqual(list(batch.entries), [])
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

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
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        logger = Logger('logger_name', CLIENT, labels=DEFAULT_LABELS)
        SENT = {
            'logName': logger.path,
            'resource': {
                'type': 'global',
            },
            'labels': DEFAULT_LABELS,
            'entries': [
                {'textPayload': TEXT, 'httpRequest': REQUEST},
                {'jsonPayload': STRUCT, 'labels': LABELS},
                {'protoPayload': json.loads(MessageToJson(message)),
                 'severity': SEVERITY},
            ],
        }
        batch = self._makeOne(logger, client=CLIENT)

        with batch as other:
            other.log_text(TEXT, http_request=REQUEST)
            other.log_struct(STRUCT, labels=LABELS)
            other.log_proto(message, severity=SEVERITY)

        self.assertEqual(list(batch.entries), [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

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
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        logger = _Logger()
        UNSENT = [
            ('text', TEXT, None, IID, None, None),
            ('struct', STRUCT, None, None, SEVERITY, None),
            ('proto', message, LABELS, None, None, REQUEST),
        ]
        batch = self._makeOne(logger, client=CLIENT)

        try:
            with batch as other:
                other.log_text(TEXT, insert_id=IID)
                other.log_struct(STRUCT, severity=SEVERITY)
                other.log_proto(message, labels=LABELS, http_request=REQUEST)
                raise _Bugout()
        except _Bugout:
            pass

        self.assertEqual(list(batch.entries), UNSENT)
        self.assertEqual(len(conn._requested), 0)


class _Logger(object):

    labels = None

    def __init__(self, name="NAME", project="PROJECT"):
        self.path = '/projects/%s/logs/%s' % (project, name)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


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
