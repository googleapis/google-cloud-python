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


class TestVertext(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.geometry import Vertex
        return Vertex

    def _make_one(self, x_coordinate, y_coordinate):
        return self._get_target_class()(x_coordinate, y_coordinate)

    def test_vertex_with_zeros(self):
        vertex = self._make_one(0.0, 0.0)
        self.assertEqual(vertex.x_coordinate, 0.0)
        self.assertEqual(vertex.y_coordinate, 0.0)
