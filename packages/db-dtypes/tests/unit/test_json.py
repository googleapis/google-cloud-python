# Copyright 2024 Google LLC
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


import pandas as pd
import pytest

import db_dtypes

# Check for minimum Pandas version.
pytest.importorskip("pandas", minversion="1.5.0")


# Python data types mirroring all standard JSON types:
# https://json-schema.org/understanding-json-schema/reference/type
JSON_DATA = {
    "boolean": True,
    "int": 100,
    "float": 0.98,
    "string": "hello world",
    "array": [0.1, 0.2],
    "dict": {
        "null_field": None,
        "order": {
            "items": ["book", "pen", "computer"],
            "total": 15.99,
            "address": {"street": "123 Main St", "city": "Anytown"},
        },
    },
    "null": None,
}


def test_construct_w_unspported_types():
    with pytest.raises(ValueError):
        db_dtypes.JSONArray(100)


def test_getitems_return_json_objects():
    data = db_dtypes.JSONArray._from_sequence(JSON_DATA.values())
    for id, key in enumerate(JSON_DATA.keys()):
        if key == "null":
            assert pd.isna(data[id])
        else:
            assert data[id] == JSON_DATA[key]


def test_getitems_w_unboxed_dict():
    data = db_dtypes.JSONArray._from_sequence([JSON_DATA["dict"]])
    assert len(data[0]) == 2

    assert data[0]["null_field"] is None
    assert data[0]["order"]["address"]["city"] == "Anytown"
    assert len(data[0]["order"]["items"]) == 3
    assert data[0]["order"]["items"][0] == "book"

    with pytest.raises(KeyError):
        data[0]["unknown"]


def test_getitems_when_iter_with_null():
    data = db_dtypes.JSONArray._from_sequence([JSON_DATA["null"]])
    s = pd.Series(data)
    result = s[:1].item()
    assert pd.isna(result)


def test_deterministic_json_serialization():
    x = {"a": 0, "b": 1}
    y = {"b": 1, "a": 0}
    data = db_dtypes.JSONArray._from_sequence([y])
    assert data[0] == x
