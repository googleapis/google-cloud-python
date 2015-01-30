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
        PROJECT = 'project'
        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT(PROJECT)
        self.assertTrue(isinstance(found, Connection))
        self.assertEqual(found.project, PROJECT)
        self.assertTrue(found._credentials is client._signed)
        self.assertTrue(client._get_app_default_called)


class Test_get_bucket(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.storage import get_bucket
        return get_bucket(*args, **kw)

    def test_it(self):
        from gcloud import storage
        from gcloud._testing import _Monkey

        bucket = object()

        class _Connection(object):

            def get_bucket(self, bucket_name):
                self._called_with = bucket_name
                return bucket

        connection = _Connection()
        _called_with = []

        def get_connection(*args, **kw):
            _called_with.append((args, kw))
            return connection

        BUCKET = 'bucket'
        PROJECT = 'project'
        with _Monkey(storage, get_connection=get_connection):
            found = self._callFUT(BUCKET, PROJECT)

        self.assertTrue(found is bucket)
        self.assertEqual(_called_with, [((PROJECT,), {})])
        self.assertEqual(connection._called_with, BUCKET)


class Test_set_default_bucket(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage import _implicit_environ
        self._replaced_bucket = _implicit_environ.BUCKET
        _implicit_environ.BUCKET = None

    def tearDown(self):
        from gcloud.storage import _implicit_environ
        _implicit_environ.BUCKET = self._replaced_bucket

    def _callFUT(self, bucket=None):
        from gcloud.storage import set_default_bucket
        return set_default_bucket(bucket=bucket)

    def _monkeyEnviron(self, implicit_bucket_name):
        import os

        from gcloud._testing import _Monkey
        from gcloud.storage import _BUCKET_ENV_VAR_NAME

        environ = {_BUCKET_ENV_VAR_NAME: implicit_bucket_name}
        return _Monkey(os, getenv=environ.get)

    def _monkeyImplicit(self, connection):
        from gcloud._testing import _Monkey
        from gcloud.storage import _implicit_environ

        return _Monkey(_implicit_environ, CONNECTION=connection)

    def test_no_env_var_set(self):
        from gcloud.storage import _implicit_environ
        with self._monkeyEnviron(None):
            with self._monkeyImplicit(None):
                self._callFUT()
        self.assertEqual(_implicit_environ.BUCKET, None)

    def test_set_from_env_var(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_BUCKET_NAME = 'IMPLICIT'
        CONNECTION = object()
        with self._monkeyEnviron(IMPLICIT_BUCKET_NAME):
            with self._monkeyImplicit(CONNECTION):
                self._callFUT()

        self.assertEqual(_implicit_environ.BUCKET.name, IMPLICIT_BUCKET_NAME)
        self.assertEqual(_implicit_environ.BUCKET.connection, CONNECTION)

    def test_set_explicit_w_env_var_set(self):
        from gcloud.storage import _implicit_environ
        EXPLICIT_BUCKET = object()
        with self._monkeyEnviron(None):
            with self._monkeyImplicit(None):
                self._callFUT(EXPLICIT_BUCKET)
        self.assertEqual(_implicit_environ.BUCKET, EXPLICIT_BUCKET)

    def test_set_explicit_no_env_var_set(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_BUCKET_NAME = 'IMPLICIT'
        CONNECTION = object()
        EXPLICIT_BUCKET = object()
        with self._monkeyEnviron(IMPLICIT_BUCKET_NAME):
            with self._monkeyImplicit(CONNECTION):
                self._callFUT(EXPLICIT_BUCKET)
        self.assertEqual(_implicit_environ.BUCKET, EXPLICIT_BUCKET)

    def test_set_explicit_None_wo_env_var_set(self):
        from gcloud.storage import _implicit_environ
        CONNECTION = object()
        with self._monkeyEnviron(None):
            with self._monkeyImplicit(CONNECTION):
                self._callFUT(None)
        self.assertEqual(_implicit_environ.BUCKET, None)

    def test_set_explicit_None_wo_connection_set(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_BUCKET_NAME = 'IMPLICIT'
        with self._monkeyEnviron(IMPLICIT_BUCKET_NAME):
            with self._monkeyImplicit(None):
                self._callFUT(None)
        self.assertEqual(_implicit_environ.BUCKET, None)

    def test_set_explicit_None_w_env_var_set(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_BUCKET_NAME = 'IMPLICIT'
        CONNECTION = object()
        with self._monkeyEnviron(IMPLICIT_BUCKET_NAME):
            with self._monkeyImplicit(CONNECTION):
                self._callFUT(None)
        self.assertEqual(_implicit_environ.BUCKET.name, IMPLICIT_BUCKET_NAME)
        self.assertEqual(_implicit_environ.BUCKET.connection, CONNECTION)


class Test_set_default_project(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage import _implicit_environ
        self._replaced_project = _implicit_environ.PROJECT
        _implicit_environ.PROJECT = None

    def tearDown(self):
        from gcloud.storage import _implicit_environ
        _implicit_environ.PROJECT = self._replaced_project

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
        self.assertEqual(_implicit_environ.PROJECT, None)

    def test_set_from_env_var(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_PROJECT = 'IMPLICIT'
        with self._monkey(IMPLICIT_PROJECT):
            self._callFUT()
        self.assertEqual(_implicit_environ.PROJECT, IMPLICIT_PROJECT)

    def test_set_explicit_w_env_var_set(self):
        from gcloud.storage import _implicit_environ
        EXPLICIT_PROJECT = 'EXPLICIT'
        with self._monkey(None):
            self._callFUT(EXPLICIT_PROJECT)
        self.assertEqual(_implicit_environ.PROJECT, EXPLICIT_PROJECT)

    def test_set_explicit_no_env_var_set(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_PROJECT = 'IMPLICIT'
        EXPLICIT_PROJECT = 'EXPLICIT'
        with self._monkey(IMPLICIT_PROJECT):
            self._callFUT(EXPLICIT_PROJECT)
        self.assertEqual(_implicit_environ.PROJECT, EXPLICIT_PROJECT)

    def test_set_explicit_None_wo_env_var_set(self):
        from gcloud.storage import _implicit_environ
        with self._monkey(None):
            self._callFUT(None)
        self.assertEqual(_implicit_environ.PROJECT, None)

    def test_set_explicit_None_w_env_var_set(self):
        from gcloud.storage import _implicit_environ
        IMPLICIT_PROJECT = 'IMPLICIT'
        with self._monkey(IMPLICIT_PROJECT):
            self._callFUT(None)
        self.assertEqual(_implicit_environ.PROJECT, IMPLICIT_PROJECT)


class Test_set_default_connection(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage import _implicit_environ
        self._replaced_connection = _implicit_environ.CONNECTION
        _implicit_environ.CONNECTION = None

    def tearDown(self):
        from gcloud.storage import _implicit_environ
        _implicit_environ.CONNECTION = self._replaced_connection

    def _callFUT(self, project=None, connection=None):
        from gcloud.storage import set_default_connection
        return set_default_connection(project=project, connection=connection)

    def test_set_explicit(self):
        from gcloud.storage import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)
        fake_cnxn = object()
        self._callFUT(connection=fake_cnxn)
        self.assertEqual(_implicit_environ.CONNECTION, fake_cnxn)

    def test_set_implicit_no_project(self):
        from gcloud._testing import _Monkey
        from gcloud import storage
        from gcloud.storage import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)

        fake_cnxn = object()
        _called_args = []
        _called_kwargs = []

        def mock_get_connection(*args, **kwargs):
            _called_args.append(args)
            _called_kwargs.append(kwargs)
            return fake_cnxn

        with _Monkey(storage, get_connection=mock_get_connection):
            self._callFUT()

        self.assertEqual(_implicit_environ.CONNECTION, fake_cnxn)
        self.assertEqual(_called_args, [(None,)])
        self.assertEqual(_called_kwargs, [{}])

    def test_set_implicit_with_implicit_project(self):
        from gcloud._testing import _Monkey
        from gcloud import storage
        from gcloud.storage import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)

        fake_cnxn = object()
        _called_args = []
        _called_kwargs = []

        def mock_get_connection(*args, **kwargs):
            _called_args.append(args)
            _called_kwargs.append(kwargs)
            return fake_cnxn

        PROJECT = 'project'

        with _Monkey(_implicit_environ, PROJECT=PROJECT):
            with _Monkey(storage, get_connection=mock_get_connection):
                self._callFUT()

        self.assertEqual(_implicit_environ.CONNECTION, fake_cnxn)
        self.assertEqual(_called_args, [(PROJECT,)])
        self.assertEqual(_called_kwargs, [{}])

    def test_set_implicit_with_explicit_project(self):
        from gcloud._testing import _Monkey
        from gcloud import storage
        from gcloud.storage import _implicit_environ

        self.assertEqual(_implicit_environ.CONNECTION, None)

        fake_cnxn = object()
        _called_args = []
        _called_kwargs = []

        def mock_get_connection(*args, **kwargs):
            _called_args.append(args)
            _called_kwargs.append(kwargs)
            return fake_cnxn

        PROJECT = 'project'

        with _Monkey(storage, get_connection=mock_get_connection):
            self._callFUT(PROJECT)

        self.assertEqual(_implicit_environ.CONNECTION, fake_cnxn)
        self.assertEqual(_called_args, [(PROJECT,)])
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

        def call_set_connection(project=None, connection=None):
            SET_CONNECTION_CALLED.append((project, connection))

        with _Monkey(storage, set_default_bucket=call_set_bucket,
                     set_default_connection=call_set_connection,
                     set_default_project=call_set_project):
            self._callFUT(bucket=BUCKET, project=PROJECT,
                          connection=CONNECTION)

        self.assertEqual(SET_PROJECT_CALLED, [PROJECT])
        self.assertEqual(SET_CONNECTION_CALLED, [(PROJECT, CONNECTION)])
        self.assertEqual(SET_BUCKET_CALLED, [BUCKET])
