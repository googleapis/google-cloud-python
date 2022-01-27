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
from ..common.python import CommonPython


class TestAppEngineFlex(Common, CommonPython, unittest.TestCase):

    environment = "appengine_flex_python"
    language = "python"

    monitored_resource_name = "gae_app"
    monitored_resource_labels = ["project_id", "module_id", "version_id", "zone"]

    def test_pylogging_gae_trace_label(self):
        """
        Check to make sure 'appengine.googleapis.com/trace_id' label is set on GAE environments
        """
        expected_trace = "123"
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(
            log_text, "pylogging_flask", trace=expected_trace
        )
        found_log = log_list[-1]

        self.assertIsNotNone(found_log.labels)
        self.assertIsNotNone(found_log.trace)
        self.assertEqual(
            found_log.labels["appengine.googleapis.com/trace_id"], found_log.trace
        )
        self.assertIn(expected_trace, found_log.trace)
