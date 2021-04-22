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
from unittest.mock import patch
import mock

from google.cloud.logging_v2.handlers._monitored_resources import (
    _FUNCTION_ENV_VARS,
    _GAE_ENV_VARS,
)


class TestCloudLoggingFilter(unittest.TestCase):

    PROJECT = "PROJECT"

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.handlers import CloudLoggingFilter

        return CloudLoggingFilter

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

    def test_filter_record(self):
        """
        test adding fields to a standard record
        """
        import logging

        filter_obj = self._make_one()
        logname = "loggername"
        message = "hello world，嗨 世界"
        pathname = "testpath"
        lineno = 1
        func = "test-function"
        record = logging.LogRecord(
            logname, logging.INFO, pathname, lineno, message, None, None, func=func
        )

        success = filter_obj.filter(record)
        self.assertTrue(success)

        self.assertEqual(record.line, lineno)
        self.assertEqual(record.msg, message)
        self.assertEqual(record.function, func)
        self.assertEqual(record.file, pathname)
        self.assertEqual(record.trace, "")
        self.assertEqual(record.http_request, {})
        self.assertEqual(record.request_method, "")
        self.assertEqual(record.request_url, "")
        self.assertEqual(record.user_agent, "")
        self.assertEqual(record.protocol, "")

    def test_minimal_record(self):
        """
        test filter adds empty strings on missing attributes
        """
        import logging

        filter_obj = self._make_one()
        record = logging.LogRecord(None, logging.INFO, None, None, None, None, None,)
        record.created = None

        success = filter_obj.filter(record)
        self.assertTrue(success)

        self.assertEqual(record.line, 0)
        self.assertEqual(record.msg, "")
        self.assertEqual(record.function, "")
        self.assertEqual(record.file, "")
        self.assertEqual(record.trace, "")
        self.assertEqual(record.http_request, {})
        self.assertEqual(record.request_method, "")
        self.assertEqual(record.request_url, "")
        self.assertEqual(record.user_agent, "")
        self.assertEqual(record.protocol, "")

    def test_record_with_request(self):
        """
        test filter adds http request data when available
        """
        import logging

        filter_obj = self._make_one()
        record = logging.LogRecord(None, logging.INFO, None, None, None, None, None,)
        record.created = None

        expected_path = "http://testserver/123"
        expected_agent = "Mozilla/5.0"
        expected_trace = "123"
        expected_request = {
            "requestMethod": "PUT",
            "requestUrl": expected_path,
            "userAgent": expected_agent,
            "protocol": "HTTP/1.1",
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
            success = filter_obj.filter(record)
            self.assertTrue(success)

            self.assertEqual(record.trace, expected_trace)
            for key, val in expected_request.items():
                self.assertEqual(record.http_request[key], val)
            self.assertEqual(record.request_method, "PUT")
            self.assertEqual(record.request_url, expected_path)
            self.assertEqual(record.user_agent, expected_agent)
            self.assertEqual(record.protocol, "HTTP/1.1")

    def test_user_overrides(self):
        """
        ensure user can override fields
        """
        import logging

        filter_obj = self._make_one()
        record = logging.LogRecord(
            "name", logging.INFO, "default", 99, "message", None, None, func="default"
        )
        record.created = 5.03

        app = self.create_app()
        with app.test_client() as c:
            c.put(
                path="http://testserver/123",
                data="body",
                headers={"User-Agent": "default", "X_CLOUD_TRACE_CONTEXT": "default"},
            )
            # override values
            overwritten_trace = "456"
            record.trace = overwritten_trace
            overwritten_method = "GET"
            overwritten_url = "www.google.com"
            overwritten_agent = "custom"
            overwritten_protocol = "test"
            overwritten_request_object = {
                "requestMethod": overwritten_method,
                "requestUrl": overwritten_url,
                "userAgent": overwritten_agent,
                "protocol": overwritten_protocol,
            }
            overwritten_line = 22
            overwritten_function = "test-func"
            overwritten_file = "test-file"
            overwritten_source_location = {
                "file": overwritten_file,
                "line": overwritten_line,
                "function": overwritten_function,
            }
            record.http_request = overwritten_request_object
            record.source_location = overwritten_source_location
            success = filter_obj.filter(record)
            self.assertTrue(success)

            self.assertEqual(record.trace, overwritten_trace)
            self.assertEqual(record.http_request, overwritten_request_object)
            self.assertEqual(record.request_method, overwritten_method)
            self.assertEqual(record.request_url, overwritten_url)
            self.assertEqual(record.user_agent, overwritten_agent)
            self.assertEqual(record.protocol, overwritten_protocol)
            self.assertEqual(record.line, overwritten_line)
            self.assertEqual(record.function, overwritten_function)
            self.assertEqual(record.file, overwritten_file)


class TestCloudLoggingHandler(unittest.TestCase):

    PROJECT = "PROJECT"

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.handlers import CloudLoggingHandler

        return CloudLoggingHandler

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        import sys
        from google.cloud.logging_v2.logger import _GLOBAL_RESOURCE
        from google.cloud.logging_v2.handlers.handlers import DEFAULT_LOGGER_NAME

        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            return_value=None,
        )
        with patch:
            client = _Client(self.PROJECT)
            handler = self._make_one(client, transport=_Transport)
            self.assertEqual(handler.name, DEFAULT_LOGGER_NAME)
            self.assertIs(handler.client, client)
            self.assertIsInstance(handler.transport, _Transport)
            self.assertIs(handler.transport.client, client)
            self.assertEqual(handler.transport.name, DEFAULT_LOGGER_NAME)
            self.assertEqual(handler.resource, _GLOBAL_RESOURCE)
            self.assertIsNone(handler.labels)
            self.assertIs(handler.stream, sys.stderr)

    def test_ctor_explicit(self):
        import io
        from google.cloud.logging import Resource

        resource = Resource("resource_type", {"resource_label": "value"})
        labels = {"handler_lable": "value"}
        name = "test-logger"
        client = _Client(self.PROJECT)
        stream = io.BytesIO()
        handler = self._make_one(
            client,
            name=name,
            transport=_Transport,
            resource=resource,
            labels=labels,
            stream=stream,
        )
        self.assertEqual(handler.name, name)
        self.assertIs(handler.client, client)
        self.assertIsInstance(handler.transport, _Transport)
        self.assertIs(handler.transport.client, client)
        self.assertEqual(handler.transport.name, name)
        self.assertIs(handler.resource, resource)
        self.assertEqual(handler.labels, labels)
        self.assertIs(handler.stream, stream)

    def test_emit(self):
        from google.cloud.logging_v2.logger import _GLOBAL_RESOURCE

        client = _Client(self.PROJECT)
        handler = self._make_one(
            client, transport=_Transport, resource=_GLOBAL_RESOURCE
        )
        logname = "loggername"
        message = "hello world"
        record = logging.LogRecord(logname, logging, None, None, message, None, None)
        handler.handle(record)
        self.assertEqual(
            handler.transport.send_called_with,
            (record, message, _GLOBAL_RESOURCE, None, None, None, None, None),
        )

    def test_emit_manual_field_override(self):
        from google.cloud.logging_v2.logger import _GLOBAL_RESOURCE
        from google.cloud.logging_v2.resource import Resource

        client = _Client(self.PROJECT)
        default_labels = {
            "default_key": "default-value",
            "overwritten_key": "bad_value",
        }
        handler = self._make_one(
            client,
            transport=_Transport,
            resource=_GLOBAL_RESOURCE,
            labels=default_labels,
        )
        logname = "loggername"
        message = "hello world"
        record = logging.LogRecord(logname, logging, None, None, message, None, None)
        # set attributes manually
        expected_trace = "123"
        setattr(record, "trace", expected_trace)
        expected_span = "456"
        setattr(record, "span_id", expected_span)
        expected_http = {"reuqest_url": "manual"}
        setattr(record, "http_request", expected_http)
        expected_source = {"file": "test-file"}
        setattr(record, "source_location", expected_source)
        expected_resource = Resource(type="test", labels={})
        setattr(record, "resource", expected_resource)
        added_labels = {"added_key": "added_value", "overwritten_key": "new_value"}
        expected_labels = {
            "default_key": "default-value",
            "overwritten_key": "new_value",
            "added_key": "added_value",
        }
        setattr(record, "labels", added_labels)
        handler.handle(record)

        self.assertEqual(
            handler.transport.send_called_with,
            (
                record,
                message,
                expected_resource,
                expected_labels,
                expected_trace,
                expected_span,
                expected_http,
                expected_source,
            ),
        )


