# Copyright 2015 Google Inc.
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


class Test_ClientFactoryMixin(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.client import _ClientFactoryMixin
        return _ClientFactoryMixin

    def test_virtual(self):
        klass = self._get_target_class()
        self.assertFalse('__init__' in klass.__dict__)


class TestClient(unittest.TestCase):

    def setUp(self):
        KLASS = self._get_target_class()
        self.original_cnxn_class = KLASS._connection_class
        KLASS._connection_class = _MockConnection

    def tearDown(self):
        KLASS = self._get_target_class()
        KLASS._connection_class = self.original_cnxn_class

    @staticmethod
    def _get_target_class():
        from google.cloud.client import Client
        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        from google.cloud._testing import _Monkey
        from google.cloud import client

        CREDENTIALS = object()
        FUNC_CALLS = []

        def mock_get_credentials():
            FUNC_CALLS.append('get_credentials')
            return CREDENTIALS

        with _Monkey(client, get_credentials=mock_get_credentials):
            client_obj = self._make_one()

        self.assertIsInstance(client_obj._connection, _MockConnection)
        self.assertIs(client_obj._connection.credentials, CREDENTIALS)
        self.assertEqual(FUNC_CALLS, ['get_credentials'])

    def test_ctor_explicit(self):
        CREDENTIALS = object()
        HTTP = object()
        client_obj = self._make_one(credentials=CREDENTIALS, http=HTTP)

        self.assertIsInstance(client_obj._connection, _MockConnection)
        self.assertIs(client_obj._connection.credentials, CREDENTIALS)
        self.assertIs(client_obj._connection.http, HTTP)

    def test_from_service_account_json(self):
        from google.cloud._testing import _Monkey
        from google.cloud import client

        KLASS = self._get_target_class()
        MOCK_FILENAME = 'foo.path'
        mock_creds = _MockServiceAccountCredentials()
        with _Monkey(client, ServiceAccountCredentials=mock_creds):
            client_obj = KLASS.from_service_account_json(MOCK_FILENAME)

        self.assertIs(client_obj._connection.credentials, mock_creds._result)
        self.assertEqual(mock_creds.json_called, [MOCK_FILENAME])

    def test_from_service_account_json_fail(self):
        KLASS = self._get_target_class()
        CREDENTIALS = object()
        self.assertRaises(TypeError, KLASS.from_service_account_json, None,
                          credentials=CREDENTIALS)

    def test_from_service_account_p12(self):
        from google.cloud._testing import _Monkey
        from google.cloud import client

        KLASS = self._get_target_class()
        CLIENT_EMAIL = 'phred@example.com'
        MOCK_FILENAME = 'foo.path'
        mock_creds = _MockServiceAccountCredentials()
        with _Monkey(client, ServiceAccountCredentials=mock_creds):
            client_obj = KLASS.from_service_account_p12(CLIENT_EMAIL,
                                                        MOCK_FILENAME)

        self.assertIs(client_obj._connection.credentials, mock_creds._result)
        self.assertEqual(mock_creds.p12_called,
                         [(CLIENT_EMAIL, MOCK_FILENAME)])

    def test_from_service_account_p12_fail(self):
        KLASS = self._get_target_class()
        CREDENTIALS = object()
        self.assertRaises(TypeError, KLASS.from_service_account_p12, None,
                          None, credentials=CREDENTIALS)


class TestJSONClient(unittest.TestCase):

    def setUp(self):
        KLASS = self._get_target_class()
        self.original_cnxn_class = KLASS._connection_class
        KLASS._connection_class = _MockConnection

    def tearDown(self):
        KLASS = self._get_target_class()
        KLASS._connection_class = self.original_cnxn_class

    @staticmethod
    def _get_target_class():
        from google.cloud.client import JSONClient
        return JSONClient

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        from google.cloud._testing import _Monkey
        from google.cloud import client

        PROJECT = 'PROJECT'
        CREDENTIALS = object()
        FUNC_CALLS = []

        def mock_determine_proj(project):
            FUNC_CALLS.append((project, '_determine_default_project'))
            return PROJECT

        def mock_get_credentials():
            FUNC_CALLS.append('get_credentials')
            return CREDENTIALS

        with _Monkey(client, get_credentials=mock_get_credentials,
                     _determine_default_project=mock_determine_proj):
            client_obj = self._make_one()

        self.assertEqual(client_obj.project, PROJECT)
        self.assertIsInstance(client_obj._connection, _MockConnection)
        self.assertIs(client_obj._connection.credentials, CREDENTIALS)
        self.assertEqual(
            FUNC_CALLS,
            [(None, '_determine_default_project'), 'get_credentials'])

    def test_ctor_missing_project(self):
        from google.cloud._testing import _Monkey
        from google.cloud import client

        FUNC_CALLS = []

        def mock_determine_proj(project):
            FUNC_CALLS.append((project, '_determine_default_project'))
            return None

        with _Monkey(client, _determine_default_project=mock_determine_proj):
            self.assertRaises(EnvironmentError, self._make_one)

        self.assertEqual(FUNC_CALLS, [(None, '_determine_default_project')])

    def test_ctor_w_invalid_project(self):
        CREDENTIALS = object()
        HTTP = object()
        with self.assertRaises(ValueError):
            self._make_one(project=object(), credentials=CREDENTIALS,
                           http=HTTP)

    def _explicit_ctor_helper(self, project):
        import six

        CREDENTIALS = object()
        HTTP = object()

        client_obj = self._make_one(project=project, credentials=CREDENTIALS,
                                    http=HTTP)

        if isinstance(project, six.binary_type):
            self.assertEqual(client_obj.project, project.decode('utf-8'))
        else:
            self.assertEqual(client_obj.project, project)
        self.assertIsInstance(client_obj._connection, _MockConnection)
        self.assertIs(client_obj._connection.credentials, CREDENTIALS)
        self.assertIs(client_obj._connection.http, HTTP)

    def test_ctor_explicit_bytes(self):
        PROJECT = b'PROJECT'
        self._explicit_ctor_helper(PROJECT)

    def test_ctor_explicit_unicode(self):
        PROJECT = u'PROJECT'
        self._explicit_ctor_helper(PROJECT)


class _MockConnection(object):

    def __init__(self, credentials=None, http=None):
        self.credentials = credentials
        self.http = http


class _MockServiceAccountCredentials(object):

    def __init__(self):
        self.p12_called = []
        self.json_called = []
        self._result = object()

    def from_p12_keyfile(self, email, path):
        self.p12_called.append((email, path))
        return self._result

    def from_json_keyfile_name(self, path):
        self.json_called.append(path)
        return self._result
