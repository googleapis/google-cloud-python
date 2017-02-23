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

        self.assertIsInstance(colors.red, float)
        self.assertIsInstance(colors.green, float)
        self.assertIsInstance(colors.blue, float)
        self.assertIsInstance(colors.alpha, float)
        self.assertEqual(colors.red, 255.0)
        self.assertEqual(colors.green, 255.0)
        self.assertEqual(colors.blue, 255.0)
        self.assertEqual(colors.alpha, 0.5)

    def test_empty_pb_rgb_color_data(self):
        from google.type.color_pb2 import Color

        color_pb = Color()
        color_class = self._get_target_class()
        color = color_class.from_pb(color_pb)
        self.assertEqual(color.red, 0.0)
        self.assertEqual(color.green, 0.0)
        self.assertEqual(color.blue, 0.0)
        self.assertEqual(color.alpha, 0.0)

    def test_pb_rgb_color_data(self):
        from google.protobuf.wrappers_pb2 import FloatValue
        from google.type.color_pb2 import Color

        alpha = FloatValue(value=1.0)
        color_pb = Color(red=1.0, green=2.0, blue=3.0, alpha=alpha)
        color_class = self._get_target_class()
        color = color_class.from_pb(color_pb)
        self.assertEqual(color.red, 1.0)
        self.assertEqual(color.green, 2.0)
        self.assertEqual(color.blue, 3.0)
        self.assertEqual(color.alpha, 1.0)

    def test_pb_rgb_color_no_alpha_data(self):
        from google.protobuf.wrappers_pb2 import FloatValue
        from google.type.color_pb2 import Color

        alpha = FloatValue()
        color_pb = Color(red=1.0, green=2.0, blue=3.0, alpha=alpha)
        color_class = self._get_target_class()
        color = color_class.from_pb(color_pb)
        self.assertEqual(color.red, 1.0)
        self.assertEqual(color.green, 2.0)
        self.assertEqual(color.blue, 3.0)
        self.assertEqual(color.alpha, 0.0)

    def test_missing_rgb_values(self):
        colors = {}
        color_class = self._get_target_class()
        colors = color_class.from_api_repr(colors)

        self.assertEqual(colors.red, 0)
        self.assertEqual(colors.green, 0)
        self.assertEqual(colors.blue, 0)
        self.assertEqual(colors.alpha, 0.0)


class TestImagePropertiesAnnotation(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.color import ImagePropertiesAnnotation
        return ImagePropertiesAnnotation

    def test_image_properties_annotation_from_pb(self):
        from google.cloud.proto.vision.v1 import image_annotator_pb2
        from google.protobuf.wrappers_pb2 import FloatValue
        from google.type.color_pb2 import Color

        alpha = FloatValue(value=1.0)
        color_pb = Color(red=1.0, green=2.0, blue=3.0, alpha=alpha)
        color_info_pb = image_annotator_pb2.ColorInfo(color=color_pb,
                                                      score=1.0,
                                                      pixel_fraction=1.0)
        dominant_colors = image_annotator_pb2.DominantColorsAnnotation(
            colors=[color_info_pb])

        image_properties_pb = image_annotator_pb2.ImageProperties(
            dominant_colors=dominant_colors)

        color_info = self._get_target_class()
        image_properties = color_info.from_pb(image_properties_pb)

        self.assertEqual(image_properties.colors[0].pixel_fraction, 1.0)
        self.assertEqual(image_properties.colors[0].score, 1.0)
        self.assertEqual(image_properties.colors[0].color.red, 1.0)
        self.assertEqual(image_properties.colors[0].color.green, 2.0)
        self.assertEqual(image_properties.colors[0].color.blue, 3.0)
        self.assertEqual(image_properties.colors[0].color.alpha, 1.0)

    def test_empty_image_properties_annotation_from_pb(self):
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        image_properties_pb = image_annotator_pb2.ImageProperties()

        color_info = self._get_target_class()
        image_properties = color_info.from_pb(image_properties_pb)
        self.assertIsNone(image_properties)
