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


class TestSafeSearchAnnotation(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.safe_search import SafeSearchAnnotation

        return SafeSearchAnnotation

    def test_safe_search_annotation(self):
        from google.cloud.vision.likelihood import Likelihood
        from tests.unit._fixtures import SAFE_SEARCH_DETECTION_RESPONSE

        response = SAFE_SEARCH_DETECTION_RESPONSE['responses'][0]
        safe_search_response = response['safeSearchAnnotation']

        safe_search = self._get_target_class().from_api_repr(
            safe_search_response)

        self.assertIs(safe_search.adult, Likelihood.VERY_UNLIKELY)
        self.assertIs(safe_search.spoof, Likelihood.UNLIKELY)
        self.assertIs(safe_search.medical, Likelihood.POSSIBLE)
        self.assertIs(safe_search.violence, Likelihood.VERY_UNLIKELY)

    def test_pb_safe_search_annotation(self):
        from google.cloud.vision.likelihood import Likelihood
        from google.cloud.proto.vision.v1.image_annotator_pb2 import (
            Likelihood as LikelihoodPB)
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        possible = LikelihoodPB.Value('POSSIBLE')
        possible_name = Likelihood.POSSIBLE
        safe_search_annotation = image_annotator_pb2.SafeSearchAnnotation(
            adult=possible, spoof=possible, medical=possible, violence=possible
        )

        safe_search = self._get_target_class().from_pb(safe_search_annotation)

        self.assertIs(safe_search.adult, possible_name)
        self.assertIs(safe_search.spoof, possible_name)
        self.assertIs(safe_search.medical, possible_name)
        self.assertIs(safe_search.violence, possible_name)

    def test_empty_pb_safe_search_annotation(self):
        from google.cloud.vision.likelihood import Likelihood
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        unknown = Likelihood.UNKNOWN
        safe_search_annotation = image_annotator_pb2.SafeSearchAnnotation()

        safe_search = self._get_target_class().from_pb(safe_search_annotation)

        self.assertIs(safe_search.adult, unknown)
        self.assertIs(safe_search.spoof, unknown)
        self.assertIs(safe_search.medical, unknown)
        self.assertIs(safe_search.violence, unknown)
