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


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):

    PROJECT = 'PROJECT'
    LOGGER_NAME = 'LOGGER_NAME'
    SINK_NAME = 'SINK_NAME'
    FILTER = 'logName:syslog AND severity>=ERROR'
    DESTINATION_URI = 'faux.googleapis.com/destination'
    METRIC_NAME = 'metric_name'
    FILTER = 'logName:syslog AND severity>=ERROR'
    DESCRIPTION = 'DESCRIPTION'

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.client import Client

        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        self.assertEqual(client.project, self.PROJECT)

    def test_logging_api_wo_gax(self):
        from google.cloud.logging._http import _LoggingAPI

        client = self._make_one(self.PROJECT,
                                credentials=_make_credentials(),
                                _use_grpc=False)

        conn = client._connection = _Connection()
        api = client.logging_api

        self.assertIsInstance(api, _LoggingAPI)
        self.assertEqual(api.api_request, conn.api_request)
        # API instance is cached
        again = client.logging_api
        self.assertIs(again, api)

    def test_logging_api_w_gax(self):
        clients = []
        api_obj = object()

        def make_api(client_obj):
            clients.append(client_obj)
            return api_obj

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _use_grpc=True)

        patch = mock.patch(
            'google.cloud.logging.client.make_gax_logging_api',
            new=make_api)
        with patch:
            api = client.logging_api

        self.assertIs(api, api_obj)
        self.assertEqual(clients, [client])
        # API instance is cached
        again = client.logging_api
        self.assertIs(again, api)

    def test_no_gax_ctor(self):
        from google.cloud.logging._http import _LoggingAPI

        creds = _make_credentials()
        patch = mock.patch(
            'google.cloud.logging.client._USE_GRPC',
            new=True)
        with patch:
            client = self._make_one(project=self.PROJECT, credentials=creds,
                                    _use_grpc=False)

        api = client.logging_api
        self.assertIsInstance(api, _LoggingAPI)

    def test_sinks_api_wo_gax(self):
        from google.cloud.logging._http import _SinksAPI

        client = self._make_one(
            self.PROJECT, credentials=_make_credentials(),
            _use_grpc=False)

        conn = client._connection = _Connection()
        api = client.sinks_api

        self.assertIsInstance(api, _SinksAPI)
        self.assertEqual(api.api_request, conn.api_request)
        # API instance is cached
        again = client.sinks_api
        self.assertIs(again, api)

    def test_sinks_api_w_gax(self):
        clients = []
        api_obj = object()

        def make_api(client_obj):
            clients.append(client_obj)
            return api_obj

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _use_grpc=True)

        patch = mock.patch(
            'google.cloud.logging.client.make_gax_sinks_api',
            new=make_api)
        with patch:
            api = client.sinks_api

        self.assertIs(api, api_obj)
        self.assertEqual(clients, [client])
        # API instance is cached
        again = client.sinks_api
        self.assertIs(again, api)

    def test_metrics_api_wo_gax(self):
        from google.cloud.logging._http import _MetricsAPI

        client = self._make_one(
            self.PROJECT, credentials=_make_credentials(),
            _use_grpc=False)

        conn = client._connection = _Connection()
        api = client.metrics_api

        self.assertIsInstance(api, _MetricsAPI)
        self.assertEqual(api.api_request, conn.api_request)
        # API instance is cached
        again = client.metrics_api
        self.assertIs(again, api)

    def test_metrics_api_w_gax(self):
        clients = []
        api_obj = object()

        def make_api(client_obj):
            clients.append(client_obj)
            return api_obj

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _use_grpc=True)

        patch = mock.patch(
            'google.cloud.logging.client.make_gax_metrics_api',
            new=make_api)
        with patch:
            api = client.metrics_api

        self.assertIs(api, api_obj)
        self.assertEqual(clients, [client])
        # API instance is cached
        again = client.metrics_api
        self.assertIs(again, api)

    def test_logger(self):
        from google.cloud.logging.logger import Logger

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        logger = client.logger(self.LOGGER_NAME)
        self.assertIsInstance(logger, Logger)
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertIs(logger.client, client)
        self.assertEqual(logger.project, self.PROJECT)

    def test_list_entries_defaults(self):
        import six
        from google.cloud.logging.entries import TextEntry

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
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                _use_grpc=False)
        returned = {
            'entries': ENTRIES,
            'nextPageToken': TOKEN,
        }
        client._connection = _Connection(returned)

        iterator = client.list_entries()
        page = six.next(iterator.pages)
        entries = list(page)
        token = iterator.next_page_token

        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertIsInstance(entry, TextEntry)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.payload, TEXT)
        logger = entry.logger
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertIs(logger.client, client)
        self.assertEqual(logger.project, self.PROJECT)
        self.assertEqual(token, TOKEN)

        called_with = client._connection._called_with
        self.assertEqual(called_with, {
            'path': '/entries:list',
            'method': 'POST',
            'data': {'projectIds': [self.PROJECT]},
        })

    def test_list_entries_explicit(self):
        from google.cloud.logging import DESCENDING
        from google.cloud.logging.entries import ProtobufEntry
        from google.cloud.logging.entries import StructEntry
        from google.cloud.logging.logger import Logger

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
        client = self._make_one(self.PROJECT, credentials=_make_credentials(),
                                _use_grpc=False)
        returned = {'entries': ENTRIES}
        client._connection = _Connection(returned)

        iterator = client.list_entries(
            projects=[PROJECT1, PROJECT2], filter_=FILTER, order_by=DESCENDING,
            page_size=PAGE_SIZE, page_token=TOKEN)
        entries = list(iterator)
        token = iterator.next_page_token

        # First, check the token.
        self.assertIsNone(token)
        # Then check the entries.
        self.assertEqual(len(entries), 2)
        entry = entries[0]
        self.assertIsInstance(entry, StructEntry)
        self.assertEqual(entry.insert_id, IID1)
        self.assertEqual(entry.payload, PAYLOAD)
        logger = entry.logger
        self.assertIsInstance(logger, Logger)
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertIs(logger.client, client)
        self.assertEqual(logger.project, self.PROJECT)

        entry = entries[1]
        self.assertIsInstance(entry, ProtobufEntry)
        self.assertEqual(entry.insert_id, IID2)
        self.assertEqual(entry.payload, PROTO_PAYLOAD)
        logger = entry.logger
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertIs(logger.client, client)
        self.assertEqual(logger.project, self.PROJECT)

        self.assertIs(entries[0].logger, entries[1].logger)

        called_with = client._connection._called_with
        self.assertEqual(called_with, {
            'path': '/entries:list',
            'method': 'POST',
            'data': {
                'filter': FILTER,
                'orderBy': DESCENDING,
                'pageSize': PAGE_SIZE,
                'pageToken': TOKEN,
                'projectIds': [PROJECT1, PROJECT2],
            },
        })

    def test_sink_defaults(self):
        from google.cloud.logging.sink import Sink

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        sink = client.sink(self.SINK_NAME)
        self.assertIsInstance(sink, Sink)
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertIsNone(sink.filter_)
        self.assertIsNone(sink.destination)
        self.assertIs(sink.client, client)
        self.assertEqual(sink.project, self.PROJECT)

    def test_sink_explicit(self):
        from google.cloud.logging.sink import Sink

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        sink = client.sink(self.SINK_NAME, self.FILTER, self.DESTINATION_URI)
        self.assertIsInstance(sink, Sink)
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter_, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertIs(sink.client, client)
        self.assertEqual(sink.project, self.PROJECT)

    def test_list_sinks_no_paging(self):
        import six
        from google.cloud.logging.sink import Sink

        PROJECT = 'PROJECT'
        TOKEN = 'TOKEN'
        SINK_NAME = 'sink_name'
        FILTER = 'logName:syslog AND severity>=ERROR'
        SINKS = [{
            'name': SINK_NAME,
            'filter': FILTER,
            'destination': self.DESTINATION_URI,
        }]
        client = self._make_one(project=PROJECT,
                                credentials=_make_credentials(),
                                _use_grpc=False)
        returned = {
            'sinks': SINKS,
            'nextPageToken': TOKEN,
        }
        client._connection = _Connection(returned)

        iterator = client.list_sinks()
        page = six.next(iterator.pages)
        sinks = list(page)
        token = iterator.next_page_token

        # First check the token.
        self.assertEqual(token, TOKEN)
        # Then check the sinks returned.
        self.assertEqual(len(sinks), 1)
        sink = sinks[0]
        self.assertIsInstance(sink, Sink)
        self.assertEqual(sink.name, SINK_NAME)
        self.assertEqual(sink.filter_, FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertIs(sink.client, client)

        # Verify the mocked transport.
        called_with = client._connection._called_with
        path = '/projects/%s/sinks' % (self.PROJECT,)
        self.assertEqual(called_with, {
            'method': 'GET',
            'path': path,
            'query_params': {},
        })

    def test_list_sinks_with_paging(self):
        from google.cloud.logging.sink import Sink

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
        client = self._make_one(
            project=PROJECT, credentials=_make_credentials(), _use_grpc=False)
        returned = {
            'sinks': SINKS,
        }
        client._connection = _Connection(returned)

        iterator = client.list_sinks(PAGE_SIZE, TOKEN)
        sinks = list(iterator)
        token = iterator.next_page_token

        # First check the token.
        self.assertIsNone(token)
        # Then check the sinks returned.
        self.assertEqual(len(sinks), 1)
        sink = sinks[0]
        self.assertIsInstance(sink, Sink)
        self.assertEqual(sink.name, SINK_NAME)
        self.assertEqual(sink.filter_, FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertIs(sink.client, client)

        # Verify the mocked transport.
        called_with = client._connection._called_with
        path = '/projects/%s/sinks' % (self.PROJECT,)
        self.assertEqual(called_with, {
            'method': 'GET',
            'path': path,
            'query_params': {
                'pageSize': PAGE_SIZE,
                'pageToken': TOKEN,
            },
        })

    def test_metric_defaults(self):
        from google.cloud.logging.metric import Metric

        creds = _make_credentials()

        client_obj = self._make_one(project=self.PROJECT, credentials=creds)
        metric = client_obj.metric(self.METRIC_NAME)
        self.assertIsInstance(metric, Metric)
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertIsNone(metric.filter_)
        self.assertEqual(metric.description, '')
        self.assertIs(metric.client, client_obj)
        self.assertEqual(metric.project, self.PROJECT)

    def test_metric_explicit(self):
        from google.cloud.logging.metric import Metric

        creds = _make_credentials()

        client_obj = self._make_one(project=self.PROJECT, credentials=creds)
        metric = client_obj.metric(self.METRIC_NAME, self.FILTER,
                                   description=self.DESCRIPTION)
        self.assertIsInstance(metric, Metric)
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertIs(metric.client, client_obj)
        self.assertEqual(metric.project, self.PROJECT)

    def test_list_metrics_no_paging(self):
        from google.cloud.logging.metric import Metric

        metrics = [{
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }]
        client = self._make_one(
            project=self.PROJECT, credentials=_make_credentials(),
            _use_grpc=False)
        returned = {
            'metrics': metrics,
        }
        client._connection = _Connection(returned)

        # Execute request.
        iterator = client.list_metrics()
        metrics = list(iterator)

        # Check the metrics returned.
        self.assertEqual(len(metrics), 1)
        metric = metrics[0]
        self.assertIsInstance(metric, Metric)
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertIs(metric.client, client)

        # Verify mocked transport.
        called_with = client._connection._called_with
        path = '/projects/%s/metrics' % (self.PROJECT,)
        self.assertEqual(called_with, {
            'method': 'GET',
            'path': path,
            'query_params': {},
        })

    def test_list_metrics_with_paging(self):
        import six
        from google.cloud.logging.metric import Metric

        token = 'TOKEN'
        next_token = 'T00KEN'
        page_size = 42
        metrics = [{
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }]
        client = self._make_one(
            project=self.PROJECT, credentials=_make_credentials(),
            _use_grpc=False)
        returned = {
            'metrics': metrics,
            'nextPageToken': next_token,
        }
        client._connection = _Connection(returned)

        # Execute request.
        iterator = client.list_metrics(page_size, token)
        page = six.next(iterator.pages)
        metrics = list(page)

        # First check the token.
        self.assertEqual(iterator.next_page_token, next_token)
        # Then check the metrics returned.
        self.assertEqual(len(metrics), 1)
        metric = metrics[0]
        self.assertIsInstance(metric, Metric)
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertIs(metric.client, client)

        # Verify mocked transport.
        called_with = client._connection._called_with
        path = '/projects/%s/metrics' % (self.PROJECT,)
        self.assertEqual(called_with, {
            'method': 'GET',
            'path': path,
            'query_params': {
                'pageSize': page_size,
                'pageToken': token,
            },
        })

    def test_get_default_handler_app_engine(self):
        import httplib2
        import os
        from google.cloud._testing import _Monkey
        from google.cloud.logging.client import _APPENGINE_FLEXIBLE_ENV_VM
        from google.cloud.logging.handlers import AppEngineHandler

        http_mock = mock.Mock(spec=httplib2.Http)
        credentials = _make_credentials()
        deepcopy = mock.Mock(return_value=http_mock)

        with _Monkey(os, environ={_APPENGINE_FLEXIBLE_ENV_VM: 'True'}):
            with mock.patch('copy.deepcopy', new=deepcopy):
                client = self._make_one(project=self.PROJECT,
                                        credentials=credentials,
                                        _use_grpc=False)
                handler = client.get_default_handler()
                deepcopy.assert_called_once_with(client._http)

        self.assertIsInstance(handler, AppEngineHandler)

    def test_get_default_handler_container_engine(self):
        import os
        from google.cloud._testing import _Monkey
        from google.cloud.logging.client import _CONTAINER_ENGINE_ENV
        from google.cloud.logging.handlers import ContainerEngineHandler

        client = self._make_one(project=self.PROJECT,
                                credentials=_make_credentials(),
                                _use_grpc=False)

        with _Monkey(os, environ={_CONTAINER_ENGINE_ENV: 'True'}):
            handler = client.get_default_handler()

        self.assertIsInstance(handler, ContainerEngineHandler)

    def test_get_default_handler_general(self):
        import httplib2
        from google.cloud.logging.handlers import CloudLoggingHandler

        http_mock = mock.Mock(spec=httplib2.Http)
        credentials = _make_credentials()
        deepcopy = mock.Mock(return_value=http_mock)

        with mock.patch('copy.deepcopy', new=deepcopy):
            client = self._make_one(project=self.PROJECT,
                                    credentials=credentials,
                                    _use_grpc=False)
            handler = client.get_default_handler()
            deepcopy.assert_called_once_with(client._http)

        self.assertIsInstance(handler, CloudLoggingHandler)

    def test_setup_logging(self):
        import httplib2

        http_mock = mock.Mock(spec=httplib2.Http)
        deepcopy = mock.Mock(return_value=http_mock)
        setup_logging = mock.Mock(spec=[])

        credentials = _make_credentials()

        with mock.patch('copy.deepcopy', new=deepcopy):
            with mock.patch('google.cloud.logging.client.setup_logging',
                            new=setup_logging):
                client = self._make_one(project=self.PROJECT,
                                        credentials=credentials,
                                        _use_grpc=False)
                client.setup_logging()
                deepcopy.assert_called_once_with(client._http)

        setup_logging.assert_called()


class _Connection(object):

    _called_with = None

    def __init__(self, *responses):
        self._responses = responses

    def api_request(self, **kw):
        self._called_with = kw
        response, self._responses = self._responses[0], self._responses[1:]
        return response
