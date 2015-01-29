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


class Test_set_default_dataset_id(unittest2.TestCase):

    def setUp(self):
        from gcloud.datastore import _implicit_environ
        self._replaced_dataset_id = _implicit_environ.DATASET_ID
        _implicit_environ.DATASET_ID = None

    def tearDown(self):
        from gcloud.datastore import _implicit_environ
        _implicit_environ.DATASET_ID = self._replaced_dataset_id

    def _callFUT(self, dataset_id=None):
        from gcloud.datastore import set_default_dataset_id
        return set_default_dataset_id(dataset_id=dataset_id)

    def _monkey(self, implicit_dataset_id, httplib=None, app_identity=None):
        from contextlib import nested
        import os

        from gcloud._testing import _Monkey
        from gcloud.datastore import _DATASET_ENV_VAR_NAME
        from gcloud.datastore import _implicit_environ

        environ = {_DATASET_ENV_VAR_NAME: implicit_dataset_id}
        httplib = httplib or _Httplib(None, status=404)
        return nested(_Monkey(os, getenv=environ.get),
                      _Monkey(_implicit_environ, httplib=httplib,
                              app_identity=app_identity))

    def test_no_env_var_set(self):
        from gcloud.datastore import _implicit_environ
        with self._monkey(None):
            self._callFUT()
        self.assertEqual(_implicit_environ.DATASET_ID, None)

    def test_set_from_env_var(self):
        from gcloud.datastore import _implicit_environ
        IMPLICIT_DATASET_ID = 'IMPLICIT'
        with self._monkey(IMPLICIT_DATASET_ID):
            self._callFUT()
        self.assertEqual(_implicit_environ.DATASET_ID, IMPLICIT_DATASET_ID)

    def test_set_explicit_w_env_var_set(self):
        from gcloud.datastore import _implicit_environ
        EXPLICIT_DATASET_ID = 'EXPLICIT'
        with self._monkey(None):
            self._callFUT(EXPLICIT_DATASET_ID)
        self.assertEqual(_implicit_environ.DATASET_ID, EXPLICIT_DATASET_ID)

    def test_set_explicit_no_env_var_set(self):
        from gcloud.datastore import _implicit_environ
        IMPLICIT_DATASET_ID = 'IMPLICIT'
        EXPLICIT_DATASET_ID = 'EXPLICIT'
        with self._monkey(IMPLICIT_DATASET_ID):
            self._callFUT(EXPLICIT_DATASET_ID)
        self.assertEqual(_implicit_environ.DATASET_ID, EXPLICIT_DATASET_ID)

    def test_set_explicit_None_wo_env_var_set(self):
        from gcloud.datastore import _implicit_environ
        with self._monkey(None):
            self._callFUT(None)
        self.assertEqual(_implicit_environ.DATASET_ID, None)

    def test_set_explicit_None_w_env_var_set(self):
        from gcloud.datastore import _implicit_environ
        IMPLICIT_DATASET_ID = 'IMPLICIT'
        with self._monkey(IMPLICIT_DATASET_ID):
            self._callFUT(None)
        self.assertEqual(_implicit_environ.DATASET_ID, IMPLICIT_DATASET_ID)

    def test_set_implicit_from_appengine(self):
        from gcloud.datastore import _implicit_environ

        APP_ENGINE_ID = 'GAE'
        APP_IDENTITY = _AppIdentity(APP_ENGINE_ID)

        with self._monkey(None, app_identity=APP_IDENTITY):
            self._callFUT()

        self.assertEqual(_implicit_environ.DATASET_ID, APP_ENGINE_ID)

    def test_set_implicit_both_env_and_appengine(self):
        from gcloud.datastore import _implicit_environ

        IMPLICIT_DATASET_ID = 'IMPLICIT'
        APP_IDENTITY = _AppIdentity('GAE')

        with self._monkey(IMPLICIT_DATASET_ID, app_identity=APP_IDENTITY):
            self._callFUT()

        self.assertEqual(_implicit_environ.DATASET_ID, IMPLICIT_DATASET_ID)

    def _implicit_compute_engine_helper(self, status):
        from gcloud.datastore import _implicit_environ

        COMPUTE_ENGINE_ID = 'GCE'
        HTTPLIB = _Httplib(COMPUTE_ENGINE_ID, status=status)
        if status == 200:
            EXPECTED_ID = COMPUTE_ENGINE_ID
        else:
            EXPECTED_ID = None

        with self._monkey(None, httplib=HTTPLIB):
            self._callFUT()

        self.assertEqual(_implicit_environ.DATASET_ID, EXPECTED_ID)
        self.assertEqual(len(HTTPLIB._http_connections), 1)

        (host, timeout, http_connection), = HTTPLIB._http_connections
        self.assertEqual(host, '169.254.169.254')
        self.assertEqual(timeout, 0.1)
        self.assertEqual(
            http_connection._called_args,
            [('GET', '/computeMetadata/v1/project/project-id')])
        expected_kwargs = {
            'headers': {
                'Metadata-Flavor': 'Google',
            },
        }
        self.assertEqual(http_connection._called_kwargs, [expected_kwargs])
        self.assertEqual(http_connection._close_count, 1)

    def test_set_implicit_from_compute_engine(self):
        self._implicit_compute_engine_helper(200)

    def test_set_implicit_from_compute_engine_bad_status(self):
        self._implicit_compute_engine_helper(404)

    def test_set_implicit_from_compute_engine_raise_timeout(self):
        self._implicit_compute_engine_helper('RAISE')

    def test_set_implicit_both_appengine_and_compute(self):
        from gcloud.datastore import _implicit_environ

        APP_ENGINE_ID = 'GAE'
        APP_IDENTITY = _AppIdentity(APP_ENGINE_ID)
        HTTPLIB = _Httplib('GCE')

        with self._monkey(None, httplib=HTTPLIB, app_identity=APP_IDENTITY):
            self._callFUT()

        self.assertEqual(_implicit_environ.DATASET_ID, APP_ENGINE_ID)
        self.assertEqual(len(HTTPLIB._http_connections), 0)

    def test_set_implicit_three_env_appengine_and_compute(self):
        from gcloud.datastore import _implicit_environ

        IMPLICIT_DATASET_ID = 'IMPLICIT'
        APP_IDENTITY = _AppIdentity('GAE')
        HTTPLIB = _Httplib('GCE')

        with self._monkey(IMPLICIT_DATASET_ID, httplib=HTTPLIB,
                          app_identity=APP_IDENTITY):
            self._callFUT()

        self.assertEqual(_implicit_environ.DATASET_ID, IMPLICIT_DATASET_ID)
        self.assertEqual(len(HTTPLIB._http_connections), 0)


