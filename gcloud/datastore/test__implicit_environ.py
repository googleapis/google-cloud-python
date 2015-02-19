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
