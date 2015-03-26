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


class Test_set_default_connection(unittest2.TestCase):

    def setUp(self):
        from gcloud.pubsub._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.pubsub._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self, connection=None):
        from gcloud.pubsub import set_default_connection
        return set_default_connection(connection=connection)

    def test_set_explicit(self):
        from gcloud.pubsub import _implicit_environ

        self.assertEqual(_implicit_environ.get_default_connection(), None)
        fake_cnxn = object()
        self._callFUT(connection=fake_cnxn)
        self.assertEqual(_implicit_environ.get_default_connection(), fake_cnxn)

    def test_set_implicit(self):
        from gcloud._testing import _Monkey
        from gcloud import pubsub
        from gcloud.pubsub import _implicit_environ

        self.assertEqual(_implicit_environ.get_default_connection(), None)

        fake_cnxn = object()
        _called_args = []
        _called_kwargs = []

        def mock_get_connection(*args, **kwargs):
            _called_args.append(args)
            _called_kwargs.append(kwargs)
            return fake_cnxn

        with _Monkey(pubsub, get_connection=mock_get_connection):
            self._callFUT()

        self.assertEqual(_implicit_environ.get_default_connection(), fake_cnxn)
        self.assertEqual(_called_args, [()])
        self.assertEqual(_called_kwargs, [{}])


class Test_set_defaults(unittest2.TestCase):

    def _callFUT(self, project=None, connection=None):
        from gcloud.pubsub import set_defaults
        return set_defaults(project=project, connection=connection)

    def test_it(self):
        from gcloud._testing import _Monkey
        from gcloud import pubsub

        PROJECT = object()
        CONNECTION = object()

        SET_PROJECT_CALLED = []

        def call_set_project(project=None):
            SET_PROJECT_CALLED.append(project)

        SET_CONNECTION_CALLED = []

        def call_set_connection(connection=None):
            SET_CONNECTION_CALLED.append(connection)

        with _Monkey(pubsub,
                     set_default_connection=call_set_connection,
                     set_default_project=call_set_project):
            self._callFUT(project=PROJECT, connection=CONNECTION)

        self.assertEqual(SET_PROJECT_CALLED, [PROJECT])
        self.assertEqual(SET_CONNECTION_CALLED, [CONNECTION])


class Test_get_connection(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.pubsub import get_connection
        return get_connection(*args, **kw)

    def test_it(self):
        from gcloud import credentials
        from gcloud.pubsub import SCOPE
        from gcloud.pubsub.connection import Connection
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey
        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT()
        self.assertTrue(isinstance(found, Connection))
        self.assertTrue(found._credentials is client._signed)
        self.assertEqual(found._credentials._scopes, SCOPE)
        self.assertTrue(client._get_app_default_called)
