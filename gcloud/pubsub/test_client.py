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


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        from gcloud._testing import _Monkey
        from gcloud.pubsub import SCOPE
        from gcloud.pubsub import client
        from gcloud.pubsub.connection import Connection

        PROJECT = 'PROJECT'
        CREDS = _Credentials()
        FUNC_CALLS = []

        def mock_get_proj():
            FUNC_CALLS.append('_get_production_project')
            return PROJECT

        def mock_get_credentials():
            FUNC_CALLS.append('get_credentials')
            return CREDS

        with _Monkey(client, get_credentials=mock_get_credentials,
                     _get_production_project=mock_get_proj):
            client_obj = self._makeOne()

        self.assertEqual(client_obj.project, PROJECT)
        self.assertTrue(isinstance(client_obj.connection, Connection))
        self.assertTrue(client_obj.connection._credentials is CREDS)
        self.assertEqual(client_obj.connection._credentials._scopes, SCOPE)
        self.assertEqual(FUNC_CALLS,
                         ['_get_production_project', 'get_credentials'])

    def test_ctor_missing_project(self):
        from gcloud._testing import _Monkey
        from gcloud.pubsub import client

        FUNC_CALLS = []

        def mock_get_proj():
            FUNC_CALLS.append('_get_production_project')
            return None

        with _Monkey(client, _get_production_project=mock_get_proj):
            self.assertRaises(ValueError, self._makeOne)

        self.assertEqual(FUNC_CALLS, ['_get_production_project'])

    def test_ctor_explicit(self):
        from gcloud.pubsub import SCOPE
        from gcloud.pubsub.connection import Connection

        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        client_obj = self._makeOne(project=PROJECT, credentials=CREDS)

        self.assertEqual(client_obj.project, PROJECT)
        self.assertTrue(isinstance(client_obj.connection, Connection))
        self.assertTrue(client_obj.connection._credentials is CREDS)
        self.assertEqual(CREDS._scopes, SCOPE)

    def test_with_service_account_json(self):
        from gcloud._testing import _Monkey
        from gcloud.pubsub import client
        from gcloud.pubsub.connection import Connection

        PROJECT = 'PROJECT'
        KLASS = self._getTargetClass()
        CREDS = _Credentials()
        _CALLED = []

        def mock_creds(arg1):
            _CALLED.append((arg1,))
            return CREDS

        BOGUS_ARG = object()
        with _Monkey(client, get_for_service_account_json=mock_creds):
            client_obj = KLASS.with_service_account_json(
                BOGUS_ARG, project=PROJECT)

        self.assertEqual(client_obj.project, PROJECT)
        self.assertTrue(isinstance(client_obj.connection, Connection))
        self.assertTrue(client_obj.connection._credentials is CREDS)
        self.assertEqual(_CALLED, [(BOGUS_ARG,)])

    def test_with_service_account_p12(self):
        from gcloud._testing import _Monkey
        from gcloud.pubsub import client
        from gcloud.pubsub.connection import Connection

        PROJECT = 'PROJECT'
        KLASS = self._getTargetClass()
        CREDS = _Credentials()
        _CALLED = []

        def mock_creds(arg1, arg2):
            _CALLED.append((arg1, arg2))
            return CREDS

        BOGUS_ARG1 = object()
        BOGUS_ARG2 = object()
        with _Monkey(client, get_for_service_account_p12=mock_creds):
            client_obj = KLASS.with_service_account_p12(
                BOGUS_ARG1, BOGUS_ARG2, project=PROJECT)

        self.assertEqual(client_obj.project, PROJECT)
        self.assertTrue(isinstance(client_obj.connection, Connection))
        self.assertTrue(client_obj.connection._credentials is CREDS)
        self.assertEqual(_CALLED, [(BOGUS_ARG1, BOGUS_ARG2)])


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self
