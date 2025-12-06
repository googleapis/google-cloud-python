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


def test_row_set_constructor():
    from google.cloud.bigtable.row_set import RowSet

    row_set = RowSet()
    assert [] == row_set.row_keys
    assert [] == row_set.row_ranges


def test_row_set__eq__():
    from google.cloud.bigtable.row_set import RowRange
    from google.cloud.bigtable.row_set import RowSet

    row_key1 = b"row_key1"
    row_key2 = b"row_key1"
    row_range1 = RowRange(b"row_key4", b"row_key9")
    row_range2 = RowRange(b"row_key4", b"row_key9")

    row_set1 = RowSet()
    row_set2 = RowSet()

    row_set1.add_row_key(row_key1)
    row_set2.add_row_key(row_key2)
    row_set1.add_row_range(row_range1)
    row_set2.add_row_range(row_range2)

    assert row_set1 == row_set2


def test_row_set__eq__type_differ():
    from google.cloud.bigtable.row_set import RowSet

    row_set1 = RowSet()
    row_set2 = object()
    assert not (row_set1 == row_set2)


def test_row_set__eq__len_row_keys_differ():
    from google.cloud.bigtable.row_set import RowSet

    row_key1 = b"row_key1"
    row_key2 = b"row_key1"

    row_set1 = RowSet()
    row_set2 = RowSet()

    row_set1.add_row_key(row_key1)
    row_set1.add_row_key(row_key2)
    row_set2.add_row_key(row_key2)

    assert not (row_set1 == row_set2)


def test_row_set__eq__len_row_ranges_differ():
    from google.cloud.bigtable.row_set import RowRange
    from google.cloud.bigtable.row_set import RowSet

    row_range1 = RowRange(b"row_key4", b"row_key9")
    row_range2 = RowRange(b"row_key4", b"row_key9")

    row_set1 = RowSet()
    row_set2 = RowSet()

    row_set1.add_row_range(row_range1)
    row_set1.add_row_range(row_range2)
    row_set2.add_row_range(row_range2)

    assert not (row_set1 == row_set2)


def test_row_set__eq__row_keys_differ():
    from google.cloud.bigtable.row_set import RowSet

    row_set1 = RowSet()
    row_set2 = RowSet()

    row_set1.add_row_key(b"row_key1")
    row_set1.add_row_key(b"row_key2")
    row_set1.add_row_key(b"row_key3")
    row_set2.add_row_key(b"row_key1")
    row_set2.add_row_key(b"row_key2")
    row_set2.add_row_key(b"row_key4")

    assert not (row_set1 == row_set2)


def test_row_set__eq__row_ranges_differ():
    from google.cloud.bigtable.row_set import RowRange
    from google.cloud.bigtable.row_set import RowSet

    row_range1 = RowRange(b"row_key4", b"row_key9")
    row_range2 = RowRange(b"row_key14", b"row_key19")
    row_range3 = RowRange(b"row_key24", b"row_key29")

    row_set1 = RowSet()
    row_set2 = RowSet()

    row_set1.add_row_range(row_range1)
    row_set1.add_row_range(row_range2)
    row_set1.add_row_range(row_range3)
    row_set2.add_row_range(row_range1)
    row_set2.add_row_range(row_range2)

    assert not (row_set1 == row_set2)


def test_row_set__ne__():
    from google.cloud.bigtable.row_set import RowRange
    from google.cloud.bigtable.row_set import RowSet

    row_key1 = b"row_key1"
    row_key2 = b"row_key1"
    row_range1 = RowRange(b"row_key4", b"row_key9")
    row_range2 = RowRange(b"row_key5", b"row_key9")

    row_set1 = RowSet()
    row_set2 = RowSet()

    row_set1.add_row_key(row_key1)
    row_set2.add_row_key(row_key2)
    row_set1.add_row_range(row_range1)
    row_set2.add_row_range(row_range2)

    assert row_set1 != row_set2


def test_row_set__ne__same_value():
    from google.cloud.bigtable.row_set import RowRange
    from google.cloud.bigtable.row_set import RowSet

    row_key1 = b"row_key1"
    row_key2 = b"row_key1"
    row_range1 = RowRange(b"row_key4", b"row_key9")
    row_range2 = RowRange(b"row_key4", b"row_key9")

    row_set1 = RowSet()
    row_set2 = RowSet()

    row_set1.add_row_key(row_key1)
    row_set2.add_row_key(row_key2)
    row_set1.add_row_range(row_range1)
    row_set2.add_row_range(row_range2)

    assert not (row_set1 != row_set2)


def test_row_set_add_row_key():
    from google.cloud.bigtable.row_set import RowSet

    row_set = RowSet()
    row_set.add_row_key("row_key1")
    row_set.add_row_key("row_key2")
    assert ["row_key1" == "row_key2"], row_set.row_keys


