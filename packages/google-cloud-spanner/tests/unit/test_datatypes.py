# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 ( disputes );
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

import json
import unittest

from google.cloud.spanner_v1.data_types import JsonObject


class Test_JsonObject(unittest.TestCase):
    def _make_one(self, *args, **kwargs):
        return JsonObject(*args, **kwargs)

    def test_serialize_dict(self):
        data = {"id": "m1", "content": "hello"}
        obj = self._make_one(data)
        expected = json.dumps(data, sort_keys=True, separators=(",", ":"))
        self.assertEqual(obj.serialize(), expected)

    def test_serialize_array(self):
        data = [{"id": "m1", "content": "hello"}]
        obj = self._make_one(data)
        expected = json.dumps(data, sort_keys=True, separators=(",", ":"))
        self.assertEqual(obj.serialize(), expected)

    def test_serialize_scalar(self):
        obj = self._make_one("hello")
        self.assertEqual(obj.serialize(), '"hello"')

    def test_serialize_null(self):
        obj = self._make_one(None)
        self.assertIsNone(obj.serialize())

    def test_serialize_nested_array_jsonobject(self):
        obj = self._make_one([JsonObject([1, 2]), JsonObject(42)])
        self.assertEqual(obj.serialize(), "[[1,2],42]")

    def test_from_str(self):
        obj = JsonObject.from_str('{"id": "m1"}')
        self.assertEqual(obj.serialize(), '{"id":"m1"}')

    def test_from_str_array(self):
        obj = JsonObject.from_str('[{"id": "m1"}]')
        self.assertEqual(obj.serialize(), '[{"id":"m1"}]')

    def test_from_str_null(self):
        obj = JsonObject.from_str("null")
        self.assertIsNone(obj.serialize())


class Test_JsonObject_dict_protocol(unittest.TestCase):
    """Verify that JsonObject behaves correctly with standard Python
    operations (len, bool, iteration, indexing) for all JSON variants."""

    def test_isinstance_dict(self):
        obj = JsonObject({"a": 1})
        self.assertTrue(isinstance(obj, dict))
        obj_arr = JsonObject([1, 2])
        self.assertTrue(isinstance(obj_arr, dict))

    def test_array_len(self):
        obj = JsonObject([{"id": 1}, {"id": 2}])
        self.assertEqual(len(obj), 2)

    def test_array_bool_truthy(self):
        obj = JsonObject([{"id": 1}])
        self.assertTrue(obj)

    def test_array_bool_empty(self):
        obj = JsonObject([])
        self.assertFalse(obj)

    def test_array_iter(self):
        data = [{"a": 1}, {"b": 2}]
        obj = JsonObject(data)
        self.assertEqual(list(obj), data)

    def test_array_getitem(self):
        data = [{"a": 1}, {"b": 2}]
        obj = JsonObject(data)
        self.assertEqual(obj[0], {"a": 1})
        self.assertEqual(obj[1], {"b": 2})

    def test_array_contains(self):
        data = [1, 2, 3]
        obj = JsonObject(data)
        self.assertIn(2, obj)
        self.assertNotIn(4, obj)

    def test_array_eq(self):
        data = [{"id": 1}]
        obj = JsonObject(data)
        self.assertEqual(obj, data)

    def test_dict_len(self):
        obj = JsonObject({"a": 1, "b": 2})
        self.assertEqual(len(obj), 2)

    def test_dict_bool(self):
        obj = JsonObject({"a": 1})
        self.assertTrue(obj)

    def test_dict_iter(self):
        obj = JsonObject({"a": 1, "b": 2})
        self.assertEqual(sorted(obj), ["a", "b"])

    def test_dict_getitem(self):
        obj = JsonObject({"key": "value"})
        self.assertEqual(obj["key"], "value")

    def test_null_len(self):
        obj = JsonObject(None)
        self.assertEqual(len(obj), 0)

    def test_null_bool(self):
        obj = JsonObject(None)
        self.assertFalse(obj)

    def test_scalar_len(self):
        obj = JsonObject(42)
        self.assertEqual(len(obj), 1)

    def test_scalar_bool(self):
        obj = JsonObject(42)
        self.assertTrue(obj)

    def test_scalar_not_iterable(self):
        obj = JsonObject(42)
        with self.assertRaises(TypeError):
            iter(obj)

    def test_scalar_not_subscriptable(self):
        obj = JsonObject(42)
        with self.assertRaises(TypeError):
            _ = obj[0]


class Test_JsonObject_complex_nested(unittest.TestCase):
    """Complex integration unit tests for deeply nested JsonObject compositions,
    multi-level arrays/dicts, cross-type equality, and edge cases."""

    def test_deeply_nested_serialization(self):
        complex_obj = JsonObject(
            {
                "config": JsonObject({"enabled": True, "timeout": 30}),
                "data": JsonObject(
                    [
                        JsonObject([1, 2]),
                        JsonObject({"score": 42.5}),
                        JsonObject(None),
                    ]
                ),
                "meta": JsonObject("v1.0"),
            }
        )
        expected = (
            '{"config":{"enabled":true,"timeout":30},'
            '"data":[[1,2],{"score":42.5},null],'
            '"meta":"v1.0"}'
        )
        self.assertEqual(complex_obj.serialize(), expected)

    def test_deeply_nested_equality(self):
        obj1 = JsonObject(
            {
                "users": JsonObject(
                    [
                        JsonObject({"id": 1, "roles": JsonObject(["admin"])}),
                        JsonObject({"id": 2, "roles": JsonObject(["user"])}),
                    ]
                )
            }
        )
        obj2 = JsonObject(
            {
                "users": [
                    {"id": 1, "roles": ["admin"]},
                    {"id": 2, "roles": ["user"]},
                ]
            }
        )
        raw_native = {
            "users": [
                {"id": 1, "roles": ["admin"]},
                {"id": 2, "roles": ["user"]},
            ]
        }
        self.assertEqual(obj1, obj2)
        self.assertEqual(obj1, raw_native)

    def test_multi_level_indexing_and_iteration(self):
        data = JsonObject(
            [
                JsonObject([10, 20, 30]),
                JsonObject({"key": "val"}),
            ]
        )
        self.assertEqual(data[0][1], 20)
        self.assertEqual(data[1]["key"], "val")
        self.assertEqual(len(data), 2)
        self.assertEqual(len(data[0]), 3)
        self.assertIn({"key": "val"}, data)

    def test_triple_rewrapping(self):
        obj = JsonObject(JsonObject(JsonObject([1, 2, 3])))
        self.assertTrue(obj._is_array)
        self.assertEqual(len(obj), 3)
        self.assertEqual(obj[0], 1)
        self.assertEqual(obj.serialize(), "[1,2,3]")
