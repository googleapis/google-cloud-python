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


class Test_get_connection(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.storage import get_connection
        return get_connection(*args, **kw)

    def test_it(self):
        from gcloud import credentials
        from gcloud.storage.connection import Connection
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey
        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT()
        self.assertTrue(isinstance(found, Connection))
        self.assertTrue(found._credentials is client._signed)
        self.assertTrue(client._get_app_default_called)


class Test_set_default_bucket(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.storage._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self, bucket=None):
        from gcloud.storage import set_default_bucket
        return set_default_bucket(bucket=bucket)

    def _monkeyEnviron(self, implicit_bucket_name):
        import os

        from gcloud._testing import _Monkey
        from gcloud.storage import _BUCKET_ENV_VAR_NAME

        environ = {_BUCKET_ENV_VAR_NAME: implicit_bucket_name}
        return _Monkey(os, getenv=environ.get)

    def test_no_env_var_set(self):
        from gcloud.storage._testing import _monkey_defaults
        from gcloud.storage import _implicit_environ

        with self._monkeyEnviron(None):
            with _monkey_defaults():
                self._callFUT()
                self.assertEqual(_implicit_environ.get_default_bucket(), None)

    def test_set_from_env_var(self):
        from gcloud.storage._testing import _monkey_defaults
        from gcloud.storage import _implicit_environ
        IMPLICIT_BUCKET_NAME = 'IMPLICIT'
        CONNECTION = object()
        with self._monkeyEnviron(IMPLICIT_BUCKET_NAME):
            with _monkey_defaults(connection=CONNECTION):
                self._callFUT()

                default_bucket = _implicit_environ.get_default_bucket()
                self.assertEqual(default_bucket.name, IMPLICIT_BUCKET_NAME)
                self.assertEqual(default_bucket.connection, CONNECTION)

    def test_set_explicit_w_env_var_set(self):
        from gcloud.storage._testing import _monkey_defaults
        from gcloud.storage import _implicit_environ
        EXPLICIT_BUCKET = object()
        with self._monkeyEnviron(None):
            with _monkey_defaults():
                self._callFUT(EXPLICIT_BUCKET)

                self.assertEqual(_implicit_environ.get_default_bucket(),
                                 EXPLICIT_BUCKET)

    def test_set_explicit_no_env_var_set(self):
        from gcloud.storage._testing import _monkey_defaults
        from gcloud.storage import _implicit_environ
        IMPLICIT_BUCKET_NAME = 'IMPLICIT'
        CONNECTION = object()
        EXPLICIT_BUCKET = object()
        with self._monkeyEnviron(IMPLICIT_BUCKET_NAME):
            with _monkey_defaults(connection=CONNECTION):
                self._callFUT(EXPLICIT_BUCKET)

                self.assertEqual(_implicit_environ.get_default_bucket(),
                                 EXPLICIT_BUCKET)

    def test_set_explicit_None_wo_env_var_set(self):
        from gcloud.storage._testing import _monkey_defaults
        from gcloud.storage import _implicit_environ
        CONNECTION = object()
        with self._monkeyEnviron(None):
            with _monkey_defaults(connection=CONNECTION):
                self._callFUT(None)
        self.assertEqual(_implicit_environ.get_default_bucket(), None)

    def test_set_explicit_None_wo_connection_set(self):
        from gcloud.storage._testing import _monkey_defaults
        from gcloud.storage import _implicit_environ
        IMPLICIT_BUCKET_NAME = 'IMPLICIT'
        with self._monkeyEnviron(IMPLICIT_BUCKET_NAME):
            with _monkey_defaults():
                self._callFUT(None)
        self.assertEqual(_implicit_environ.get_default_bucket(), None)

    def test_set_explicit_None_w_env_var_set(self):
        from gcloud.storage._testing import _monkey_defaults
        from gcloud.storage import _implicit_environ
        IMPLICIT_BUCKET_NAME = 'IMPLICIT'
        CONNECTION = object()
        with self._monkeyEnviron(IMPLICIT_BUCKET_NAME):
            with _monkey_defaults(connection=CONNECTION):
                self._callFUT(None)

                default_bucket = _implicit_environ.get_default_bucket()
                self.assertEqual(default_bucket.name, IMPLICIT_BUCKET_NAME)
                self.assertEqual(default_bucket.connection, CONNECTION)


class Test_set_default_project(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.storage._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self, project=None):
        from gcloud.storage import set_default_project
        return set_default_project(project=project)

    def _monkey(self, implicit_project):
        import os
        from gcloud.storage import _PROJECT_ENV_VAR_NAME
        from gcloud._testing import _Monkey
        environ = {_PROJECT_ENV_VAR_NAME: implicit_project}
        return _Monkey(os, getenv=environ.get)

    def test_no_env_var_set(self):
        from gcloud.storage import _implicit_environ
        with self._monkey(None):
            self._callFUT()
        self.assertEqual(_implicit_environ.get_default_project(), None)

    def test_set_from_env_var(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_PROJECT = 'IMPLICIT'
        with self._monkey(IMPLICIT_PROJECT):
            self._callFUT()
        self.assertEqual(_implicit_environ.get_default_project(),
                         IMPLICIT_PROJECT)

    def test_set_explicit_w_env_var_set(self):
        from gcloud.storage import _implicit_environ
        EXPLICIT_PROJECT = 'EXPLICIT'
        with self._monkey(None):
            self._callFUT(EXPLICIT_PROJECT)
        self.assertEqual(_implicit_environ.get_default_project(),
                         EXPLICIT_PROJECT)

    def test_set_explicit_no_env_var_set(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_PROJECT = 'IMPLICIT'
        EXPLICIT_PROJECT = 'EXPLICIT'
        with self._monkey(IMPLICIT_PROJECT):
            self._callFUT(EXPLICIT_PROJECT)
        self.assertEqual(_implicit_environ.get_default_project(),
                         EXPLICIT_PROJECT)

    def test_set_explicit_None_wo_env_var_set(self):
        from gcloud.storage import _implicit_environ
        with self._monkey(None):
            self._callFUT(None)
        self.assertEqual(_implicit_environ.get_default_project(), None)

    def test_set_explicit_None_w_env_var_set(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_PROJECT = 'IMPLICIT'
        with self._monkey(IMPLICIT_PROJECT):
            self._callFUT(None)
        self.assertEqual(_implicit_environ.get_default_project(),
                         IMPLICIT_PROJECT)


class Test_set_default_connection(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.storage._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self, connection=None):
        from gcloud.storage import set_default_connection
        return set_default_connection(connection=connection)

    def test_set_explicit(self):
        from gcloud.storage import _implicit_environ

        self.assertEqual(_implicit_environ.get_default_connection(), None)
        fake_cnxn = object()
        self._callFUT(connection=fake_cnxn)
        self.assertEqual(_implicit_environ.get_default_connection(), fake_cnxn)

    def test_set_implicit(self):
        from gcloud._testing import _Monkey
        from gcloud import storage
        from gcloud.storage import _implicit_environ

        self.assertEqual(_implicit_environ.get_default_connection(), None)

        fake_cnxn = object()
        _called_args = []
        _called_kwargs = []

        def mock_get_connection(*args, **kwargs):
            _called_args.append(args)
            _called_kwargs.append(kwargs)
            return fake_cnxn

        with _Monkey(storage, get_connection=mock_get_connection):
            self._callFUT()

        self.assertEqual(_implicit_environ.get_default_connection(), fake_cnxn)
        self.assertEqual(_called_args, [()])
        self.assertEqual(_called_kwargs, [{}])


class Test_set_defaults(unittest2.TestCase):

    def _callFUT(self, bucket=None, project=None, connection=None):
        from gcloud.storage import set_defaults
        return set_defaults(bucket=bucket, project=project,
                            connection=connection)

    def test_it(self):
        from gcloud._testing import _Monkey
        from gcloud import storage

        BUCKET = object()
        PROJECT = object()
        CONNECTION = object()

        SET_BUCKET_CALLED = []

        def call_set_bucket(bucket=None):
            SET_BUCKET_CALLED.append(bucket)

        SET_PROJECT_CALLED = []

        def call_set_project(project=None):
            SET_PROJECT_CALLED.append(project)

        SET_CONNECTION_CALLED = []

        def call_set_connection(connection=None):
            SET_CONNECTION_CALLED.append(connection)

        with _Monkey(storage, set_default_bucket=call_set_bucket,
                     set_default_connection=call_set_connection,
                     set_default_project=call_set_project):
            self._callFUT(bucket=BUCKET, project=PROJECT,
                          connection=CONNECTION)

        self.assertEqual(SET_PROJECT_CALLED, [PROJECT])
        self.assertEqual(SET_CONNECTION_CALLED, [CONNECTION])
        self.assertEqual(SET_BUCKET_CALLED, [BUCKET])