def test_row_set_add_row_range():
    from google.cloud.bigtable.row_set import RowRange
    from google.cloud.bigtable.row_set import RowSet

    row_set = RowSet()
    row_range1 = RowRange(b"row_key1", b"row_key9")
    row_range2 = RowRange(b"row_key21", b"row_key29")
    row_set.add_row_range(row_range1)
    row_set.add_row_range(row_range2)
    expected = [row_range1, row_range2]
    assert expected == row_set.row_ranges


def test_row_set_add_row_range_from_keys():
    from google.cloud.bigtable.row_set import RowSet

    row_set = RowSet()
    row_set.add_row_range_from_keys(
        start_key=b"row_key1",
        end_key=b"row_key9",
        start_inclusive=False,
        end_inclusive=True,
    )
    assert row_set.row_ranges[0].end_key == b"row_key9"


def test_row_set_add_row_range_with_prefix():
    from google.cloud.bigtable.row_set import RowSet

    row_set = RowSet()
    row_set.add_row_range_with_prefix("row")
    assert row_set.row_ranges[0].end_key == b"rox"


def test_row_set__update_message_request():
    from google.cloud._helpers import _to_bytes
    from google.cloud.bigtable.row_set import RowRange
    from google.cloud.bigtable.row_set import RowSet

    row_set = RowSet()
    table_name = "table_name"
    row_set.add_row_key("row_key1")
    row_range1 = RowRange(b"row_key21", b"row_key29")
    row_set.add_row_range(row_range1)

    request = _ReadRowsRequestPB(table_name=table_name)
    row_set._update_message_request(request)

    expected_request = _ReadRowsRequestPB(table_name=table_name)
    expected_request.rows.row_keys.append(_to_bytes("row_key1"))

    expected_request.rows.row_ranges.append(row_range1.get_range_kwargs())

    assert request == expected_request


def test_row_range_constructor():
    from google.cloud.bigtable.row_set import RowRange

    start_key = "row_key1"
    end_key = "row_key9"
    row_range = RowRange(start_key, end_key)
    assert start_key == row_range.start_key
    assert end_key == row_range.end_key
    assert row_range.start_inclusive
    assert not row_range.end_inclusive


def test_row_range___hash__set_equality():
    from google.cloud.bigtable.row_set import RowRange

    row_range1 = RowRange("row_key1", "row_key9")
    row_range2 = RowRange("row_key1", "row_key9")
    set_one = {row_range1, row_range2}
    set_two = {row_range1, row_range2}
    assert set_one == set_two


def test_row_range___hash__not_equals():
    from google.cloud.bigtable.row_set import RowRange

    row_range1 = RowRange("row_key1", "row_key9")
    row_range2 = RowRange("row_key1", "row_key19")
    set_one = {row_range1}
    set_two = {row_range2}
    assert set_one != set_two


def test_row_range__eq__():
    from google.cloud.bigtable.row_set import RowRange

    start_key = b"row_key1"
    end_key = b"row_key9"
    row_range1 = RowRange(start_key, end_key, True, False)
    row_range2 = RowRange(start_key, end_key, True, False)
    assert row_range1 == row_range2


def test_row_range___eq__type_differ():
    from google.cloud.bigtable.row_set import RowRange

    start_key = b"row_key1"
    end_key = b"row_key9"
    row_range1 = RowRange(start_key, end_key, True, False)
    row_range2 = object()
    assert row_range1 != row_range2


def test_row_range__ne__():
    from google.cloud.bigtable.row_set import RowRange

    start_key = b"row_key1"
    end_key = b"row_key9"
    row_range1 = RowRange(start_key, end_key, True, False)
    row_range2 = RowRange(start_key, end_key, False, True)
    assert row_range1 != row_range2


def test_row_range__ne__same_value():
    from google.cloud.bigtable.row_set import RowRange

    start_key = b"row_key1"
    end_key = b"row_key9"
    row_range1 = RowRange(start_key, end_key, True, False)
    row_range2 = RowRange(start_key, end_key, True, False)
    assert not (row_range1 != row_range2)


def test_row_range_get_range_kwargs_closed_open():
    from google.cloud.bigtable.row_set import RowRange

    start_key = b"row_key1"
    end_key = b"row_key9"
    expected_result = {"start_key_closed": start_key, "end_key_open": end_key}
    row_range = RowRange(start_key, end_key)
    actual_result = row_range.get_range_kwargs()
    assert expected_result == actual_result


def test_row_range_get_range_kwargs_open_closed():
    from google.cloud.bigtable.row_set import RowRange

    start_key = b"row_key1"
    end_key = b"row_key9"
    expected_result = {"start_key_open": start_key, "end_key_closed": end_key}
    row_range = RowRange(start_key, end_key, False, True)
    actual_result = row_range.get_range_kwargs()
    assert expected_result == actual_result


def _ReadRowsRequestPB(*args, **kw):
    from google.cloud.bigtable_v2.types import bigtable as messages_v2_pb2

    return messages_v2_pb2.ReadRowsRequest(*args, **kw)
