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

    def _monkey(self, implicit_dataset_id):
        import os
        from gcloud.datastore import _DATASET_ENV_VAR_NAME
        from gcloud._testing import _Monkey
        environ = {_DATASET_ENV_VAR_NAME: implicit_dataset_id}
        return _Monkey(os, getenv=environ.get)

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
