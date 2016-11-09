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


class TestEntityAnnotation(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.entity import EntityAnnotation
        return EntityAnnotation

    def test_logo_annotation(self):
        from unit_tests._fixtures import LOGO_DETECTION_RESPONSE

        LOGO = LOGO_DETECTION_RESPONSE['responses'][0]['logoAnnotations'][0]
        entity_class = self._get_target_class()
        logo = entity_class.from_api_repr(LOGO)

        self.assertEqual('/m/05b5c', logo.mid)
        self.assertEqual('Brand1', logo.description)
        self.assertEqual(0.63192177, logo.score)
        self.assertEqual(162, logo.bounds.vertices[0].y_coordinate)
