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


class Test_get_default_bucket(unittest2.TestCase):

    def _callFUT(self):
        from gcloud.storage._implicit_environ import get_default_bucket
        return get_default_bucket()

    def test_wo_override(self):
        self.assertTrue(self._callFUT() is None)


class Test_get_default_connection(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.storage._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self):
        from gcloud.storage._implicit_environ import get_default_connection
        return get_default_connection()

    def test_wo_override(self):
        self.assertTrue(self._callFUT() is None)


class Test_get_connection(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.storage._implicit_environ import get_connection
        return get_connection(*args, **kw)

    def test_it(self):
        from gcloud import credentials
        from gcloud.storage import SCOPE
        from gcloud.storage.connection import Connection
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey
        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT()
        self.assertTrue(isinstance(found, Connection))
        self.assertTrue(found._credentials is client._signed)
        self.assertEqual(found._credentials._scopes, SCOPE)
        self.assertTrue(client._get_app_default_called)


class Test_set_default_connection(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.storage._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self, connection=None):
        from gcloud.storage._implicit_environ import set_default_connection
        return set_default_connection(connection=connection)

    def test_set_explicit(self):
        from gcloud.storage import _implicit_environ

        self.assertEqual(_implicit_environ.get_default_connection(), None)
        fake_cnxn = object()
        self._callFUT(connection=fake_cnxn)
        self.assertEqual(_implicit_environ.get_default_connection(), fake_cnxn)

    def test_set_implicit(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import _implicit_environ

        self.assertEqual(_implicit_environ.get_default_connection(), None)

        fake_cnxn = object()
        _called_args = []
        _called_kwargs = []

        def mock_get_connection(*args, **kwargs):
            _called_args.append(args)
            _called_kwargs.append(kwargs)
            return fake_cnxn

        with _Monkey(_implicit_environ, get_connection=mock_get_connection):
            self._callFUT()

        self.assertEqual(_implicit_environ.get_default_connection(), fake_cnxn)
        self.assertEqual(_called_args, [()])
        self.assertEqual(_called_kwargs, [{}])


class Test_lazy_loading(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage._testing import _setup_defaults
        _setup_defaults(self, implicit=True)

    def tearDown(self):
        from gcloud.storage._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def test_descriptor_for_connection(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import _implicit_environ

        self.assertFalse(
            'connection' in _implicit_environ._DEFAULTS.__dict__)

        DEFAULT = object()

        with _Monkey(_implicit_environ, get_connection=lambda: DEFAULT):
            lazy_loaded = _implicit_environ._DEFAULTS.connection

        self.assertEqual(lazy_loaded, DEFAULT)
        self.assertTrue(
            'connection' in _implicit_environ._DEFAULTS.__dict__)
