# Copyright 2018 Google LLC
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


import unittest
from google.cloud.bigtable.row_set import RowRange
from google.cloud._helpers import _to_bytes


class TestRowSet(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_set import RowSet

        return RowSet

    def _make_one(self):
        return self._get_target_class()()

    def test_constructor(self):
        row_set = self._make_one()
        self.assertEqual([], row_set.row_keys)
        self.assertEqual([], row_set.row_ranges)

    def test__eq__(self):
        row_key1 = b"row_key1"
        row_key2 = b"row_key1"
        row_range1 = RowRange(b"row_key4", b"row_key9")
        row_range2 = RowRange(b"row_key4", b"row_key9")

        row_set1 = self._make_one()
        row_set2 = self._make_one()

        row_set1.add_row_key(row_key1)
        row_set2.add_row_key(row_key2)
        row_set1.add_row_range(row_range1)
        row_set2.add_row_range(row_range2)

        self.assertEqual(row_set1, row_set2)

    def test__eq__type_differ(self):
        row_set1 = self._make_one()
        row_set2 = object()
        self.assertNotEqual(row_set1, row_set2)

    def test__eq__len_row_keys_differ(self):
        row_key1 = b"row_key1"
        row_key2 = b"row_key1"

        row_set1 = self._make_one()
        row_set2 = self._make_one()

        row_set1.add_row_key(row_key1)
        row_set1.add_row_key(row_key2)
        row_set2.add_row_key(row_key2)

        self.assertNotEqual(row_set1, row_set2)

    def test__eq__len_row_ranges_differ(self):
        row_range1 = RowRange(b"row_key4", b"row_key9")
        row_range2 = RowRange(b"row_key4", b"row_key9")

        row_set1 = self._make_one()
        row_set2 = self._make_one()

        row_set1.add_row_range(row_range1)
        row_set1.add_row_range(row_range2)
        row_set2.add_row_range(row_range2)

        self.assertNotEqual(row_set1, row_set2)

    def test__eq__row_keys_differ(self):
        row_set1 = self._make_one()
        row_set2 = self._make_one()

        row_set1.add_row_key(b"row_key1")
        row_set1.add_row_key(b"row_key2")
        row_set1.add_row_key(b"row_key3")
        row_set2.add_row_key(b"row_key1")
        row_set2.add_row_key(b"row_key2")
        row_set2.add_row_key(b"row_key4")

        self.assertNotEqual(row_set1, row_set2)

    def test__eq__row_ranges_differ(self):
        row_range1 = RowRange(b"row_key4", b"row_key9")
        row_range2 = RowRange(b"row_key14", b"row_key19")
        row_range3 = RowRange(b"row_key24", b"row_key29")

        row_set1 = self._make_one()
        row_set2 = self._make_one()

        row_set1.add_row_range(row_range1)
        row_set1.add_row_range(row_range2)
        row_set1.add_row_range(row_range3)
        row_set2.add_row_range(row_range1)
        row_set2.add_row_range(row_range2)

        self.assertNotEqual(row_set1, row_set2)

    def test__ne__(self):
        row_key1 = b"row_key1"
        row_key2 = b"row_key1"
        row_range1 = RowRange(b"row_key4", b"row_key9")
        row_range2 = RowRange(b"row_key5", b"row_key9")

        row_set1 = self._make_one()
        row_set2 = self._make_one()

        row_set1.add_row_key(row_key1)
        row_set2.add_row_key(row_key2)
        row_set1.add_row_range(row_range1)
        row_set2.add_row_range(row_range2)

        self.assertNotEqual(row_set1, row_set2)

    def test__ne__same_value(self):
        row_key1 = b"row_key1"
        row_key2 = b"row_key1"
        row_range1 = RowRange(b"row_key4", b"row_key9")
        row_range2 = RowRange(b"row_key4", b"row_key9")

        row_set1 = self._make_one()
        row_set2 = self._make_one()

        row_set1.add_row_key(row_key1)
        row_set2.add_row_key(row_key2)
        row_set1.add_row_range(row_range1)
        row_set2.add_row_range(row_range2)

        comparison_val = row_set1 != row_set2
        self.assertFalse(comparison_val)

    def test_add_row_key(self):
        row_set = self._make_one()
        row_set.add_row_key("row_key1")
        row_set.add_row_key("row_key2")
        self.assertEqual(["row_key1", "row_key2"], row_set.row_keys)

    def test_add_row_range(self):
        row_set = self._make_one()
        row_range1 = RowRange(b"row_key1", b"row_key9")
        row_range2 = RowRange(b"row_key21", b"row_key29")
        row_set.add_row_range(row_range1)
        row_set.add_row_range(row_range2)
        expected = [row_range1, row_range2]
        self.assertEqual(expected, row_set.row_ranges)

    def test_add_row_range_from_keys(self):
        row_set = self._make_one()
        row_set.add_row_range_from_keys(
            start_key=b"row_key1",
            end_key=b"row_key9",
            start_inclusive=False,
            end_inclusive=True,
        )
        self.assertEqual(row_set.row_ranges[0].end_key, b"row_key9")

    def test__update_message_request(self):
        row_set = self._make_one()
        table_name = "table_name"
        row_set.add_row_key("row_key1")
        row_range1 = RowRange(b"row_key21", b"row_key29")
        row_set.add_row_range(row_range1)

        request = _ReadRowsRequestPB(table_name=table_name)
        row_set._update_message_request(request)

        expected_request = _ReadRowsRequestPB(table_name=table_name)
        expected_request.rows.row_keys.append(_to_bytes("row_key1"))

        expected_request.rows.row_ranges.add(**row_range1.get_range_kwargs())

        self.assertEqual(request, expected_request)


class TestRowRange(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row_set import RowRange

        return RowRange

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        start_key = "row_key1"
        end_key = "row_key9"
        row_range = self._make_one(start_key, end_key)
        self.assertEqual(start_key, row_range.start_key)
        self.assertEqual(end_key, row_range.end_key)
        self.assertTrue(row_range.start_inclusive)
        self.assertFalse(row_range.end_inclusive)

    def test___hash__set_equality(self):
        row_range1 = self._make_one("row_key1", "row_key9")
        row_range2 = self._make_one("row_key1", "row_key9")
        set_one = {row_range1, row_range2}
        set_two = {row_range1, row_range2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        row_range1 = self._make_one("row_key1", "row_key9")
        row_range2 = self._make_one("row_key1", "row_key19")
        set_one = {row_range1}
        set_two = {row_range2}
        self.assertNotEqual(set_one, set_two)

    def test__eq__(self):
        start_key = b"row_key1"
        end_key = b"row_key9"
        row_range1 = self._make_one(start_key, end_key, True, False)
        row_range2 = self._make_one(start_key, end_key, True, False)
        self.assertEqual(row_range1, row_range2)

    def test___eq__type_differ(self):
        start_key = b"row_key1"
        end_key = b"row_key9"
        row_range1 = self._make_one(start_key, end_key, True, False)
        row_range2 = object()
        self.assertNotEqual(row_range1, row_range2)

    def test__ne__(self):
        start_key = b"row_key1"
        end_key = b"row_key9"
        row_range1 = self._make_one(start_key, end_key, True, False)
        row_range2 = self._make_one(start_key, end_key, False, True)
        self.assertNotEqual(row_range1, row_range2)

    def test__ne__same_value(self):
        start_key = b"row_key1"
        end_key = b"row_key9"
        row_range1 = self._make_one(start_key, end_key, True, False)
        row_range2 = self._make_one(start_key, end_key, True, False)
        comparison_val = row_range1 != row_range2
        self.assertFalse(comparison_val)

    def test_get_range_kwargs_closed_open(self):
        start_key = b"row_key1"
        end_key = b"row_key9"
        expected_result = {"start_key_closed": start_key, "end_key_open": end_key}
        row_range = self._make_one(start_key, end_key)
        actual_result = row_range.get_range_kwargs()
        self.assertEqual(expected_result, actual_result)

    def test_get_range_kwargs_open_closed(self):
        start_key = b"row_key1"
        end_key = b"row_key9"
        expected_result = {"start_key_open": start_key, "end_key_closed": end_key}
        row_range = self._make_one(start_key, end_key, False, True)
        actual_result = row_range.get_range_kwargs()
        self.assertEqual(expected_result, actual_result)


def _ReadRowsRequestPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import bigtable_pb2 as messages_v2_pb2

    return messages_v2_pb2.ReadRowsRequest(*args, **kw)
