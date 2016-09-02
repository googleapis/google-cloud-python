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
import time
import unittest


class TestBackgroundThreadHandler(unittest.TestCase):

    PROJECT = 'PROJECT'

    def _getTargetClass(self):
        from gcloud.logging.handlers.transports import (
            BackgroundThreadTransport)
        return BackgroundThreadTransport

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        NAME = 'python_logger'
        transport = self._makeOne(client, NAME)
        self.assertEquals(transport.worker.logger.name, NAME)

    def test_send(self):
        client = _Client(self.PROJECT)
        NAME = 'python_logger'
        transport = self._makeOne(client, NAME)
        transport.worker.batch = client.logger(NAME).batch()

        PYTHON_LOGGER_NAME = 'mylogger'
        MESSAGE = 'hello world'
        record = _Record(PYTHON_LOGGER_NAME, logging.INFO, MESSAGE)
        transport.send(record, MESSAGE)

        EXPECTED_STRUCT = {
            'message': MESSAGE,
            'python_logger': PYTHON_LOGGER_NAME
        }
        EXPECTED_SENT = (EXPECTED_STRUCT, logging.INFO)
        self.assertEqual(transport.worker.batch.log_struct_called_with,
                         EXPECTED_SENT)


class TestWorker(unittest.TestCase):

    def _getTargetClass(self):
        from gcloud.logging.handlers.transports.background_thread import (
            _Worker)
        return _Worker

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        NAME = 'python_logger'
        logger = _Logger(NAME)
        worker = self._makeOne(logger)
        self.assertEquals(worker.batch, logger._batch)

    def test_run(self):
        NAME = 'python_logger'
        logger = _Logger(NAME)
        worker = self._makeOne(logger)

        PYTHON_LOGGER_NAME = 'mylogger'
        MESSAGE = 'hello world'
        record = _Record(PYTHON_LOGGER_NAME, logging.INFO, MESSAGE)

        worker._start()

        # first sleep is for branch coverage - ensure condition
        # where queue is empty occurs
        time.sleep(1)
        # second polling is to avoid starting/stopping worker
        # before anything ran
        while not worker.started:
            time.sleep(1)  # pragma: NO COVER

        worker.enqueue(record, MESSAGE)
        # Set timeout to none so worker thread finishes
        worker._stop_timeout = None
        worker._stop()
        self.assertTrue(worker.batch.commit_called)

    def test_run_after_stopped(self):
        # No-op
        NAME = 'python_logger'
        logger = _Logger(NAME)
        worker = self._makeOne(logger)

        PYTHON_LOGGER_NAME = 'mylogger'
        MESSAGE = 'hello world'
        record = _Record(PYTHON_LOGGER_NAME, logging.INFO, MESSAGE)

        worker._start()
        while not worker.started:
            time.sleep(1)  # pragma: NO COVER
        worker._stop_timeout = None
        worker._stop()
        worker.enqueue(record, MESSAGE)
        self.assertFalse(worker.batch.commit_called)
        worker._stop()

    def test_run_enqueue_early(self):
        # No-op
        NAME = 'python_logger'
        logger = _Logger(NAME)
        worker = self._makeOne(logger)

        PYTHON_LOGGER_NAME = 'mylogger'
        MESSAGE = 'hello world'
        record = _Record(PYTHON_LOGGER_NAME, logging.INFO, MESSAGE)

        worker.enqueue(record, MESSAGE)
        worker._start()
        while not worker.started:
            time.sleep(1)  # pragma: NO COVER
        worker._stop_timeout = None
        worker._stop()
        self.assertTrue(worker.stopped)


class _Record(object):

    def __init__(self, name, level, message):
        self.name = name
        self.levelname = level
        self.message = message
        self.exc_info = None
        self.exc_text = None
        self.stack_info = None


class _Batch(object):

    def __init__(self):
        self.entries = []
        self.commit_called = False

    def log_struct(self, record, severity=logging.INFO):
        self.log_struct_called_with = (record, severity)
        self.entries.append(record)

    def commit(self):
        self.commit_called = True
        del self.entries[:]


class _Credentials(object):

    def authorize(self, _):
        pass


class _Connection(object):

    def __init__(self):
        self.http = None
        self.credentials = _Credentials()


class _Logger(object):

    def __init__(self, name):
        self.name = name

    def batch(self):
        self._batch = _Batch()
        return self._batch


class _Client(object):

    def __init__(self, project):
        self.project = project
        self.connection = _Connection()

    def logger(self, name):  # pylint: disable=unused-argument
        self._logger = _Logger(name)
        return self._logger
