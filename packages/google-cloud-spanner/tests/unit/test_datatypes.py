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

    def test_to_python_dict(self):
        obj = JsonObject({"a": 1, "b": [2, 3]})
        self.assertFalse(obj.is_null)
        self.assertFalse(obj.is_array)
        self.assertFalse(obj.is_scalar)
        self.assertEqual(obj.to_python(), {"a": 1, "b": [2, 3]})

    def test_to_python_array(self):
        obj = JsonObject([{"a": 1}, 2, "str"])
        self.assertFalse(obj.is_null)
        self.assertTrue(obj.is_array)
        self.assertFalse(obj.is_scalar)
        self.assertEqual(obj.to_python(), [{"a": 1}, 2, "str"])

    def test_to_python_scalar_and_null(self):
        scalar_obj = JsonObject("hello")
        self.assertTrue(scalar_obj.is_scalar)
        self.assertEqual(scalar_obj.to_python(), "hello")

        null_obj = JsonObject(None)
        self.assertTrue(null_obj.is_null)
        self.assertIsNone(null_obj.to_python())
