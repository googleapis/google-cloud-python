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
    FILTER = 'logName:syslog AND severity>=ERROR'

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


@unittest2.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_LoggingAPI(_Base, unittest2.TestCase):
    LOG_NAME = 'log_name'

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
        self.assertEqual(entry['logName'], self.LOG_NAME)
        self.assertEqual(entry['resource'], {'type': 'global'})
        self.assertEqual(entry['textPayload'], TEXT)
        self.assertEqual(next_token, TOKEN)

        projects, filter_, order_by, page_size, options = (
            gax_api._list_log_entries_called_with)
        self.assertEqual(projects, [self.PROJECT])
        self.assertEqual(filter_, self.FILTER)
        self.assertEqual(order_by, DESCENDING)
        self.assertEqual(page_size, 0)
        self.assertTrue(options.page_token is INITIAL_PAGE)

    def test_list_entries_with_paging(self):
        from google.protobuf.struct_pb2 import Value
        from gcloud._testing import _GAXPageIterator
        SIZE = 23
        TOKEN = 'TOKEN'
        NEW_TOKEN = 'NEW_TOKEN'
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'sunny'}
        struct_pb = _StructPB(dict([(key, Value(string_value=value))
                                    for key, value in PAYLOAD.items()]))
        response = _GAXPageIterator(
            [_LogEntryPB(self.LOG_NAME, json_payload=struct_pb)], NEW_TOKEN)
        gax_api = _GAXLoggingAPI(_list_log_entries_response=response)
        api = self._makeOne(gax_api)

        entries, next_token = api.list_entries(
            [self.PROJECT], page_size=SIZE, page_token=TOKEN)

        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertIsInstance(entry, dict)
        self.assertEqual(entry['logName'], self.LOG_NAME)
        self.assertEqual(entry['resource'], {'type': 'global'})
        self.assertEqual(entry['jsonPayload'], PAYLOAD)
        self.assertEqual(next_token, NEW_TOKEN)

        projects, filter_, order_by, page_size, options = (
            gax_api._list_log_entries_called_with)
        self.assertEqual(projects, [self.PROJECT])
        self.assertEqual(filter_, '')
        self.assertEqual(order_by, '')
        self.assertEqual(page_size, SIZE)
        self.assertEqual(options.page_token, TOKEN)

    def test_list_entries_with_extra_properties(self):
        from datetime import datetime
        from google.logging.type.log_severity_pb2 import WARNING
        from gcloud._testing import _GAXPageIterator
        from gcloud._helpers import UTC
        from gcloud._helpers import _datetime_to_rfc3339
        from gcloud._helpers import _datetime_to_pb_timestamp
        NOW = datetime.utcnow().replace(tzinfo=UTC)
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
            'severity': WARNING,
            'labels': LABELS,
            'insert_id': IID,
            'http_request': request,
            'operation': operation,
        }
        ENTRY = _LogEntryPB(self.LOG_NAME, proto_payload=PAYLOAD, **EXTRAS)
        ENTRY.resource.labels['foo'] = 'bar'
        ENTRY.timestamp = _datetime_to_pb_timestamp(NOW)
        response = _GAXPageIterator([ENTRY], NEW_TOKEN)
        gax_api = _GAXLoggingAPI(_list_log_entries_response=response)
        api = self._makeOne(gax_api)

        entries, next_token = api.list_entries(
            [self.PROJECT], page_size=SIZE, page_token=TOKEN)

        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertIsInstance(entry, dict)
        self.assertEqual(entry['logName'], self.LOG_NAME)
        self.assertEqual(entry['resource'],
                         {'type': 'global', 'labels': {'foo': 'bar'}})
        self.assertEqual(entry['protoPayload'], PAYLOAD)
        self.assertEqual(entry['severity'], SEVERITY)
        self.assertEqual(entry['labels'], LABELS)
        self.assertEqual(entry['insertId'], IID)
        self.assertEqual(entry['timestamp'], _datetime_to_rfc3339(NOW))
        EXPECTED_REQUEST = {
            'requestMethod': request.request_method,
            'requestUrl': request.request_url,
            'status': request.status,
            'requestSize': request.request_size,
            'responseSize': request.response_size,
            'referer': request.referer,
            'userAgent': request.user_agent,
            'remoteIp': request.remote_ip,
            'cacheHit': request.cache_hit,
        }
        self.assertEqual(entry['httpRequest'], EXPECTED_REQUEST)
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
            'logName': LOG_PATH,
            'resource': {'type': 'global'},
            'textPayload': TEXT,
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
            'logName': LOG_PATH,
            'resource': {'type': 'global'},
            'textPayload': TEXT,
            'severity': SEVERITY,
            'labels': LABELS,
            'insertId': IID,
            'timestamp': NOW,
            'httpRequest': REQUEST,
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
        import datetime
        from google.logging.type.log_severity_pb2 import WARNING
        from google.logging.v2.log_entry_pb2 import LogEntry
        from google.protobuf.any_pb2 import Any
        from google.protobuf.struct_pb2 import Struct
        from gcloud._helpers import _datetime_to_rfc3339, UTC
        TEXT = 'TEXT'
        NOW = datetime.datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP_TYPE_URL = 'type.googleapis.com/google.protobuf.Timestamp'
        JSON = {'payload': 'PAYLOAD', 'type': 'json'}
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
            {'jsonPayload': JSON,
             'operation': {'producer': PRODUCER, 'id': OPID}},
            {'protoPayload': PROTO,
             'httpRequest': {'requestUrl': URL}},
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


