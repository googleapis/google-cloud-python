# Copyright 2016 Google Inc. All rights reserved.
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
    def _getTargetClass(self):
        from gcloud.vision.feature import Feature
        return Feature

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_construct_feature(self):
        from gcloud.vision.feature import FeatureTypes
        feature = self._makeOne(FeatureTypes.LABEL_DETECTION)
        self.assertEqual(1, feature.max_results)
        self.assertEqual('LABEL_DETECTION', feature.feature_type)

        feature = self._makeOne(FeatureTypes.FACE_DETECTION, 3)
        self.assertEqual(3, feature.max_results)
        self.assertEqual('FACE_DETECTION', feature.feature_type)

    def test_feature_as_dict(self):
        from gcloud.vision.feature import FeatureTypes
        feature = self._makeOne(FeatureTypes.FACE_DETECTION, max_results=5)
        EXPECTED = {
            'type': 'FACE_DETECTION',
            'maxResults': 5
        }
        self.assertEqual(EXPECTED, feature.as_dict())

    def test_bad_feature_type(self):
        with self.assertRaises(AttributeError):
            self._makeOne('something_not_feature_type',
                          max_results=5)
