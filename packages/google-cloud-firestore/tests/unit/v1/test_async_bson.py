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

from google.cloud.firestore_v1._helpers import decode_dict, encode_dict
from google.cloud.firestore_v1.async_client import AsyncClient
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


def test_async_client_decode_bson_flag():
    client_default = AsyncClient(project="project", decode_bson=False)
    assert client_default.decode_bson is False
    assert client_default._to_sync_copy().decode_bson is False

    client_enabled = AsyncClient(project="project", decode_bson=True)
    assert client_enabled.decode_bson is True
    assert client_enabled._to_sync_copy().decode_bson is True


def test_async_bson_encode_decode_roundtrip():
    data = {
        "oid": BSONObjectID("507f1f77bcf86cd799439011"),
        "dec": BSONDecimal128("123.456"),
        "ts": BSONTimestamp(100, 200),
        "reg": BSONRegex("foo", "i"),
        "bin": BSONBinary(b"bar", subtype=1),
        "int32": BSONInt32(42),
        "min": BSONMinKey(),
        "max": BSONMaxKey(),
    }

    encoded = encode_dict(data)

    client_disabled = AsyncClient(project="proj", decode_bson=False)
    decoded_raw = decode_dict(encoded, client=client_disabled)
    assert isinstance(decoded_raw["oid"], dict)
    assert decoded_raw["oid"]["__oid__"] == "507f1f77bcf86cd799439011"

    client_enabled = AsyncClient(project="proj", decode_bson=True)
    decoded_bson = decode_dict(encoded, client=client_enabled)
    assert isinstance(decoded_bson["oid"], BSONObjectID)
    assert decoded_bson["oid"].value == "507f1f77bcf86cd799439011"
    assert isinstance(decoded_bson["dec"], BSONDecimal128)
    assert isinstance(decoded_bson["ts"], BSONTimestamp)
    assert isinstance(decoded_bson["reg"], BSONRegex)
    assert isinstance(decoded_bson["bin"], BSONBinary)
    assert isinstance(decoded_bson["int32"], BSONInt32)
    assert isinstance(decoded_bson["min"], BSONMinKey)
    assert isinstance(decoded_bson["max"], BSONMaxKey)
