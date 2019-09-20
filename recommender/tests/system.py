# -*- coding: utf-8 -*-
# Copyright 2019 Google LLC
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

import os
import unittest

from google.cloud.recommender_v1beta1.services.recommender import Recommender
from google.cloud.recommender_v1beta1 import ListRecommendationsRequest


class TestRecommender(unittest.TestCase):
    def test_list_recommendations(self):
        client = Recommender()
        PROJECT_ID = os.environ.get("PROJECT_ID")
        parent = f"projects/{PROJECT_ID}/locations/global"
        request = ListRecommendationsRequest(parent=parent)
        client.list_recommendations(request=request)