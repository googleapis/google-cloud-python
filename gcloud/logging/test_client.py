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

    def test_logging_api_wo_gax(self):
        from gcloud.logging.connection import _LoggingAPI
        from gcloud.logging import client as MUT
        from gcloud._testing import _Monkey
        client = self._makeOne(self.PROJECT, credentials=_Credentials())
        conn = client.connection = object()

        with _Monkey(MUT, _USE_GAX=False):
            api = client.logging_api

        self.assertTrue(isinstance(api, _LoggingAPI))
        self.assertTrue(api._connection is conn)
        # API instance is cached
        again = client.logging_api
        self.assertTrue(again is api)

    def test_logging_api_w_gax(self):
        from gcloud.logging import client as MUT
        from gcloud._testing import _Monkey

        wrapped = object()
        _called_with = []

        def _generated_api(*args, **kw):
            _called_with.append((args, kw))
            return wrapped

        class _GaxLoggingAPI(object):

            def __init__(self, _wrapped):
                self._wrapped = _wrapped

        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)

        with _Monkey(MUT,
                     _USE_GAX=True,
                     GeneratedLoggingAPI=_generated_api,
                     GAXLoggingAPI=_GaxLoggingAPI):
            api = client.logging_api

        self.assertIsInstance(api, _GaxLoggingAPI)
        self.assertTrue(api._wrapped is wrapped)
        # API instance is cached
        again = client.logging_api
        self.assertTrue(again is api)

    def test_sinks_api_wo_gax(self):
        from gcloud.logging.connection import _SinksAPI
        from gcloud.logging import client as MUT
        from gcloud._testing import _Monkey
        client = self._makeOne(self.PROJECT, credentials=_Credentials())
        conn = client.connection = object()

        with _Monkey(MUT, _USE_GAX=False):
            api = client.sinks_api

        self.assertTrue(isinstance(api, _SinksAPI))
        self.assertTrue(api._connection is conn)
        # API instance is cached
        again = client.sinks_api
        self.assertTrue(again is api)

    def test_sinks_api_w_gax(self):
        from gcloud.logging import client as MUT
        from gcloud._testing import _Monkey

        wrapped = object()
        _called_with = []

        def _generated_api(*args, **kw):
            _called_with.append((args, kw))
            return wrapped

        class _GaxSinksAPI(object):

            def __init__(self, _wrapped):
                self._wrapped = _wrapped

        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)

        with _Monkey(MUT,
                     _USE_GAX=True,
                     GeneratedSinksAPI=_generated_api,
                     GAXSinksAPI=_GaxSinksAPI):
            api = client.sinks_api

        self.assertIsInstance(api, _GaxSinksAPI)
        self.assertTrue(api._wrapped is wrapped)
        # API instance is cached
        again = client.sinks_api
        self.assertTrue(again is api)

    def test_metrics_api_wo_gax(self):
        from gcloud.logging.connection import _MetricsAPI
        from gcloud.logging import client as MUT
        from gcloud._testing import _Monkey
        client = self._makeOne(self.PROJECT, credentials=_Credentials())
        conn = client.connection = object()

        with _Monkey(MUT, _USE_GAX=False):
            api = client.metrics_api

        self.assertTrue(isinstance(api, _MetricsAPI))
        self.assertTrue(api._connection is conn)
        # API instance is cached
        again = client.metrics_api
        self.assertTrue(again is api)

    def test_metrics_api_w_gax(self):
        from gcloud.logging import client as MUT
        from gcloud._testing import _Monkey

        wrapped = object()
        _called_with = []

        def _generated_api(*args, **kw):
            _called_with.append((args, kw))
            return wrapped

        class _GaxMetricsAPI(object):

            def __init__(self, _wrapped):
                self._wrapped = _wrapped

        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)

        with _Monkey(MUT,
                     _USE_GAX=True,
                     GeneratedMetricsAPI=_generated_api,
                     GAXMetricsAPI=_GaxMetricsAPI):
            api = client.metrics_api

        self.assertIsInstance(api, _GaxMetricsAPI)
        self.assertTrue(api._wrapped is wrapped)
        # API instance is cached
        again = client.metrics_api
        self.assertTrue(again is api)

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
        from gcloud.logging.entries import TextEntry
        IID = 'IID'
        TEXT = 'TEXT'
        TOKEN = 'TOKEN'
        ENTRIES = [{
            'textPayload': TEXT,
            'insertId': IID,
            'resource': {
                'type': 'global',
            },
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
        }]
        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)
        api = client._logging_api = _DummyLoggingAPI()
        api._list_entries_response = ENTRIES, TOKEN

        entries, token = client.list_entries()

        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertTrue(isinstance(entry, TextEntry))
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.payload, TEXT)
        logger = entry.logger
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)
        self.assertEqual(token, TOKEN)

        self.assertEqual(
            api._list_entries_called_with,
            ([self.PROJECT], None, None, None, None))

    def test_list_entries_explicit(self):
        from gcloud.logging import DESCENDING
        from gcloud.logging.entries import ProtobufEntry
        from gcloud.logging.entries import StructEntry
        from gcloud.logging.logger import Logger
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        FILTER = 'logName:LOGNAME'
        IID1 = 'IID1'
        IID2 = 'IID2'
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'partly cloudy'}
        PROTO_PAYLOAD = PAYLOAD.copy()
        PROTO_PAYLOAD['@type'] = 'type.googleapis.com/testing.example'
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        ENTRIES = [{
            'jsonPayload': PAYLOAD,
            'insertId': IID1,
            'resource': {
                'type': 'global',
            },
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
        }, {
            'protoPayload': PROTO_PAYLOAD,
            'insertId': IID2,
            'resource': {
                'type': 'global',
            },
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
        }]
        client = self._makeOne(self.PROJECT, credentials=_Credentials())
        api = client._logging_api = _DummyLoggingAPI()
        api._list_entries_response = ENTRIES, None

        entries, token = client.list_entries(
            projects=[PROJECT1, PROJECT2], filter_=FILTER, order_by=DESCENDING,
            page_size=PAGE_SIZE, page_token=TOKEN)
        self.assertEqual(len(entries), 2)

        entry = entries[0]
        self.assertTrue(isinstance(entry, StructEntry))
        self.assertEqual(entry.insert_id, IID1)
        self.assertEqual(entry.payload, PAYLOAD)
        logger = entry.logger
        self.assertTrue(isinstance(logger, Logger))
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)

        entry = entries[1]
        self.assertTrue(isinstance(entry, ProtobufEntry))
        self.assertEqual(entry.insert_id, IID2)
        self.assertEqual(entry.payload, PROTO_PAYLOAD)
        logger = entry.logger
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)

        self.assertTrue(entries[0].logger is entries[1].logger)

        self.assertEqual(token, None)
        self.assertEqual(
            api._list_entries_called_with,
            ([PROJECT1, PROJECT2], FILTER, DESCENDING, PAGE_SIZE, TOKEN))

    def test_sink_defaults(self):
        from gcloud.logging.sink import Sink
        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)
        sink = client.sink(self.SINK_NAME)
        self.assertTrue(isinstance(sink, Sink))
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter_, None)
        self.assertEqual(sink.destination, None)
        self.assertTrue(sink.client is client)
        self.assertEqual(sink.project, self.PROJECT)

    def test_sink_explicit(self):
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
        TOKEN = 'TOKEN'
        SINK_NAME = 'sink_name'
        FILTER = 'logName:syslog AND severity>=ERROR'
        SINKS = [{
            'name': SINK_NAME,
            'filter': FILTER,
            'destination': self.DESTINATION_URI,
        }]
        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        api = client._sinks_api = _DummySinksAPI()
        api._list_sinks_response = SINKS, TOKEN

        sinks, token = client.list_sinks()

        self.assertEqual(len(sinks), 1)
        sink = sinks[0]
        self.assertTrue(isinstance(sink, Sink))
        self.assertEqual(sink.name, SINK_NAME)
        self.assertEqual(sink.filter_, FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)

        self.assertEqual(token, TOKEN)
        self.assertEqual(api._list_sinks_called_with,
                         (PROJECT, None, None))

    def test_list_sinks_with_paging(self):
        from gcloud.logging.sink import Sink
        PROJECT = 'PROJECT'
        SINK_NAME = 'sink_name'
        FILTER = 'logName:syslog AND severity>=ERROR'
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        SINKS = [{
            'name': SINK_NAME,
            'filter': FILTER,
            'destination': self.DESTINATION_URI,
        }]
        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        api = client._sinks_api = _DummySinksAPI()
        api._list_sinks_response = SINKS, None

        sinks, token = client.list_sinks(PAGE_SIZE, TOKEN)

        self.assertEqual(len(sinks), 1)
        sink = sinks[0]
        self.assertTrue(isinstance(sink, Sink))
        self.assertEqual(sink.name, SINK_NAME)
        self.assertEqual(sink.filter_, FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertEqual(token, None)
        self.assertEqual(api._list_sinks_called_with,
                         (PROJECT, PAGE_SIZE, TOKEN))

    def test_metric_defaults(self):
        from gcloud.logging.metric import Metric
        creds = _Credentials()

        client_obj = self._makeOne(project=self.PROJECT, credentials=creds)
        metric = client_obj.metric(self.METRIC_NAME)
        self.assertTrue(isinstance(metric, Metric))
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, None)
        self.assertEqual(metric.description, '')
        self.assertTrue(metric.client is client_obj)
        self.assertEqual(metric.project, self.PROJECT)

    def test_metric_explicit(self):
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
        TOKEN = 'TOKEN'
        METRICS = [{
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }]
        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        api = client._metrics_api = _DummyMetricsAPI()
        api._list_metrics_response = METRICS, TOKEN

        metrics, token = client.list_metrics()

        self.assertEqual(len(metrics), 1)
        metric = metrics[0]
        self.assertTrue(isinstance(metric, Metric))
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertEqual(token, TOKEN)
        self.assertEqual(api._list_metrics_called_with,
                         (PROJECT, None, None))

    def test_list_metrics_with_paging(self):
        from gcloud.logging.metric import Metric
        PROJECT = 'PROJECT'
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        METRICS = [{
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }]
        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        api = client._metrics_api = _DummyMetricsAPI()
        api._list_metrics_response = METRICS, None

        # Execute request.
        metrics, token = client.list_metrics(PAGE_SIZE, TOKEN)
        # Test values are correct.
        self.assertEqual(len(metrics), 1)
        metric = metrics[0]
        self.assertTrue(isinstance(metric, Metric))
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertEqual(token, None)
        self.assertEqual(api._list_metrics_called_with,
                         (PROJECT, PAGE_SIZE, TOKEN))


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _DummyLoggingAPI(object):

    def list_entries(self, projects, filter_, order_by, page_size, page_token):
        self._list_entries_called_with = (
            projects, filter_, order_by, page_size, page_token)
        return self._list_entries_response


class _DummySinksAPI(object):

    def list_sinks(self, project, page_size, page_token):
        self._list_sinks_called_with = (project, page_size, page_token)
        return self._list_sinks_response


class _DummyMetricsAPI(object):

    def list_metrics(self, project, page_size, page_token):
        self._list_metrics_called_with = (project, page_size, page_token)
        return self._list_metrics_response
