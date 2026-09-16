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
import pickle

import pytest

from google.cloud.firestore_v1.bson import (
    BSONInt32,
    BSONMaxKey,
    BSONMinKey,
    BSONObjectId,
    _BSONType,
)


def test_bson_type_abc_cannot_be_instantiated():
    with pytest.raises(TypeError):
        _BSONType()  # type: ignore


def test_bson_type_inheritance():
    oid = BSONObjectId("507f191e810c19729de860ea")
    assert isinstance(oid, _BSONType)


def test_bson_object_id_from_hex_string():
    hex_str = "507f191e810c19729de860ea"
    oid = BSONObjectId(hex_str)
    assert oid.value == hex_str


def test_bson_object_id_from_uppercase_hex_string():
    oid = BSONObjectId("507F191E810C19729DE860EA")
    assert oid.value == "507f191e810c19729de860ea"


def test_bson_object_id_from_bytes():
    raw_bytes = b"\x50\x7f\x19\x1e\x81\x0c\x19\x72\x9d\xe8\x60\xea"
    oid = BSONObjectId(raw_bytes)
    assert oid.value == "507f191e810c19729de860ea"


def test_bson_object_id_to_map_value():
    hex_str = "507f191e810c19729de860ea"
    oid = BSONObjectId(hex_str)
    assert oid._to_map_value() == {"__oid__": hex_str}


@pytest.mark.parametrize(
    "invalid_input, exc_type, match_msg",
    [
        ("invalid_hex", ValueError, "24-character hex string"),
        (b"short", ValueError, "12 raw bytes"),
        (bytearray(b"\x50" * 12), TypeError, "requires str or bytes"),
        (12345, TypeError, "requires str or bytes"),
        (None, TypeError, "requires str or bytes"),
    ],
)
def test_bson_object_id_invalid_inputs(invalid_input, exc_type, match_msg):
    with pytest.raises(exc_type, match=match_msg):
        BSONObjectId(invalid_input)


def test_bson_object_id_equality():
    oid1 = BSONObjectId("507f191e810c19729de860ea")
    oid2 = BSONObjectId("507f191e810c19729de860ea")
    oid3 = BSONObjectId("507f191e810c19729de860eb")

    assert oid1 == oid2
    assert oid1 != oid3
    assert oid1 != "507f191e810c19729de860ea"


def test_bson_object_id_equality_not_implemented():
    oid = BSONObjectId("507f191e810c19729de860ea")

    class CooperativeOther:
        def __eq__(self, other):
            return True

    assert oid == CooperativeOther()


def test_bson_object_id_hash_and_dict_key():
    oid1 = BSONObjectId("507f191e810c19729de860ea")
    oid2 = BSONObjectId("507f191e810c19729de860ea")

    assert hash(oid1) == hash(oid2)
    lookup = {oid1: "success"}
    assert lookup[oid2] == "success"
    assert len({oid1, oid2}) == 1


def test_bson_object_id_repr():
    oid = BSONObjectId("507f191e810c19729de860ea")
    assert repr(oid) == "BSONObjectId('507f191e810c19729de860ea')"


def test_bson_object_id_str():
    oid = BSONObjectId("507f191e810c19729de860ea")
    assert str(oid) == "507f191e810c19729de860ea"


def test_bson_object_id_copy():
    oid = BSONObjectId("507f191e810c19729de860ea")
    assert copy.copy(oid) == oid
    assert copy.deepcopy(oid) == oid


def test_bson_object_id_pickle():
    oid = BSONObjectId("507f191e810c19729de860ea")
    unpickled = pickle.loads(pickle.dumps(oid))
    assert unpickled == oid
    assert unpickled.value == oid.value


def test_bson_minkey_to_map_value():
    assert BSONMinKey()._to_map_value() == {"__min__": None}


def test_bson_minkey_equality():
    key1 = BSONMinKey()
    key2 = BSONMinKey()
    assert key1 == key2
    assert key1 != BSONMaxKey()
    assert key1 != "min"


def test_bson_minkey_hash_and_dict_key():
    key1 = BSONMinKey()
    key2 = BSONMinKey()
    assert hash(key1) == hash(key2)
    assert len({key1, key2}) == 1


def test_bson_minkey_repr():
    assert repr(BSONMinKey()) == "BSONMinKey()"


def test_bson_minkey_copy():
    key = BSONMinKey()
    assert copy.copy(key) == key
    assert copy.deepcopy(key) == key


def test_bson_minkey_pickle():
    key = BSONMinKey()
    assert pickle.loads(pickle.dumps(key)) == key


def test_bson_maxkey_to_map_value():
    assert BSONMaxKey()._to_map_value() == {"__max__": None}


def test_bson_maxkey_equality():
    key1 = BSONMaxKey()
    key2 = BSONMaxKey()
    assert key1 == key2
    assert key1 != BSONMinKey()
    assert key1 != "max"


def test_bson_maxkey_hash_and_dict_key():
    key1 = BSONMaxKey()
    key2 = BSONMaxKey()
    assert hash(key1) == hash(key2)
    assert len({key1, key2}) == 1


def test_bson_maxkey_repr():
    assert repr(BSONMaxKey()) == "BSONMaxKey()"


def test_bson_maxkey_copy():
    key = BSONMaxKey()
    assert copy.copy(key) == key
    assert copy.deepcopy(key) == key


def test_bson_maxkey_pickle():
    key = BSONMaxKey()
    assert pickle.loads(pickle.dumps(key)) == key


def test_bson_int32_valid():
    val = BSONInt32(42)
    assert val.value == 42
    assert int(val) == 42
    assert str(val) == "42"
    assert repr(val) == "BSONInt32(42)"
    assert val._to_map_value() == {"__int__": 42}


def test_bson_int32_boundaries():
    min_val = BSONInt32(-2147483648)
    max_val = BSONInt32(2147483647)
    assert min_val.value == -2147483648
    assert max_val.value == 2147483647


@pytest.mark.parametrize(
    "invalid_input, exc_type, match_msg",
    [
        (2147483648, ValueError, "must be between"),
        (-2147483649, ValueError, "must be between"),
        (True, TypeError, "requires an int"),
        (False, TypeError, "requires an int"),
        ("42", TypeError, "requires an int"),
        (42.0, TypeError, "requires an int"),
        (None, TypeError, "requires an int"),
    ],
)
def test_bson_int32_invalid_inputs(invalid_input, exc_type, match_msg):
    with pytest.raises(exc_type, match=match_msg):
        BSONInt32(invalid_input)


def test_bson_int32_equality():
    val1 = BSONInt32(42)
    val2 = BSONInt32(42)
    val3 = BSONInt32(100)
    assert val1 == val2
    assert val1 != val3
    assert val1 != 42


def test_bson_int32_hash_and_dict_key():
    val1 = BSONInt32(42)
    val2 = BSONInt32(42)
    assert hash(val1) == hash(val2)
    assert len({val1, val2}) == 1


def test_bson_int32_copy():
    val = BSONInt32(42)
    assert copy.copy(val) == val
    assert copy.deepcopy(val) == val


def test_bson_int32_pickle():
    val = BSONInt32(42)
    assert pickle.loads(pickle.dumps(val)) == val
