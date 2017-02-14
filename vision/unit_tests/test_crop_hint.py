# Copyright 2017 Google Inc.
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


class TestCropHint(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.crop_hint import CropHint
        return CropHint

    def test_crop_hint_annotation(self):
        from google.cloud.vision.geometry import Bounds
        from unit_tests._fixtures import CROP_HINTS_RESPONSE

        response = CROP_HINTS_RESPONSE['responses'][0]['cropHintsAnnotation']
        crop_hints_dict = response['cropHints'][0]
        crop_hints_class = self._get_target_class()
        crop_hints = crop_hints_class.from_api_repr(crop_hints_dict)

        self.assertIsInstance(crop_hints.bounds, Bounds)
        self.assertEqual(len(crop_hints.bounds.vertices), 4)
        self.assertEqual(crop_hints.confidence, 0.5)
        self.assertEqual(crop_hints.importance_fraction, 1.22)

    def test_crop_hint_annotation_pb(self):
        from google.cloud.proto.vision.v1 import geometry_pb2
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        vertex = geometry_pb2.Vertex(x=1, y=2)
        bounds = geometry_pb2.BoundingPoly(vertices=[vertex])
        crop_hint_pb = image_annotator_pb2.CropHint(
            bounding_poly=bounds, confidence=1.23, importance_fraction=4.56)
        crop_hints_class = self._get_target_class()
        crop_hint = crop_hints_class.from_pb(crop_hint_pb)

        self.assertEqual(len(crop_hint.bounds.vertices), 1)
        self.assertEqual(crop_hint.bounds.vertices[0].x_coordinate, 1)
        self.assertEqual(crop_hint.bounds.vertices[0].y_coordinate, 2)
        self.assertAlmostEqual(crop_hint.confidence, 1.23, 4)
        self.assertAlmostEqual(crop_hint.importance_fraction, 4.56, 4)
