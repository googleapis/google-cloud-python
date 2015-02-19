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


class Test_get_default_connection(unittest2.TestCase):

    def setUp(self):
        from gcloud.datastore._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.datastore._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self):
        from gcloud.datastore._implicit_environ import get_default_connection
        return get_default_connection()

    def test_default(self):
        self.assertEqual(self._callFUT(), None)

    def test_preset(self):
        from gcloud.datastore._testing import _monkey_defaults

        SENTINEL = object()
        with _monkey_defaults(connection=SENTINEL):
            self.assertEqual(self._callFUT(), SENTINEL)


class Test_get_default_dataset_id(unittest2.TestCase):

    def setUp(self):
        from gcloud.datastore._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.datastore._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self):
        from gcloud.datastore._implicit_environ import get_default_dataset_id
        return get_default_dataset_id()

    def test_default(self):
        self.assertEqual(self._callFUT(), None)

    def test_preset(self):
        from gcloud.datastore._testing import _monkey_defaults

        SENTINEL = object()
        with _monkey_defaults(dataset_id=SENTINEL):
            self.assertEqual(self._callFUT(), SENTINEL)


class Test_set_default_dataset_id(unittest2.TestCase):

    def setUp(self):
        from gcloud.datastore._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.datastore._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self, dataset_id=None):
        from gcloud.datastore._implicit_environ import set_default_dataset_id
        return set_default_dataset_id(dataset_id=dataset_id)

    def _monkeyEnviron(self, implicit_dataset_id, environ=None):
        import os
        from gcloud._testing import _Monkey
        from gcloud.datastore._implicit_environ import _DATASET_ENV_VAR_NAME
        environ = environ or {_DATASET_ENV_VAR_NAME: implicit_dataset_id}
        return _Monkey(os, getenv=environ.get)

    def _monkeyImplicit(self, connection=None, app_identity=None):
        from gcloud._testing import _Monkey
        from gcloud.datastore import _implicit_environ

        if connection is None:
            connection = _HTTPConnection(404, None)

        def _factory(host, timeout):
            connection.host = host
            connection.timeout = timeout
            return connection

        return _Monkey(_implicit_environ,
                       HTTPConnection=_factory,
                       app_identity=app_identity)

    def test_no_env_var_set(self):
        from gcloud.datastore import _implicit_environ

        with self._monkeyEnviron(None):
            with self._monkeyImplicit():
                self.assertRaises(EnvironmentError, self._callFUT)

        self.assertEqual(_implicit_environ.get_default_dataset_id(), None)

    def test_set_from_env_var(self):
        from gcloud.datastore import _implicit_environ
        IMPLICIT_DATASET_ID = 'IMPLICIT'

        with self._monkeyEnviron(IMPLICIT_DATASET_ID):
            with self._monkeyImplicit():
                self._callFUT()

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         IMPLICIT_DATASET_ID)

    def test_set_explicit_w_env_var_set(self):
        from gcloud.datastore import _implicit_environ
        EXPLICIT_DATASET_ID = 'EXPLICIT'

        with self._monkeyEnviron(None):
            with self._monkeyImplicit():
                self._callFUT(EXPLICIT_DATASET_ID)

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         EXPLICIT_DATASET_ID)

    def test_set_explicit_no_env_var_set(self):
        from gcloud.datastore import _implicit_environ
        IMPLICIT_DATASET_ID = 'IMPLICIT'
        EXPLICIT_DATASET_ID = 'EXPLICIT'

        with self._monkeyEnviron(IMPLICIT_DATASET_ID):
            with self._monkeyImplicit():
                self._callFUT(EXPLICIT_DATASET_ID)

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         EXPLICIT_DATASET_ID)

    def test_set_explicit_None_wo_env_var_set(self):
        from gcloud.datastore import _implicit_environ

        with self._monkeyEnviron(None):
            with self._monkeyImplicit():
                self.assertRaises(EnvironmentError, self._callFUT, None)

        self.assertEqual(_implicit_environ.get_default_dataset_id(), None)

    def test_set_explicit_None_w_env_var_set(self):
        from gcloud.datastore import _implicit_environ
        IMPLICIT_DATASET_ID = 'IMPLICIT'

        with self._monkeyEnviron(IMPLICIT_DATASET_ID):
            with self._monkeyImplicit():
                self._callFUT(None)

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         IMPLICIT_DATASET_ID)

    def test_set_from_gcd_env_var(self):
        from gcloud.datastore import _implicit_environ

        GCD_ENV = _implicit_environ._GCD_DATASET_ENV_VAR_NAME
        GCD_DATASET_ID = 'GCD-IMPLICIT'
        ENVIRON = {GCD_ENV: GCD_DATASET_ID}

        with self._monkeyEnviron(None, environ=ENVIRON):
            with self._monkeyImplicit():
                self._callFUT()

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         GCD_DATASET_ID)

    def test_set_gcd_and_production_env_vars(self):
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore._implicit_environ import _DATASET_ENV_VAR_NAME

        GCD_ENV = _implicit_environ._GCD_DATASET_ENV_VAR_NAME
        IMPLICIT_DATASET_ID = 'IMPLICIT'
        GCD_DATASET_ID = 'GCD-IMPLICIT'
        ENVIRON = {
            _DATASET_ENV_VAR_NAME: IMPLICIT_DATASET_ID,
            GCD_ENV: GCD_DATASET_ID,
        }

        with self._monkeyEnviron(None, environ=ENVIRON):
            with self._monkeyImplicit():
                self._callFUT()

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         IMPLICIT_DATASET_ID)

    def test_set_gcd_env_vars_and_appengine(self):
        from gcloud.datastore import _implicit_environ

        GCD_ENV = _implicit_environ._GCD_DATASET_ENV_VAR_NAME
        GCD_DATASET_ID = 'GCD-IMPLICIT'
        ENVIRON = {GCD_ENV: GCD_DATASET_ID}

        APP_ENGINE_ID = 'GAE'
        APP_IDENTITY = _AppIdentity(APP_ENGINE_ID)

        with self._monkeyEnviron(None, environ=ENVIRON):
            with self._monkeyImplicit(app_identity=APP_IDENTITY):
                self._callFUT()

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         GCD_DATASET_ID)

    def test_set_implicit_from_appengine(self):
        from gcloud.datastore import _implicit_environ

        APP_ENGINE_ID = 'GAE'
        APP_IDENTITY = _AppIdentity(APP_ENGINE_ID)

        with self._monkeyEnviron(None):
            with self._monkeyImplicit(app_identity=APP_IDENTITY):
                self._callFUT()

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         APP_ENGINE_ID)

    def test_set_implicit_both_env_and_appengine(self):
        from gcloud.datastore import _implicit_environ

        IMPLICIT_DATASET_ID = 'IMPLICIT'
        APP_IDENTITY = _AppIdentity('GAE')

        with self._monkeyEnviron(IMPLICIT_DATASET_ID):
            with self._monkeyImplicit(app_identity=APP_IDENTITY):
                self._callFUT()

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         IMPLICIT_DATASET_ID)

    def _implicit_compute_engine_helper(self, status):
        from gcloud.datastore import _implicit_environ

        COMPUTE_ENGINE_ID = 'GCE'
        if status == 200:
            EXPECTED_ID = COMPUTE_ENGINE_ID
        else:
            EXPECTED_ID = None

        if status == 'RAISE':
            connection = _TimeoutHTTPConnection()
        else:
            connection = _HTTPConnection(status, EXPECTED_ID)

        with self._monkeyEnviron(None):
            with self._monkeyImplicit(connection=connection):
                if EXPECTED_ID is None:
                    self.assertRaises(EnvironmentError, self._callFUT)
                else:
                    self._callFUT()

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         EXPECTED_ID)
        self.assertEqual(connection.host, '169.254.169.254')
        self.assertEqual(connection.timeout, 0.1)
        self.assertEqual(
            connection._called_args,
            [('GET', '/computeMetadata/v1/project/project-id')])
        expected_kwargs = {
            'headers': {
                'Metadata-Flavor': 'Google',
            },
        }
        self.assertEqual(connection._called_kwargs, [expected_kwargs])
        self.assertEqual(connection._close_count, 1)

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
        connection = _HTTPConnection(200, 'GCE')

        with self._monkeyEnviron(None):
            with self._monkeyImplicit(connection=connection,
                                      app_identity=APP_IDENTITY):
                self._callFUT()

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         APP_ENGINE_ID)
        self.assertEqual(connection.host, None)
        self.assertEqual(connection.timeout, None)

    def test_set_implicit_three_env_appengine_and_compute(self):
        from gcloud.datastore import _implicit_environ

        IMPLICIT_DATASET_ID = 'IMPLICIT'
        APP_IDENTITY = _AppIdentity('GAE')
        connection = _HTTPConnection(200, 'GCE')

        with self._monkeyEnviron(IMPLICIT_DATASET_ID):
            with self._monkeyImplicit(connection=connection,
                                      app_identity=APP_IDENTITY):
                self._callFUT()

        self.assertEqual(_implicit_environ.get_default_dataset_id(),
                         IMPLICIT_DATASET_ID)
        self.assertEqual(connection.host, None)
        self.assertEqual(connection.timeout, None)


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
