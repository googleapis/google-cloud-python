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


class CommonPython:
    def test_pylogging_receive_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, "pylogging")

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")
        self.assertTrue(isinstance(found_log.payload, str), "expected textPayload")
        self.assertTrue(found_log.payload.startswith(log_text))
        self.assertEqual(len(log_list), 1, "expected 1 log")

    def test_pylogging_receive_unicode_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name} 嗨 世界 😀"
        log_list = self.trigger_and_retrieve(log_text, "pylogging")

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")
        self.assertTrue(isinstance(found_log.payload, str), "expected textPayload")
        self.assertTrue(found_log.payload.startswith(log_text))

    def test_pylogging_json_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name} {uuid.uuid1()}"
        log_dict = {"unicode_field": "嗨 世界 😀", "num_field": 2}
        log_list = self.trigger_and_retrieve(
            log_text, "pylogging_json", append_uuid=False, **log_dict
        )

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")
        self.assertTrue(isinstance(found_log.payload, dict), "expected jsonPayload")
        expected_dict = {"message": log_text, **log_dict}
        self.assertEqual(found_log.payload, expected_dict)

    def test_pylogging_encoded_json_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name} {uuid.uuid1()}"
        log_dict = {"unicode_field": "嗨 世界 😀", "num_field": 2}
        log_list = self.trigger_and_retrieve(
            log_text,
            "pylogging_json",
            string_encode="True",
            append_uuid=False,
            **log_dict,
        )

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")
        self.assertTrue(isinstance(found_log.payload, dict), "expected jsonPayload")
        raw_str = found_log.payload.pop("raw_str")
        expected_dict = {"message": log_text, **log_dict}
        self.assertEqual(json.loads(raw_str), expected_dict)
        self.assertEqual(found_log.payload, expected_dict)

    def test_pylogging_multiline(self):
        first_line = f"{inspect.currentframe().f_code.co_name}"
        second_line = "hello world"
        log_list = self.trigger_and_retrieve(
            first_line, "pylogging_multiline", second_line=second_line
        )
        found_log = log_list[-1]
        found_message = (
            found_log.payload.get("message", None)
            if isinstance(found_log.payload, dict)
            else str(found_log.payload)
        )

        self.assertTrue(re.match(f"{first_line} .*\n{second_line}", found_message))

    def test_pylogging_with_argument(self):
        log_text = f"{inspect.currentframe().f_code.co_name} Name: %s"
        name_arg = "Daniel"
        log_list = self.trigger_and_retrieve(log_text, "pylogging_with_arg")
        found_log = log_list[-1]
        found_message = (
            found_log.payload.get("message", None)
            if isinstance(found_log.payload, dict)
            else str(found_log.payload)
        )

        self.assertTrue(re.match(f"Arg: {log_text} .*", found_message))

    def test_pylogging_with_formatter(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        format_str = "%(levelname)s :: %(message)s"
        log_list = self.trigger_and_retrieve(
            log_text, "pylogging_with_formatter", format_str=format_str
        )
        found_log = log_list[-1]
        found_message = (
            found_log.payload.get("message", None)
            if isinstance(found_log.payload, dict)
            else str(found_log.payload)
        )

        self.assertTrue(re.match(f"ERROR :: {log_text} .*", found_message))

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
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, "pylogging")
        found_source = log_list[-1].source_location

        self.assertIsNotNone(found_source)
        self.assertIsNotNone(found_source["file"])
        self.assertIsNotNone(found_source["function"])
        self.assertIsNotNone(found_source["line"])
        self.assertIn("snippets.py", found_source["file"])
        self.assertEqual(found_source["function"], "pylogging")
        self.assertTrue(int(found_source["line"]) > 0)

    def test_flask_http_request_pylogging(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"

        expected_agent = "test-agent"
        expected_base_url = "http://test"
        expected_path = "/pylogging"
        expected_trace = "123"
        expected_span = "456"
        trace_header = f"{expected_trace}/{expected_span};o=1"

        log_list = self.trigger_and_retrieve(
            log_text,
            "pylogging_flask",
            path=expected_path,
            trace=trace_header,
            base_url=expected_base_url,
            agent=expected_agent,
        )
        found_request = log_list[-1].http_request

        self.assertIsNotNone(found_request)
        self.assertIsNotNone(found_request["requestMethod"])
        self.assertIsNotNone(found_request["requestUrl"])
        self.assertIsNotNone(found_request["userAgent"])
        self.assertIsNotNone(found_request["protocol"])
        self.assertEqual(found_request["requestMethod"], "GET")
        self.assertEqual(found_request["requestUrl"], expected_base_url + expected_path)
        self.assertEqual(found_request["userAgent"], expected_agent)
        self.assertEqual(found_request["protocol"], "HTTP/1.1")

        found_trace = log_list[-1].trace
        found_span = log_list[-1].span_id
        found_sampled = log_list[-1].trace_sampled
        self.assertIsNotNone(found_trace)
        self.assertIn("projects/", found_trace)
        if self.environment != "functions":
            # functions seems to override the user's trace value
            self.assertIn(expected_trace, found_trace)
            self.assertEqual(expected_span, found_span)
            self.assertTrue(found_sampled)

    def test_flask_traceparent(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"

        expected_agent = "test-agent"
        expected_base_url = "http://test"
        expected_path = "/pylogging"
        expected_trace = "4bf92f3577b34da6a3ce929d0e0e4736"
        expected_span = "00f067aa0ba902b7"
        trace_header = f"00-{expected_trace}-{expected_span}-09"

        log_list = self.trigger_and_retrieve(
            log_text,
            "pylogging_flask",
            path=expected_path,
            trace="",
            traceparent=trace_header,
            base_url=expected_base_url,
            agent=expected_agent,
        )
        found_request = log_list[-1].http_request

        self.assertIsNotNone(found_request)

        found_trace = log_list[-1].trace
        found_span = log_list[-1].span_id
        found_sampled = log_list[-1].trace_sampled
        self.assertIsNotNone(found_trace)
        self.assertIn("projects/", found_trace)
        if self.environment != "functions":
            # functions seems to override the user's trace value
            self.assertIn(expected_trace, found_trace)
            self.assertEqual(expected_span, found_span)
            self.assertTrue(found_sampled)

    def test_pylogging_extras(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        kwargs = {
            "trace": "123",
            "span_id": "456",
            "requestMethod": "POST",
            "requestUrl": "http://test",
            "userAgent": "agent",
            "protocol": "test",
            "line": 25,
            "file": "test-file",
            "function": "test-function",
            "label_custom": "test-label",
        }
        log_list = self.trigger_and_retrieve(log_text, "pylogging", **kwargs)
        found_log = log_list[-1]

        if self.environment != "functions":
            # functions seems to override the user's trace value
            self.assertEqual(found_log.trace, kwargs["trace"])
            self.assertEqual(found_log.span_id, kwargs["span_id"])

        # check that custom http request fields were set
        self.assertIsNotNone(found_log.http_request)
        for field in ["requestMethod", "requestUrl", "userAgent", "protocol"]:
            self.assertIsNotNone(
                found_log.http_request[field],
                "http_request[{field}] is unexpectedly None",
            )
            self.assertEqual(
                found_log.http_request[field],
                kwargs[field],
                f"http_request[{field}] != {kwargs[field]}",
            )
        # check that custom source location fields were set
        self.assertIsNotNone(found_log.source_location)
        for field in ["line", "file", "function"]:
            self.assertIsNotNone(
                found_log.source_location[field],
                f"source_location[{field}] is unexpectedly None",
            )
            self.assertEqual(
                found_log.source_location[field],
                kwargs[field],
                f"source_location[{field}] != {kwargs[field]}",
            )
        # check that custom label is set
        self.assertIsNotNone(found_log.labels)
        self.assertEqual(found_log.labels["custom"], kwargs["label_custom"])

    def test_pylogging_extras_sparse(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        kwargs = {
            "requestMethod": "POST",
            "file": "test-file",
        }
        log_list = self.trigger_and_retrieve(log_text, "pylogging", **kwargs)
        found_log = log_list[-1]

        # check that custom http request fields were set
        self.assertIsNotNone(found_log.http_request)
        self.assertEqual(
            found_log.http_request["requestMethod"], kwargs["requestMethod"]
        )
        for field in ["requestUrl", "userAgent", "protocol"]:
            self.assertIsNone(
                found_log.http_request.get(field, None),
                f"http_request[{field}] is unexpectedly not None",
            )
        # check that custom source location fields were set
        self.assertIsNotNone(found_log.source_location)
        self.assertEqual(found_log.source_location["file"], kwargs["file"])
        for field in ["line", "function"]:
            self.assertIsNone(
                found_log.source_location.get(field, None),
                f"source_location[{field}] is unexpectedly not None",
            )

    def test_pylogging_exception(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        exception_text = "test_exception"
        log_list = self.trigger_and_retrieve(
            log_text, "pylogging_exception", exception_text=exception_text
        )
        found_log = log_list[-1]

        message = (
            found_log.payload.get("message", None)
            if isinstance(found_log.payload, dict)
            else str(found_log.payload)
        )

        self.assertIn(log_text, message)
        self.assertIn(f"Exception: {exception_text}", message)
        self.assertIn("Traceback (most recent call last):", message)

    def test_pylogging_pandas(self):
        """
        Ensure pandas dataframes are parsed without crashing
        https://github.com/googleapis/python-logging/issues/409
        """
        import pandas as pd

        log_text = f"{inspect.currentframe().f_code.co_name} {str(uuid.uuid1())[-10:]}"

        log_list = self.trigger_and_retrieve(
            log_text, "pylogging_pandas", append_uuid=False
        )
        found_log = log_list[-1]

        message = (
            found_log.payload.get("message", None)
            if isinstance(found_log.payload, dict)
            else str(found_log.payload)
        )

        df = pd.DataFrame(columns=["log_text"])
        df = df.append({"log_text": log_text}, ignore_index=True)

        self.assertEqual(str(df), message)
