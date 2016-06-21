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


try:
    # pylint: disable=unused-import
    import gcloud.pubsub._gax
    # pylint: enable=unused-import
except ImportError:  # pragma: NO COVER
    _HAVE_GAX = False
else:
    _HAVE_GAX = True


class _Base(object):
    PROJECT = 'PROJECT'
    PROJECT_PATH = 'projects/%s' % (PROJECT,)
    LIST_SINKS_PATH = '%s/sinks' % (PROJECT_PATH,)
    SINK_NAME = 'sink_name'
    SINK_PATH = 'projects/%s/sinks/%s' % (PROJECT, SINK_NAME)

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


@unittest2.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_LoggingAPI(_Base, unittest2.TestCase):
    LOG_NAME = 'log_name'
    FILTER = 'logName:syslog AND severity>=ERROR'

    def _getTargetClass(self):
        from gcloud.logging._gax import _LoggingAPI
        return _LoggingAPI

    def test_ctor(self):
        gax_api = _GAXLoggingAPI()
        api = self._makeOne(gax_api)
        self.assertTrue(api._gax_api is gax_api)

    def test_list_entries_no_paging(self):
        from google.gax import INITIAL_PAGE
        from gcloud.logging import DESCENDING
        from gcloud._testing import _GAXPageIterator
        TOKEN = 'TOKEN'
        TEXT = 'TEXT'
        response = _GAXPageIterator(
            [_LogEntryPB(self.LOG_NAME, text_payload=TEXT)], TOKEN)
        gax_api = _GAXLoggingAPI(_list_log_entries_response=response)
        api = self._makeOne(gax_api)

        entries, next_token = api.list_entries(
            [self.PROJECT], self.FILTER, DESCENDING)

        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertIsInstance(entry, dict)
        self.assertEqual(entry['log_name'], self.LOG_NAME)
        self.assertEqual(entry['resource'], {'type': 'global'})
        self.assertEqual(entry['text_payload'], TEXT)
        self.assertEqual(next_token, TOKEN)

        projects, filter_, order_by, page_size, options = (
            gax_api._list_log_entries_called_with)
        self.assertEqual(projects, [self.PROJECT])
        self.assertEqual(filter_, self.FILTER)
        self.assertEqual(order_by, DESCENDING)
        self.assertEqual(page_size, 0)
        self.assertTrue(options.page_token is INITIAL_PAGE)

    def test_list_entries_with_paging(self):
        from gcloud._testing import _GAXPageIterator
        SIZE = 23
        TOKEN = 'TOKEN'
        NEW_TOKEN = 'NEW_TOKEN'
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'sunny'}
        response = _GAXPageIterator(
            [_LogEntryPB(self.LOG_NAME, json_payload=PAYLOAD)], NEW_TOKEN)
        gax_api = _GAXLoggingAPI(_list_log_entries_response=response)
        api = self._makeOne(gax_api)

        entries, next_token = api.list_entries(
            [self.PROJECT], page_size=SIZE, page_token=TOKEN)

        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertIsInstance(entry, dict)
        self.assertEqual(entry['log_name'], self.LOG_NAME)
        self.assertEqual(entry['resource'], {'type': 'global'})
        self.assertEqual(entry['json_payload'], PAYLOAD)
        self.assertEqual(next_token, NEW_TOKEN)

        projects, filter_, order_by, page_size, options = (
            gax_api._list_log_entries_called_with)
        self.assertEqual(projects, [self.PROJECT])
        self.assertEqual(filter_, '')
        self.assertEqual(order_by, '')
        self.assertEqual(page_size, SIZE)
        self.assertEqual(options.page_token, TOKEN)

    def test_list_entries_with_extra_properties(self):
        from gcloud._testing import _GAXPageIterator
        SIZE = 23
        TOKEN = 'TOKEN'
        NEW_TOKEN = 'NEW_TOKEN'
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'sunny'}
        SEVERITY = 'WARNING'
        LABELS = {
            'foo': 'bar',
        }
        IID = 'IID'
        request = _HTTPRequestPB()
        operation = _LogEntryOperationPB()
        EXTRAS = {
            'severity': SEVERITY,
            'labels': LABELS,
            'insert_id': IID,
            'http_request': request,
            'operation': operation,
        }
        ENTRY = _LogEntryPB(self.LOG_NAME, proto_payload=PAYLOAD, **EXTRAS)
        response = _GAXPageIterator([ENTRY], NEW_TOKEN)
        gax_api = _GAXLoggingAPI(_list_log_entries_response=response)
        api = self._makeOne(gax_api)

        entries, next_token = api.list_entries(
            [self.PROJECT], page_size=SIZE, page_token=TOKEN)

        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertIsInstance(entry, dict)
        self.assertEqual(entry['log_name'], self.LOG_NAME)
        self.assertEqual(entry['resource'], {'type': 'global'})
        self.assertEqual(entry['proto_payload'], PAYLOAD)
        self.assertEqual(entry['severity'], SEVERITY)
        self.assertEqual(entry['labels'], LABELS)
        self.assertEqual(entry['insert_id'], IID)
        EXPECTED_REQUEST = {
            'request_method': request.request_method,
            'request_url': request.request_url,
            'status': request.status,
            'request_size': request.request_size,
            'response_size': request.response_size,
            'referer': request.referer,
            'user_agent': request.user_agent,
            'remote_ip': request.remote_ip,
            'cache_hit': request.cache_hit,
        }
        self.assertEqual(entry['http_request'], EXPECTED_REQUEST)
        EXPECTED_OPERATION = {
            'producer': operation.producer,
            'id': operation.id,
            'first': operation.first,
            'last': operation.last,
        }
        self.assertEqual(entry['operation'], EXPECTED_OPERATION)
        self.assertEqual(next_token, NEW_TOKEN)

        projects, filter_, order_by, page_size, options = (
            gax_api._list_log_entries_called_with)
        self.assertEqual(projects, [self.PROJECT])
        self.assertEqual(filter_, '')
        self.assertEqual(order_by, '')
        self.assertEqual(page_size, SIZE)
        self.assertEqual(options.page_token, TOKEN)

    def test_write_entries_single(self):
        from google.logging.v2.log_entry_pb2 import LogEntry
        TEXT = 'TEXT'
        LOG_PATH = 'projects/%s/logs/%s' % (self.PROJECT, self.LOG_NAME)
        ENTRY = {
            'log_name': LOG_PATH,
            'resource': {'type': 'global'},
            'text_payload': TEXT,
        }
        gax_api = _GAXLoggingAPI()
        api = self._makeOne(gax_api)

        api.write_entries([ENTRY])

        entries, log_name, resource, labels, partial_success, options = (
            gax_api._write_log_entries_called_with)
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertTrue(isinstance(entry, LogEntry))
        self.assertEqual(entry.log_name, LOG_PATH)
        self.assertEqual(entry.resource.type, 'global')
        self.assertEqual(entry.labels, {})
        self.assertEqual(entry.text_payload, TEXT)

        self.assertEqual(log_name, None)
        self.assertEqual(resource, None)
        self.assertEqual(labels, None)
        self.assertEqual(partial_success, False)
        self.assertEqual(options, None)

    def test_write_entries_w_extra_properties(self):
        # pylint: disable=too-many-statements
        from datetime import datetime
        from google.logging.type.log_severity_pb2 import WARNING
        from google.logging.v2.log_entry_pb2 import LogEntry
        from gcloud._helpers import UTC, _pb_timestamp_to_datetime
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TEXT = 'TEXT'
        LOG_PATH = 'projects/%s/logs/%s' % (self.PROJECT, self.LOG_NAME)
        SEVERITY = 'WARNING'
        LABELS = {
            'foo': 'bar',
        }
        IID = 'IID'
        REQUEST_METHOD = 'GET'
        REQUEST_URL = 'http://example.com/requested'
        STATUS = 200
        REQUEST_SIZE = 256
        RESPONSE_SIZE = 1024
        REFERRER_URL = 'http://example.com/referer'
        USER_AGENT = 'Agent/1.0'
        REMOTE_IP = '1.2.3.4'
        REQUEST = {
            'request_method': REQUEST_METHOD,
            'request_url': REQUEST_URL,
            'status': STATUS,
            'request_size': REQUEST_SIZE,
            'response_size': RESPONSE_SIZE,
            'referer': REFERRER_URL,
            'user_agent': USER_AGENT,
            'remote_ip': REMOTE_IP,
            'cache_hit': False,
        }
        PRODUCER = 'PRODUCER'
        OPID = 'OPID'
        OPERATION = {
            'producer': PRODUCER,
            'id': OPID,
            'first': False,
            'last': True,
        }
        ENTRY = {
            'log_name': LOG_PATH,
            'resource': {'type': 'global'},
            'text_payload': TEXT,
            'severity': SEVERITY,
            'labels': LABELS,
            'insert_id': IID,
            'timestamp': NOW,
            'http_request': REQUEST,
            'operation': OPERATION,
        }
        gax_api = _GAXLoggingAPI()
        api = self._makeOne(gax_api)

        api.write_entries([ENTRY])

        entries, log_name, resource, labels, partial_success, options = (
            gax_api._write_log_entries_called_with)
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertTrue(isinstance(entry, LogEntry))
        self.assertEqual(entry.log_name, LOG_PATH)
        self.assertEqual(entry.resource.type, 'global')
        self.assertEqual(entry.text_payload, TEXT)
        self.assertEqual(entry.severity, WARNING)
        self.assertEqual(entry.labels, LABELS)
        self.assertEqual(entry.insert_id, IID)
        stamp = _pb_timestamp_to_datetime(entry.timestamp)
        self.assertEqual(stamp, NOW)

        request = entry.http_request
        self.assertEqual(request.request_method, REQUEST_METHOD)
        self.assertEqual(request.request_url, REQUEST_URL)
        self.assertEqual(request.status, STATUS)
        self.assertEqual(request.request_size, REQUEST_SIZE)
        self.assertEqual(request.response_size, RESPONSE_SIZE)
        self.assertEqual(request.referer, REFERRER_URL)
        self.assertEqual(request.user_agent, USER_AGENT)
        self.assertEqual(request.remote_ip, REMOTE_IP)
        self.assertEqual(request.cache_hit, False)

        operation = entry.operation
        self.assertEqual(operation.producer, PRODUCER)
        self.assertEqual(operation.id, OPID)
        self.assertFalse(operation.first)
        self.assertTrue(operation.last)

        self.assertEqual(log_name, None)
        self.assertEqual(resource, None)
        self.assertEqual(labels, None)
        self.assertEqual(partial_success, False)
        self.assertEqual(options, None)
        # pylint: enable=too-many-statements

    def test_write_entries_multiple(self):
        # pylint: disable=too-many-statements
        from google.logging.type.log_severity_pb2 import WARNING
        from google.logging.v2.log_entry_pb2 import LogEntry
        from google.protobuf.any_pb2 import Any
        from google.protobuf.struct_pb2 import Struct
        TEXT = 'TEXT'
        TIMESTAMP = _LogEntryPB._make_timestamp()
        TIMESTAMP_TYPE_URL = 'type.googleapis.com/google.protobuf.Timestamp'
        JSON = {'payload': 'PAYLOAD', 'type': 'json'}
        PROTO = {
            '@type': TIMESTAMP_TYPE_URL,
            'value': TIMESTAMP,
        }
        PRODUCER = 'PRODUCER'
        OPID = 'OPID'
        URL = 'http://example.com/'
        ENTRIES = [
            {'text_payload': TEXT,
             'severity': WARNING},
            {'json_payload': JSON,
             'operation': {'producer': PRODUCER, 'id': OPID}},
            {'proto_payload': PROTO,
             'http_request': {'request_url': URL}},
        ]
        LOG_PATH = 'projects/%s/logs/%s' % (self.PROJECT, self.LOG_NAME)
        RESOURCE = {
            'type': 'global',
        }
        LABELS = {
            'foo': 'bar',
        }
        gax_api = _GAXLoggingAPI()
        api = self._makeOne(gax_api)

        api.write_entries(ENTRIES, LOG_PATH, RESOURCE, LABELS)

        entries, log_name, resource, labels, partial_success, options = (
            gax_api._write_log_entries_called_with)
        self.assertEqual(len(entries), len(ENTRIES))

        entry = entries[0]
        self.assertTrue(isinstance(entry, LogEntry))
        self.assertEqual(entry.log_name, '')
        self.assertEqual(entry.resource.type, '')
        self.assertEqual(entry.labels, {})
        self.assertEqual(entry.text_payload, TEXT)
        self.assertEqual(entry.severity, WARNING)

        entry = entries[1]
        self.assertTrue(isinstance(entry, LogEntry))
        self.assertEqual(entry.log_name, '')
        self.assertEqual(entry.resource.type, '')
        self.assertEqual(entry.labels, {})
        json_struct = entry.json_payload
        self.assertTrue(isinstance(json_struct, Struct))
        self.assertEqual(json_struct.fields['payload'].string_value,
                         JSON['payload'])
        operation = entry.operation
        self.assertEqual(operation.producer, PRODUCER)
        self.assertEqual(operation.id, OPID)

        entry = entries[2]
        self.assertTrue(isinstance(entry, LogEntry))
        self.assertEqual(entry.log_name, '')
        self.assertEqual(entry.resource.type, '')
        self.assertEqual(entry.labels, {})
        proto = entry.proto_payload
        self.assertTrue(isinstance(proto, Any))
        self.assertEqual(proto.type_url, TIMESTAMP_TYPE_URL)
        request = entry.http_request
        self.assertEqual(request.request_url, URL)

        self.assertEqual(log_name, LOG_PATH)
        self.assertEqual(resource, RESOURCE)
        self.assertEqual(labels, LABELS)
        self.assertEqual(partial_success, False)
        self.assertEqual(options, None)
        # pylint: enable=too-many-statements

    def test_logger_delete(self):
        LOG_PATH = 'projects/%s/logs/%s' % (self.PROJECT, self.LOG_NAME)
        gax_api = _GAXLoggingAPI()
        api = self._makeOne(gax_api)

        api.logger_delete(self.PROJECT, self.LOG_NAME)

        log_name, options = gax_api._delete_log_called_with
        self.assertEqual(log_name, LOG_PATH)
        self.assertEqual(options, None)


