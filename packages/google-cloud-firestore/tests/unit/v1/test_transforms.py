# Copyright 2017 Google LLC All rights reserved.
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


class Test_ValueList(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.transforms import _ValueList

        return _ValueList

    def _make_one(self, values):
        return self._get_target_class()(values)

    def test_ctor_w_non_list_non_tuple(self):
        invalid_values = (None, u"phred", b"DEADBEEF", 123, {}, object())
        for invalid_value in invalid_values:
            with self.assertRaises(ValueError):
                self._make_one(invalid_value)

    def test_ctor_w_empty(self):
        with self.assertRaises(ValueError):
            self._make_one([])

    def test_ctor_w_non_empty_list(self):
        values = ["phred", "bharney"]
        inst = self._make_one(values)
        self.assertEqual(inst.values, values)

    def test_ctor_w_non_empty_tuple(self):
        values = ("phred", "bharney")
        inst = self._make_one(values)
        self.assertEqual(inst.values, list(values))

    def test___eq___other_type(self):
        values = ("phred", "bharney")
        inst = self._make_one(values)
        other = object()
        self.assertFalse(inst == other)

    def test___eq___different_values(self):
        values = ("phred", "bharney")
        other_values = ("wylma", "bhetty")
        inst = self._make_one(values)
        other = self._make_one(other_values)
        self.assertFalse(inst == other)

    def test___eq___same_values(self):
        values = ("phred", "bharney")
        inst = self._make_one(values)
        other = self._make_one(values)
        self.assertTrue(inst == other)


class Test_NumericValue(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.transforms import _NumericValue

        return _NumericValue

    def _make_one(self, values):
        return self._get_target_class()(values)

    def test_ctor_w_invalid_types(self):
        invalid_values = (None, u"phred", b"DEADBEEF", [], {}, object())
        for invalid_value in invalid_values:
            with self.assertRaises(ValueError):
                self._make_one(invalid_value)

    def test_ctor_w_int(self):
        values = (-10, -1, 0, 1, 10)
        for value in values:
            inst = self._make_one(value)
            self.assertEqual(inst.value, value)

    def test_ctor_w_float(self):
        values = (-10.0, -1.0, 0.0, 1.0, 10.0)
        for value in values:
            inst = self._make_one(value)
            self.assertEqual(inst.value, value)

    def test___eq___other_type(self):
        value = 3.1415926
        inst = self._make_one(value)
        other = object()
        self.assertFalse(inst == other)

    def test___eq___different_value(self):
        value = 3.1415926
        other_value = 2.71828
        inst = self._make_one(value)
        other = self._make_one(other_value)
        self.assertFalse(inst == other)

    def test___eq___same_value(self):
        value = 3.1415926
        inst = self._make_one(value)
        other = self._make_one(value)
        self.assertTrue(inst == other)
