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


class TestDataset(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.dataset import Dataset
        return Dataset

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_missing_dataset_id(self):
        self.assertRaises(TypeError, self._makeOne)

    def test_ctor_defaults(self):
        DATASET_ID = 'DATASET'
        dataset = self._makeOne(DATASET_ID)
        self.assertEqual(dataset.id(), DATASET_ID)
        self.assertEqual(dataset.connection(), None)

    def test_ctor_explicit(self):
        DATASET_ID = 'DATASET'
        CONNECTION = object()
        dataset = self._makeOne(DATASET_ID, CONNECTION)
        self.assertEqual(dataset.id(), DATASET_ID)
        self.assertTrue(dataset.connection() is CONNECTION)