class _GAXLoggingAPI(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def list_log_entries(
            self, projects, filter_, order_by, page_size, options):
        self._list_log_entries_called_with = (
            projects, filter_, order_by, page_size, options)
        return self._list_log_entries_response

    def write_log_entries(self, entries, log_name, resource, labels,
                          partial_success, options):
        self._write_log_entries_called_with = (
            entries, log_name, resource, labels, partial_success, options)

    def delete_log(self, log_name, options):
        self._delete_log_called_with = log_name, options


class _HTTPRequestPB(object):

    request_url = 'http://example.com/requested'
    request_method = 'GET'
    status = 200
    referer = 'http://example.com/referer'
    user_agent = 'AGENT'
    cache_hit = False
    request_size = 256
    response_size = 1024
    remote_ip = '192.168.1.254'


class _LogEntryOperationPB(object):

    producer = 'PRODUCER'
    first = last = False
    id = 'OPID'


class _LogEntryPB(object):

    severity = 'DEFAULT'
    http_request = operation = insert_id = None
    text_payload = json_payload = proto_payload = None

    def __init__(self, log_name, **kw):
        self.log_name = log_name
        self.resource = {'type': 'global'}
        self.timestamp = self._make_timestamp()
        self.labels = kw.pop('labels', {})
        self.__dict__.update(kw)

    @staticmethod
    def _make_timestamp():
        from datetime import datetime
        from gcloud._helpers import UTC
        from gcloud.logging.test_entries import _datetime_to_rfc3339_w_nanos
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        return _datetime_to_rfc3339_w_nanos(NOW)
