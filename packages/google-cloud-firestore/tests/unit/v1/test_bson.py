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
import pytest

from google.cloud.firestore_v1._helpers import decode_dict, decode_value, encode_dict, encode_value
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


def test_bson_object_id():
    oid_str = "507f191e810c19729de860ea"
    oid = BSONObjectID(oid_str)
    assert oid.value == oid_str
    assert repr(oid) == f"BSONObjectID('{oid_str}')"
    assert oid == BSONObjectID(oid_str)

    # Invalid hex string length or characters
    with pytest.raises(ValueError):
        BSONObjectID("invalid")
    with pytest.raises(ValueError):
        BSONObjectID("507f191e810c19729de860eg")  # 'g' is invalid hex

    # Encoding / Decoding roundtrip
    encoded = encode_value(oid)
    decoded = decode_value(encoded, client=None)
    assert decoded == oid


def test_bson_decimal128():
    dec_val = "123.45678901234567890"
    dec = BSONDecimal128(dec_val)
    assert dec.value == dec_val
    assert repr(dec) == f"BSONDecimal128('{dec_val}')"
    assert dec == BSONDecimal128(dec_val)

    encoded = encode_value(dec)
    decoded = decode_value(encoded, client=None)
    assert decoded == dec


def test_bson_int32():
    val = 42
    b_int = BSONInt32(val)
    assert b_int.value == val
    assert repr(b_int) == "BSONInt32(42)"
    assert b_int == BSONInt32(val)

    encoded = encode_value(b_int)
    decoded = decode_value(encoded, client=None)
    assert decoded == b_int


def test_bson_regex():
    reg = BSONRegex(pattern="^test.*", flags="i")
    assert reg.pattern == "^test.*"
    assert reg.flags == "i"
    assert repr(reg) == "BSONRegex(pattern='^test.*', flags='i')"
    assert reg == BSONRegex(pattern="^test.*", flags="i")

    encoded = encode_value(reg)
    decoded = decode_value(encoded, client=None)
    assert decoded == reg


def test_bson_timestamp():
    ts = BSONTimestamp(seconds=1600000000, increment=1)
    assert ts.seconds == 1600000000
    assert ts.increment == 1
    assert repr(ts) == "BSONTimestamp(seconds=1600000000, increment=1)"
    assert ts == BSONTimestamp(seconds=1600000000, increment=1)

    encoded = encode_value(ts)
    decoded = decode_value(encoded, client=None)
    assert decoded == ts


def test_bson_binary():
    bin_data = BSONBinary(sub_type=128, data=b"\x01\x02\x03\x04")
    assert bin_data.sub_type == 128
    assert bin_data.data == b"\x01\x02\x03\x04"
    assert repr(bin_data) == "BSONBinary(sub_type=128, data=b'\\x01\\x02\\x03\\x04')"
    assert bin_data == BSONBinary(sub_type=128, data=b"\x01\x02\x03\x04")

    encoded = encode_value(bin_data)
    decoded = decode_value(encoded, client=None)
    assert decoded == bin_data


def test_bson_min_key():
    min_key = BSONMinKey()
    assert repr(min_key) == "BSONMinKey()"
    assert min_key == BSONMinKey()

    encoded = encode_value(min_key)
    decoded = decode_value(encoded, client=None)
    assert decoded == min_key


def test_bson_max_key():
    max_key = BSONMaxKey()
    assert repr(max_key) == "BSONMaxKey()"
    assert max_key == BSONMaxKey()

    encoded = encode_value(max_key)
    decoded = decode_value(encoded, client=None)
    assert decoded == max_key


def test_bson_nested_dict_encoding_decoding():
    data = {
        "_id": BSONObjectID("507f191e810c19729de860ea"),
        "price": BSONDecimal128("99.99"),
        "quantity": BSONInt32(10),
        "regex": BSONRegex(pattern="abc", flags="m"),
        "ts": BSONTimestamp(seconds=1700000000, increment=5),
        "bin": BSONBinary(sub_type=0, data=b"hello"),
        "min": BSONMinKey(),
        "max": BSONMaxKey(),
    }

    encoded_dict = encode_dict(data)
    decoded_dict = decode_dict(encoded_dict, client=None)
    assert decoded_dict == data

