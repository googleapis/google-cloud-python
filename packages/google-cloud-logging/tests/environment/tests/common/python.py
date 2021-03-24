# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
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


class CommonPython:
    def pylogging_test_receive_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, function="pylogging")

        found_log = None
        for log in log_list:
            message = (
                log.payload.get("message", None)
                if isinstance(log.payload, dict)
                else str(log.payload)
            )
            if message and log_text in message:
                found_log = log
        self.assertIsNotNone(found_log, "expected log text not found")

    def test_monitored_resource_pylogging(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, function="pylogging")
        found_resource = log_list[-1].resource

        self.assertIsNotNone(self.monitored_resource_name)
        self.assertIsNotNone(self.monitored_resource_labels)

        self.assertEqual(found_resource.type, self.monitored_resource_name)
        for label in self.monitored_resource_labels:
            self.assertTrue(
                found_resource.labels[label], f"resource.labels[{label}] is not set"
            )

    def test_severity_pylogging(self):
        severities = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
        for severity in severities:
            log_text = f"{inspect.currentframe().f_code.co_name}"
            log_list = self.trigger_and_retrieve(
                log_text, function="pylogging", severity=severity
            )
            found_severity = log_list[-1].severity

            self.assertEqual(found_severity.lower(), severity.lower())
