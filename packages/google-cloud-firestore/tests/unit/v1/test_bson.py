# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
#
"""Unit tests for google.cloud.firestore_v1.bson classes."""

import copy
import decimal
import pickle

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
    BSONType,
)


def test_bson_object_id_constructors_and_properties():
    # 24-char hex string
    hex_str = "507f191e810c19729de860ea"
    oid1 = BSONObjectID(hex_str)
    assert oid1.value == hex_str
    assert oid1.to_map_value() == {"__oid__": hex_str}

    # 12 raw bytes
    raw_bytes = b"\x50\x7f\x19\x1e\x81\x0c\x19\x72\x9d\xe8\x60\xea"
    oid2 = BSONObjectID(raw_bytes)
    assert oid2.value == hex_str

    # Invalid bytes length raises ValueError
    with pytest.raises(ValueError, match="must be 12 raw bytes"):
        BSONObjectID(b"invalid_bytes_len")


def test_bson_constructors_validation():
    # bytearray is rejected (requires str or bytes)
    raw_bytes = bytes.fromhex("507f1f77bcf86cd799439011")
    with pytest.raises(TypeError, match="requires str or bytes"):
        BSONObjectID(bytearray(raw_bytes))

    # Invalid constructors
    with pytest.raises(ValueError):
        BSONObjectID("invalid_hex")

    with pytest.raises(ValueError):
        BSONObjectID(b"short")

    with pytest.raises(TypeError):
        BSONObjectID(12345)


def test_bson_object_id_equality_hash_pickle():
    oid1 = BSONObjectID("507f191e810c19729de860ea")
    oid2 = BSONObjectID("507f191e810c19729de860ea")
    oid3 = BSONObjectID("000000000000000000000000")

    assert oid1 == oid2
    assert oid1 != oid3
    assert hash(oid1) == hash(oid2)

    # Pickle
    pickled = pickle.dumps(oid1)
    unpickled = pickle.loads(pickled)
    assert unpickled == oid1
    assert unpickled.value == oid1.value


def test_bson_decimal128():
    dec1 = BSONDecimal128("0.10")
    assert dec1.value == "0.10"
    assert dec1.to_decimal() == decimal.Decimal("0.10")
    assert dec1.to_map_value() == {"__decimal128__": "0.10"}

    dec_nan = BSONDecimal128("NaN")
    assert dec_nan.to_decimal().is_nan()
    assert BSONDecimal128("NaN") == BSONDecimal128("NaN")
    assert len({BSONDecimal128("NaN"), BSONDecimal128("NaN")}) == 1
    assert BSONDecimal128("NaN") != decimal.Decimal("NaN")

    # Eager validation
    with pytest.raises(ValueError):
        BSONDecimal128("not_a_number")

    with pytest.raises(TypeError):
        BSONDecimal128(True)

    # Decimal vs Decimal128 equality and hash parity
    py_dec = decimal.Decimal("0.10")
    assert dec1 == py_dec
    assert py_dec == dec1
    assert hash(dec1) == hash(py_dec)
    assert dec1 in {py_dec}

    # Pickle
    pickled = pickle.dumps(dec1)
    unpickled = pickle.loads(pickled)
    assert unpickled == dec1


def test_bson_timestamp():
    ts1 = BSONTimestamp(1600000000, 1)
    assert ts1.seconds == 1600000000
    assert ts1.increment == 1
    assert ts1.to_map_value() == {
        "__timestamp__": {"seconds": 1600000000, "increment": 1}
    }

    # Bounds validation
    with pytest.raises(ValueError):
        BSONTimestamp(4294967296, 1)

    with pytest.raises(TypeError):
        BSONTimestamp(100.5, 1)

    # Pickle
    pickled = pickle.dumps(ts1)
    unpickled = pickle.loads(pickled)
    assert unpickled == ts1


def test_bson_regex():
    reg = BSONRegex("abc", "ixm")
    assert reg.pattern == "abc"
    assert reg.options == "imx"
    assert reg.to_map_value() == {"__regex__": {"pattern": "abc", "options": "imx"}}

    # Pickle
    pickled = pickle.dumps(reg)
    unpickled = pickle.loads(pickled)
    assert unpickled == reg


def test_bson_binary():
    bin1 = BSONBinary(b"data", 0)
    assert bin1.data == b"data"
    assert bin1.subtype == 0
    assert bin1.to_map_value() == {"__binary__": {"sub_type": 0, "bytes": b"data"}}

    # Default subtype=0
    bin_default = BSONBinary(b"data")
    assert bin_default.subtype == 0

    # Pickle
    pickled = pickle.dumps(bin1)
    unpickled = pickle.loads(pickled)
    assert unpickled == bin1
    assert unpickled.data == b"data"
    assert unpickled.subtype == 0


def test_bson_int32():
    val = BSONInt32(100)
    assert isinstance(val, BSONInt32)
    assert not isinstance(val, int)
    assert val.value == 100
    assert val == 100
    assert val.to_map_value() == {"__int__": 100}

    # Bounds validation
    with pytest.raises(ValueError):
        BSONInt32(2147483648)

    with pytest.raises(ValueError):
        BSONInt32(-2147483649)

    with pytest.raises(TypeError):
        BSONInt32(True)

    # Direct addition raises TypeError for standalone wrapper
    with pytest.raises(TypeError):
        val + 50

    # Pickle
    pickled = pickle.dumps(val)
    unpickled = pickle.loads(pickled)
    assert unpickled == val
    assert isinstance(unpickled, BSONInt32)
    assert unpickled.value == 100


def test_bson_min_key_and_max_key():
    min1 = BSONMinKey()
    min2 = BSONMinKey()
    assert min1 == min2
    assert hash(min1) == hash(min2)
    assert min1.to_map_value() == {"__minkey__": 1}

    max1 = BSONMaxKey()
    max2 = BSONMaxKey()
    assert max1 == max2
    assert hash(max1) == hash(max2)
    assert max1.to_map_value() == {"__maxkey__": 1}

    # Copy / Deepcopy
    assert copy.copy(min1) == min1
    assert copy.deepcopy(max1) == max1

    # Pickle
    assert pickle.loads(pickle.dumps(min1)) == min1
    assert pickle.loads(pickle.dumps(max1)) == max1


def test_bson_int_enum_subclass_support():
    import enum

    class MySubtype(enum.IntEnum):
        USER_DEFINED = 128

    class MySec(enum.IntEnum):
        VAL = 100

    bin_enum = BSONBinary(b"data", MySubtype.USER_DEFINED)
    assert bin_enum.subtype == 128

    ts_enum = BSONTimestamp(MySec.VAL, MySec.VAL)
    assert ts_enum.seconds == 100
    assert ts_enum.increment == 100

    int_enum = BSONInt32(MySec.VAL)
    assert int_enum.value == 100


def test_bson_type_base_class_inheritance():
    instances = [
        BSONObjectID("507f191e810c19729de860ea"),
        BSONDecimal128("123.45"),
        BSONTimestamp(100, 1),
        BSONRegex("abc", "i"),
        BSONBinary(b"data", 0),
        BSONInt32(42),
        BSONMinKey(),
        BSONMaxKey(),
    ]
    for obj in instances:
        assert isinstance(obj, BSONType)
        assert hasattr(obj, "to_map_value")
        assert isinstance(obj.to_map_value(), dict)