class Test_set_default_connection(unittest2.TestCase):

    def setUp(self):
        from gcloud.datastore import _implicit_environ
        self._replaced_connection = _implicit_environ.CONNECTION
        _implicit_environ.CONNECTION = None

    def tearDown(self):
        from gcloud.datastore import _implicit_environ
        _implicit_environ.CONNECTION = self._replaced_connection

    def _callFUT(self, connection=None):
        from gcloud.datastore import set_default_connection
        return set_default_connection(connection=connection)

    def test_set_explicit(self):
        from gcloud.datastore import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)
        fake_cnxn = object()
        self._callFUT(connection=fake_cnxn)
        self.assertEqual(_implicit_environ.CONNECTION, fake_cnxn)

    def test_set_implicit(self):
        from gcloud._testing import _Monkey
        from gcloud import datastore
        from gcloud.datastore import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)

        fake_cnxn = object()
        with _Monkey(datastore, get_connection=lambda: fake_cnxn):
            self._callFUT()

        self.assertEqual(_implicit_environ.CONNECTION, fake_cnxn)


class Test_set_defaults(unittest2.TestCase):

    def _callFUT(self, dataset_id=None, connection=None):
        from gcloud.datastore import set_defaults
        return set_defaults(dataset_id=dataset_id, connection=connection)

    def test_it(self):
        from gcloud._testing import _Monkey
        from gcloud import datastore

        DATASET_ID = object()
        CONNECTION = object()

        SET_DATASET_CALLED = []

        def call_set_dataset(dataset_id=None):
            SET_DATASET_CALLED.append(dataset_id)

        SET_CONNECTION_CALLED = []

        def call_set_connection(connection=None):
            SET_CONNECTION_CALLED.append(connection)

        with _Monkey(datastore, set_default_dataset_id=call_set_dataset,
                     set_default_connection=call_set_connection):
            self._callFUT(dataset_id=DATASET_ID, connection=CONNECTION)

        self.assertEqual(SET_DATASET_CALLED, [DATASET_ID])
        self.assertEqual(SET_CONNECTION_CALLED, [CONNECTION])


class Test_get_connection(unittest2.TestCase):

    def _callFUT(self):
        from gcloud.datastore import get_connection
        return get_connection()

    def test_it(self):
        from gcloud import credentials
        from gcloud.datastore.connection import Connection
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey

        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT()
        self.assertTrue(isinstance(found, Connection))
        self.assertTrue(found._credentials is client._signed)
        self.assertTrue(client._get_app_default_called)


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


class _HTTPConnection(object):

    def __init__(self, parent):
        self.parent = parent
        self._close_count = 0
        self._called_args = []
        self._called_kwargs = []

    def request(self, method, uri, **kwargs):
        self._called_args.append((method, uri))
        self._called_kwargs.append(kwargs)

    def getresponse(self):
        import socket

        if self.parent.status == 'RAISE':
            raise socket.timeout('timed out')
        else:
            return _HTTPResponse(self.parent.status, self.parent.project_id)

    def close(self):
        self._close_count += 1


class _Httplib(object):

    def __init__(self, project_id, status=200):
        self.project_id = project_id
        self.status = status
        self._http_connections = []

    def HTTPConnection(self, host, timeout=None):
        result = _HTTPConnection(self)
        self._http_connections.append((host, timeout, result))
        return result
