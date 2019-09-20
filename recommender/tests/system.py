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

from google.cloud import recommender_v1beta1


class TestRecommender(unittest.TestCase):
    def test_list_recommendations(self):
        client = recommender_v1beta1.RecommenderClient()
        project_id = os.environ.get('PROJECT_ID')
        location = 'global'
        recommender = 'google.iam.policy.RoleRecommender'
        parent = client.recommender_path(project_id, location, recommender)
        client.list_recommendations(parent)