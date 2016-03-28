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

    def test_ctor(self):
        conn = _Connection()
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)
        self.assertEqual(logger.full_name, 'projects/%s/logs/%s'
                         % (self.PROJECT, self.LOGGER_NAME))

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

    def test_log_text_w_unicode_explicit_client(self):
        TEXT = u'TEXT'
        conn = _Connection({})
        client1 = _Client(self.PROJECT, object())
        client2 = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client1)
        logger.log_text(TEXT, client=client2)
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

    def test_log_struct_w_explicit_client(self):
        STRUCT = {'message': 'MESSAGE', 'weather': 'cloudy'}
        conn = _Connection({})
        client1 = _Client(self.PROJECT, object())
        client2 = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client1)
        logger.log_struct(STRUCT, client=client2)
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

    def test_log_proto_w_explicit_client(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        conn = _Connection({})
        client1 = _Client(self.PROJECT, object())
        client2 = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client1)
        logger.log_proto(message, client=client2)
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

    def test_log_text(self):
        TEXT = 'This is the entry text'
        connection = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=connection)
        logger = _Logger()
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_text(TEXT)
        self.assertEqual(len(connection._requested), 0)
        self.assertEqual(batch.entries, [('text', TEXT)])

    def test_log_struct(self):
        STRUCT = {'message': 'Message text', 'weather': 'partly cloudy'}
        connection = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=connection)
        logger = _Logger()
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_struct(STRUCT)
        self.assertEqual(len(connection._requested), 0)
        self.assertEqual(batch.entries, [('struct', STRUCT)])

    def test_log_proto(self):
        from google.protobuf.struct_pb2 import Struct, Value
        message = Struct(fields={'foo': Value(bool_value=True)})
        connection = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=connection)
        logger = _Logger()
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_proto(message)
        self.assertEqual(len(connection._requested), 0)
        self.assertEqual(batch.entries, [('proto', message)])

    def test_commit_w_bound_client(self):
        import json
        from google.protobuf.json_format import MessageToJson
        from google.protobuf.struct_pb2 import Struct, Value
        TEXT = 'This is the entry text'
        STRUCT = {'message': TEXT, 'weather': 'partly cloudy'}
        message = Struct(fields={'foo': Value(bool_value=True)})
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        logger = _Logger()
        SENT = {
            'logName': logger.path,
            'resource': {
                'type': 'global',
            },
            'entries': [
                {'textPayload': TEXT},
                {'structPayload': STRUCT},
                {'protoPayload': json.loads(MessageToJson(message))},
            ],
        }
        batch = self._makeOne(logger, client=CLIENT)
        batch.log_text(TEXT)
        batch.log_struct(STRUCT)
        batch.log_proto(message)
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
        TEXT = 'This is the entry text'
        STRUCT = {'message': TEXT, 'weather': 'partly cloudy'}
        message = Struct(fields={'foo': Value(bool_value=True)})
        conn1 = _Connection()
        conn2 = _Connection({})
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        logger = _Logger()
        SENT = {
            'logName': logger.path,
            'resource': {'type': 'global'},
            'entries': [
                {'textPayload': TEXT},
                {'structPayload': STRUCT},
                {'protoPayload': json.loads(MessageToJson(message))},
            ],
        }
        batch = self._makeOne(logger, client=CLIENT1)
        batch.log_text(TEXT)
        batch.log_struct(STRUCT)
        batch.log_proto(message)
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
        TEXT = 'This is the entry text'
        STRUCT = {'message': TEXT, 'weather': 'partly cloudy'}
        message = Struct(fields={'foo': Value(bool_value=True)})
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        logger = _Logger()
        SENT = {
            'logName': logger.path,
            'resource': {
                'type': 'global',
            },
            'entries': [
                {'textPayload': TEXT},
                {'structPayload': STRUCT},
                {'protoPayload': json.loads(MessageToJson(message))},
            ],
        }
        batch = self._makeOne(logger, client=CLIENT)

        with batch as other:
            other.log_text(TEXT)
            other.log_struct(STRUCT)
            other.log_proto(message)

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
        message = Struct(fields={'foo': Value(bool_value=True)})
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        logger = _Logger()
        UNSENT = [('text', TEXT), ('struct', STRUCT), ('proto', message)]
        batch = self._makeOne(logger, client=CLIENT)

        try:
            with batch as other:
                other.log_text(TEXT)
                other.log_struct(STRUCT)
                other.log_proto(message)
                raise _Bugout()
        except _Bugout:
            pass

        self.assertEqual(list(batch.entries), UNSENT)
        self.assertEqual(len(conn._requested), 0)


class _Logger(object):

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
