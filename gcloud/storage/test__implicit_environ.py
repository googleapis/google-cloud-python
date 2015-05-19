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


class Test__require_connection(unittest2.TestCase):

    def _callFUT(self, connection=None):
        from gcloud.storage._implicit_environ import _require_connection
        return _require_connection(connection=connection)

    def _monkey(self, connection):
        from gcloud.storage._testing import _monkey_defaults
        return _monkey_defaults(connection=connection)

    def test_implicit_unset(self):
        with self._monkey(None):
            with self.assertRaises(EnvironmentError):
                self._callFUT()

    def test_implicit_unset_w_existing_batch(self):
        CONNECTION = object()
        with self._monkey(None):
            with _NoCommitBatch(connection=CONNECTION):
                self.assertEqual(self._callFUT(), CONNECTION)

    def test_implicit_unset_passed_explicitly(self):
        CONNECTION = object()
        with self._monkey(None):
            self.assertTrue(self._callFUT(CONNECTION) is CONNECTION)

    def test_implicit_set(self):
        IMPLICIT_CONNECTION = object()
        with self._monkey(IMPLICIT_CONNECTION):
            self.assertTrue(self._callFUT() is IMPLICIT_CONNECTION)

    def test_implicit_set_passed_explicitly(self):
        IMPLICIT_CONNECTION = object()
        CONNECTION = object()
        with self._monkey(IMPLICIT_CONNECTION):
            self.assertTrue(self._callFUT(CONNECTION) is CONNECTION)


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
        from gcloud import credentials
        from gcloud._testing import _Monkey
        from gcloud.test_credentials import _Client
        from gcloud.storage import _implicit_environ
        from gcloud.storage.connection import Connection

        self.assertEqual(_implicit_environ.get_default_connection(), None)

        client = _Client()
        with _Monkey(credentials, client=client):
            self._callFUT()

        found = _implicit_environ.get_default_connection()
        self.assertTrue(isinstance(found, Connection))


class Test_lazy_loading(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage._testing import _setup_defaults
        _setup_defaults(self, implicit=True)

    def tearDown(self):
        from gcloud.storage._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def test_descriptor_for_connection(self):
        from gcloud import credentials
        from gcloud._testing import _Monkey
        from gcloud.test_credentials import _Client
        from gcloud.storage import _implicit_environ
        from gcloud.storage.connection import Connection

        self.assertFalse(
            'connection' in _implicit_environ._DEFAULTS.__dict__)

        client = _Client()
        with _Monkey(credentials, client=client):
            lazy_loaded = _implicit_environ._DEFAULTS.connection

        self.assertTrue(isinstance(lazy_loaded, Connection))
        self.assertTrue(
            'connection' in _implicit_environ._DEFAULTS.__dict__)


class _NoCommitBatch(object):

    def __init__(self, connection):
        self._connection = connection

    def __enter__(self):
        from gcloud.storage.connection import _CONNECTIONS
        _CONNECTIONS.push(self._connection)
        return self._connection

    def __exit__(self, *args):
        from gcloud.storage.connection import _CONNECTIONS
        _CONNECTIONS.pop()
