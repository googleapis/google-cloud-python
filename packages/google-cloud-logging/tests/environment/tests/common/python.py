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
        log_list = self.trigger_and_retrieve(log_text, "pylogging")

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
        log_list = self.trigger_and_retrieve(log_text, "pylogging")
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
                log_text, "pylogging", severity=severity
            )
            found_severity = log_list[-1].severity

            self.assertEqual(found_severity.lower(), severity.lower())

    def test_source_location_pylogging(self):
        if self.environment == "kubernetes" or "appengine" in self.environment:
            # disable these tests on environments with custom handlers
            # todo: enable in v3.0.0
            return
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, "pylogging")
        found_source = log_list[-1].source_location

        self.assertIsNotNone(found_source)
        self.assertIsNotNone(found_source['file'])
        self.assertIsNotNone(found_source['function'])
        self.assertIsNotNone(found_source['line'])
        self.assertIn("snippets.py", found_source['file'])
        self.assertEqual(found_source['function'], "pylogging")
        self.assertTrue(int(found_source['line']) > 0)

    def test_flask_http_request_pylogging(self):
        if self.environment == "kubernetes" or "appengine" in self.environment:
            # disable these tests on environments with custom handlers
            # todo: enable in v3.0.0
            return
        log_text = f"{inspect.currentframe().f_code.co_name}"

        expected_agent = "test-agent"
        expected_base_url = "http://test"
        expected_path = "/pylogging"
        expected_trace = "123"

        log_list = self.trigger_and_retrieve(log_text, "pylogging_flask",
                path=expected_path, trace=expected_trace, base_url=expected_base_url, agent=expected_agent)
        found_request = log_list[-1].http_request

        self.assertIsNotNone(found_request)
        self.assertIsNotNone(found_request['requestMethod'])
        self.assertIsNotNone(found_request['requestUrl'])
        self.assertIsNotNone(found_request['userAgent'])
        self.assertIsNotNone(found_request['protocol'])
        self.assertEqual(found_request['requestMethod'], 'GET')
        self.assertEqual(found_request['requestUrl'], expected_base_url + expected_path)
        self.assertEqual(found_request['userAgent'], expected_agent)
        self.assertEqual(found_request['protocol'], 'HTTP/1.1')

        found_trace = log_list[-1].trace
        self.assertIsNotNone(found_trace)
        self.assertIn("projects/", found_trace)

    def test_pylogging_extras(self):
        if self.environment == "kubernetes" or "appengine" in self.environment:
            # disable these tests on environments with custom handlers
            # todo: enable in v3.0.0
            return
        log_text = f"{inspect.currentframe().f_code.co_name}"
        kwargs = {
            'trace': '123',
            'requestMethod': 'POST',
            'requestUrl': 'http://test',
            'userAgent': 'agent',
            'protocol': 'test',
            'line': 25,
            'file': 'test-file',
            'function': 'test-function'
        }
        log_list = self.trigger_and_retrieve(log_text, "pylogging", **kwargs)
        found_log = log_list[-1]

        if self.environment != "functions":
            # functions seems to override the user's trace value
            self.assertEqual(found_log.trace, kwargs['trace'])

        # check that custom http request fields were set
        self.assertIsNotNone(found_log.http_request)
        for field in ['requestMethod', 'requestUrl', 'userAgent', 'protocol']:
            self.assertIsNotNone(found_log.http_request[field],
                    'http_request[{field}] is unexpectedly None')
            self.assertEqual(found_log.http_request[field], kwargs[field],
                    f'http_request[{field}] != {kwargs[field]}')
        # check that custom source location fields were set
        self.assertIsNotNone(found_log.source_location)
        for field in ['line', 'file', 'function']:
            self.assertIsNotNone(found_log.source_location[field],
                    f'source_location[{field}] is unexpectedly None')
            self.assertEqual(found_log.source_location[field], kwargs[field],
                    f'source_location[{field}] != {kwargs[field]}')

    def test_pylogging_extras_sparse(self):
        if self.environment == "kubernetes" or "appengine" in self.environment:
            # disable these tests on environments with custom handlers
            # todo: enable in v3.0.0
            return
        log_text = f"{inspect.currentframe().f_code.co_name}"
        kwargs = {
            'requestMethod': 'POST',
            'file': 'test-file',
        }
        log_list = self.trigger_and_retrieve(log_text, "pylogging", **kwargs)
        found_log = log_list[-1]

        # check that custom http request fields were set
        self.assertIsNotNone(found_log.http_request)
        self.assertEqual(found_log.http_request["requestMethod"], kwargs["requestMethod"])
        for field in ['requestUrl', 'userAgent', 'protocol']:
            self.assertIsNone(found_log.http_request.get(field, None),
                    f'http_request[{field}] is unexpectedly not None')
        # check that custom source location fields were set
        self.assertIsNotNone(found_log.source_location)
        self.assertEqual(found_log.source_location['file'], kwargs['file'])
        for field in ['line', 'function']:
            self.assertIsNone(found_log.source_location.get(field, None),
                    f'source_location[{field}] is unexpectedly not None')
