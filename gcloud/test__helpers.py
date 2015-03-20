# Copyright 2014 Google Inc. All rights reserved.
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


class Test__LocalStack(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud._helpers import _LocalStack

        return _LocalStack

    def _makeOne(self):
        return self._getTargetClass()()

    def test_it(self):
        batch1, batch2 = object(), object()
        batches = self._makeOne()
        self.assertEqual(list(batches), [])
        self.assertTrue(batches.top is None)
        batches.push(batch1)
        self.assertTrue(batches.top is batch1)
        batches.push(batch2)
        self.assertTrue(batches.top is batch2)
        popped = batches.pop()
        self.assertTrue(popped is batch2)
        self.assertTrue(batches.top is batch1)
        self.assertEqual(list(batches), [batch1])
        popped = batches.pop()
        self.assertTrue(batches.top is None)
        self.assertEqual(list(batches), [])


class Test__LazyProperty(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud._helpers import _LazyProperty
        return _LazyProperty

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_prop_on_class(self):
        # Don't actually need a callable for ``method`` since
        # __get__ will just return ``self`` in this test.
        data_prop = self._makeOne('dataset_id', None)

        class FakeEnv(object):
            dataset_id = data_prop

        self.assertTrue(FakeEnv.dataset_id is data_prop)

    def test_prop_on_instance(self):
        RESULT = object()
        data_prop = self._makeOne('dataset_id', lambda: RESULT)

        class FakeEnv(object):
            dataset_id = data_prop

        self.assertTrue(FakeEnv().dataset_id is RESULT)


class Test__lazy_property_deco(unittest2.TestCase):

    def _callFUT(self, deferred_callable):
        from gcloud._helpers import _lazy_property_deco
        return _lazy_property_deco(deferred_callable)

    def test_on_function(self):
        def test_func():
            pass  # pragma: NO COVER never gets called

        lazy_prop = self._callFUT(test_func)
        self.assertTrue(lazy_prop._deferred_callable is test_func)
        self.assertEqual(lazy_prop._name, 'test_func')

    def test_on_staticmethod(self):
        def test_func():
            pass  # pragma: NO COVER never gets called

        lazy_prop = self._callFUT(staticmethod(test_func))
        self.assertTrue(lazy_prop._deferred_callable is test_func)
        self.assertEqual(lazy_prop._name, 'test_func')


class Test_app_engine_id(unittest2.TestCase):

    def _callFUT(self):
        from gcloud._helpers import app_engine_id
        return app_engine_id()

    def test_no_value(self):
        from gcloud._testing import _Monkey
        from gcloud import _helpers

        with _Monkey(_helpers, app_identity=None):
            dataset_id = self._callFUT()
            self.assertEqual(dataset_id, None)

    def test_value_set(self):
        from gcloud._testing import _Monkey
        from gcloud import _helpers

        APP_ENGINE_ID = object()
        APP_IDENTITY = _AppIdentity(APP_ENGINE_ID)
        with _Monkey(_helpers, app_identity=APP_IDENTITY):
            dataset_id = self._callFUT()
            self.assertEqual(dataset_id, APP_ENGINE_ID)


class Test_compute_engine_id(unittest2.TestCase):

    def _callFUT(self):
        from gcloud._helpers import compute_engine_id
        return compute_engine_id()

    def _monkeyConnection(self, connection):
        from gcloud._testing import _Monkey
        from gcloud import _helpers

        def _factory(host, timeout):
            connection.host = host
            connection.timeout = timeout
            return connection

        return _Monkey(_helpers, HTTPConnection=_factory)

    def test_bad_status(self):
        connection = _HTTPConnection(404, None)
        with self._monkeyConnection(connection):
            dataset_id = self._callFUT()
            self.assertEqual(dataset_id, None)

    def test_success(self):
        COMPUTE_ENGINE_ID = object()
        connection = _HTTPConnection(200, COMPUTE_ENGINE_ID)
        with self._monkeyConnection(connection):
            dataset_id = self._callFUT()
            self.assertEqual(dataset_id, COMPUTE_ENGINE_ID)

    def test_socket_raises(self):
        connection = _TimeoutHTTPConnection()
        with self._monkeyConnection(connection):
            dataset_id = self._callFUT()
            self.assertEqual(dataset_id, None)


class _AppIdentity(object):

    def __init__(self, app_id):
        self.app_id = app_id

    def get_application_id(self):
        return self.app_id


class _HTTPResponse(object):

    def __init__(self, status, data):
        self.status = status
        self.data = data

    def read(self):
        return self.data


class _BaseHTTPConnection(object):

    host = timeout = None

    def __init__(self):
        self._close_count = 0
        self._called_args = []
        self._called_kwargs = []

    def request(self, method, uri, **kwargs):
        self._called_args.append((method, uri))
        self._called_kwargs.append(kwargs)

    def close(self):
        self._close_count += 1


class _HTTPConnection(_BaseHTTPConnection):

    def __init__(self, status, project_id):
        super(_HTTPConnection, self).__init__()
        self.status = status
        self.project_id = project_id

    def getresponse(self):
        return _HTTPResponse(self.status, self.project_id)


class _TimeoutHTTPConnection(_BaseHTTPConnection):

    def getresponse(self):
        import socket
        raise socket.timeout('timed out')
