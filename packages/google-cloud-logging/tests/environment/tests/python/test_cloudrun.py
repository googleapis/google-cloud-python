# Copyright 2021 Google LLC
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
import uuid

import google.cloud.logging
from google.cloud.logging_v2.resource import Resource

from ..common.common import Common
from ..common.python import CommonPython


class TestCloudRun(Common, CommonPython, unittest.TestCase):

    environment = "cloudrun"
    language = "python"

    monitored_resource_name = "cloud_run_revision"
    monitored_resource_labels = [
        "project_id",
        "service_name",
        "revision_name",
        "location",
        "configuration_name",
    ]

    def test_default_http_request_pylogging(self):
        """
        Cloud Run should automatically attach http request information
        """
        log_text = f"{inspect.currentframe().f_code.co_name}"

        log_list = self.trigger_and_retrieve(log_text, "pylogging")
        found_request = log_list[-1].http_request
        found_trace = log_list[-1].trace

        self.assertIsNotNone(found_request)
        self.assertIsNotNone(found_request["requestMethod"])
        self.assertIsNotNone(found_request["requestUrl"])
        self.assertIsNotNone(found_request["userAgent"])
        self.assertIsNotNone(found_request["protocol"])
        self.assertEqual(found_request["requestMethod"], "POST")
        self.assertEqual(found_request["protocol"], "HTTP/1.1")

        self.assertIsNotNone(found_trace)
        self.assertIn("projects/", found_trace)
