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
from google.cloud import firestore
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
