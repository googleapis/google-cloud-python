# -*- coding: utf-8 -*-
# Copyright 2017 Google LLC All rights reserved.
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

import decimal
import mock
import pytest

from google.cloud.firestore_v1.bson import (
    BSONBinary,
    BSONDecimal128,
    BSONInt32,
    BSONMaxKey,
    BSONMinKey,
    BSONObjectID,
    BSONRegex,
    BSONTimestamp,
)
from google.cloud.firestore_v1.order import Order, TypeOrder, _TYPE_ORDER_MAP


def _make_order(*args, **kwargs):
    return Order(*args, **kwargs)


def test_order_compare_across_heterogenous_values():
    int_max_value = 2**31 - 1
    int_min_value = -(2**31)
    float_min_value = 1.175494351**-38
    float_nan = float("nan")
    inf = float("inf")

    groups = []

    # Rank 1: MinKey
    groups.append([BSONMinKey()])

    # Rank 2: Null
    groups.append([nullValue()])

    # Rank 3: Boolean
    groups.append([_boolean_value(False)])
    groups.append([_boolean_value(True)])

    # Rank 4: Numbers
    groups.append([_double_value(-inf)])
    groups.append([_int_value(int_min_value - 1)])
    groups.append([_int_value(int_min_value), BSONInt32(int_min_value)])
    groups.append([_double_value(-1.1)])
    groups.append([_int_value(-1), _double_value(-1.0), BSONInt32(-1), BSONDecimal128("-1.0")])
    groups.append([_double_value(-float_min_value)])
    groups.append([_int_value(0), _double_value(-0.0), _double_value(0.0), BSONInt32(0), BSONDecimal128("0")])
    groups.append([_double_value(float_min_value)])
    groups.append([_int_value(1), _double_value(1.0), BSONInt32(1), BSONDecimal128("1")])
    groups.append([_double_value(1.1)])
    groups.append([_int_value(int_max_value), BSONInt32(int_max_value)])
    groups.append([_int_value(int_max_value + 1)])
    groups.append([_double_value(inf)])
    # NaNs sort after +Infinity
    groups.append([_double_value(float_nan), _double_value(float_nan), BSONDecimal128("NaN")])

    # Rank 5: Native Timestamps
    groups.append([_timestamp_value(123, 0)])
    groups.append([_timestamp_value(123, 123)])
    groups.append([_timestamp_value(345, 0)])

    # Rank 6: BSONTimestamp
    groups.append([BSONTimestamp(100, 1)])
    groups.append([BSONTimestamp(100, 2)])
    groups.append([BSONTimestamp(200, 0)])

    # Rank 7: Strings
    groups.append([_string_value("")])
    groups.append([_string_value("a")])
    groups.append([_string_value("abc def")])

    # Rank 8: Blobs
    groups.append([_blob_value(b"")])
    groups.append([_blob_value(b"\x00")])
    groups.append([_blob_value(b"\x7f")])

    # Rank 9: BSONBinary
    groups.append([BSONBinary(b"\x00", subtype=0)])
    groups.append([BSONBinary(b"\x00", subtype=1)])
    groups.append([BSONBinary(b"\x01", subtype=0)])

    # Rank 10: Refs / Resource names
    groups.append([_reference_value("projects/p1/databases/d1/documents/c1/doc1")])
    groups.append([_reference_value("projects/p1/databases/d1/documents/c1/doc2")])

    # Rank 11: BSONObjectID
    groups.append([BSONObjectID("000000000000000000000001")])
    groups.append([BSONObjectID("507f1f77bcf86cd799439011")])

    # Rank 12: GeoPoint
    groups.append([_geoPoint_value(-90, -180)])
    groups.append([_geoPoint_value(0, 0)])
    groups.append([_geoPoint_value(90, 180)])

    # Rank 13: BSONRegex
    groups.append([BSONRegex("a", "i")])
    groups.append([BSONRegex("a", "m")])
    groups.append([BSONRegex("b", "i")])

    # Rank 14: Arrays
    groups.append([_array_value()])
    groups.append([_array_value(["bar"])])
    groups.append([_array_value(["foo"])])

    # Rank 15: Vectors
    groups.append([_object_value({"__type__": "__vector__", "value": [3.0, 2.0]})])
    groups.append([_object_value({"__type__": "__vector__", "value": [1.0, 2.0, 5.0]})])

    # Rank 16: Objects
    groups.append([_object_value({"bar": 0})])
    groups.append([_object_value({"bar": 1})])

    # Rank 17: MaxKey
    groups.append([BSONMaxKey()])

    target = _make_order()

    for i in range(len(groups)):
        for left in groups[i]:
            for j in range(len(groups)):
                for right in groups[j]:
                    expected = Order._compare_to(i, j)
                    res = target.compare(left, right)
                    assert res == expected, f"Failed comparing group {i} ({left!r}) vs group {j} ({right!r}), got {res}, expected {expected}"


