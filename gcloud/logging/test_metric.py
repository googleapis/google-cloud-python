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

    def test_create_w_bound_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        RESOURCE = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
        }
        conn = _Connection({'name': FULL})
        client = _Client(project=self.PROJECT, connection=conn)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=client)
        metric.create()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % FULL)
        self.assertEqual(req['data'], RESOURCE)

    def test_create_w_alternate_client(self):
        FULL = 'projects/%s/metrics/%s' % (self.PROJECT, self.METRIC_NAME)
        RESOURCE = {
            'name': self.METRIC_NAME,
            'filter': self.FILTER,
            'description': self.DESCRIPTION,
        }
        conn1 = _Connection({'name': FULL})
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({'name': FULL})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        metric = self._makeOne(self.METRIC_NAME, self.FILTER, client=client1,
                               description=self.DESCRIPTION)
        metric.create(client=client2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % FULL)
        self.assertEqual(req['data'], RESOURCE)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:  # pragma: NO COVER
            raise NotFound('miss')
        else:
            return response


class _Client(object):

    def __init__(self, project, connection=None):
        self.project = project
        self.connection = connection
