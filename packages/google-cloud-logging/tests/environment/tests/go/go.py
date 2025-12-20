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
import re
import uuid
import json

import google.cloud.logging

from ..common.common import Common


class CommonGolang:
    """
    Common tests to run on all go environments
    """

    def test_standard_logger_receive_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, "standardlogger")

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")
        self.assertTrue(isinstance(found_log.payload, str), "expected textPayload")
        self.assertTrue(found_log.payload.startswith(log_text))
        self.assertEqual(len(log_list), 1, "expected 1 log")

    def test_standard_logger_receive_unicode_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name} 嗨 世界 😀"
        log_list = self.trigger_and_retrieve(log_text, "standardlogger")

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")
        self.assertTrue(isinstance(found_log.payload, str), "expected textPayload")
        self.assertTrue(found_log.payload.startswith(log_text))

    def test_severity_standard_logger(self):
        severities = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
        for severity in severities:
            log_text = f"{inspect.currentframe().f_code.co_name}"
            log_list = self.trigger_and_retrieve(
                log_text, "standardlogger", severity=severity
            )
            found_severity = log_list[-1].severity

            self.assertEqual(found_severity.lower(), severity.lower())

    def test_synclog_receive_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, "synclog")

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")
        self.assertTrue(isinstance(found_log.payload, str), "expected textPayload")
        self.assertTrue(found_log.payload.startswith(log_text))
        self.assertEqual(len(log_list), 1, "expected 1 log")

    def test_synclog_receive_unicode_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name} 嗨 世界 😀"
        log_list = self.trigger_and_retrieve(log_text, "synclog")

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")
        self.assertTrue(isinstance(found_log.payload, str), "expected textPayload")
        self.assertTrue(found_log.payload.startswith(log_text))

    def test_severity_synclog(self):
        severities = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
        for severity in severities:
            log_text = f"{inspect.currentframe().f_code.co_name}"
            log_list = self.trigger_and_retrieve(
                log_text, "synclog", severity=severity
            )
            found_severity = log_list[-1].severity

            self.assertEqual(found_severity.lower(), severity.lower())

    def test_http_request(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        test_url = "www.google.com"
        log_list = self.trigger_and_retrieve(log_text, "simplelog", http_request_url=test_url)

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")

        found_request = log_list[-1].http_request
        self.assertIsNotNone(found_request)
        self.assertIsNotNone(found_request["requestUrl"])
        self.assertEqual(found_request["requestUrl"], test_url)


