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

    def test_ctor_defaults(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        client = _Client(self.PROJECT)
        sink = self._makeOne(self.SINK_NAME, client=client)
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter_, None)
        self.assertEqual(sink.destination, None)
        self.assertTrue(sink.client is client)
        self.assertEqual(sink.project, self.PROJECT)
        self.assertEqual(sink.full_name, FULL)
        self.assertEqual(sink.path, '/%s' % (FULL,))

    def test_ctor_explicit(self):
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        client = _Client(self.PROJECT)
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
        client = _Client(project=self.PROJECT)
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        klass = self._getTargetClass()
        sink = klass.from_api_repr(RESOURCE, client=client)
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter_, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertTrue(sink._client is client)
        self.assertEqual(sink.project, self.PROJECT)
        self.assertEqual(sink.full_name, FULL)

    def test_from_api_repr_w_description(self):
        client = _Client(project=self.PROJECT)
        FULL = 'projects/%s/sinks/%s' % (self.PROJECT, self.SINK_NAME)
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        klass = self._getTargetClass()
        sink = klass.from_api_repr(RESOURCE, client=client)
        self.assertEqual(sink.name, self.SINK_NAME)
        self.assertEqual(sink.filter_, self.FILTER)
        self.assertEqual(sink.destination, self.DESTINATION_URI)
        self.assertTrue(sink._client is client)
        self.assertEqual(sink.project, self.PROJECT)
        self.assertEqual(sink.full_name, FULL)

    def test_create_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.sinks_api = _DummySinksAPI()
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client)

        sink.create()

        self.assertEqual(
            api._sink_create_called_with,
            (self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI))

    def test_create_w_alternate_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client1)
        api = client2.sinks_api = _DummySinksAPI()

        sink.create(client=client2)

        self.assertEqual(
            api._sink_create_called_with,
            (self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI))

    def test_exists_miss_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.sinks_api = _DummySinksAPI()
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client)

        self.assertFalse(sink.exists())

        self.assertEqual(api._sink_get_called_with,
                         (self.PROJECT, self.SINK_NAME))

    def test_exists_hit_w_alternate_client(self):
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': self.FILTER,
            'destination': self.DESTINATION_URI,
        }
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.sinks_api = _DummySinksAPI()
        api._sink_get_response = RESOURCE
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client1)

        self.assertTrue(sink.exists(client=client2))

        self.assertEqual(api._sink_get_called_with,
                         (self.PROJECT, self.SINK_NAME))

    def test_reload_w_bound_client(self):
        NEW_FILTER = 'logName:syslog AND severity>=INFO'
        NEW_DESTINATION_URI = 'faux.googleapis.com/other'
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': NEW_FILTER,
            'destination': NEW_DESTINATION_URI,
        }
        client = _Client(project=self.PROJECT)
        api = client.sinks_api = _DummySinksAPI()
        api._sink_get_response = RESOURCE
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client)

        sink.reload()

        self.assertEqual(sink.filter_, NEW_FILTER)
        self.assertEqual(sink.destination, NEW_DESTINATION_URI)
        self.assertEqual(api._sink_get_called_with,
                         (self.PROJECT, self.SINK_NAME))

    def test_reload_w_alternate_client(self):
        NEW_FILTER = 'logName:syslog AND severity>=INFO'
        NEW_DESTINATION_URI = 'faux.googleapis.com/other'
        RESOURCE = {
            'name': self.SINK_NAME,
            'filter': NEW_FILTER,
            'destination': NEW_DESTINATION_URI,
        }
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.sinks_api = _DummySinksAPI()
        api._sink_get_response = RESOURCE
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client1)

        sink.reload(client=client2)

        self.assertEqual(sink.filter_, NEW_FILTER)
        self.assertEqual(sink.destination, NEW_DESTINATION_URI)
        self.assertEqual(api._sink_get_called_with,
                         (self.PROJECT, self.SINK_NAME))

    def test_update_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.sinks_api = _DummySinksAPI()
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client)

        sink.update()

        self.assertEqual(
            api._sink_update_called_with,
            (self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI))

    def test_update_w_alternate_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.sinks_api = _DummySinksAPI()
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client1)

        sink.update(client=client2)

        self.assertEqual(
            api._sink_update_called_with,
            (self.PROJECT, self.SINK_NAME, self.FILTER, self.DESTINATION_URI))

    def test_delete_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.sinks_api = _DummySinksAPI()
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client)

        sink.delete()

        self.assertEqual(api._sink_delete_called_with,
                         (self.PROJECT, self.SINK_NAME))

    def test_delete_w_alternate_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.sinks_api = _DummySinksAPI()
        sink = self._makeOne(self.SINK_NAME, self.FILTER, self.DESTINATION_URI,
                             client=client1)

        sink.delete(client=client2)

        self.assertEqual(api._sink_delete_called_with,
                         (self.PROJECT, self.SINK_NAME))


class _Client(object):

    def __init__(self, project):
        self.project = project


class _DummySinksAPI(object):

    def sink_create(self, project, sink_name, filter_, destination):
        self._sink_create_called_with = (
            project, sink_name, filter_, destination)

    def sink_get(self, project, sink_name):
        from gcloud.exceptions import NotFound
        self._sink_get_called_with = (project, sink_name)
        try:
            return self._sink_get_response
        except AttributeError:
            raise NotFound('miss')

    def sink_update(self, project, sink_name, filter_, destination):
        self._sink_update_called_with = (
            project, sink_name, filter_, destination)

    def sink_delete(self, project, sink_name):
        self._sink_delete_called_with = (project, sink_name)
