# Copyright 2016 Google Inc.
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

import unittest

import mock

try:
    # pylint: disable=unused-import
    import google.cloud.logging._gax
    # pylint: enable=unused-import
except ImportError:  # pragma: NO COVER
    _HAVE_GAX = False
else:
    _HAVE_GAX = True

from google.cloud._testing import _GAXBaseAPI


def _make_credentials():
    # pylint: disable=redefined-outer-name
    import google.auth.credentials
    # pylint: enable=redefined-outer-name

    return mock.Mock(spec=google.auth.credentials.Credentials)


class _Base(object):
    PROJECT = 'PROJECT'
    PROJECT_PATH = 'projects/%s' % (PROJECT,)
    FILTER = 'logName:syslog AND severity>=ERROR'

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)


@unittest.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_LoggingAPI(_Base, unittest.TestCase):
    LOG_NAME = 'log_name'
    LOG_PATH = 'projects/%s/logs/%s' % (_Base.PROJECT, LOG_NAME)

    @staticmethod
    def _get_target_class():
        from google.cloud.logging._gax import _LoggingAPI

        return _LoggingAPI

    def test_ctor(self):
        gax_api = _GAXLoggingAPI()
        client = object()
        api = self._make_one(gax_api, client)
        self.assertIs(api._gax_api, gax_api)
        self.assertIs(api._client, client)

    def test_list_entries_no_paging(self):
        import datetime

        from google.api.monitored_resource_pb2 import MonitoredResource
        from google.gax import INITIAL_PAGE
        from google.cloud.proto.logging.v2.log_entry_pb2 import LogEntry

        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud._helpers import UTC
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.logging import DESCENDING
        from google.cloud.logging.client import Client
        from google.cloud.logging.entries import TextEntry
        from google.cloud.logging.logger import Logger

        TOKEN = 'TOKEN'
        TEXT = 'TEXT'
        resource_pb = MonitoredResource(type='global')
        timestamp = datetime.datetime.utcnow().replace(tzinfo=UTC)
        timestamp_pb = _datetime_to_pb_timestamp(timestamp)
        entry_pb = LogEntry(log_name=self.LOG_PATH,
                            resource=resource_pb,
                            timestamp=timestamp_pb,
                            text_payload=TEXT)
        response = _GAXPageIterator([entry_pb], page_token=TOKEN)
        gax_api = _GAXLoggingAPI(_list_log_entries_response=response)
        client = Client(project=self.PROJECT, credentials=_make_credentials(),
                        use_gax=True)
        api = self._make_one(gax_api, client)

        iterator = api.list_entries(
            [self.PROJECT], self.FILTER, DESCENDING)
        entries = list(iterator)
        next_token = iterator.next_page_token

        # First check the token.
        self.assertEqual(next_token, TOKEN)
        # Then check the entries returned.
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertIsInstance(entry, TextEntry)
        self.assertEqual(entry.payload, TEXT)
        self.assertIsInstance(entry.logger, Logger)
        self.assertEqual(entry.logger.name, self.LOG_NAME)
        self.assertIsNone(entry.insert_id)
        self.assertEqual(entry.timestamp, timestamp)
        self.assertIsNone(entry.labels)
        self.assertIsNone(entry.severity)
        self.assertIsNone(entry.http_request)

        resource_names, projects, filter_, order_by, page_size, options = (
            gax_api._list_log_entries_called_with)
        self.assertEqual(resource_names, [])
        self.assertEqual(projects, [self.PROJECT])
        self.assertEqual(filter_, self.FILTER)
        self.assertEqual(order_by, DESCENDING)
        self.assertEqual(page_size, 0)
        self.assertIs(options.page_token, INITIAL_PAGE)

    def _list_entries_with_paging_helper(self, payload, struct_pb):
        import datetime

        from google.api.monitored_resource_pb2 import MonitoredResource
        from google.cloud.proto.logging.v2.log_entry_pb2 import LogEntry
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud._helpers import UTC
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.logging.client import Client
        from google.cloud.logging.entries import StructEntry
        from google.cloud.logging.logger import Logger

        SIZE = 23
        TOKEN = 'TOKEN'
        NEW_TOKEN = 'NEW_TOKEN'
        resource_pb = MonitoredResource(type='global')
        timestamp = datetime.datetime.utcnow().replace(tzinfo=UTC)
        timestamp_pb = _datetime_to_pb_timestamp(timestamp)
        entry_pb = LogEntry(log_name=self.LOG_PATH,
                            resource=resource_pb,
                            timestamp=timestamp_pb,
                            json_payload=struct_pb)
        response = _GAXPageIterator([entry_pb], page_token=NEW_TOKEN)
        gax_api = _GAXLoggingAPI(_list_log_entries_response=response)
        client = Client(project=self.PROJECT, credentials=_make_credentials(),
                        use_gax=True)
        api = self._make_one(gax_api, client)

        iterator = api.list_entries(
            [self.PROJECT], page_size=SIZE, page_token=TOKEN)
        entries = list(iterator)
        next_token = iterator.next_page_token

        # First check the token.
        self.assertEqual(next_token, NEW_TOKEN)
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertIsInstance(entry, StructEntry)
        self.assertEqual(entry.payload, payload)
        self.assertIsInstance(entry.logger, Logger)
        self.assertEqual(entry.logger.name, self.LOG_NAME)
        self.assertIsNone(entry.insert_id)
        self.assertEqual(entry.timestamp, timestamp)
        self.assertIsNone(entry.labels)
        self.assertIsNone(entry.severity)
        self.assertIsNone(entry.http_request)

        resource_names, projects, filter_, order_by, page_size, options = (
            gax_api._list_log_entries_called_with)
        self.assertEqual(resource_names, [])
        self.assertEqual(projects, [self.PROJECT])
        self.assertEqual(filter_, '')
        self.assertEqual(order_by, '')
        self.assertEqual(page_size, SIZE)
        self.assertEqual(options.page_token, TOKEN)

    def test_list_entries_with_paging(self):
        from google.protobuf.struct_pb2 import Struct
        from google.protobuf.struct_pb2 import Value

        payload = {'message': 'MESSAGE', 'weather': 'sunny'}
        struct_pb = Struct(fields={
            key: Value(string_value=value) for key, value in payload.items()
        })
        self._list_entries_with_paging_helper(payload, struct_pb)

    def test_list_entries_with_paging_nested_payload(self):
        from google.protobuf.struct_pb2 import Struct
        from google.protobuf.struct_pb2 import Value

        payload = {}
        struct_fields = {}
        # Add a simple key.
        key = 'message'
        payload[key] = 'MESSAGE'
        struct_fields[key] = Value(string_value=payload[key])
        # Add a nested key.
        key = 'weather'
        sub_value = {}
        sub_fields = {}
        sub_key = 'temperature'
        sub_value[sub_key] = 75
        sub_fields[sub_key] = Value(number_value=sub_value[sub_key])
        sub_key = 'precipitation'
        sub_value[sub_key] = False
        sub_fields[sub_key] = Value(bool_value=sub_value[sub_key])
        # Update the parent payload.
        payload[key] = sub_value
        struct_fields[key] = Value(struct_value=Struct(fields=sub_fields))
        # Make the struct_pb for our dict.
        struct_pb = Struct(fields=struct_fields)
        self._list_entries_with_paging_helper(payload, struct_pb)

    def _make_log_entry_with_extras(self, labels, iid, type_url, now):
        from google.api.monitored_resource_pb2 import MonitoredResource
        from google.cloud.proto.logging.v2.log_entry_pb2 import LogEntry
        from google.cloud.proto.logging.v2.log_entry_pb2 import (
            LogEntryOperation)
        from google.logging.type.http_request_pb2 import HttpRequest
        from google.logging.type.log_severity_pb2 import WARNING
        from google.protobuf.any_pb2 import Any

        from google.cloud._helpers import _datetime_to_pb_timestamp

        resource_pb = MonitoredResource(
            type='global', labels=labels)
        proto_payload = Any(type_url=type_url)
        timestamp_pb = _datetime_to_pb_timestamp(now)
        request_pb = HttpRequest(
            request_url='http://example.com/requested',
            request_method='GET',
            status=200,
            referer='http://example.com/referer',
            user_agent='AGENT',
            cache_hit=True,
            request_size=256,
            response_size=1024,
            remote_ip='1.2.3.4',
        )
        operation_pb = LogEntryOperation(
            producer='PRODUCER',
            first=True,
            last=True,
            id='OPID',
        )
        entry_pb = LogEntry(log_name=self.LOG_PATH,
                            resource=resource_pb,
                            proto_payload=proto_payload,
                            timestamp=timestamp_pb,
                            severity=WARNING,
                            insert_id=iid,
                            http_request=request_pb,
                            labels=labels,
                            operation=operation_pb)
        return entry_pb

    def test_list_entries_with_extra_properties(self):
        import datetime

        # Import the wrappers to register the type URL for BoolValue
        # pylint: disable=unused-variable
        from google.protobuf import wrappers_pb2
        # pylint: enable=unused-variable

        from google.cloud._helpers import UTC
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.logging.client import Client
        from google.cloud.logging.entries import ProtobufEntry
        from google.cloud.logging.logger import Logger

        NOW = datetime.datetime.utcnow().replace(tzinfo=UTC)
        SIZE = 23
        TOKEN = 'TOKEN'
        NEW_TOKEN = 'NEW_TOKEN'
        SEVERITY = 'WARNING'
        LABELS = {
            'foo': 'bar',
        }
        IID = 'IID'
        bool_type_url = 'type.googleapis.com/google.protobuf.BoolValue'
        entry_pb = self._make_log_entry_with_extras(
            LABELS, IID, bool_type_url, NOW)

        response = _GAXPageIterator([entry_pb], page_token=NEW_TOKEN)
        gax_api = _GAXLoggingAPI(_list_log_entries_response=response)
        client = Client(project=self.PROJECT, credentials=_make_credentials(),
                        use_gax=True)
        api = self._make_one(gax_api, client)

        iterator = api.list_entries(
            [self.PROJECT], page_size=SIZE, page_token=TOKEN)
        entries = list(iterator)
        next_token = iterator.next_page_token

        # First check the token.
        self.assertEqual(next_token, NEW_TOKEN)
        # Then check the entries returned.
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertIsInstance(entry, ProtobufEntry)
        self.assertEqual(entry.payload, {
            '@type': bool_type_url,
            'value': False,
        })
        self.assertIsInstance(entry.logger, Logger)
        self.assertEqual(entry.logger.name, self.LOG_NAME)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, NOW)
        self.assertEqual(entry.labels, {'foo': 'bar'})
        self.assertEqual(entry.severity, SEVERITY)
        self.assertEqual(entry.http_request, {
            'requestMethod': entry_pb.http_request.request_method,
            'requestUrl': entry_pb.http_request.request_url,
            'status': entry_pb.http_request.status,
            'requestSize': str(entry_pb.http_request.request_size),
            'responseSize': str(entry_pb.http_request.response_size),
            'referer': entry_pb.http_request.referer,
            'userAgent': entry_pb.http_request.user_agent,
            'remoteIp': entry_pb.http_request.remote_ip,
            'cacheHit': entry_pb.http_request.cache_hit,
        })

        resource_names, projects, filter_, order_by, page_size, options = (
            gax_api._list_log_entries_called_with)
        self.assertEqual(resource_names, [])
        self.assertEqual(projects, [self.PROJECT])
        self.assertEqual(filter_, '')
        self.assertEqual(order_by, '')
        self.assertEqual(page_size, SIZE)
        self.assertEqual(options.page_token, TOKEN)

    def test_write_entries_single(self):
        from google.cloud.proto.logging.v2.log_entry_pb2 import LogEntry

        TEXT = 'TEXT'
        ENTRY = {
            'logName': self.LOG_PATH,
            'resource': {'type': 'global'},
            'textPayload': TEXT,
        }
        gax_api = _GAXLoggingAPI()
        api = self._make_one(gax_api, None)

        api.write_entries([ENTRY])

        entries, log_name, resource, labels, partial_success, options = (
            gax_api._write_log_entries_called_with)
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertIsInstance(entry, LogEntry)
        self.assertEqual(entry.log_name, self.LOG_PATH)
        self.assertEqual(entry.resource.type, 'global')
        self.assertEqual(entry.labels, {})
        self.assertEqual(entry.text_payload, TEXT)

        self.assertIsNone(log_name)
        self.assertIsNone(resource)
        self.assertIsNone(labels)
        self.assertEqual(partial_success, False)
        self.assertIsNone(options)

    def test_write_entries_w_extra_properties(self):
        # pylint: disable=too-many-statements
        from datetime import datetime
        from google.logging.type.log_severity_pb2 import WARNING
        from google.cloud.proto.logging.v2.log_entry_pb2 import LogEntry
        from google.cloud._helpers import _datetime_to_rfc3339
        from google.cloud._helpers import UTC, _pb_timestamp_to_datetime

        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TEXT = 'TEXT'
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
            'requestMethod': REQUEST_METHOD,
            'requestUrl': REQUEST_URL,
            'status': STATUS,
            'requestSize': REQUEST_SIZE,
            'responseSize': RESPONSE_SIZE,
            'referer': REFERRER_URL,
            'userAgent': USER_AGENT,
            'remoteIp': REMOTE_IP,
            'cacheHit': False,
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
            'logName': self.LOG_PATH,
            'resource': {'type': 'global'},
            'textPayload': TEXT,
            'severity': SEVERITY,
            'labels': LABELS,
            'insertId': IID,
            'timestamp': _datetime_to_rfc3339(NOW),
            'httpRequest': REQUEST,
            'operation': OPERATION,
        }
        gax_api = _GAXLoggingAPI()
        api = self._make_one(gax_api, None)

        api.write_entries([ENTRY])

        entries, log_name, resource, labels, partial_success, options = (
            gax_api._write_log_entries_called_with)
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertIsInstance(entry, LogEntry)
        self.assertEqual(entry.log_name, self.LOG_PATH)
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

        self.assertIsNone(log_name)
        self.assertIsNone(resource)
        self.assertIsNone(labels)
        self.assertEqual(partial_success, False)
        self.assertIsNone(options)
        # pylint: enable=too-many-statements

    def _write_entries_multiple_helper(self, json_payload, json_struct_pb):
        # pylint: disable=too-many-statements
        import datetime
        from google.logging.type.log_severity_pb2 import WARNING
        from google.cloud.proto.logging.v2.log_entry_pb2 import LogEntry
        from google.protobuf.any_pb2 import Any
        from google.cloud._helpers import _datetime_to_rfc3339
        from google.cloud._helpers import UTC

        TEXT = 'TEXT'
        NOW = datetime.datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP_TYPE_URL = 'type.googleapis.com/google.protobuf.Timestamp'
        PROTO = {
            '@type': TIMESTAMP_TYPE_URL,
            'value': _datetime_to_rfc3339(NOW),
        }
        PRODUCER = 'PRODUCER'
        OPID = 'OPID'
        URL = 'http://example.com/'
        ENTRIES = [
            {'textPayload': TEXT,
             'severity': WARNING},
            {'jsonPayload': json_payload,
             'operation': {'producer': PRODUCER, 'id': OPID}},
            {'protoPayload': PROTO,
             'httpRequest': {'requestUrl': URL}},
        ]
        RESOURCE = {
            'type': 'global',
        }
        LABELS = {
            'foo': 'bar',
        }
        gax_api = _GAXLoggingAPI()
        api = self._make_one(gax_api, None)

        api.write_entries(ENTRIES, self.LOG_PATH, RESOURCE, LABELS)

        entries, log_name, resource, labels, partial_success, options = (
            gax_api._write_log_entries_called_with)
        self.assertEqual(len(entries), len(ENTRIES))

        entry = entries[0]
        self.assertIsInstance(entry, LogEntry)
        self.assertEqual(entry.log_name, '')
        self.assertEqual(entry.resource.type, '')
        self.assertEqual(entry.labels, {})
        self.assertEqual(entry.text_payload, TEXT)
        self.assertEqual(entry.severity, WARNING)

        entry = entries[1]
        self.assertIsInstance(entry, LogEntry)
        self.assertEqual(entry.log_name, '')
        self.assertEqual(entry.resource.type, '')
        self.assertEqual(entry.labels, {})
        self.assertEqual(entry.json_payload, json_struct_pb)
        operation = entry.operation
        self.assertEqual(operation.producer, PRODUCER)
        self.assertEqual(operation.id, OPID)

        entry = entries[2]
        self.assertIsInstance(entry, LogEntry)
        self.assertEqual(entry.log_name, '')
        self.assertEqual(entry.resource.type, '')
        self.assertEqual(entry.labels, {})
        proto = entry.proto_payload
        self.assertIsInstance(proto, Any)
        self.assertEqual(proto.type_url, TIMESTAMP_TYPE_URL)
        request = entry.http_request
        self.assertEqual(request.request_url, URL)

        self.assertEqual(log_name, self.LOG_PATH)
        self.assertEqual(resource, RESOURCE)
        self.assertEqual(labels, LABELS)
        self.assertEqual(partial_success, False)
        self.assertIsNone(options)
        # pylint: enable=too-many-statements

    def test_write_entries_multiple(self):
        from google.protobuf.struct_pb2 import Struct
        from google.protobuf.struct_pb2 import Value

        json_payload = {'payload': 'PAYLOAD', 'type': 'json'}
        json_struct_pb = Struct(fields={
            key: Value(string_value=value)
            for key, value in json_payload.items()
        })
        self._write_entries_multiple_helper(json_payload, json_struct_pb)

    def test_write_entries_multiple_nested_payload(self):
        from google.protobuf.struct_pb2 import Struct
        from google.protobuf.struct_pb2 import Value

        json_payload = {}
        struct_fields = {}
        # Add a simple key.
        key = 'hello'
        json_payload[key] = 'me you looking for'
        struct_fields[key] = Value(string_value=json_payload[key])
        # Add a nested key.
        key = 'everything'
        sub_value = {}
        sub_fields = {}
        sub_key = 'answer'
        sub_value[sub_key] = 42
        sub_fields[sub_key] = Value(number_value=sub_value[sub_key])
        sub_key = 'really?'
        sub_value[sub_key] = False
        sub_fields[sub_key] = Value(bool_value=sub_value[sub_key])
        # Update the parent payload.
        json_payload[key] = sub_value
        struct_fields[key] = Value(struct_value=Struct(fields=sub_fields))
        # Make the struct_pb for our dict.
        json_struct_pb = Struct(fields=struct_fields)
        self._write_entries_multiple_helper(json_payload, json_struct_pb)

    def test_logger_delete(self):
        gax_api = _GAXLoggingAPI()
        api = self._make_one(gax_api, None)

        api.logger_delete(self.PROJECT, self.LOG_NAME)

        log_name, options = gax_api._delete_log_called_with
        self.assertEqual(log_name, self.LOG_PATH)
        self.assertIsNone(options)

    def test_logger_delete_not_found(self):
        from google.cloud.exceptions import NotFound

        gax_api = _GAXLoggingAPI(_delete_not_found=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(NotFound):
            api.logger_delete(self.PROJECT, self.LOG_NAME)

        log_name, options = gax_api._delete_log_called_with
        self.assertEqual(log_name, self.LOG_PATH)
        self.assertIsNone(options)

    def test_logger_delete_error(self):
        from google.gax.errors import GaxError

        gax_api = _GAXLoggingAPI(_random_gax_error=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(GaxError):
            api.logger_delete(self.PROJECT, self.LOG_NAME)

        log_name, options = gax_api._delete_log_called_with
        self.assertEqual(log_name, self.LOG_PATH)
        self.assertIsNone(options)


@unittest.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_SinksAPI(_Base, unittest.TestCase):
    SINK_NAME = 'sink_name'
    SINK_PATH = 'projects/%s/sinks/%s' % (_Base.PROJECT, SINK_NAME)
    DESTINATION_URI = 'faux.googleapis.com/destination'

    @staticmethod
    def _get_target_class():
        from google.cloud.logging._gax import _SinksAPI

        return _SinksAPI

    def test_ctor(self):
        gax_api = _GAXSinksAPI()
        client = object()
        api = self._make_one(gax_api, client)
        self.assertIs(api._gax_api, gax_api)
        self.assertIs(api._client, client)

    def test_list_sinks_no_paging(self):
        import six
        from google.gax import INITIAL_PAGE
        from google.cloud.proto.logging.v2.logging_config_pb2 import LogSink
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.logging.sink import Sink

        TOKEN = 'TOKEN'
        sink_pb = LogSink(name=self.SINK_PATH,
                          destination=self.DESTINATION_URI,
                          filter=self.FILTER)
        response = _GAXPageIterator([sink_pb], page_token=TOKEN)
        gax_api = _GAXSinksAPI(_list_sinks_response=response)
        client = object()
        api = self._make_one(gax_api, client)

        iterator = api.list_sinks(self.PROJECT)
        page = six.next(iterator.pages)
        sinks = list(page)
        token = iterator.next_page_token

        # First check the token.
        self.assertEqual(token, TOKEN)
        # Then check the sinks returned.
        self.assertEqual(len(sinks), 1)
        sink = sinks[0]
        self.assertIsInstance(sink, Sink)
        self.assertEqual(sink.name, self.SINK_PATH)
        self.assertEqual(sink.filter_, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertIs(sink.client, client)

        project, page_size, options = gax_api._list_sinks_called_with
        self.assertEqual(project, self.PROJECT_PATH)
        self.assertEqual(page_size, 0)
        self.assertEqual(options.page_token, INITIAL_PAGE)

    def test_list_sinks_w_paging(self):
        from google.cloud.proto.logging.v2.logging_config_pb2 import LogSink
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.logging.sink import Sink

        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        sink_pb = LogSink(name=self.SINK_PATH,
                          destination=self.DESTINATION_URI,
                          filter=self.FILTER)
        response = _GAXPageIterator([sink_pb])
        gax_api = _GAXSinksAPI(_list_sinks_response=response)
        client = object()
        api = self._make_one(gax_api, client)

        iterator = api.list_sinks(
            self.PROJECT, page_size=PAGE_SIZE, page_token=TOKEN)
        sinks = list(iterator)
        token = iterator.next_page_token

        # First check the token.
        self.assertIsNone(token)
        # Then check the sinks returned.
        self.assertEqual(len(sinks), 1)
        sink = sinks[0]
        self.assertIsInstance(sink, Sink)
        self.assertEqual(sink.name, self.SINK_PATH)
        self.assertEqual(sink.filter_, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertIs(sink.client, client)

        project, page_size, options = gax_api._list_sinks_called_with
        self.assertEqual(project, self.PROJECT_PATH)
        self.assertEqual(page_size, PAGE_SIZE)
        self.assertEqual(options.page_token, TOKEN)

    def test_sink_create_error(self):
        from google.gax.errors import GaxError

        gax_api = _GAXSinksAPI(_random_gax_error=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(GaxError):
            api.sink_create(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

    def test_sink_create_conflict(self):
        from google.cloud.exceptions import Conflict

        gax_api = _GAXSinksAPI(_create_sink_conflict=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(Conflict):
            api.sink_create(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

    def test_sink_create_ok(self):
        from google.cloud.proto.logging.v2.logging_config_pb2 import LogSink

        gax_api = _GAXSinksAPI()
        api = self._make_one(gax_api, None)

        api.sink_create(
            self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI)

        parent, sink, options = (
            gax_api._create_sink_called_with)
        self.assertEqual(parent, self.PROJECT_PATH)
        self.assertIsInstance(sink, LogSink)
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertIsNone(options)

    def test_sink_get_error(self):
        from google.cloud.exceptions import NotFound

        gax_api = _GAXSinksAPI()
        api = self._make_one(gax_api, None)

        with self.assertRaises(NotFound):
            api.sink_get(self.PROJECT, self.SINK_NAME)

    def test_sink_get_miss(self):
        from google.gax.errors import GaxError

        gax_api = _GAXSinksAPI(_random_gax_error=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(GaxError):
            api.sink_get(self.PROJECT, self.SINK_NAME)

    def test_sink_get_hit(self):
        from google.cloud.proto.logging.v2.logging_config_pb2 import LogSink

        RESPONSE = {
            'name': self.SINK_PATH,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        sink_pb = LogSink(name=self.SINK_PATH,
                          destination=self.DESTINATION_URI,
                          filter=self.FILTER)
        gax_api = _GAXSinksAPI(_get_sink_response=sink_pb)
        api = self._make_one(gax_api, None)

        response = api.sink_get(self.PROJECT, self.SINK_NAME)

        self.assertEqual(response, RESPONSE)

        sink_name, options = gax_api._get_sink_called_with
        self.assertEqual(sink_name, self.SINK_PATH)
        self.assertIsNone(options)

    def test_sink_update_error(self):
        from google.gax.errors import GaxError

        gax_api = _GAXSinksAPI(_random_gax_error=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(GaxError):
            api.sink_update(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

    def test_sink_update_miss(self):
        from google.cloud.exceptions import NotFound

        gax_api = _GAXSinksAPI()
        api = self._make_one(gax_api, None)

        with self.assertRaises(NotFound):
            api.sink_update(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

    def test_sink_update_hit(self):
        from google.cloud.proto.logging.v2.logging_config_pb2 import LogSink

        response = LogSink(name=self.SINK_NAME,
                           destination=self.DESTINATION_URI,
                           filter=self.FILTER)
        gax_api = _GAXSinksAPI(_update_sink_response=response)
        api = self._make_one(gax_api, None)

        api.sink_update(
            self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI)

        sink_name, sink, options = (
            gax_api._update_sink_called_with)
        self.assertEqual(sink_name, self.SINK_PATH)
        self.assertIsInstance(sink, LogSink)
        self.assertEqual(sink.name, self.SINK_PATH)
        self.assertEqual(sink.filter, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertIsNone(options)

    def test_sink_delete_error(self):
        from google.gax.errors import GaxError

        gax_api = _GAXSinksAPI(_random_gax_error=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(GaxError):
            api.sink_delete(self.PROJECT, self.SINK_NAME)

    def test_sink_delete_miss(self):
        from google.cloud.exceptions import NotFound

        gax_api = _GAXSinksAPI(_sink_not_found=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(NotFound):
            api.sink_delete(self.PROJECT, self.SINK_NAME)

    def test_sink_delete_hit(self):
        gax_api = _GAXSinksAPI()
        api = self._make_one(gax_api, None)

        api.sink_delete(self.PROJECT, self.SINK_NAME)

        sink_name, options = gax_api._delete_sink_called_with
        self.assertEqual(sink_name, self.SINK_PATH)
        self.assertIsNone(options)


@unittest.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_MetricsAPI(_Base, unittest.TestCase):
    METRIC_NAME = 'metric_name'
    METRIC_PATH = 'projects/%s/metrics/%s' % (_Base.PROJECT, METRIC_NAME)
    DESCRIPTION = 'Description'

    @staticmethod
    def _get_target_class():
        from google.cloud.logging._gax import _MetricsAPI

        return _MetricsAPI

    def test_ctor(self):
        gax_api = _GAXMetricsAPI()
        api = self._make_one(gax_api, None)
        self.assertIs(api._gax_api, gax_api)

    def test_list_metrics_no_paging(self):
        import six
        from google.gax import INITIAL_PAGE
        from google.cloud.proto.logging.v2.logging_metrics_pb2 import LogMetric
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.logging.metric import Metric

        TOKEN = 'TOKEN'
        metric_pb = LogMetric(name=self.METRIC_PATH,
                              description=self.DESCRIPTION,
                              filter=self.FILTER)
        response = _GAXPageIterator([metric_pb], page_token=TOKEN)
        gax_api = _GAXMetricsAPI(_list_log_metrics_response=response)
        client = object()
        api = self._make_one(gax_api, client)

        iterator = api.list_metrics(self.PROJECT)
        page = six.next(iterator.pages)
        metrics = list(page)
        token = iterator.next_page_token

        # First check the token.
        self.assertEqual(token, TOKEN)
        # Then check the metrics returned.
        self.assertEqual(len(metrics), 1)
        metric = metrics[0]
        self.assertIsInstance(metric, Metric)
        self.assertEqual(metric.name, self.METRIC_PATH)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertIs(metric.client, client)

        project, page_size, options = gax_api._list_log_metrics_called_with
        self.assertEqual(project, self.PROJECT_PATH)
        self.assertEqual(page_size, 0)
        self.assertEqual(options.page_token, INITIAL_PAGE)

    def test_list_metrics_w_paging(self):
        from google.cloud.proto.logging.v2.logging_metrics_pb2 import LogMetric
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.logging.metric import Metric

        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        metric_pb = LogMetric(name=self.METRIC_PATH,
                              description=self.DESCRIPTION,
                              filter=self.FILTER)
        response = _GAXPageIterator([metric_pb])
        gax_api = _GAXMetricsAPI(_list_log_metrics_response=response)
        client = object()
        api = self._make_one(gax_api, client)

        iterator = api.list_metrics(
            self.PROJECT, page_size=PAGE_SIZE, page_token=TOKEN)
        metrics = list(iterator)
        token = iterator.next_page_token

        # First check the token.
        self.assertIsNone(token)
        # Then check the metrics returned.
        self.assertEqual(len(metrics), 1)
        metric = metrics[0]
        self.assertIsInstance(metric, Metric)
        self.assertEqual(metric.name, self.METRIC_PATH)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertIs(metric.client, client)

        project, page_size, options = gax_api._list_log_metrics_called_with
        self.assertEqual(project, self.PROJECT_PATH)
        self.assertEqual(page_size, PAGE_SIZE)
        self.assertEqual(options.page_token, TOKEN)

    def test_metric_create_error(self):
        from google.gax.errors import GaxError

        gax_api = _GAXMetricsAPI(_random_gax_error=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(GaxError):
            api.metric_create(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

    def test_metric_create_conflict(self):
        from google.cloud.exceptions import Conflict

        gax_api = _GAXMetricsAPI(_create_log_metric_conflict=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(Conflict):
            api.metric_create(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

    def test_metric_create_ok(self):
        from google.cloud.proto.logging.v2.logging_metrics_pb2 import LogMetric

        gax_api = _GAXMetricsAPI()
        api = self._make_one(gax_api, None)

        api.metric_create(
            self.PROJECT, self.METRIC_NAME, self.FILTER, self.DESCRIPTION)

        parent, metric, options = (
            gax_api._create_log_metric_called_with)
        self.assertEqual(parent, self.PROJECT_PATH)
        self.assertIsInstance(metric, LogMetric)
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertIsNone(options)

    def test_metric_get_error(self):
        from google.cloud.exceptions import NotFound

        gax_api = _GAXMetricsAPI()
        api = self._make_one(gax_api, None)

        with self.assertRaises(NotFound):
            api.metric_get(self.PROJECT, self.METRIC_NAME)

    def test_metric_get_miss(self):
        from google.gax.errors import GaxError

        gax_api = _GAXMetricsAPI(_random_gax_error=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(GaxError):
            api.metric_get(self.PROJECT, self.METRIC_NAME)

    def test_metric_get_hit(self):
        from google.cloud.proto.logging.v2.logging_metrics_pb2 import LogMetric

        RESPONSE = {
            'name': self.METRIC_PATH,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }
        metric_pb = LogMetric(name=self.METRIC_PATH,
                              description=self.DESCRIPTION,
                              filter=self.FILTER)
        gax_api = _GAXMetricsAPI(_get_log_metric_response=metric_pb)
        api = self._make_one(gax_api, None)

        response = api.metric_get(self.PROJECT, self.METRIC_NAME)

        self.assertEqual(response, RESPONSE)

        metric_name, options = gax_api._get_log_metric_called_with
        self.assertEqual(metric_name, self.METRIC_PATH)
        self.assertIsNone(options)

    def test_metric_update_error(self):
        from google.gax.errors import GaxError

        gax_api = _GAXMetricsAPI(_random_gax_error=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(GaxError):
            api.metric_update(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

    def test_metric_update_miss(self):
        from google.cloud.exceptions import NotFound

        gax_api = _GAXMetricsAPI()
        api = self._make_one(gax_api, None)

        with self.assertRaises(NotFound):
            api.metric_update(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

    def test_metric_update_hit(self):
        from google.cloud.proto.logging.v2.logging_metrics_pb2 import LogMetric

        response = LogMetric(name=self.METRIC_NAME,
                             description=self.DESCRIPTION,
                             filter=self.FILTER)
        gax_api = _GAXMetricsAPI(_update_log_metric_response=response)
        api = self._make_one(gax_api, None)

        api.metric_update(
            self.PROJECT, self.METRIC_NAME, self.FILTER, self.DESCRIPTION)

        metric_name, metric, options = (
            gax_api._update_log_metric_called_with)
        self.assertEqual(metric_name, self.METRIC_PATH)
        self.assertIsInstance(metric, LogMetric)
        self.assertEqual(metric.name, self.METRIC_PATH)
        self.assertEqual(metric.filter, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertIsNone(options)

    def test_metric_delete_error(self):
        from google.gax.errors import GaxError

        gax_api = _GAXMetricsAPI(_random_gax_error=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(GaxError):
            api.metric_delete(self.PROJECT, self.METRIC_NAME)

    def test_metric_delete_miss(self):
        from google.cloud.exceptions import NotFound

        gax_api = _GAXMetricsAPI(_log_metric_not_found=True)
        api = self._make_one(gax_api, None)

        with self.assertRaises(NotFound):
            api.metric_delete(self.PROJECT, self.METRIC_NAME)

    def test_metric_delete_hit(self):
        gax_api = _GAXMetricsAPI()
        api = self._make_one(gax_api, None)

        api.metric_delete(self.PROJECT, self.METRIC_NAME)

        metric_name, options = gax_api._delete_log_metric_called_with
        self.assertEqual(metric_name, self.METRIC_PATH)
        self.assertIsNone(options)


@unittest.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_make_gax_logging_api(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.logging._gax import make_gax_logging_api

        return make_gax_logging_api(client)

    def test_it(self):
        from google.cloud.logging import __version__
        from google.cloud.logging._gax import _LoggingAPI
        from google.cloud.logging._gax import DEFAULT_USER_AGENT

        creds = object()
        client = mock.Mock(_credentials=creds, spec=['_credentials'])
        channels = []
        channel_args = []
        generated_api_kwargs = []
        channel_obj = object()
        generated = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def generated_api(channel=None, **kwargs):
            channels.append(channel)
            generated_api_kwargs.append(kwargs)
            return generated

        host = 'foo.apis.invalid'
        generated_api.SERVICE_ADDRESS = host

        patch = mock.patch.multiple(
            'google.cloud.logging._gax',
            LoggingServiceV2Client=generated_api,
            make_secure_channel=make_channel)
        with patch:
            logging_api = self._call_fut(client)

        self.assertEqual(channels, [channel_obj])
        self.assertEqual(channel_args,
                         [(creds, DEFAULT_USER_AGENT, host)])

        self.assertEqual(len(generated_api_kwargs), 1)
        self.assertEqual(generated_api_kwargs[0]['lib_name'], 'gccl')
        self.assertEqual(generated_api_kwargs[0]['lib_version'], __version__)

        self.assertIsInstance(logging_api, _LoggingAPI)
        self.assertIs(logging_api._gax_api, generated)
        self.assertIs(logging_api._client, client)


@unittest.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_make_gax_metrics_api(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.logging._gax import make_gax_metrics_api

        return make_gax_metrics_api(client)

    def test_it(self):
        from google.cloud.logging import __version__
        from google.cloud.logging._gax import _MetricsAPI
        from google.cloud.logging._gax import DEFAULT_USER_AGENT

        creds = object()
        client = mock.Mock(_credentials=creds, spec=['_credentials'])
        channels = []
        channel_args = []
        generated_api_kwargs = []
        channel_obj = object()
        generated = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def generated_api(channel=None, **kwargs):
            channels.append(channel)
            generated_api_kwargs.append(kwargs)
            return generated

        host = 'foo.apis.invalid'
        generated_api.SERVICE_ADDRESS = host

        patch = mock.patch.multiple(
            'google.cloud.logging._gax',
            MetricsServiceV2Client=generated_api,
            make_secure_channel=make_channel)
        with patch:
            metrics_api = self._call_fut(client)

        self.assertEqual(channels, [channel_obj])
        self.assertEqual(channel_args,
                         [(creds, DEFAULT_USER_AGENT, host)])

        self.assertEqual(len(generated_api_kwargs), 1)
        self.assertEqual(generated_api_kwargs[0]['lib_name'], 'gccl')
        self.assertEqual(generated_api_kwargs[0]['lib_version'], __version__)

        self.assertIsInstance(metrics_api, _MetricsAPI)
        self.assertIs(metrics_api._gax_api, generated)
        self.assertIs(metrics_api._client, client)


@unittest.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_make_gax_sinks_api(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.logging._gax import make_gax_sinks_api

        return make_gax_sinks_api(client)

    def test_it(self):
        from google.cloud.logging import __version__
        from google.cloud.logging._gax import _SinksAPI
        from google.cloud.logging._gax import DEFAULT_USER_AGENT

        creds = object()
        client = mock.Mock(_credentials=creds, spec=['_credentials'])
        channels = []
        channel_args = []
        generated_api_kwargs = []
        channel_obj = object()
        generated = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def generated_api(channel=None, **kwargs):
            channels.append(channel)
            generated_api_kwargs.append(kwargs)
            return generated

        host = 'foo.apis.invalid'
        generated_api.SERVICE_ADDRESS = host

        patch = mock.patch.multiple(
            'google.cloud.logging._gax',
            ConfigServiceV2Client=generated_api,
            make_secure_channel=make_channel)
        with patch:
            sinks_api = self._call_fut(client)

        self.assertEqual(channels, [channel_obj])
        self.assertEqual(channel_args,
                         [(creds, DEFAULT_USER_AGENT, host)])

        self.assertEqual(len(generated_api_kwargs), 1)
        self.assertEqual(generated_api_kwargs[0]['lib_name'], 'gccl')
        self.assertEqual(generated_api_kwargs[0]['lib_version'], __version__)

        self.assertIsInstance(sinks_api, _SinksAPI)
        self.assertIs(sinks_api._gax_api, generated)
        self.assertIs(sinks_api._client, client)


class _GAXLoggingAPI(_GAXBaseAPI):

    _delete_not_found = False

    def list_log_entries(
            self, resource_names, project_ids, filter_,
            order_by, page_size, options):
        self._list_log_entries_called_with = (
            resource_names, project_ids, filter_,
            order_by, page_size, options)
        return self._list_log_entries_response

    def write_log_entries(self, entries, log_name, resource, labels,
                          partial_success, options):
        self._write_log_entries_called_with = (
            entries, log_name, resource, labels, partial_success, options)

    def delete_log(self, log_name, options):
        from google.gax.errors import GaxError

        self._delete_log_called_with = log_name, options
        if self._random_gax_error:
            raise GaxError('error')
        if self._delete_not_found:
            raise GaxError('notfound', self._make_grpc_not_found())


class _GAXSinksAPI(_GAXBaseAPI):

    _create_sink_conflict = False
    _sink_not_found = False

    def list_sinks(self, parent, page_size, options):
        self._list_sinks_called_with = parent, page_size, options
        return self._list_sinks_response

    def create_sink(self, parent, sink, options):
        from google.gax.errors import GaxError

        self._create_sink_called_with = parent, sink, options
        if self._random_gax_error:
            raise GaxError('error')
        if self._create_sink_conflict:
            raise GaxError('conflict', self._make_grpc_failed_precondition())

    def get_sink(self, sink_name, options):
        from google.gax.errors import GaxError

        self._get_sink_called_with = sink_name, options
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._get_sink_response
        except AttributeError:
            raise GaxError('notfound', self._make_grpc_not_found())

    def update_sink(self, sink_name, sink, options=None):
        from google.gax.errors import GaxError

        self._update_sink_called_with = sink_name, sink, options
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._update_sink_response
        except AttributeError:
            raise GaxError('notfound', self._make_grpc_not_found())

    def delete_sink(self, sink_name, options=None):
        from google.gax.errors import GaxError

        self._delete_sink_called_with = sink_name, options
        if self._random_gax_error:
            raise GaxError('error')
        if self._sink_not_found:
            raise GaxError('notfound', self._make_grpc_not_found())


class _GAXMetricsAPI(_GAXBaseAPI):

    _create_log_metric_conflict = False
    _log_metric_not_found = False

    def list_log_metrics(self, parent, page_size, options):
        self._list_log_metrics_called_with = parent, page_size, options
        return self._list_log_metrics_response

    def create_log_metric(self, parent, metric, options):
        from google.gax.errors import GaxError

        self._create_log_metric_called_with = parent, metric, options
        if self._random_gax_error:
            raise GaxError('error')
        if self._create_log_metric_conflict:
            raise GaxError('conflict', self._make_grpc_failed_precondition())

    def get_log_metric(self, metric_name, options):
        from google.gax.errors import GaxError

        self._get_log_metric_called_with = metric_name, options
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._get_log_metric_response
        except AttributeError:
            raise GaxError('notfound', self._make_grpc_not_found())

    def update_log_metric(self, metric_name, metric, options=None):
        from google.gax.errors import GaxError

        self._update_log_metric_called_with = metric_name, metric, options
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._update_log_metric_response
        except AttributeError:
            raise GaxError('notfound', self._make_grpc_not_found())

    def delete_log_metric(self, metric_name, options=None):
        from google.gax.errors import GaxError

        self._delete_log_metric_called_with = metric_name, options
        if self._random_gax_error:
            raise GaxError('error')
        if self._log_metric_not_found:
            raise GaxError('notfound', self._make_grpc_not_found())
