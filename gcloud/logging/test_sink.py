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


class Test__sink_name_from_path(unittest2.TestCase):

    def _callFUT(self, path, project):
        from gcloud.logging.sink import _sink_name_from_path
        return _sink_name_from_path(path, project)

    def test_invalid_path_length(self):
        PATH = 'projects/foo'
        PROJECT = None
        self.assertRaises(ValueError, self._callFUT, PATH, PROJECT)

    def test_invalid_path_format(self):
        SINK_NAME = 'SINK_NAME'
        PROJECT = 'PROJECT'
        PATH = 'foo/%s/bar/%s' % (PROJECT, SINK_NAME)
        self.assertRaises(ValueError, self._callFUT, PATH, PROJECT)

    def test_invalid_project(self):
        SINK_NAME = 'SINK_NAME'
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        PATH = 'projects/%s/sinks/%s' % (PROJECT1, SINK_NAME)
        self.assertRaises(ValueError, self._callFUT, PATH, PROJECT2)

    def test_valid_data(self):
        SINK_NAME = 'SINK_NAME'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/sinks/%s' % (PROJECT, SINK_NAME)
        sink_name = self._callFUT(PATH, PROJECT)
        self.assertEqual(sink_name, SINK_NAME)


class TestSink(unittest2.TestCase):

    PROJECT = 'test-project'
    SINK_NAME = 'sink-name'
    FILTER = 'logName:syslog AND severity>=INFO'
    DESTINATION_URI = 'faux.googleapis.com/destination'

    def _getTargetClass(self):
        from gcloud.logging.sink import Sink
        return Sink

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        conn = _Connection()
        client = _Client(self.PROJECT, conn)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client)
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter_, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertTrue(sink.client is client)
        self.assertEqual(sink.project, self.PROJECT)
        self.assertEqual(sink.full_name, FULL)
        self.assertEqual(sink.path, '/%s' % (FULL,))

    def test_from_api_repr_minimal(self):
        CLIENT = _Client(project=self.PROJECT)
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        RESOURCE = {
            'name': FULL,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        klass = self._getTargetClass()
        sink = klass.from_api_repr(RESOURCE, client=CLIENT)
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter_, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertTrue(sink._client is CLIENT)
        self.assertEqual(sink.project, self.PROJECT)
        self.assertEqual(sink.full_name, FULL)

    def test_from_api_repr_w_description(self):
        CLIENT = _Client(project=self.PROJECT)
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        RESOURCE = {
            'name': FULL,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        klass = self._getTargetClass()
        sink = klass.from_api_repr(RESOURCE, client=CLIENT)
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter_, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertTrue(sink._client is CLIENT)
        self.assertEqual(sink.project, self.PROJECT)
        self.assertEqual(sink.full_name, FULL)

    def test_from_api_repr_with_mismatched_project(self):
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        CLIENT = _Client(project=PROJECT1)
        FULL = 'projects/%s/sinks/%s' % (PROJECT2, self.SINK_NAME)
        RESOURCE = {
            'name': FULL,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        klass = self._getTargetClass()
        self.assertRaises(ValueError, klass.from_api_repr,
                          RESOURCE, client=CLIENT)

    def test_create_w_bound_client(self):
        TARGET = 'projects/%s/sinks' % (self.PROJECT,)
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client)
        sink.create()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % TARGET)
        self.assertEqual(req['data'], RESOURCE)

    def test_create_w_alternate_client(self):
        TARGET = 'projects/%s/sinks' % (self.PROJECT,)
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client1)
        sink.create(client=client2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % TARGET)
        self.assertEqual(req['data'], RESOURCE)

    def test_exists_miss_w_bound_client(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        conn = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=CLIENT)
        self.assertFalse(sink.exists())
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_exists_hit_w_alternate_client(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({'name': FULL})
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=CLIENT1)
        self.assertTrue(sink.exists(client=CLIENT2))
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_reload_w_bound_client(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        NEW_FILTER = 'logName:syslog AND severity>=INFO'
        NEW_DESTINATION_URI = 'faux.googleapis.com/other'
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': NEW_FILTER,
            'destination': NEW_DESTINATION_URI,
        }
        conn = _Connection(RESOURCE)
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=CLIENT)
        sink.reload()
        self.assertEqual(sink.filter_, NEW_FILTER)
        self.assertEqual(sink.destination, NEW_DESTINATION_URI)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_reload_w_alternate_client(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        NEW_FILTER = 'logName:syslog AND severity>=INFO'
        NEW_DESTINATION_URI = 'faux.googleapis.com/other'
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': NEW_FILTER,
            'destination': NEW_DESTINATION_URI,
        }
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=CLIENT1)
        sink.reload(client=CLIENT2)
        self.assertEqual(sink.filter_, NEW_FILTER)
        self.assertEqual(sink.destination, NEW_DESTINATION_URI)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_update_w_bound_client(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        conn = _Connection(RESOURCE)
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=CLIENT)
        sink.update()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % FULL)
        self.assertEqual(req['data'], RESOURCE)

    def test_update_w_alternate_client(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=CLIENT1)
        sink.update(client=CLIENT2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % FULL)
        self.assertEqual(req['data'], RESOURCE)

    def test_delete_w_bound_client(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=CLIENT)
        sink.delete()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_delete_w_alternate_client(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=CLIENT1)
        sink.delete(client=CLIENT2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % FULL)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response


class _Client(object):

    def __init__(self, project, connection=None):
        self.project = project
        self.connection = connection
