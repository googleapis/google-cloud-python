# Copyright 2024 Google LLC All rights reserved.
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


import json
import unittest

from google.cloud.spanner_v1.data_types import JsonObject


class Test_JsonObject_serde(unittest.TestCase):
    def test_w_dict(self):
        data = {"foo": "bar"}
        expected = json.dumps(data, sort_keys=True, separators=(",", ":"))
        data_jsonobject = JsonObject(data)
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_list_of_dict(self):
        data = [{"foo1": "bar1"}, {"foo2": "bar2"}]
        expected = json.dumps(data, sort_keys=True, separators=(",", ":"))
        data_jsonobject = JsonObject(data)
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_JsonObject_of_dict(self):
        data = {"foo": "bar"}
        expected = json.dumps(data, sort_keys=True, separators=(",", ":"))
        data_jsonobject = JsonObject(JsonObject(data))
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_JsonObject_of_list_of_dict(self):
        data = [{"foo1": "bar1"}, {"foo2": "bar2"}]
        expected = json.dumps(data, sort_keys=True, separators=(",", ":"))
        data_jsonobject = JsonObject(JsonObject(data))
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_simple_float_JsonData(self):
        data = 1.1
        expected = json.dumps(data)
        data_jsonobject = JsonObject(data)
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_simple_str_JsonData(self):
        data = "foo"
        expected = json.dumps(data)
        data_jsonobject = JsonObject(data)
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_empty_str_JsonData(self):
        data = ""
        expected = json.dumps(data)
        data_jsonobject = JsonObject(data)
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_None_JsonData(self):
        data = None
        data_jsonobject = JsonObject(data)
        self.assertEqual(data_jsonobject.serialize(), None)

    def test_w_list_of_simple_JsonData(self):
        data = [1.1, "foo"]
        expected = json.dumps(data, sort_keys=True, separators=(",", ":"))
        data_jsonobject = JsonObject(data)
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_empty_list(self):
        data = []
        expected = json.dumps(data)
        data_jsonobject = JsonObject(data)
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_empty_dict(self):
        data = [{}]
        expected = json.dumps(data)
        data_jsonobject = JsonObject(data)
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_JsonObject_of_simple_JsonData(self):
        data = 1.1
        expected = json.dumps(data)
        data_jsonobject = JsonObject(JsonObject(data))
        self.assertEqual(data_jsonobject.serialize(), expected)

    def test_w_JsonObject_of_list_of_simple_JsonData(self):
        data = [1.1, "foo"]
        expected = json.dumps(data, sort_keys=True, separators=(",", ":"))
        data_jsonobject = JsonObject(JsonObject(data))
        self.assertEqual(data_jsonobject.serialize(), expected)


class Test_JsonObject_dict_protocol(unittest.TestCase):
    """Verify that JsonObject behaves correctly with standard Python
    operations (len, bool, iteration, indexing) for all JSON variants."""

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

    def test_array_json_dumps(self):
        data = [{"id": "m1", "content": "hello"}]
        obj = JsonObject(data)
        result = json.loads(json.dumps(list(obj)))
        self.assertEqual(result, data)

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
            obj[0]
