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


class TestColumnFamily(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.column_family import ColumnFamily
        return ColumnFamily

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        column_family_id = u'column-family-id'
        table = object()
        column_family = self._makeOne(column_family_id, table)

        self.assertEqual(column_family.column_family_id, column_family_id)
        self.assertTrue(column_family._table is table)