class TestSetupLogging(unittest.TestCase):
    def _call_fut(self, handler, excludes=None):
        from google.cloud.logging.handlers import setup_logging

        if excludes:
            return setup_logging(handler, excluded_loggers=excludes)
        else:
            return setup_logging(handler)

    def test_setup_logging(self):
        handler = _Handler(logging.INFO)
        self._call_fut(handler)

        root_handlers = logging.getLogger().handlers
        self.assertIn(handler, root_handlers)

    def test_setup_logging_excludes(self):
        INCLUDED_LOGGER_NAME = "includeme"
        EXCLUDED_LOGGER_NAME = "excludeme"

        handler = _Handler(logging.INFO)
        self._call_fut(handler, (EXCLUDED_LOGGER_NAME,))

        included_logger = logging.getLogger(INCLUDED_LOGGER_NAME)
        self.assertTrue(included_logger.propagate)

        excluded_logger = logging.getLogger(EXCLUDED_LOGGER_NAME)
        self.assertNotIn(handler, excluded_logger.handlers)
        self.assertFalse(excluded_logger.propagate)

    @patch.dict("os.environ", {envar: "1" for envar in _FUNCTION_ENV_VARS})
    def test_remove_handlers_gcf(self):
        logger = logging.getLogger()
        # add fake handler
        added_handler = logging.StreamHandler()
        logger.addHandler(added_handler)

        handler = _Handler(logging.INFO)
        self._call_fut(handler)
        self.assertNotIn(added_handler, logger.handlers)
        # handler should be removed from logger
        self.assertEqual(len(logger.handlers), 1)

    @patch.dict("os.environ", {envar: "1" for envar in _GAE_ENV_VARS})
    def test_remove_handlers_gae(self):
        logger = logging.getLogger()
        # add fake handler
        added_handler = logging.StreamHandler()
        logger.addHandler(added_handler)

        handler = _Handler(logging.INFO)
        self._call_fut(handler)
        self.assertNotIn(added_handler, logger.handlers)
        # handler should be removed from logger
        self.assertEqual(len(logger.handlers), 1)

    def test_keep_handlers_others(self):
        # mock non-cloud environment
        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            return_value=None,
        )
        with patch:
            # add fake handler
            added_handler = logging.StreamHandler()
            logger = logging.getLogger()
            logger.addHandler(added_handler)

            handler = _Handler(logging.INFO)
            self._call_fut(handler)
            # added handler should remain in logger
            self.assertIn(added_handler, logger.handlers)

    def setUp(self):
        self._handlers_cache = logging.getLogger().handlers[:]

    def tearDown(self):
        # cleanup handlers
        logging.getLogger().handlers = self._handlers_cache[:]


class _Handler(object):
    def __init__(self, level):
        self.level = level

    def acquire(self):
        pass  # pragma: NO COVER

    def release(self):
        pass  # pragma: NO COVER


class _Client(object):
    def __init__(self, project):
        self.project = project


class _Transport(object):
    def __init__(self, client, name):
        self.client = client
        self.name = name

    def send(
        self,
        record,
        message,
        resource,
        labels=None,
        trace=None,
        span_id=None,
        http_request=None,
        source_location=None,
    ):
        self.send_called_with = (
            record,
            message,
            resource,
            labels,
            trace,
            span_id,
            http_request,
            source_location,
        )
