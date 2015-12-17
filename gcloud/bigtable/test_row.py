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


class TestRow(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row import Row
        return Row

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        row_key = b'row_key'
        table = object()

        row = self._makeOne(row_key, table)
        self.assertEqual(row._row_key, row_key)
        self.assertTrue(row._table is table)

    def test_constructor_with_unicode(self):
        row_key = u'row_key'
        row_key_bytes = b'row_key'
        table = object()

        row = self._makeOne(row_key, table)
        self.assertEqual(row._row_key, row_key_bytes)
        self.assertTrue(row._table is table)

    def test_constructor_with_non_bytes(self):
        row_key = object()
        with self.assertRaises(TypeError):
            self._makeOne(row_key, None)


class Test_RegexFilter(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row import _RegexFilter
        return _RegexFilter

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        regex = object()
        row_filter = self._makeOne(regex)
        self.assertTrue(row_filter.regex is regex)

    def test___eq__type_differ(self):
        regex = object()
        row_filter1 = self._makeOne(regex=regex)
        row_filter2 = object()
        self.assertNotEqual(row_filter1, row_filter2)

    def test___eq__same_value(self):
        regex = object()
        row_filter1 = self._makeOne(regex=regex)
        row_filter2 = self._makeOne(regex=regex)
        self.assertEqual(row_filter1, row_filter2)

    def test___ne__same_value(self):
        regex = object()
        row_filter1 = self._makeOne(regex=regex)
        row_filter2 = self._makeOne(regex=regex)
        comparison_val = (row_filter1 != row_filter2)
        self.assertFalse(comparison_val)


class TestRowKeyRegexFilter(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row import RowKeyRegexFilter
        return RowKeyRegexFilter

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_to_pb(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        regex = b'row-key-regex'
        row_filter = self._makeOne(regex)
        pb_val = row_filter.to_pb()
        expected_pb = data_pb2.RowFilter(row_key_regex_filter=regex)
        self.assertEqual(pb_val, expected_pb)


class TestFamilyNameRegexFilter(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row import FamilyNameRegexFilter
        return FamilyNameRegexFilter

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_to_pb(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        regex = u'family-regex'
        row_filter = self._makeOne(regex)
        pb_val = row_filter.to_pb()
        expected_pb = data_pb2.RowFilter(family_name_regex_filter=regex)
        self.assertEqual(pb_val, expected_pb)
