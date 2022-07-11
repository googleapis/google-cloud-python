# Copyright 2021 Google LLC All Rights Reserved.
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


class TestStructuredLogHandler(unittest.TestCase):
    PROJECT = "PROJECT"

    def _get_target_class(self):
        from google.cloud.logging.handlers import StructuredLogHandler

        return StructuredLogHandler

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    @staticmethod
    def create_app():
        import flask

        app = flask.Flask(__name__)

        @app.route("/")
        def index():
            return "test flask trace"  # pragma: NO COVER

        return app

    def test_ctor_defaults(self):
        handler = self._make_one()
        self.assertIsNone(handler.project_id)

    def test_ctor_w_project(self):
        handler = self._make_one(project_id="foo")
        self.assertEqual(handler.project_id, "foo")

    def test_format(self):
        import logging
        import json

        labels = {"default_key": "default-value"}
        handler = self._make_one(labels=labels)
        logname = "loggername"
        message = "hello world，嗨 世界"
        pathname = "testpath"
        lineno = 1
        func = "test-function"
        record = logging.LogRecord(
            logname, logging.INFO, pathname, lineno, message, None, None, func=func
        )
        expected_labels = {**labels, "python_logger": logname}
        expected_payload = {
            "message": message,
            "severity": record.levelname,
            "logging.googleapis.com/trace": "",
            "logging.googleapis.com/spanId": "",
            "logging.googleapis.com/trace_sampled": False,
            "logging.googleapis.com/sourceLocation": {
                "file": pathname,
                "line": lineno,
                "function": func,
            },
            "httpRequest": {},
            "logging.googleapis.com/labels": expected_labels,
        }
        handler.filter(record)
        result = json.loads(handler.format(record))
        for (key, value) in expected_payload.items():
            self.assertEqual(value, result[key])
        self.assertEqual(
            len(expected_payload.keys()),
            len(result.keys()),
            f"result dictionary has unexpected keys: {result.keys()}",
        )

    def test_format_minimal(self):
        import logging
        import json

        handler = self._make_one()
        record = logging.LogRecord(
            None,
            logging.INFO,
            None,
            None,
            None,
            None,
            None,
        )
        record.created = None
        expected_payload = {
            "severity": "INFO",
            "logging.googleapis.com/trace": "",
            "logging.googleapis.com/spanId": "",
            "logging.googleapis.com/trace_sampled": False,
            "logging.googleapis.com/sourceLocation": {},
            "httpRequest": {},
            "logging.googleapis.com/labels": {},
        }
        handler.filter(record)
        result = json.loads(handler.format(record))
        self.assertEqual(set(expected_payload.keys()), set(result.keys()))
        for (key, value) in expected_payload.items():
            self.assertEqual(
                value, result[key], f"expected_payload[{key}] != result[{key}]"
            )

    def test_format_with_quotes(self):
        """
        When logging a message containing quotes, escape chars should be added
        """
        import logging

        handler = self._make_one()
        message = '"test"'
        expected_result = '\\"test\\"'
        record = logging.LogRecord(
            None,
            logging.INFO,
            None,
            None,
            message,
            None,
            None,
        )
        record.created = None
        handler.filter(record)
        result = handler.format(record)
        self.assertIn(expected_result, result)

    def test_format_with_exception(self):
        """
        When logging a message with an exception, the stack trace should not be appended
        """
        import logging
        import json

        handler = self._make_one()
        exception_tuple = (Exception, Exception(), None)
        message = "test"
        record = logging.LogRecord(
            None, logging.INFO, None, None, message, None, exception_tuple
        )
        record.created = None
        handler.filter(record)
        result = json.loads(handler.format(record))
        self.assertEqual(result["message"], f"{message}\nException")

    def test_format_with_line_break(self):
        """
        When logging a message containing \n, it should be properly escaped
        """
        import logging

        handler = self._make_one()
        message = "test\ntest"
        expected_result = "test\\ntest"
        record = logging.LogRecord(
            None,
            logging.INFO,
            None,
            None,
            message,
            None,
            None,
        )
        record.created = None
        handler.filter(record)
        result = handler.format(record)
        self.assertIn(expected_result, result)

    def test_format_with_custom_formatter(self):
        """
        Handler should respect custom formatters attached
        """
        import logging

        handler = self._make_one()
        logFormatter = logging.Formatter(fmt="%(name)s :: %(levelname)s :: %(message)s")
        handler.setFormatter(logFormatter)
        message = "test"
        expected_result = "logname :: INFO :: test"
        record = logging.LogRecord(
            "logname",
            logging.INFO,
            None,
            None,
            message,
            None,
            None,
        )
        record.created = None
        handler.filter(record)
        result = handler.format(record)
        self.assertIn(expected_result, result)
        self.assertIn("message", result)

    def test_dict(self):
        """
        Handler should parse json encoded as a string
        """
        import logging

        handler = self._make_one()
        message = {"x": "test"}
        expected_result = '"x": "test"'
        record = logging.LogRecord(
            "logname",
            logging.INFO,
            None,
            None,
            message,
            None,
            None,
        )
        record.created = None
        handler.filter(record)
        result = handler.format(record)
        self.assertIn(expected_result, result)
        self.assertNotIn("message", result)

    def test_encoded_json(self):
        """
        Handler should parse json encoded as a string
        """
        import logging

        handler = self._make_one()
        logFormatter = logging.Formatter(fmt='{ "name" : "%(name)s" }')
        handler.setFormatter(logFormatter)
        expected_result = '"name": "logname"'
        record = logging.LogRecord(
            "logname",
            logging.INFO,
            None,
            None,
            None,
            None,
            None,
        )
        record.created = None
        handler.filter(record)
        result = handler.format(record)
        self.assertIn(expected_result, result)
        self.assertNotIn("message", result)

    def test_format_with_arguments(self):
        """
        Handler should support format string arguments
        """
        import logging

        handler = self._make_one()
        message = "name: %s"
        name_arg = "Daniel"
        expected_result = "name: Daniel"
        record = logging.LogRecord(
            None,
            logging.INFO,
            None,
            None,
            message,
            name_arg,
            None,
        )
        record.created = None
        handler.filter(record)
        result = handler.format(record)
        self.assertIn(expected_result, result)

    def test_format_with_request(self):
        import logging
        import json

        handler = self._make_one()
        logname = "loggername"
        message = "hello world，嗨 世界"
        record = logging.LogRecord(logname, logging.INFO, "", 0, message, None, None)
        expected_path = "http://testserver/123"
        expected_agent = "Mozilla/5.0"
        expected_trace = "123"
        expected_span = "456"
        trace_header = f"{expected_trace}/{expected_span};o=1"
        expected_payload = {
            "logging.googleapis.com/trace": expected_trace,
            "logging.googleapis.com/spanId": expected_span,
            "logging.googleapis.com/trace_sampled": True,
            "httpRequest": {
                "requestMethod": "GET",
                "requestUrl": expected_path,
                "userAgent": expected_agent,
                "protocol": "HTTP/1.1",
            },
        }

        app = self.create_app()
        with app.test_request_context(
            expected_path,
            headers={
                "User-Agent": expected_agent,
                "X_CLOUD_TRACE_CONTEXT": trace_header,
            },
        ):
            handler.filter(record)
            result = json.loads(handler.format(record))
            for (key, value) in expected_payload.items():
                self.assertEqual(value, result[key])

    def test_format_with_traceparent(self):
        import logging
        import json

        handler = self._make_one()
        logname = "loggername"
        message = "hello world，嗨 世界"
        record = logging.LogRecord(logname, logging.INFO, "", 0, message, None, None)
        expected_path = "http://testserver/123"
        expected_agent = "Mozilla/5.0"
        expected_trace = "4bf92f3577b34da6a3ce929d0e0e4736"
        expected_span = "00f067aa0ba902b7"
        trace_header = f"00-{expected_trace}-{expected_span}-09"
        expected_payload = {
            "logging.googleapis.com/trace": expected_trace,
            "logging.googleapis.com/spanId": expected_span,
            "logging.googleapis.com/trace_sampled": True,
            "httpRequest": {
                "requestMethod": "GET",
                "requestUrl": expected_path,
                "userAgent": expected_agent,
                "protocol": "HTTP/1.1",
            },
        }

        app = self.create_app()
        with app.test_request_context(
            expected_path,
            headers={"User-Agent": expected_agent, "TRACEPARENT": trace_header},
        ):
            handler.filter(record)
            result = json.loads(handler.format(record))
            for (key, value) in expected_payload.items():
                self.assertEqual(value, result[key])

    def test_format_overrides(self):
        """
        Allow users to override log fields using `logging.info("", extra={})`

        If supported fields were overriden by the user, those choices should
        take precedence.
        """
        import logging
        import json

        default_labels = {
            "default_key": "default-value",
            "overwritten_key": "bad_value",
        }
        handler = self._make_one(labels=default_labels)
        logname = "loggername"
        message = "hello world，嗨 世界"
        record = logging.LogRecord(logname, logging.INFO, "", 0, message, None, None)
        overwrite_path = "http://overwrite"
        inferred_path = "http://testserver/123"
        overwrite_trace = "abc"
        overwrite_span = "def"
        inferred_trace_span = "123/456;o=1"
        overwrite_file = "test-file"
        record.http_request = {"requestUrl": overwrite_path}
        record.source_location = {"file": overwrite_file}
        record.trace = overwrite_trace
        record.span_id = overwrite_span
        record.trace_sampled = False
        added_labels = {"added_key": "added_value", "overwritten_key": "new_value"}
        record.labels = added_labels
        expected_payload = {
            "logging.googleapis.com/trace": overwrite_trace,
            "logging.googleapis.com/spanId": overwrite_span,
            "logging.googleapis.com/trace_sampled": False,
            "logging.googleapis.com/sourceLocation": {"file": overwrite_file},
            "httpRequest": {"requestUrl": overwrite_path},
            "logging.googleapis.com/labels": {
                "default_key": "default-value",
                "overwritten_key": "new_value",
                "added_key": "added_value",
                "python_logger": logname,
            },
        }

        app = self.create_app()
        with app.test_client() as c:
            c.put(
                path=inferred_path,
                data="body",
                headers={"X_CLOUD_TRACE_CONTEXT": inferred_trace_span},
            )
            handler.filter(record)
            result = json.loads(handler.format(record))
            for (key, value) in expected_payload.items():
                self.assertEqual(value, result[key])

    def test_format_with_json_fields(self):
        """
        User can add json_fields to the record, which should populate the payload
        """
        import logging
        import json

        handler = self._make_one()
        message = "name: %s"
        name_arg = "Daniel"
        expected_result = "name: Daniel"
        json_fields = {"hello": "world", "number": 12}
        record = logging.LogRecord(
            None,
            logging.INFO,
            None,
            None,
            message,
            name_arg,
            None,
        )
        record.created = None
        setattr(record, "json_fields", json_fields)
        handler.filter(record)
        result = json.loads(handler.format(record))
        self.assertEqual(result["message"], expected_result)
        self.assertEqual(result["hello"], "world")
        self.assertEqual(result["number"], 12)

    def test_emits_instrumentation_info(self):
        import logging
        import mock
        import google.cloud.logging_v2

        handler = self._make_one()
        logname = "loggername"
        message = "Hello world!"

        record = logging.LogRecord(logname, logging.INFO, "", 0, message, None, None)

        with mock.patch.object(handler, "emit_instrumentation_info") as emit_info:

            def side_effect():
                google.cloud.logging_v2._instrumentation_emitted = True

            emit_info.side_effect = side_effect
            google.cloud.logging_v2._instrumentation_emitted = False
            handler.emit(record)
            handler.emit(record)

            # emit_instrumentation_info should be called once
            emit_info.assert_called_once()
