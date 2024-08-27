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


import unittest

import json
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
