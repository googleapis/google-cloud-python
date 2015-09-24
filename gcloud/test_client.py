# Copyright 2015 Google Inc. All rights reserved.
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


class Test_ClientFactoryMixin(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.client import _ClientFactoryMixin
        return _ClientFactoryMixin

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_virtual(self):
        self.assertRaises(NotImplementedError, self._makeOne)


class TestClient(unittest2.TestCase):

    def setUp(self):
        KLASS = self._getTargetClass()
        self.original_cnxn_class = KLASS._connection_class
        KLASS._connection_class = _MockConnection

    def tearDown(self):
        KLASS = self._getTargetClass()
        KLASS._connection_class = self.original_cnxn_class

    def _getTargetClass(self):
        from gcloud.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        from gcloud._testing import _Monkey
        from gcloud import client

        CREDENTIALS = object()
        FUNC_CALLS = []

        def mock_get_credentials():
            FUNC_CALLS.append('get_credentials')
            return CREDENTIALS

        with _Monkey(client, get_credentials=mock_get_credentials):
            client_obj = self._makeOne()

        self.assertTrue(isinstance(client_obj.connection, _MockConnection))
        self.assertTrue(client_obj.connection.credentials is CREDENTIALS)
        self.assertEqual(FUNC_CALLS, ['get_credentials'])

    def test_ctor_explicit(self):
        CREDENTIALS = object()
        HTTP = object()
        client_obj = self._makeOne(credentials=CREDENTIALS, http=HTTP)

        self.assertTrue(isinstance(client_obj.connection, _MockConnection))
        self.assertTrue(client_obj.connection.credentials is CREDENTIALS)
        self.assertTrue(client_obj.connection.http is HTTP)

    def test_from_service_account_json(self):
        from gcloud._testing import _Monkey
        from gcloud import client

        KLASS = self._getTargetClass()
        CREDENTIALS = object()
        _CALLED = []

        def mock_creds(arg1):
            _CALLED.append((arg1,))
            return CREDENTIALS

        BOGUS_ARG = object()
        with _Monkey(client, get_for_service_account_json=mock_creds):
            client_obj = KLASS.from_service_account_json(BOGUS_ARG)

        self.assertTrue(client_obj.connection.credentials is CREDENTIALS)
        self.assertEqual(_CALLED, [(BOGUS_ARG,)])

    def test_from_service_account_json_fail(self):
        KLASS = self._getTargetClass()
        CREDENTIALS = object()
        self.assertRaises(TypeError, KLASS.from_service_account_json, None,
                          credentials=CREDENTIALS)

    def test_from_service_account_p12(self):
        from gcloud._testing import _Monkey
        from gcloud import client

        KLASS = self._getTargetClass()
        CREDENTIALS = object()
        _CALLED = []

        def mock_creds(arg1, arg2):
            _CALLED.append((arg1, arg2))
            return CREDENTIALS

        BOGUS_ARG1 = object()
        BOGUS_ARG2 = object()
        with _Monkey(client, get_for_service_account_p12=mock_creds):
            client_obj = KLASS.from_service_account_p12(BOGUS_ARG1, BOGUS_ARG2)

        self.assertTrue(client_obj.connection.credentials is CREDENTIALS)
        self.assertEqual(_CALLED, [(BOGUS_ARG1, BOGUS_ARG2)])

    def test_from_service_account_p12_fail(self):
        KLASS = self._getTargetClass()
        CREDENTIALS = object()
        self.assertRaises(TypeError, KLASS.from_service_account_p12, None,
                          None, credentials=CREDENTIALS)


class TestJSONClient(unittest2.TestCase):

    def setUp(self):
        KLASS = self._getTargetClass()
        self.original_cnxn_class = KLASS._connection_class
        KLASS._connection_class = _MockConnection

    def tearDown(self):
        KLASS = self._getTargetClass()
        KLASS._connection_class = self.original_cnxn_class

    def _getTargetClass(self):
        from gcloud.client import JSONClient
        return JSONClient

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        from gcloud._testing import _Monkey
        from gcloud import client

        PROJECT = 'PROJECT'
        CREDENTIALS = object()
        FUNC_CALLS = []

        def mock_get_proj():
            FUNC_CALLS.append('_get_production_project')
            return PROJECT

        def mock_get_credentials():
            FUNC_CALLS.append('get_credentials')
            return CREDENTIALS

        with _Monkey(client, get_credentials=mock_get_credentials,
                     _get_production_project=mock_get_proj):
            client_obj = self._makeOne()

        self.assertTrue(client_obj.project is PROJECT)
        self.assertTrue(isinstance(client_obj.connection, _MockConnection))
        self.assertTrue(client_obj.connection.credentials is CREDENTIALS)
        self.assertEqual(FUNC_CALLS,
                         ['_get_production_project', 'get_credentials'])

    def test_ctor_missing_project(self):
        from gcloud._testing import _Monkey
        from gcloud import client

        FUNC_CALLS = []

        def mock_get_proj():
            FUNC_CALLS.append('_get_production_project')
            return None

        with _Monkey(client, _get_production_project=mock_get_proj):
            self.assertRaises(ValueError, self._makeOne)

        self.assertEqual(FUNC_CALLS, ['_get_production_project'])

    def test_ctor_w_invalid_project(self):
        CREDENTIALS = object()
        HTTP = object()
        with self.assertRaises(ValueError):
            self._makeOne(project=object(), credentials=CREDENTIALS, http=HTTP)

    def test_ctor_explicit(self):
        PROJECT = 'PROJECT'
        CREDENTIALS = object()
        HTTP = object()

        client_obj = self._makeOne(project=PROJECT, credentials=CREDENTIALS,
                                   http=HTTP)

        self.assertTrue(client_obj.project is PROJECT)
        self.assertTrue(isinstance(client_obj.connection, _MockConnection))
        self.assertTrue(client_obj.connection.credentials is CREDENTIALS)
        self.assertTrue(client_obj.connection.http is HTTP)


class _MockConnection(object):

    def __init__(self, credentials=None, http=None):
        self.credentials = credentials
        self.http = http
