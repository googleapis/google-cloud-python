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


class Test_set_default_connection(unittest2.TestCase):

    def setUp(self):
        from gcloud.datastore._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.datastore._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self, connection=None):
        from gcloud.datastore import set_default_connection
        return set_default_connection(connection=connection)

    def test_set_explicit(self):
        from gcloud.datastore import _implicit_environ

        self.assertEqual(_implicit_environ.get_default_connection(), None)
        fake_cnxn = object()
        self._callFUT(connection=fake_cnxn)
        self.assertEqual(_implicit_environ.get_default_connection(), fake_cnxn)

    def test_set_implicit(self):
        from gcloud._testing import _Monkey
        from gcloud import datastore
        from gcloud.datastore import _implicit_environ

        self.assertEqual(_implicit_environ.get_default_connection(), None)

        fake_cnxn = object()
        with _Monkey(datastore, get_connection=lambda: fake_cnxn):
            self._callFUT()

        self.assertEqual(_implicit_environ.get_default_connection(), fake_cnxn)


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
