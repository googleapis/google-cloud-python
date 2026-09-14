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

import pytest
from test__helpers import FIRESTORE_ENTERPRISE_DB, UNIQUE_RESOURCE_ID

from google.cloud.firestore import (
    ArrayUnion,
    BSONBinary,
    BSONDecimal128,
    BSONInt32,
    BSONMaxKey,
    BSONMinKey,
    BSONObjectID,
    BSONRegex,
    BSONTimestamp,
    Increment,
)


def test_bson_system_transforms_rejection():
    # ArrayUnion preserves BSON wrappers
    union = ArrayUnion([BSONInt32(5)])
    assert union.values[0] == BSONInt32(5)

    # Increment explicitly rejects BSONInt32 with TypeError
    with pytest.raises(TypeError):
        Increment(BSONInt32(1))

    # Increment explicitly rejects BSONDecimal128 with TypeError
    with pytest.raises(TypeError):
        Increment(BSONDecimal128("1.0"))


@pytest.mark.parametrize("database", [FIRESTORE_ENTERPRISE_DB], indirect=True)
def test_bson_document_writes(client, cleanup, database):
    """Test standard write operations for BSON types on Enterprise DB."""
    collection_id = "bson_docs_write_" + UNIQUE_RESOURCE_ID
    doc_ref = client.collection(collection_id).document("bson_doc")
    cleanup(doc_ref.delete)

    bson_payload = {
        "_id": BSONObjectID("507f191e810c19729de860ea"),
        "price": BSONDecimal128("199.99"),
        "qty": BSONInt32(50),
        "pattern": BSONRegex(pattern="^prod.*", flags="i"),
        "ts": BSONTimestamp(seconds=1710000000, increment=2),
        "binary_data": BSONBinary(sub_type=1, data=b"binary_payload"),
        "min_key": BSONMinKey(),
        "max_key": BSONMaxKey(),
    }

    doc_ref.set(bson_payload)

    snapshot = doc_ref.get()
    assert snapshot.exists


@pytest.mark.parametrize("database", [FIRESTORE_ENTERPRISE_DB], indirect=True)
def test_pymongo_document_writes(client, cleanup, database):
    """Test write operations using native duck-typed PyMongo objects on Enterprise DB."""
    import decimal

    class DummyPyMongoObjectId:
        def __init__(self, raw: bytes):
            self.binary = raw

    class DummyPyMongoDecimal128:
        def __init__(self, d: decimal.Decimal):
            self._d = d

        def to_decimal(self):
            return self._d

    class DummyPyMongoRegex:
        def __init__(self, pat: str, flags: str):
            self.pattern = pat
            self.flags = flags

    collection_id = "pymongo_docs_write_" + UNIQUE_RESOURCE_ID
    doc_ref = client.collection(collection_id).document("pymongo_doc")
    cleanup(doc_ref.delete)

    payload = {
        "_id": DummyPyMongoObjectId(bytes.fromhex("507f191e810c19729de860ea")),
        "price": DummyPyMongoDecimal128(decimal.Decimal("99.99")),
        "pattern": DummyPyMongoRegex("^test.*", "i"),
    }

    doc_ref.set(payload)

    snapshot = doc_ref.get()
    assert snapshot.exists
