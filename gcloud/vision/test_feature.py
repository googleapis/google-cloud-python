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

import unittest2

from gcloud.vision.feature import Feature
from gcloud.vision.feature import FeatureTypes


class TestFeature(unittest2.TestCase):

    def test_construct_feature(self):
        feature = Feature(FeatureTypes.LABEL_DETECTION)
        self.assertEqual(1, feature.max_results)
        self.assertEqual('LABEL_DETECTION', feature.feature_type)

        feature = Feature(FeatureTypes.FACE_DETECTION, 3)
        self.assertEqual(3, feature.max_results)
        self.assertEqual('FACE_DETECTION', feature.feature_type)
