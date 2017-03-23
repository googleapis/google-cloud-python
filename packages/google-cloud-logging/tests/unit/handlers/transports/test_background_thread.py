# Copyright 2016 Google Inc.
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

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.handlers.transports import (
            BackgroundThreadTransport)

        return BackgroundThreadTransport

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        NAME = 'python_logger'
        transport = self._make_one(client, NAME)
        self.assertEqual(transport.worker.logger.name, NAME)

    def test_send(self):
        client = _Client(self.PROJECT)
        NAME = 'python_logger'
        transport = self._make_one(client, NAME)
        transport.worker.batch = client.logger(NAME).batch()

        python_logger_name = 'mylogger'
        message = 'hello world'
        record = logging.LogRecord(python_logger_name, logging.INFO,
                                   None, None, message, None, None)
        transport.send(record, message)

        EXPECTED_STRUCT = {
            'message': message,
            'python_logger': python_logger_name
        }
        EXPECTED_SENT = (EXPECTED_STRUCT, 'INFO')
        self.assertEqual(transport.worker.batch.log_struct_called_with,
                         EXPECTED_SENT)


class TestWorker(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.handlers.transports import background_thread

        return background_thread._Worker

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        NAME = 'python_logger'
        logger = _Logger(NAME)
        worker = self._make_one(logger)
        self.assertEqual(worker.batch, logger._batch)

    def test_run(self):
        NAME = 'python_logger'
        logger = _Logger(NAME)
        worker = self._make_one(logger)

        python_logger_name = 'mylogger'
        message = 'hello world'
        record = logging.LogRecord(python_logger_name,
                                   logging.INFO, None, None,
                                   message, None, None)

        worker._start()

        # first sleep is for branch coverage - ensure condition
        # where queue is empty occurs
        time.sleep(1)
        # second polling is to avoid starting/stopping worker
        # before anything ran
        while not worker.started:
            time.sleep(1)  # pragma: NO COVER

        worker.enqueue(record, message)
        # Set timeout to none so worker thread finishes
        worker._stop_timeout = None
        worker._stop()
        self.assertTrue(worker.batch.commit_called)

    def test_run_after_stopped(self):
        # No-op
        name = 'python_logger'
        logger = _Logger(name)
        worker = self._make_one(logger)

        python_logger_name = 'mylogger'
        message = 'hello world'
        record = logging.LogRecord(python_logger_name,
                                   logging.INFO, None, None,
                                   message, None, None)

        worker._start()
        while not worker.started:
            time.sleep(1)  # pragma: NO COVER
        worker._stop_timeout = None
        worker._stop()
        worker.enqueue(record, message)
        self.assertFalse(worker.batch.commit_called)
        worker._stop()

    def test_run_enqueue_early(self):
        # No-op
        NAME = 'python_logger'
        logger = _Logger(NAME)
        worker = self._make_one(logger)

        python_logger_name = 'mylogger'
        message = 'hello world'
        record = logging.LogRecord(python_logger_name,
                                   logging.INFO, None, None,
                                   message, None, None)

        worker.enqueue(record, message)
        worker._start()
        while not worker.started:
            time.sleep(1)  # pragma: NO COVER
        worker._stop_timeout = None
        worker._stop()
        self.assertTrue(worker.stopped)


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


class _Logger(object):

    def __init__(self, name):
        self.name = name

    def batch(self):
        self._batch = _Batch()
        return self._batch


class _Client(object):

    def __init__(self, project, http=None, credentials=None):
        import mock

        self.project = project
        self._http = http
        self._credentials = credentials
        self._connection = mock.Mock(
            credentials=credentials, spec=['credentials'])

    def logger(self, name):  # pylint: disable=unused-argument
        self._logger = _Logger(name)
        return self._logger
