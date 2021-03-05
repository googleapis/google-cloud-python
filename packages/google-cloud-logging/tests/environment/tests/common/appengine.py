# Copyright 2016 Google LLC
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

import logging
import unittest
import inspect

import google.cloud.logging

from ..common.common import Common


class CommonAppEngine:
    def test_monitored_resource(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text)
        found_resource = log_list[-1].resource

        self.assertEqual(found_resource.type, "gae_app")
        self.assertTrue(found_resource.labels["project_id"])
        self.assertTrue(found_resource.labels["module_id"])
        self.assertTrue(found_resource.labels["version_id"])
        self.assertTrue(found_resource.labels["zone"])
