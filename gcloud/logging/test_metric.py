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


class Test__metric_name_from_path(unittest2.TestCase):

    def _callFUT(self, path, project):
        from gcloud.logging.metric import _metric_name_from_path
        return _metric_name_from_path(path, project)

    def test_invalid_path_length(self):
        PATH = 'projects/foo'
        PROJECT = None
        self.assertRaises(ValueError, self._callFUT, PATH, PROJECT)

    def test_invalid_path_format(self):
        METRIC_NAME = 'METRIC_NAME'
        PROJECT = 'PROJECT'
        PATH = 'foo/%s/bar/%s' % (PROJECT, METRIC_NAME)
        self.assertRaises(ValueError, self._callFUT, PATH, PROJECT)

    def test_invalid_project(self):
        METRIC_NAME = 'METRIC_NAME'
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        PATH = 'projects/%s/metrics/%s' % (PROJECT1, METRIC_NAME)
        self.assertRaises(ValueError, self._callFUT, PATH, PROJECT2)

    def test_valid_data(self):
        METRIC_NAME = 'METRIC_NAME'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/metrics/%s' % (PROJECT, METRIC_NAME)
        metric_name = self._callFUT(PATH, PROJECT)
        self.assertEqual(metric_name, METRIC_NAME)


class TestMetric(unittest2.TestCase):

    PROJECT = 'test-project'
    METRIC_NAME = 'metric-name'
    FILTER = 'logName:syslog AND severity>=ERROR'
    DESCRIPTION = 'DESCRIPTION'

    def _getTargetClass(self):
        from gcloud.logging.metric import Metric
        return Metric

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        conn = _Connection()
        client = _Client(self.PROJECT, conn)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=client)
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, '')
        self.assertTrue(metric.client is client)
        self.assertEqual(metric.project, self.PROJECT)
        self.assertEqual(metric.full_name, FULL)
        self.assertEqual(metric.path, '/%s' % (FULL,))

    def test_ctor_explicit(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        conn = _Connection()
        client = _Client(self.PROJECT, conn)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER,
                               client=client, description=self.DESCRIPTION)
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, self.DESCRIPTION)
        self.assertTrue(metric.client is client)
        self.assertEqual(metric.project, self.PROJECT)
        self.assertEqual(metric.full_name, FULL)
        self.assertEqual(metric.path, '/%s' % (FULL,))

    def test_from_api_repr_minimal(self):
        CLIENT = _Client(project=self.PROJECT)
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        RESOURCE = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
        }
        klass = self._getTargetClass()
        metric = klass.from_api_repr(RESOURCE, client=CLIENT)
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, '')
        self.assertTrue(metric._client is CLIENT)
        self.assertEqual(metric.project, self.PROJECT)
        self.assertEqual(metric.full_name, FULL)

    def test_from_api_repr_w_description(self):
        CLIENT = _Client(project=self.PROJECT)
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        DESCRIPTION = 'DESCRIPTION'
        RESOURCE = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': DESCRIPTION,
        }
        klass = self._getTargetClass()
        metric = klass.from_api_repr(RESOURCE, client=CLIENT)
        self.assertEqual(metric.name, self.METRIC_NAME)
        self.assertEqual(metric.filter_, self.FILTER)
        self.assertEqual(metric.description, DESCRIPTION)
        self.assertTrue(metric._client is CLIENT)
        self.assertEqual(metric.project, self.PROJECT)
        self.assertEqual(metric.full_name, FULL)

    def test_create_w_bound_client(self):
        TARGET = 'projects/%s/metrics' % (self.PROJECT,)
        RESOURCE = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
        }
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=client)
        metric.create()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % TARGET)
        self.assertEqual(req['data'], RESOURCE)

    def test_create_w_alternate_client(self):
        TARGET = 'projects/%s/metrics' % (self.PROJECT,)
        RESOURCE = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=client1,
                               description=self.DESCRIPTION)
        metric.create(client=client2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % TARGET)
        self.assertEqual(req['data'], RESOURCE)

    def test_exists_miss_w_bound_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        conn = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=CLIENT)
        self.assertFalse(metric.exists())
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_exists_hit_w_alternate_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({'name': FULL})
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=CLIENT1)
        self.assertTrue(metric.exists(client=CLIENT2))
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_reload_w_bound_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        DESCRIPTION = 'DESCRIPTION'
        NEW_FILTER = 'logName:syslog AND severity>=INFO'
        RESOURCE = {
            'name': self.METRIC_NAME,
            'filter': NEW_FILTER,
        }
        conn = _Connection(RESOURCE)
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=CLIENT,
                               description=DESCRIPTION)
        metric.reload()
        self.assertEqual(metric.filter_, NEW_FILTER)
        self.assertEqual(metric.description, '')
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_reload_w_alternate_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        DESCRIPTION = 'DESCRIPTION'
        NEW_FILTER = 'logName:syslog AND severity>=INFO'
        RESOURCE = {
            'name': self.METRIC_NAME,
            'description': DESCRIPTION,
            'filter': NEW_FILTER,
        }
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=CLIENT1)
        metric.reload(client=CLIENT2)
        self.assertEqual(metric.filter_, NEW_FILTER)
        self.assertEqual(metric.description, DESCRIPTION)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_update_w_bound_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        RESOURCE = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
        }
        conn = _Connection(RESOURCE)
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=CLIENT)
        metric.update()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % FULL)
        self.assertEqual(req['data'], RESOURCE)

    def test_update_w_alternate_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        DESCRIPTION = 'DESCRIPTION'
        RESOURCE = {
            'name': self.METRIC_NAME,
            'description': DESCRIPTION,
            'filter': self.FILTER,
        }
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=CLIENT1,
                               description=DESCRIPTION)
        metric.update(client=CLIENT2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % FULL)
        self.assertEqual(req['data'], RESOURCE)

    def test_delete_w_bound_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=CLIENT)
        metric.delete()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % FULL)

    def test_delete_w_alternate_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=CLIENT1)
        metric.delete(client=CLIENT2)
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
