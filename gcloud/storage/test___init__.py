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
