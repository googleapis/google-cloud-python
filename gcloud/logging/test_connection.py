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


class TestConnection(unittest2.TestCase):

    PROJECT = 'project'
    FILTER = 'logName:syslog AND severity>=ERROR'

    def _getTargetClass(self):
        from gcloud.logging.connection import Connection
        return Connection

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_default_url(self):
        creds = _Credentials()
        conn = self._makeOne(creds)
        klass = self._getTargetClass()
        self.assertEqual(conn.credentials._scopes, klass.SCOPE)


class Test_LoggingAPI(unittest2.TestCase):

    PROJECT = 'project'
    LIST_ENTRIES_PATH = 'entries:list'
    WRITE_ENTRIES_PATH = 'entries:write'
    LOGGER_NAME = 'LOGGER_NAME'
    FILTER = 'logName:syslog AND severity>=ERROR'

    def _getTargetClass(self):
        from gcloud.logging.connection import _LoggingAPI
        return _LoggingAPI

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = object()
        api = self._makeOne(connection)
        self.assertTrue(api._connection is connection)

    @staticmethod
    def _make_timestamp():
        from datetime import datetime
        from gcloud._helpers import UTC
        from gcloud.logging.test_entries import _datetime_to_rfc3339_w_nanos
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        return _datetime_to_rfc3339_w_nanos(NOW)

    def test_list_entries_no_paging(self):
        TIMESTAMP = self._make_timestamp()
        IID = 'IID'
        TEXT = 'TEXT'
        SENT = {
            'projectIds': [self.PROJECT],
        }
        TOKEN = 'TOKEN'
        RETURNED = {
            'entries': [{
                'textPayload': TEXT,
                'insertId': IID,
                'resource': {
                    'type': 'global',
                },
                'timestamp': TIMESTAMP,
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
            }],
            'nextPageToken': TOKEN,
        }
        conn = _Connection(RETURNED)
        api = self._makeOne(conn)

        entries, token = api.list_entries([self.PROJECT])

        self.assertEqual(entries, RETURNED['entries'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(conn._called_with['method'], 'POST')
        path = '/%s' % self.LIST_ENTRIES_PATH
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_list_entries_w_paging(self):
        from gcloud.logging import DESCENDING
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        TIMESTAMP = self._make_timestamp()
        IID1 = 'IID1'
        IID2 = 'IID2'
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'partly cloudy'}
        PROTO_PAYLOAD = PAYLOAD.copy()
        PROTO_PAYLOAD['@type'] = 'type.googleapis.com/testing.example'
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        SENT = {
            'projectIds': [PROJECT1, PROJECT2],
            'filter': self.FILTER,
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
        conn = _Connection(RETURNED)
        api = self._makeOne(conn)

        entries, token = api.list_entries(
            projects=[PROJECT1, PROJECT2], filter_=self.FILTER,
            order_by=DESCENDING, page_size=PAGE_SIZE, page_token=TOKEN)

        self.assertEqual(entries, RETURNED['entries'])
        self.assertEqual(token, None)

        self.assertEqual(conn._called_with['method'], 'POST')
        path = '/%s' % self.LIST_ENTRIES_PATH
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_write_entries_single(self):
        TEXT = 'TEXT'
        ENTRY = {
            'textPayload': TEXT,
            'resource': {
                'type': 'global',
            },
            'logName': 'projects/%s/logs/%s' % (
                self.PROJECT, self.LOGGER_NAME),
        }
        SENT = {
            'entries': [ENTRY],
        }
        conn = _Connection({})
        api = self._makeOne(conn)

        api.write_entries([ENTRY])

        self.assertEqual(conn._called_with['method'], 'POST')
        path = '/%s' % self.WRITE_ENTRIES_PATH
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_write_entries_multiple(self):
        TEXT = 'TEXT'
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        RESOURCE = {
            'type': 'global',
        }
        LABELS = {
            'baz': 'qux',
            'spam': 'eggs',
        }
        ENTRY1 = {
            'textPayload': TEXT,
        }
        ENTRY2 = {
            'jsonPayload': {'foo': 'bar'},
        }
        SENT = {
            'logName': LOG_NAME,
            'resource': RESOURCE,
            'labels': LABELS,
            'entries': [ENTRY1, ENTRY2],
        }
        conn = _Connection({})
        api = self._makeOne(conn)

        api.write_entries([ENTRY1, ENTRY2], LOG_NAME, RESOURCE, LABELS)

        self.assertEqual(conn._called_with['method'], 'POST')
        path = '/%s' % self.WRITE_ENTRIES_PATH
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_logger_delete(self):
        path = '/projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        conn = _Connection({})
        api = self._makeOne(conn)

        api.logger_delete(self.PROJECT, self.LOGGER_NAME)

        self.assertEqual(conn._called_with['method'], 'DELETE')
        self.assertEqual(conn._called_with['path'], path)


class Test_SinksAPI(unittest2.TestCase):

    PROJECT = 'project'
    FILTER = 'logName:syslog AND severity>=ERROR'
    LIST_SINKS_PATH = 'projects/%s/sinks' % (PROJECT,)
    SINK_NAME = 'sink_name'
    SINK_PATH = 'projects/%s/sinks/%s' % (PROJECT, SINK_NAME)
    DESTINATION_URI = 'faux.googleapis.com/destination'

    def _getTargetClass(self):
        from gcloud.logging.connection import _SinksAPI
        return _SinksAPI

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = object()
        api = self._makeOne(connection)
        self.assertTrue(api._connection is connection)

    def test_list_sinks_no_paging(self):
        TOKEN = 'TOKEN'
        RETURNED = {
            'sinks': [{
                'name': self.SINK_PATH,
                'filter': self.FILTER,
                'destination': self.DESTINATION_URI,
            }],
            'nextPageToken': TOKEN,
        }
        conn = _Connection(RETURNED)
        api = self._makeOne(conn)

        sinks, token = api.list_sinks(self.PROJECT)

        self.assertEqual(sinks, RETURNED['sinks'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(conn._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_SINKS_PATH,)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['query_params'], {})

    def test_list_sinks_w_paging(self):
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        RETURNED = {
            'sinks': [{
                'name': self.SINK_PATH,
                'filter': self.FILTER,
                'destination': self.DESTINATION_URI,
            }],
        }
        conn = _Connection(RETURNED)
        api = self._makeOne(conn)

        sinks, token = api.list_sinks(
            self.PROJECT, page_size=PAGE_SIZE, page_token=TOKEN)

        self.assertEqual(sinks, RETURNED['sinks'])
        self.assertEqual(token, None)

        self.assertEqual(conn._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_SINKS_PATH,)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['query_params'],
                         {'pageSize': PAGE_SIZE, 'pageToken': TOKEN})

    def test_sink_create_conflict(self):
        from gcloud.exceptions import Conflict
        SENT = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        conn = _Connection()
        conn._raise_conflict = True
        api = self._makeOne(conn)

        with self.assertRaises(Conflict):
            api.sink_create(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

        self.assertEqual(conn._called_with['method'], 'POST')
        path = '/projects/%s/sinks' % (self.PROJECT,)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_sink_create_ok(self):
        SENT = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        conn = _Connection({})
        api = self._makeOne(conn)

        api.sink_create(
            self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI)

        self.assertEqual(conn._called_with['method'], 'POST')
        path = '/projects/%s/sinks' % (self.PROJECT,)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_sink_get_miss(self):
        from gcloud.exceptions import NotFound
        conn = _Connection()
        api = self._makeOne(conn)

        with self.assertRaises(NotFound):
            api.sink_get(self.PROJECT, self.SINK_NAME)

        self.assertEqual(conn._called_with['method'], 'GET')
        path = '/projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        self.assertEqual(conn._called_with['path'], path)

    def test_sink_get_hit(self):
        RESPONSE = {
            'name': self.SINK_PATH,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        conn = _Connection(RESPONSE)
        api = self._makeOne(conn)

        response = api.sink_get(self.PROJECT, self.SINK_NAME)

        self.assertEqual(response, RESPONSE)
        self.assertEqual(conn._called_with['method'], 'GET')
        path = '/projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        self.assertEqual(conn._called_with['path'], path)

    def test_sink_update_miss(self):
        from gcloud.exceptions import NotFound
        SENT = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        conn = _Connection()
        api = self._makeOne(conn)

        with self.assertRaises(NotFound):
            api.sink_update(
                self.PROJECT, self.SINK_NAME, self.FILTER,
                self.DESTINATION_URI)

        self.assertEqual(conn._called_with['method'], 'PUT')
        path = '/projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_sink_update_hit(self):
        SENT = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        conn = _Connection({})
        api = self._makeOne(conn)

        api.sink_update(
            self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI)

        self.assertEqual(conn._called_with['method'], 'PUT')
        path = '/projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_sink_delete_miss(self):
        from gcloud.exceptions import NotFound
        conn = _Connection()
        api = self._makeOne(conn)

        with self.assertRaises(NotFound):
            api.sink_delete(self.PROJECT, self.SINK_NAME)

        self.assertEqual(conn._called_with['method'], 'DELETE')
        path = '/projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        self.assertEqual(conn._called_with['path'], path)

    def test_sink_delete_hit(self):
        conn = _Connection({})
        api = self._makeOne(conn)

        api.sink_delete(self.PROJECT, self.SINK_NAME)

        self.assertEqual(conn._called_with['method'], 'DELETE')
        path = '/projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        self.assertEqual(conn._called_with['path'], path)


class Test_MetricsAPI(unittest2.TestCase):

    PROJECT = 'project'
    FILTER = 'logName:syslog AND severity>=ERROR'
    LIST_METRICS_PATH = 'projects/%s/metrics' % (PROJECT,)
    METRIC_NAME = 'metric_name'
    METRIC_PATH = 'projects/%s/metrics/%s' % (PROJECT, METRIC_NAME)
    DESCRIPTION = 'DESCRIPTION'

    def _getTargetClass(self):
        from gcloud.logging.connection import _MetricsAPI
        return _MetricsAPI

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_list_metrics_no_paging(self):
        TOKEN = 'TOKEN'
        RETURNED = {
            'metrics': [{
                'name': self.METRIC_PATH,
                'filter': self.FILTER,
            }],
            'nextPageToken': TOKEN,
        }
        conn = _Connection(RETURNED)
        api = self._makeOne(conn)

        metrics, token = api.list_metrics(self.PROJECT)

        self.assertEqual(metrics, RETURNED['metrics'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(conn._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_METRICS_PATH,)
        self.assertEqual(conn._called_with['path'], path)

    def test_list_metrics_w_paging(self):
        TOKEN = 'TOKEN'
        PAGE_SIZE = 42
        RETURNED = {
            'metrics': [{
                'name': self.METRIC_PATH,
                'filter': self.FILTER,
            }],
        }
        conn = _Connection(RETURNED)
        api = self._makeOne(conn)

        metrics, token = api.list_metrics(
            self.PROJECT, page_size=PAGE_SIZE, page_token=TOKEN)

        self.assertEqual(metrics, RETURNED['metrics'])
        self.assertEqual(token, None)

        self.assertEqual(conn._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_METRICS_PATH,)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['query_params'],
                         {'pageSize': PAGE_SIZE, 'pageToken': TOKEN})

    def test_metric_create_conflict(self):
        from gcloud.exceptions import Conflict
        SENT = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }
        conn = _Connection()
        conn._raise_conflict = True
        api = self._makeOne(conn)

        with self.assertRaises(Conflict):
            api.metric_create(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

        self.assertEqual(conn._called_with['method'], 'POST')
        path = '/projects/%s/metrics' % (self.PROJECT,)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_metric_create_ok(self):
        SENT = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }
        conn = _Connection({})
        api = self._makeOne(conn)

        api.metric_create(
            self.PROJECT, self.METRIC_NAME, self.FILTER, self.DESCRIPTION)

        self.assertEqual(conn._called_with['method'], 'POST')
        path = '/projects/%s/metrics' % (self.PROJECT,)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_metric_get_miss(self):
        from gcloud.exceptions import NotFound
        conn = _Connection()
        api = self._makeOne(conn)

        with self.assertRaises(NotFound):
            api.metric_get(self.PROJECT, self.METRIC_NAME)

        self.assertEqual(conn._called_with['method'], 'GET')
        path = '/projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        self.assertEqual(conn._called_with['path'], path)

    def test_metric_get_hit(self):
        RESPONSE = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }
        conn = _Connection(RESPONSE)
        api = self._makeOne(conn)

        response = api.metric_get(self.PROJECT, self.METRIC_NAME)

        self.assertEqual(response, RESPONSE)
        self.assertEqual(conn._called_with['method'], 'GET')
        path = '/projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        self.assertEqual(conn._called_with['path'], path)

    def test_metric_update_miss(self):
        from gcloud.exceptions import NotFound
        SENT = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }
        conn = _Connection()
        api = self._makeOne(conn)

        with self.assertRaises(NotFound):
            api.metric_update(
                self.PROJECT, self.METRIC_NAME, self.FILTER,
                self.DESCRIPTION)

        self.assertEqual(conn._called_with['method'], 'PUT')
        path = '/projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_metric_update_hit(self):
        SENT = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }
        conn = _Connection({})
        api = self._makeOne(conn)

        api.metric_update(
            self.PROJECT, self.METRIC_NAME, self.FILTER, self.DESCRIPTION)

        self.assertEqual(conn._called_with['method'], 'PUT')
        path = '/projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        self.assertEqual(conn._called_with['path'], path)
        self.assertEqual(conn._called_with['data'], SENT)

    def test_metric_delete_miss(self):
        from gcloud.exceptions import NotFound
        conn = _Connection()
        api = self._makeOne(conn)

        with self.assertRaises(NotFound):
            api.metric_delete(self.PROJECT, self.METRIC_NAME)

        self.assertEqual(conn._called_with['method'], 'DELETE')
        path = '/projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        self.assertEqual(conn._called_with['path'], path)

    def test_metric_delete_hit(self):
        conn = _Connection({})
        api = self._makeOne(conn)

        api.metric_delete(self.PROJECT, self.METRIC_NAME)

        self.assertEqual(conn._called_with['method'], 'DELETE')
        path = '/projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        self.assertEqual(conn._called_with['path'], path)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Connection(object):

    _called_with = None
    _raise_conflict = False

    def __init__(self, *responses):
        self._responses = responses

    def api_request(self, **kw):
        from gcloud.exceptions import Conflict
        from gcloud.exceptions import NotFound
        self._called_with = kw
        if self._raise_conflict:
            raise Conflict('oops')
        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except IndexError:
            raise NotFound('miss')
        return response
