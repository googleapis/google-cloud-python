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


class TestFeature(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.feature import Feature

        return Feature

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_construct_feature(self):
        from google.cloud.vision.feature import FeatureTypes

        feature = self._make_one(FeatureTypes.LABEL_DETECTION)
        self.assertEqual(feature.max_results, 1)
        self.assertEqual(feature.feature_type, 'LABEL_DETECTION')

        feature = self._make_one(FeatureTypes.FACE_DETECTION, 3)
        self.assertEqual(feature.max_results, 3)
        self.assertEqual(feature.feature_type, 'FACE_DETECTION')

    def test_feature_as_dict(self):
        from google.cloud.vision.feature import FeatureTypes

        feature = self._make_one(FeatureTypes.FACE_DETECTION, max_results=5)
        expected = {
            'type': 'FACE_DETECTION',
            'maxResults': 5
        }
        self.assertEqual(feature.as_dict(), expected)

    def test_bad_feature_type(self):
        with self.assertRaises(AttributeError):
            self._make_one('something_not_feature_type',
                           max_results=5)
