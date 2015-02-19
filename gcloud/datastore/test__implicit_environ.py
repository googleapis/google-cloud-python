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

    def _callFUT(self):
        from gcloud.datastore._implicit_environ import get_default_connection
        return get_default_connection()

    def test_default(self):
        self.assertEqual(self._callFUT(), None)

    def test_preset(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import _implicit_environ

        SENTINEL = object()
        MOCK_DEFAULTS = _implicit_environ._DefaultsContainer(SENTINEL, None)
        with _Monkey(_implicit_environ, _DEFAULTS=MOCK_DEFAULTS):
            self.assertEqual(self._callFUT(), SENTINEL)


class Test_get_default_dataset_id(unittest2.TestCase):

    def _callFUT(self):
        from gcloud.datastore._implicit_environ import get_default_dataset_id
        return get_default_dataset_id()

    def test_default(self):
        self.assertEqual(self._callFUT(), None)

    def test_preset(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import _implicit_environ

        SENTINEL = object()
        MOCK_DEFAULTS = _implicit_environ._DefaultsContainer(None, SENTINEL)
        with _Monkey(_implicit_environ, _DEFAULTS=MOCK_DEFAULTS):
            self.assertEqual(self._callFUT(), SENTINEL)
