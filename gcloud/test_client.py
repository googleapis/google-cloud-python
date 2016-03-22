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

    def test_virtual(self):
        klass = self._getTargetClass()
        self.assertFalse('__init__' in klass.__dict__)


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
        MOCK_FILENAME = 'foo.path'
        mock_creds = _MockServiceAccountCredentials()
        with _Monkey(client, ServiceAccountCredentials=mock_creds):
            client_obj = KLASS.from_service_account_json(MOCK_FILENAME)

        self.assertTrue(client_obj.connection.credentials is
                        mock_creds._result)
        self.assertEqual(mock_creds.json_called, [MOCK_FILENAME])

    def test_from_service_account_json_fail(self):
        KLASS = self._getTargetClass()
        CREDENTIALS = object()
        self.assertRaises(TypeError, KLASS.from_service_account_json, None,
                          credentials=CREDENTIALS)

    def test_from_service_account_p12(self):
        from gcloud._testing import _Monkey
        from gcloud import client

        KLASS = self._getTargetClass()
        CLIENT_EMAIL = 'phred@example.com'
        MOCK_FILENAME = 'foo.path'
        mock_creds = _MockServiceAccountCredentials()
        with _Monkey(client, ServiceAccountCredentials=mock_creds):
            client_obj = KLASS.from_service_account_p12(CLIENT_EMAIL,
                                                        MOCK_FILENAME)

        self.assertTrue(client_obj.connection.credentials is
                        mock_creds._result)
        self.assertEqual(mock_creds.p12_called,
                         [(CLIENT_EMAIL, MOCK_FILENAME)])

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

        def mock_determine_proj(project):
            FUNC_CALLS.append((project, '_determine_default_project'))
            return PROJECT

        def mock_get_credentials():
            FUNC_CALLS.append('get_credentials')
            return CREDENTIALS

        with _Monkey(client, get_credentials=mock_get_credentials,
                     _determine_default_project=mock_determine_proj):
            client_obj = self._makeOne()

        self.assertEqual(client_obj.project, PROJECT)
        self.assertTrue(isinstance(client_obj.connection, _MockConnection))
        self.assertTrue(client_obj.connection.credentials is CREDENTIALS)
        self.assertEqual(
            FUNC_CALLS,
            [(None, '_determine_default_project'), 'get_credentials'])

    def test_ctor_missing_project(self):
        from gcloud._testing import _Monkey
        from gcloud import client

        FUNC_CALLS = []

        def mock_determine_proj(project):
            FUNC_CALLS.append((project, '_determine_default_project'))
            return None

        with _Monkey(client, _determine_default_project=mock_determine_proj):
            self.assertRaises(EnvironmentError, self._makeOne)

        self.assertEqual(FUNC_CALLS, [(None, '_determine_default_project')])

    def test_ctor_w_invalid_project(self):
        CREDENTIALS = object()
        HTTP = object()
        with self.assertRaises(ValueError):
            self._makeOne(project=object(), credentials=CREDENTIALS, http=HTTP)

    def _explicit_ctor_helper(self, project):
        import six

        CREDENTIALS = object()
        HTTP = object()

        client_obj = self._makeOne(project=project, credentials=CREDENTIALS,
                                   http=HTTP)

        if isinstance(project, six.binary_type):
            self.assertEqual(client_obj.project, project.decode('utf-8'))
        else:
            self.assertEqual(client_obj.project, project)
        self.assertTrue(isinstance(client_obj.connection, _MockConnection))
        self.assertTrue(client_obj.connection.credentials is CREDENTIALS)
        self.assertTrue(client_obj.connection.http is HTTP)

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
