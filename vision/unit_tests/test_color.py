# Copyright 2016 Google Inc.
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


class TestColor(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.color import Color
        return Color

    def test_rgb_color_data(self):
        colors = {
            'red': 255,
            'green': 255,
            'blue': 255,
            'alpha': 0.5,
        }
        color_class = self._get_target_class()
        colors = color_class.from_api_repr(colors)

        self.assertEqual(colors.red, 255)
        self.assertEqual(colors.green, 255)
        self.assertEqual(colors.blue, 255)
        self.assertEqual(colors.alpha, 0.5)

    def test_missing_rgb_values(self):
        colors = {}
        color_class = self._get_target_class()
        colors = color_class.from_api_repr(colors)

        self.assertEqual(colors.red, 0)
        self.assertEqual(colors.green, 0)
        self.assertEqual(colors.blue, 0)
        self.assertEqual(colors.alpha, 0.0)
