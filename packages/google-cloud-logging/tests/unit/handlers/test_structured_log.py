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
        self.assertIsNone(handler.name)

    def test_ctor_w_name(self):
        handler = self._make_one(name="foo")
        self.assertEqual(handler.name, "foo")

    def test_format(self):
        import logging
        import json

        handler = self._make_one()
        logname = "loggername"
        message = "hello world，嗨 世界"
        pathname = "testpath"
        lineno = 1
        func = "test-function"
        record = logging.LogRecord(
            logname, logging.INFO, pathname, lineno, message, None, None, func=func
        )
        expected_payload = {
            "message": message,
            "severity": record.levelname,
            "logging.googleapis.com/trace": "",
            "logging.googleapis.com/sourceLocation": {
                "file": pathname,
                "line": str(lineno),
                "function": func,
            },
            "httpRequest": {
                "requestMethod": "",
                "requestUrl": "",
                "userAgent": "",
                "protocol": "",
            },
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
        record = logging.LogRecord(None, logging.INFO, None, None, None, None, None,)
        record.created = None
        expected_payload = {
            "message": "",
            "logging.googleapis.com/trace": "",
            "logging.googleapis.com/sourceLocation": {
                "file": "",
                "line": "0",
                "function": "",
            },
            "httpRequest": {
                "requestMethod": "",
                "requestUrl": "",
                "userAgent": "",
                "protocol": "",
            },
        }
        handler.filter(record)
        result = json.loads(handler.format(record))
        for (key, value) in expected_payload.items():
            self.assertEqual(
                value, result[key], f"expected_payload[{key}] != result[{key}]"
            )

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
        expected_payload = {
            "logging.googleapis.com/trace": expected_trace,
            "httpRequest": {
                "requestMethod": "PUT",
                "requestUrl": expected_path,
                "userAgent": expected_agent,
                "protocol": "HTTP/1.1",
            },
        }

        app = self.create_app()
        with app.test_client() as c:
            c.put(
                path=expected_path,
                data="body",
                headers={
                    "User-Agent": expected_agent,
                    "X_CLOUD_TRACE_CONTEXT": expected_trace,
                },
            )
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

        handler = self._make_one()
        logname = "loggername"
        message = "hello world，嗨 世界"
        record = logging.LogRecord(logname, logging.INFO, "", 0, message, None, None)
        overwrite_path = "http://overwrite"
        inferred_path = "http://testserver/123"
        overwrite_trace = "456"
        inferred_trace = "123"
        overwrite_file = "test-file"
        record.http_request = {"requestUrl": overwrite_path}
        record.source_location = {"file": overwrite_file}
        record.trace = overwrite_trace
        expected_payload = {
            "logging.googleapis.com/trace": overwrite_trace,
            "logging.googleapis.com/sourceLocation": {
                "file": overwrite_file,
                "function": "",
                "line": "0",
            },
            "httpRequest": {
                "requestMethod": "",
                "requestUrl": overwrite_path,
                "userAgent": "",
                "protocol": "",
            },
        }

        app = self.create_app()
        with app.test_client() as c:
            c.put(
                path=inferred_path,
                data="body",
                headers={"X_CLOUD_TRACE_CONTEXT": inferred_trace},
            )
            handler.filter(record)
            result = json.loads(handler.format(record))
            for (key, value) in expected_payload.items():
                self.assertEqual(value, result[key])