@unittest2.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_SinksAPI(_Base, unittest2.TestCase):
    SINK_NAME = 'sink_name'
    SINK_PATH = 'projects/%s/sinks/%s' % (_Base.PROJECT, SINK_NAME)
    DESTINATION_URI = 'faux.googleapis.com/destination'

    def _getTargetClass(self):
        from gcloud.logging._gax import _SinksAPI
        return _SinksAPI

    def test_ctor(self):
        gax_api = _GAXSinksAPI()
        api = self._makeOne(gax_api)
        self.assertTrue(api._gax_api is gax_api)

    def test_list_sinks_no_paging(self):
        from google.gax import INITIAL_PAGE
        from gcloud._testing import _GAXPageIterator
        TOKEN = 'TOKEN'
        SINKS = [{
            'name': self.SINK_PATH,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }]
        response = _GAXPageIterator(
            [_LogSinkPB(self.SINK_PATH, self.DESTINATION_URI, self.FILTER)],
            TOKEN)
        gax_api = _GAXSinksAPI(_list_sinks_response=response)
        api = self._makeOne(gax_api)

        sinks, token = api.list_sinks(self.PROJECT)

        self.assertEqual(sinks, SINKS)
        self.assertEqual(token, TOKEN)

        project, page_size, options = gax_api._list_sinks_called_with
        self.assertEqual(project, self.PROJECT_PATH)
        self.assertEqual(page_size, 0)
        self.assertEqual(options.page_token, INITIAL_PAGE)

    def test_list_sinks_w_paging(self):
        from gcloud._testing import _GAXPageIterator
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        SINKS = [{
            'name': self.SINK_PATH,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }]
        response = _GAXPageIterator(
            [_LogSinkPB(self.SINK_PATH, self.DESTINATION_URI, self.FILTER)],
            None)
        gax_api = _GAXSinksAPI(_list_sinks_response=response)
        api = self._makeOne(gax_api)

        sinks, token = api.list_sinks(
            self.PROJECT, page_size=PAGE_SIZE, page_token=TOKEN)

        self.assertEqual(sinks, SINKS)
        self.assertEqual(token, None)

        project, page_size, options = gax_api._list_sinks_called_with
        self.assertEqual(project, self.PROJECT_PATH)
        self.assertEqual(page_size, PAGE_SIZE)
        self.assertEqual(options.page_token, TOKEN)

    def test_sink_create_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXSinksAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.sink_create(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

    def test_sink_create_conflict(self):
        from gcloud.exceptions import Conflict
        gax_api = _GAXSinksAPI(_create_sink_conflict=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(Conflict):
            api.sink_create(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

    def test_sink_create_ok(self):
        from google.logging.v2.logging_config_pb2 import LogSink
        gax_api = _GAXSinksAPI()
        api = self._makeOne(gax_api)

        api.sink_create(
            self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI)

        parent, sink, options = (
            gax_api._create_sink_called_with)
        self.assertEqual(parent, self.PROJECT_PATH)
        self.assertTrue(isinstance(sink, LogSink))
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertEqual(options, None)

    def test_sink_get_error(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXSinksAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.sink_get(self.PROJECT, self.SINK_NAME)

    def test_sink_get_miss(self):
        from google.gax.errors import GaxError
        gax_api = _GAXSinksAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.sink_get(self.PROJECT, self.SINK_NAME)

    def test_sink_get_hit(self):
        RESPONSE = {
            'name': self.SINK_PATH,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        sink_pb = _LogSinkPB(
            self.SINK_PATH, self.DESTINATION_URI, self.FILTER)
        gax_api = _GAXSinksAPI(_get_sink_response=sink_pb)
        api = self._makeOne(gax_api)

        response = api.sink_get(self.PROJECT, self.SINK_NAME)

        self.assertEqual(response, RESPONSE)

        sink_name, options = gax_api._get_sink_called_with
        self.assertEqual(sink_name, self.SINK_PATH)
        self.assertEqual(options, None)

    def test_sink_update_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXSinksAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.sink_update(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

    def test_sink_update_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXSinksAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.sink_update(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

    def test_sink_update_hit(self):
        from google.logging.v2.logging_config_pb2 import LogSink
        response = _LogSinkPB(
            self.SINK_NAME, self.FILTER, self.DESTINATION_URI)
        gax_api = _GAXSinksAPI(_update_sink_response=response)
        api = self._makeOne(gax_api)

        api.sink_update(
            self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI)

        sink_name, sink, options = (
            gax_api._update_sink_called_with)
        self.assertEqual(sink_name, self.SINK_PATH)
        self.assertTrue(isinstance(sink, LogSink))
        self.assertEqual(sink.name, self.SINK_PATH)
        self.assertEqual(sink.filter, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertEqual(options, None)

    def test_sink_delete_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXSinksAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.sink_delete(self.PROJECT, self.SINK_NAME)

    def test_sink_delete_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXSinksAPI(_sink_not_found=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.sink_delete(self.PROJECT, self.SINK_NAME)

    def test_sink_delete_hit(self):
        gax_api = _GAXSinksAPI()
        api = self._makeOne(gax_api)

        api.sink_delete(self.PROJECT, self.SINK_NAME)

        sink_name, options = gax_api._delete_sink_called_with
        self.assertEqual(sink_name, self.SINK_PATH)
        self.assertEqual(options, None)


@unittest2.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_MetricsAPI(_Base, unittest2.TestCase):
    METRIC_NAME = 'metric_name'
    METRIC_PATH = 'projects/%s/metrics/%s' % (_Base.PROJECT, METRIC_NAME)
    DESCRIPTION = 'Description'

    def _getTargetClass(self):
        from gcloud.logging._gax import _MetricsAPI
        return _MetricsAPI

    def test_ctor(self):
        gax_api = _GAXMetricsAPI()
        api = self._makeOne(gax_api)
        self.assertTrue(api._gax_api is gax_api)

    def test_list_metrics_no_paging(self):
        from google.gax import INITIAL_PAGE
        from gcloud._testing import _GAXPageIterator
        TOKEN = 'TOKEN'
        METRICS = [{
            'name': self.METRIC_PATH,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }]
        response = _GAXPageIterator(
            [_LogMetricPB(self.METRIC_PATH, self.DESCRIPTION, self.FILTER)],
            TOKEN)
        gax_api = _GAXMetricsAPI(_list_log_metrics_response=response)
        api = self._makeOne(gax_api)

        metrics, token = api.list_metrics(self.PROJECT)

        self.assertEqual(metrics, METRICS)
        self.assertEqual(token, TOKEN)

        project, page_size, options = gax_api._list_log_metrics_called_with
        self.assertEqual(project, self.PROJECT_PATH)
        self.assertEqual(page_size, 0)
        self.assertEqual(options.page_token, INITIAL_PAGE)

    def test_list_metrics_w_paging(self):
        from gcloud._testing import _GAXPageIterator
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        METRICS = [{
            'name': self.METRIC_PATH,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }]
        response = _GAXPageIterator(
            [_LogMetricPB(self.METRIC_PATH, self.DESCRIPTION, self.FILTER)],
            None)
        gax_api = _GAXMetricsAPI(_list_log_metrics_response=response)
        api = self._makeOne(gax_api)

        metrics, token = api.list_metrics(
            self.PROJECT, page_size=PAGE_SIZE, page_token=TOKEN)

        self.assertEqual(metrics, METRICS)
        self.assertEqual(token, None)

        project, page_size, options = gax_api._list_log_metrics_called_with
        self.assertEqual(project, self.PROJECT_PATH)
        self.assertEqual(page_size, PAGE_SIZE)
        self.assertEqual(options.page_token, TOKEN)

    def test_metric_create_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXMetricsAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.metric_create(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

    def test_metric_create_conflict(self):
        from gcloud.exceptions import Conflict
        gax_api = _GAXMetricsAPI(_create_log_metric_conflict=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(Conflict):
            api.metric_create(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

    def test_metric_create_ok(self):
        from google.logging.v2.logging_metrics_pb2 import LogMetric
        gax_api = _GAXMetricsAPI()
        api = self._makeOne(gax_api)

        api.metric_create(
            self.PROJECT, self.METRIC_NAME, self.FILTER, self.DESCRIPTION)

        parent, metric, options = (
            gax_api._create_log_metric_called_with)
        self.assertEqual(parent, self.PROJECT_PATH)
        self.assertTrue(isinstance(metric, LogMetric))
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertEqual(options, None)

    def test_metric_get_error(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXMetricsAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.metric_get(self.PROJECT, self.METRIC_NAME)

    def test_metric_get_miss(self):
        from google.gax.errors import GaxError
        gax_api = _GAXMetricsAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.metric_get(self.PROJECT, self.METRIC_NAME)

    def test_metric_get_hit(self):
        RESPONSE = {
            'name': self.METRIC_PATH,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }
        metric_pb = _LogMetricPB(
            self.METRIC_PATH, self.DESCRIPTION, self.FILTER)
        gax_api = _GAXMetricsAPI(_get_log_metric_response=metric_pb)
        api = self._makeOne(gax_api)

        response = api.metric_get(self.PROJECT, self.METRIC_NAME)

        self.assertEqual(response, RESPONSE)

        metric_name, options = gax_api._get_log_metric_called_with
        self.assertEqual(metric_name, self.METRIC_PATH)
        self.assertEqual(options, None)

    def test_metric_update_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXMetricsAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.metric_update(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

    def test_metric_update_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXMetricsAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.metric_update(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

    def test_metric_update_hit(self):
        from google.logging.v2.logging_metrics_pb2 import LogMetric
        response = _LogMetricPB(
            self.METRIC_NAME, self.FILTER, self.DESCRIPTION)
        gax_api = _GAXMetricsAPI(_update_log_metric_response=response)
        api = self._makeOne(gax_api)

        api.metric_update(
            self.PROJECT, self.METRIC_NAME, self.FILTER, self.DESCRIPTION)

        metric_name, metric, options = (
            gax_api._update_log_metric_called_with)
        self.assertEqual(metric_name, self.METRIC_PATH)
        self.assertTrue(isinstance(metric, LogMetric))
        self.assertEqual(metric.name, self.METRIC_PATH)
        self.assertEqual(metric.filter, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertEqual(options, None)

    def test_metric_delete_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXMetricsAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.metric_delete(self.PROJECT, self.METRIC_NAME)

    def test_metric_delete_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXMetricsAPI(_log_metric_not_found=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.metric_delete(self.PROJECT, self.METRIC_NAME)

    def test_metric_delete_hit(self):
        gax_api = _GAXMetricsAPI()
        api = self._makeOne(gax_api)

        api.metric_delete(self.PROJECT, self.METRIC_NAME)

        metric_name, options = gax_api._delete_log_metric_called_with
        self.assertEqual(metric_name, self.METRIC_PATH)
        self.assertEqual(options, None)


@unittest2.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_value_pb_to_value(_Base, unittest2.TestCase):

    def _callFUT(self, value_pb):
        from gcloud.logging._gax import _value_pb_to_value
        return _value_pb_to_value(value_pb)

    def test_w_null_values(self):
        from google.protobuf.struct_pb2 import Value
        value_pb = Value()
        self.assertEqual(self._callFUT(value_pb), None)
        value_pb = Value(null_value=None)
        self.assertEqual(self._callFUT(value_pb), None)

    def test_w_string_value(self):
        from google.protobuf.struct_pb2 import Value
        STRING = 'STRING'
        value_pb = Value(string_value=STRING)
        self.assertEqual(self._callFUT(value_pb), STRING)

    def test_w_bool_values(self):
        from google.protobuf.struct_pb2 import Value
        true_value_pb = Value(bool_value=True)
        self.assertTrue(self._callFUT(true_value_pb) is True)
        false_value_pb = Value(bool_value=False)
        self.assertTrue(self._callFUT(false_value_pb) is False)

    def test_w_number_values(self):
        from google.protobuf.struct_pb2 import Value
        ANSWER = 42
        PI = 3.1415926
        int_value_pb = Value(number_value=ANSWER)
        self.assertEqual(self._callFUT(int_value_pb), ANSWER)
        float_value_pb = Value(number_value=PI)
        self.assertEqual(self._callFUT(float_value_pb), PI)

    def test_w_list_value(self):
        from google.protobuf.struct_pb2 import Value
        STRING = 'STRING'
        PI = 3.1415926
        value_pb = Value()
        value_pb.list_value.values.add(string_value=STRING)
        value_pb.list_value.values.add(bool_value=True)
        value_pb.list_value.values.add(number_value=PI)
        self.assertEqual(self._callFUT(value_pb), [STRING, True, PI])

    def test_w_struct_value(self):
        from google.protobuf.struct_pb2 import Value
        STRING = 'STRING'
        PI = 3.1415926
        value_pb = Value()
        value_pb.struct_value.fields['string'].string_value = STRING
        value_pb.struct_value.fields['bool'].bool_value = True
        value_pb.struct_value.fields['number'].number_value = PI
        self.assertEqual(self._callFUT(value_pb),
                         {'string': STRING, 'bool': True, 'number': PI})

    def test_w_unknown_kind(self):

        class _Value(object):

            def WhichOneof(self, name):
                assert name == 'kind'
                return 'UNKNOWN'

        with self.assertRaises(ValueError):
            self._callFUT(_Value())


class _GAXBaseAPI(object):

    _random_gax_error = False

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def _make_grpc_error(self, status_code):
        from grpc.framework.interfaces.face.face import AbortionError

        class _DummyException(AbortionError):
            code = status_code

            def __init__(self):
                super(_DummyException, self).__init__(
                    None, None, self.code, None)

        return _DummyException()

    def _make_grpc_not_found(self):
        from grpc.beta.interfaces import StatusCode
        return self._make_grpc_error(StatusCode.NOT_FOUND)

    def _make_grpc_failed_precondition(self):
        from grpc.beta.interfaces import StatusCode
        return self._make_grpc_error(StatusCode.FAILED_PRECONDITION)


class _GAXLoggingAPI(_GAXBaseAPI):

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


class _HTTPRequestPB(object):

    request_url = 'http://example.com/requested'
    request_method = 'GET'
    status = 200
    referer = 'http://example.com/referer'
    user_agent = 'AGENT'
    cache_hit = False
    request_size = 256
    response_size = 1024
    remote_ip = '1.2.3.4'


class _LogEntryOperationPB(object):

    producer = 'PRODUCER'
    first = last = False
    id = 'OPID'


class _ResourcePB(object):

    def __init__(self, type_='global', **labels):
        self.type = type_
        self.labels = labels


class _StructPB(object):

    def __init__(self, fields):
        self.fields = fields


class _LogEntryPB(object):

    severity = 0
    http_request = operation = insert_id = None
    text_payload = json_payload = proto_payload = None

    def __init__(self, log_name, **kw):
        self.log_name = log_name
        self.resource = _ResourcePB()
        self.timestamp = self._make_timestamp()
        self.labels = kw.pop('labels', {})
        self.__dict__.update(kw)

    def HasField(self, field_name):
        return getattr(self, field_name, None) is not None

    @staticmethod
    def _make_timestamp():
        from datetime import datetime
        from gcloud._helpers import UTC
        from gcloud._helpers import _datetime_to_pb_timestamp
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        return _datetime_to_pb_timestamp(NOW)


class _LogSinkPB(object):

    def __init__(self, name, destination, filter_):
        self.name = name
        self.destination = destination
        self.filter = filter_


class _LogMetricPB(object):

    def __init__(self, name, description, filter_):
        self.name = name
        self.description = description
        self.filter = filter_
