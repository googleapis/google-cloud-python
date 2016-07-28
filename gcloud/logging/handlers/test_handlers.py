# Copyright 2016 Google Inc. All Rights Reserved.
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

import unittest2


class TestCloudLoggingHandler(unittest2.TestCase):

    PROJECT = 'PROJECT'

    def _getTargetClass(self):
        from gcloud.logging.handlers.handlers import CloudLoggingHandler
        return CloudLoggingHandler

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        handler = self._makeOne(client, transport=_Transport)
        self.assertEqual(handler.client, client)

    def test_emit(self):
        client = _Client(self.PROJECT)
        handler = self._makeOne(client, transport=_Transport)
        LOGNAME = 'loggername'
        MESSAGE = 'hello world'
        record = _Record(LOGNAME, logging.INFO, MESSAGE)
        handler.emit(record)

        self.assertEqual(handler.transport.send_called_with, (record, MESSAGE))


class TestSetupLogging(unittest2.TestCase):

    def _callFUT(self, handler, excludes=None):
        from gcloud.logging.handlers.handlers import setup_logging
        if excludes:
            return setup_logging(handler, excluded_loggers=excludes)
        else:
            return setup_logging(handler)

    def test_setup_logging(self):
        handler = _Handler(logging.INFO)
        self._callFUT(handler)

        root_handlers = logging.getLogger().handlers
        self.assertIn(handler, root_handlers)

    def test_setup_logging_excludes(self):
        INCLUDED_LOGGER_NAME = 'includeme'
        EXCLUDED_LOGGER_NAME = 'excludeme'

        handler = _Handler(logging.INFO)
        self._callFUT(handler, (EXCLUDED_LOGGER_NAME,))

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


class _Record(object):

    def __init__(self, name, level, message):
        self.name = name
        self.levelname = level
        self.message = message
        self.exc_info = None
        self.exc_text = None
        self.stack_info = None

    def getMessage(self):
        return self.message


class _Transport(object):

    def __init__(self, client, name):
        pass

    def send(self, record, message):
        self.send_called_with = (record, message)
