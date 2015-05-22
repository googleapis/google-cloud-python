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


class Test__app_engine_id(unittest2.TestCase):

    def _callFUT(self):
        from gcloud._helpers import _app_engine_id
        return _app_engine_id()

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


class Test__compute_engine_id(unittest2.TestCase):

    def _callFUT(self):
        from gcloud._helpers import _compute_engine_id
        return _compute_engine_id()

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


class Test__get_production_project(unittest2.TestCase):

    def _callFUT(self):
        from gcloud._helpers import _get_production_project
        return _get_production_project()

    def test_no_value(self):
        import os
        from gcloud._testing import _Monkey

        environ = {}
        with _Monkey(os, getenv=environ.get):
            project = self._callFUT()
            self.assertEqual(project, None)

    def test_value_set(self):
        import os
        from gcloud._testing import _Monkey
        from gcloud._helpers import _PROJECT_ENV_VAR_NAME

        MOCK_PROJECT = object()
        environ = {_PROJECT_ENV_VAR_NAME: MOCK_PROJECT}
        with _Monkey(os, getenv=environ.get):
            project = self._callFUT()
            self.assertEqual(project, MOCK_PROJECT)


class Test__determine_default_project(unittest2.TestCase):

    def _callFUT(self, project=None):
        from gcloud._helpers import _determine_default_project
        return _determine_default_project(project=project)

    def _determine_default_helper(self, prod=None, project=None):
        from gcloud._testing import _Monkey
        from gcloud import _helpers

        _callers = []

        def prod_mock():
            _callers.append('prod_mock')
            return prod

        patched_methods = {
            '_get_production_project': prod_mock,
        }

        with _Monkey(_helpers, **patched_methods):
            returned_project = self._callFUT(project)

        return returned_project, _callers

    def test_no_value(self):
        project, callers = self._determine_default_helper()
        self.assertEqual(project, None)
        self.assertEqual(callers, ['prod_mock'])

    def test_explicit(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(project=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, [])

    def test_prod(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(prod=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, ['prod_mock'])


class Test_set_default_project(unittest2.TestCase):

    def setUp(self):
        from gcloud._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self, project=None):
        from gcloud._helpers import set_default_project
        return set_default_project(project=project)

    def test_raises(self):
        from gcloud._testing import _Monkey
        from gcloud import _helpers
        _called_project = []

        def mock_determine(project):
            _called_project.append(project)
            return None

        with _Monkey(_helpers, _determine_default_project=mock_determine):
            self.assertRaises(EnvironmentError, self._callFUT)

        self.assertEqual(_called_project, [None])

    def test_set_correctly(self):
        from gcloud._testing import _Monkey
        from gcloud import _helpers

        self.assertEqual(_helpers._DEFAULTS.project, None)

        PROJECT = object()
        _called_project = []

        def mock_determine(project):
            _called_project.append(project)
            return PROJECT

        with _Monkey(_helpers,
                     _determine_default_project=mock_determine):
            self._callFUT()

        self.assertEqual(_helpers._DEFAULTS.project, PROJECT)
        self.assertEqual(_called_project, [None])


class Test_lazy_loading(unittest2.TestCase):

    def setUp(self):
        from gcloud._testing import _setup_defaults
        _setup_defaults(self, implicit=True)

    def tearDown(self):
        from gcloud._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def test_descriptor_for_project(self):
        from gcloud._testing import _Monkey
        from gcloud import _helpers

        self.assertFalse('project' in _helpers._DEFAULTS.__dict__)

        DEFAULT = object()

        with _Monkey(_helpers,
                     _determine_default_project=lambda: DEFAULT):
            lazy_loaded = _helpers._DEFAULTS.project

        self.assertEqual(lazy_loaded, DEFAULT)
        self.assertTrue('project' in _helpers._DEFAULTS.__dict__)


class _Dummy(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)


class Test_ClientProxy(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud._helpers import _ClientProxy
        return _ClientProxy

    def _makeOne(self, wrapped, client):
        return self._getTargetClass()(wrapped, client)

    def test_ctor_and_attr_and_property(self):
        NAME = 'name'

        class _Wrapped(object):

            def __init__(self, **kw):
                self.__dict__.update(kw)

            @property
            def a_property(self):
                return NAME

        wrapped = _Wrapped(name=NAME)
        client = object()
        proxy = self._makeOne(wrapped, client)
        self.assertTrue(proxy._wrapped is wrapped)
        self.assertTrue(proxy._client is client)
        self.assertEqual(proxy.name, NAME)
        self.assertEqual(proxy.a_property, NAME)
        self.assertRaises(AttributeError, getattr, proxy, 'nonesuch')

    def test_method_taking_neither_connection_nor_project(self):

        class _Wrapped(_Dummy):

            def a_method(self, *args, **kw):
                return args, kw

        wrapped = _Wrapped()
        client = object()
        proxy = self._makeOne(wrapped, client)
        self.assertEqual(proxy.a_method('foo', bar=1), (('foo',), {'bar': 1}))

    def test_method_taking_connection_not_project(self):

        class _Wrapped(_Dummy):

            def a_method(self, connection):
                return connection

        wrapped = _Wrapped()
        connection = object()
        client = _Dummy(connection=connection)
        proxy = self._makeOne(wrapped, client)
        self.assertEqual(proxy.a_method(), connection)

    def test_method_taking_project_not_connection(self):
        PROJECT = 'PROJECT'

        class _Wrapped(_Dummy):

            def a_method(self, project):
                return project

        wrapped = _Wrapped()
        client = _Dummy(project=PROJECT)
        proxy = self._makeOne(wrapped, client)
        self.assertEqual(proxy.a_method(), PROJECT)

    def test_method_taking_connection_and_project(self):
        PROJECT = 'PROJECT'

        class _Wrapped(_Dummy):

            def a_method(self, connection, project):
                return connection, project

        wrapped = _Wrapped()
        connection = object()
        client = _Dummy(connection=connection, project=PROJECT)
        proxy = self._makeOne(wrapped, client)
        self.assertEqual(proxy.a_method(), (connection, PROJECT))


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

    def __init__(self, status, project):
        super(_HTTPConnection, self).__init__()
        self.status = status
        self.project = project

    def getresponse(self):
        return _HTTPResponse(self.status, self.project)


class _TimeoutHTTPConnection(_BaseHTTPConnection):

    def getresponse(self):
        import socket
        raise socket.timeout('timed out')
