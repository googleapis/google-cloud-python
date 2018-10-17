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


class TestCloudLoggingHandler(unittest.TestCase):

    PROJECT = "PROJECT"

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.handlers.handlers import CloudLoggingHandler

        return CloudLoggingHandler

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        import sys
        from google.cloud.logging.logger import _GLOBAL_RESOURCE
        from google.cloud.logging.handlers.handlers import DEFAULT_LOGGER_NAME

        client = _Client(self.PROJECT)
        handler = self._make_one(client, transport=_Transport)
        self.assertEqual(handler.name, DEFAULT_LOGGER_NAME)
        self.assertIs(handler.client, client)
        self.assertIsInstance(handler.transport, _Transport)
        self.assertIs(handler.transport.client, client)
        self.assertEqual(handler.transport.name, DEFAULT_LOGGER_NAME)
        self.assertIs(handler.resource, _GLOBAL_RESOURCE)
        self.assertIsNone(handler.labels)
        self.assertIs(handler.stream, sys.stderr)

    def test_ctor_explicit(self):
        import io
        from google.cloud.logging.resource import Resource

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
        from google.cloud.logging.logger import _GLOBAL_RESOURCE

        client = _Client(self.PROJECT)
        handler = self._make_one(
            client, transport=_Transport, resource=_GLOBAL_RESOURCE
        )
        logname = "loggername"
        message = "hello world"
        record = logging.LogRecord(logname, logging, None, None, message, None, None)
        handler.emit(record)

        self.assertEqual(
            handler.transport.send_called_with,
            (record, message, _GLOBAL_RESOURCE, None),
        )


class TestSetupLogging(unittest.TestCase):
    def _call_fut(self, handler, excludes=None):
        from google.cloud.logging.handlers.handlers import setup_logging

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

    def send(self, record, message, resource, labels=None):
        self.send_called_with = (record, message, resource, labels)