def test_order_all_value_present():
    for type_order in TypeOrder:
        assert type_order in _TYPE_ORDER_MAP


def test_order_nan_bypassing_and_precision():
    target = _make_order()
    nan_decimal = BSONDecimal128("NaN")
    inf_decimal = BSONDecimal128("Infinity")
    normal_decimal = BSONDecimal128("123.45678901234567890123456789")

    # NaN sorts after +Infinity
    assert target.compare(nan_decimal, inf_decimal) == 1
    assert target.compare(inf_decimal, nan_decimal) == -1
    assert target.compare(nan_decimal, nan_decimal) == 0

    # Decimal vs int comparison equality
    assert target.compare(BSONInt32(5), BSONDecimal128("5.0")) == 0
    assert target.compare(BSONInt32(5), 5) == 0


def test_order_compare_raw_legacy_single_key_dict():
    target = _make_order()
    oid1 = {"__oid__": "507f1f77bcf86cd799439011"}
    oid2 = {"__oid__": "507f1f77bcf86cd799439011"}
    assert target.compare(oid1, oid2) == 0


def test_bson_binary_sorting_order():
    target = _make_order()
    b1 = BSONBinary(b"aaa", subtype=2)
    b2 = BSONBinary(b"bbb", subtype=0)
    b3 = BSONBinary(b"aaa", subtype=3)

    # Data bytes comparison first
    assert target.compare(b1, b2) == -1

    # Subtype as secondary tie-breaker
    assert target.compare(b1, b3) == -1


def _boolean_value(b):
    from google.cloud.firestore_v1._helpers import encode_value
    return encode_value(b)


def _double_value(d):
    from google.cloud.firestore_v1._helpers import encode_value
    return encode_value(d)


def _int_value(value):
    from google.cloud.firestore_v1._helpers import encode_value
    return encode_value(value)


def _string_value(s):
    from google.cloud.firestore_v1._helpers import encode_value
    return encode_value(s)


def _reference_value(r):
    from google.cloud.firestore_v1.types import document
    return document.Value(reference_value=r)


def _blob_value(b):
    from google.cloud.firestore_v1._helpers import encode_value
    return encode_value(b)


def nullValue():
    from google.cloud.firestore_v1._helpers import encode_value
    return encode_value(None)


def _timestamp_value(seconds, nanos):
    from google.protobuf import timestamp_pb2
    from google.cloud.firestore_v1.types import document
    return document.Value(
        timestamp_value=timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)
    )


def _geoPoint_value(latitude, longitude):
    from google.cloud.firestore_v1._helpers import GeoPoint, encode_value
    return encode_value(GeoPoint(latitude, longitude))


def _array_value(values=[]):
    from google.cloud.firestore_v1._helpers import encode_value
    return encode_value(values)


def _object_value(keysAndValues):
    from google.cloud.firestore_v1._helpers import encode_value
    return encode_value(keysAndValues)
