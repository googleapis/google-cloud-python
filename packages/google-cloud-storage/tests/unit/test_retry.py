# Copyright 2020 Google LLC
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

from google.cloud.storage.retry import DEFAULT_RETRY
from google.cloud.storage.retry import DEFAULT_RETRY_IF_GENERATION_SPECIFIED
from google.cloud.storage.retry import DEFAULT_RETRY_IF_METAGENERATION_SPECIFIED
from google.cloud.storage.retry import DEFAULT_RETRY_IF_ETAG_IN_JSON


class TestConditionalRetryPolicy(unittest.TestCase):
    def test_is_generation_specified_match_metageneration(self):
        conditional_policy = DEFAULT_RETRY_IF_GENERATION_SPECIFIED
        policy = conditional_policy.get_retry_policy_if_conditions_met(
            query_params={"if_generation_match": 1}
        )
        self.assertEqual(policy, DEFAULT_RETRY)

    def test_is_generation_specified_match_generation(self):
        conditional_policy = DEFAULT_RETRY_IF_GENERATION_SPECIFIED
        policy = conditional_policy.get_retry_policy_if_conditions_met(
            query_params={"generation": 1}
        )
        self.assertEqual(policy, DEFAULT_RETRY)

    def test_is_generation_specified_mismatch(self):
        conditional_policy = DEFAULT_RETRY_IF_GENERATION_SPECIFIED
        policy = conditional_policy.get_retry_policy_if_conditions_met(
            query_params={"if_metageneration_match": 1}
        )
        self.assertEqual(policy, None)

    def test_is_metageneration_specified_match(self):
        conditional_policy = DEFAULT_RETRY_IF_METAGENERATION_SPECIFIED
        policy = conditional_policy.get_retry_policy_if_conditions_met(
            query_params={"if_metageneration_match": 1}
        )
        self.assertEqual(policy, DEFAULT_RETRY)

    def test_is_metageneration_specified_mismatch(self):
        conditional_policy = DEFAULT_RETRY_IF_METAGENERATION_SPECIFIED
        policy = conditional_policy.get_retry_policy_if_conditions_met(
            query_params={"if_generation_match": 1}
        )
        self.assertEqual(policy, None)

    def test_is_etag_in_json_etag_match(self):
        conditional_policy = DEFAULT_RETRY_IF_ETAG_IN_JSON
        policy = conditional_policy.get_retry_policy_if_conditions_met(
            query_params={"if_generation_match": 1}, data='{"etag": "12345678"}'
        )
        self.assertEqual(policy, DEFAULT_RETRY)

    def test_is_etag_in_json_mismatch(self):
        conditional_policy = DEFAULT_RETRY_IF_ETAG_IN_JSON
        policy = conditional_policy.get_retry_policy_if_conditions_met(
            query_params={"if_generation_match": 1}, data="{}"
        )
        self.assertEqual(policy, None)

    def test_is_meta_or_etag_in_json_invalid(self):
        conditional_policy = DEFAULT_RETRY_IF_ETAG_IN_JSON
        policy = conditional_policy.get_retry_policy_if_conditions_met(
            query_params={"if_generation_match": 1}, data="I am invalid JSON!"
        )
        self.assertEqual(policy, None)
