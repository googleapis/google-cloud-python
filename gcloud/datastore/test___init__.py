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


class Test_get_dataset(unittest2.TestCase):

    def _callFUT(self, dataset_id):
        from gcloud.datastore import get_dataset
        return get_dataset(dataset_id)

    def test_it(self):
        from gcloud import credentials
        from gcloud.datastore.connection import Connection
        from gcloud.datastore.dataset import Dataset
        from gcloud.test_credentials import _Client
        from gcloud._testing import _Monkey

        DATASET_ID = 'DATASET'
        client = _Client()
        with _Monkey(credentials, client=client):
            found = self._callFUT(DATASET_ID)
        self.assertTrue(isinstance(found, Dataset))
        self.assertTrue(isinstance(found.connection(), Connection))
        self.assertEqual(found.id(), DATASET_ID)
        self.assertTrue(client._get_app_default_called)
