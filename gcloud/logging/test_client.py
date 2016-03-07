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


class TestClient(unittest2.TestCase):

    PROJECT = 'PROJECT'
    LOGGER_NAME = 'LOGGER_NAME'
    SINK_NAME = 'SINK_NAME'
    FILTER = 'logName:syslog AND severity>=ERROR'
    DESTINATION_URI = 'faux.googleapis.com/destination'
    METRIC_NAME = 'metric_name'
    FILTER = 'logName:syslog AND severity>=ERROR'
    DESCRIPTION = 'DESCRIPTION'

    def _getTargetClass(self):
        from gcloud.logging.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)
        self.assertEqual(client.project, self.PROJECT)

    def test_logger(self):
        from gcloud.logging.logger import Logger
        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)
        logger = client.logger(self.LOGGER_NAME)
        self.assertTrue(isinstance(logger, Logger))
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)

    def test__entry_from_resource_unknown_type(self):
        PROJECT = 'PROJECT'
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        loggers = {}
        with self.assertRaises(ValueError):
            client._entry_from_resource({'unknownPayload': {}}, loggers)

    def test_list_entries_defaults(self):
        from datetime import datetime
        from gcloud._helpers import UTC
        from gcloud.logging.entries import TextEntry
        from gcloud.logging.test_entries import _datetime_to_rfc3339_w_nanos
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP = _datetime_to_rfc3339_w_nanos(NOW)
        IID1 = 'IID1'
        TEXT = 'TEXT'
        SENT = {
            'projectIds': [self.PROJECT],
        }
        TOKEN = 'TOKEN'
        RETURNED = {
            'entries': [{
                'textPayload': TEXT,
                'insertId': IID1,
                'resource': {
                    'type': 'global',
                },
                'timestamp': TIMESTAMP,
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
            }],
            'nextPageToken': TOKEN,
        }
        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)
        conn = client.connection = _Connection(RETURNED)
        entries, token = client.list_entries()
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertTrue(isinstance(entry, TextEntry))
        self.assertEqual(entry.insert_id, IID1)
        self.assertEqual(entry.payload, TEXT)
        self.assertEqual(entry.timestamp, NOW)
        logger = entry.logger
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)
        self.assertEqual(token, TOKEN)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:list')
        self.assertEqual(req['data'], SENT)

    def test_list_entries_explicit(self):
        # pylint: disable=too-many-statements
        from datetime import datetime
        from gcloud._helpers import UTC
        from gcloud.logging import DESCENDING
        from gcloud.logging.entries import ProtobufEntry
        from gcloud.logging.entries import StructEntry
        from gcloud.logging.logger import Logger
        from gcloud.logging.test_entries import _datetime_to_rfc3339_w_nanos
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        FILTER = 'logName:LOGNAME'
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP = _datetime_to_rfc3339_w_nanos(NOW)
        IID1 = 'IID1'
        IID2 = 'IID2'
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'partly cloudy'}
        PROTO_PAYLOAD = PAYLOAD.copy()
        PROTO_PAYLOAD['@type'] = 'type.googleapis.com/testing.example'
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        SENT = {
            'projectIds': [PROJECT1, PROJECT2],
            'filter': FILTER,
            'orderBy': DESCENDING,
            'pageSize': PAGE_SIZE,
            'pageToken': TOKEN,
        }
        RETURNED = {
            'entries': [{
                'jsonPayload': PAYLOAD,
                'insertId': IID1,
                'resource': {
                    'type': 'global',
                },
                'timestamp': TIMESTAMP,
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
            }, {
                'protoPayload': PROTO_PAYLOAD,
                'insertId': IID2,
                'resource': {
                    'type': 'global',
                },
                'timestamp': TIMESTAMP,
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
            }],
        }
        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)
        conn = client.connection = _Connection(RETURNED)
        entries, token = client.list_entries(
            projects=[PROJECT1, PROJECT2], filter_=FILTER, order_by=DESCENDING,
            page_size=PAGE_SIZE, page_token=TOKEN)
        self.assertEqual(len(entries), 2)

        entry = entries[0]
        self.assertTrue(isinstance(entry, StructEntry))
        self.assertEqual(entry.insert_id, IID1)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertEqual(entry.timestamp, NOW)
        logger = entry.logger
        self.assertTrue(isinstance(logger, Logger))
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)

        entry = entries[1]
        self.assertTrue(isinstance(entry, ProtobufEntry))
        self.assertEqual(entry.insert_id, IID2)
        self.assertEqual(entry.payload, PROTO_PAYLOAD)
        self.assertEqual(entry.timestamp, NOW)
        logger = entry.logger
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)

        self.assertTrue(entries[0].logger is entries[1].logger)

        self.assertEqual(token, None)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:list')
        self.assertEqual(req['data'], SENT)

    def test_sink(self):
        from gcloud.logging.sink import Sink
        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)
        sink = client.sink(self.SINK_NAME, self.FILTER, self.DESTINATION_URI)
        self.assertTrue(isinstance(sink, Sink))
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter_, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertTrue(sink.client is client)
        self.assertEqual(sink.project, self.PROJECT)

    def test_list_sinks_no_paging(self):
        from gcloud.logging.sink import Sink
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        SINK_NAME = 'sink_name'
        FILTER = 'logName:syslog AND severity>=ERROR'
        SINK_PATH = 'projects/%s/sinks/%s' % (PROJECT, SINK_NAME)

        RETURNED = {
            'sinks': [{
                'name': SINK_PATH,
                'filter': FILTER,
                'destination': self.DESTINATION_URI,
            }],
        }
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        sinks, next_page_token = CLIENT_OBJ.list_sinks()
        # Test values are correct.
        self.assertEqual(len(sinks), 1)
        sink = sinks[0]
        self.assertTrue(isinstance(sink, Sink))
        self.assertEqual(sink.name, SINK_NAME)
        self.assertEqual(sink.filter_, FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/sinks' % (PROJECT,))
        self.assertEqual(req['query_params'], {})

    def test_list_sinks_with_paging(self):
        from gcloud.logging.sink import Sink
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        SINK_NAME = 'sink_name'
        FILTER = 'logName:syslog AND severity>=ERROR'
        SINK_PATH = 'projects/%s/sinks/%s' % (PROJECT, SINK_NAME)
        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        RETURNED = {
            'sinks': [{
                'name': SINK_PATH,
                'filter': FILTER,
                'destination': self.DESTINATION_URI,
            }],
            'nextPageToken': TOKEN2,
        }
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        sinks, next_page_token = CLIENT_OBJ.list_sinks(SIZE, TOKEN1)
        # Test values are correct.
        self.assertEqual(len(sinks), 1)
        sink = sinks[0]
        self.assertTrue(isinstance(sink, Sink))
        self.assertEqual(sink.name, SINK_NAME)
        self.assertEqual(sink.filter_, FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertEqual(next_page_token, TOKEN2)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/sinks' % (PROJECT,))
        self.assertEqual(req['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN1})

    def test_list_sinks_missing_key(self):
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        RETURNED = {}
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        sinks, next_page_token = CLIENT_OBJ.list_sinks()
        # Test values are correct.
        self.assertEqual(len(sinks), 0)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/sinks' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_metric(self):
        from gcloud.logging.metric import Metric
        creds = _Credentials()

        client_obj = self._makeOne(project=self.PROJECT, credentials=creds)
        metric = client_obj.metric(self.METRIC_NAME, self.FILTER,
                                   description=self.DESCRIPTION)
        self.assertTrue(isinstance(metric, Metric))
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertTrue(metric.client is client_obj)
        self.assertEqual(metric.project, self.PROJECT)

    def test_list_metrics_no_paging(self):
        from gcloud.logging.metric import Metric
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        RETURNED = {
            'metrics': [{
                'name': self.METRIC_NAME,
                'filter': self.FILTER,
                'description': self.DESCRIPTION,
            }],
        }
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        metrics, next_page_token = CLIENT_OBJ.list_metrics()
        # Test values are correct.
        self.assertEqual(len(metrics), 1)
        metric = metrics[0]
        self.assertTrue(isinstance(metric, Metric))
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/metrics' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_list_metrics_with_paging(self):
        from gcloud.logging.metric import Metric
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        RETURNED = {
            'metrics': [{
                'name': self.METRIC_NAME,
                'filter': self.FILTER,
                'description': self.DESCRIPTION,
            }],
            'nextPageToken': TOKEN2,
        }
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        metrics, next_page_token = CLIENT_OBJ.list_metrics(SIZE, TOKEN1)
        # Test values are correct.
        self.assertEqual(len(metrics), 1)
        metric = metrics[0]
        self.assertTrue(isinstance(metric, Metric))
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertEqual(next_page_token, TOKEN2)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['path'], '/projects/%s/metrics' % PROJECT)
        self.assertEqual(req['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN1})

    def test_list_metrics_missing_key(self):
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        RETURNED = {}
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        metrics, next_page_token = CLIENT_OBJ.list_metrics()
        # Test values are correct.
        self.assertEqual(len(metrics), 0)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/metrics' % PROJECT)
        self.assertEqual(req['query_params'], {})


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
