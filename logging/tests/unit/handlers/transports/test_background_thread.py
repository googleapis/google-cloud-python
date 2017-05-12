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
import unittest

import mock


class TestBackgroundThreadHandler(unittest.TestCase):
    PROJECT = 'PROJECT'

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.handlers.transports import (
            BackgroundThreadTransport)

        return BackgroundThreadTransport

    def _make_one(self, *args, **kw):
        worker_patch = mock.patch(
            'google.cloud.logging.handlers.transports.'
            'background_thread._Worker',
            autospec=True)
        with worker_patch as worker_mock:
            return self._get_target_class()(*args, **kw), worker_mock

    def test_ctor(self):
        client = _Client(self.PROJECT)
        name = 'python_logger'

        transport, worker = self._make_one(client, name)

        logger = worker.call_args[0][0]
        self.assertEqual(logger.name, name)

    def test_send(self):
        client = _Client(self.PROJECT)
        name = 'python_logger'

        transport, _ = self._make_one(client, name)

        python_logger_name = 'mylogger'
        message = 'hello world'
        record = logging.LogRecord(
            python_logger_name, logging.INFO,
            None, None, message, None, None)

        transport.send(record, message)

        transport.worker.enqueue.assert_called_once_with(record, message)


class TestWorker(unittest.TestCase):
    NAME = 'python_logger'

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.handlers.transports import background_thread

        return background_thread._Worker

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _make_one_with_mock_thread(self, *args, **kw):
        with mock.patch('threading.Thread', new=_Thread):
            with mock.patch('atexit.register') as atexit_mock:
                self.atexit_mock = atexit_mock
                return self._make_one(*args, **kw)

    def test_ctor(self):
        logger = _Logger(self.NAME)
        grace_period = 50
        batch_size = 50

        worker = self._make_one_with_mock_thread(
            logger, grace_period=grace_period, batch_size=batch_size)

        self.assertEqual(worker._cloud_logger, logger)
        self.assertEqual(worker._grace_period, grace_period)
        self.assertEqual(worker._batch_size, batch_size)
        self.assertTrue(worker.is_alive)
        self.assertIsNotNone(worker._thread)

    def test_start(self):
        from google.cloud.logging.handlers.transports import background_thread

        worker = self._make_one_with_mock_thread(_Logger(self.NAME))

        # Start is implicitly called by worker's ctor

        self.assertTrue(worker.is_alive)
        self.assertIsNotNone(worker._thread)
        self.assertTrue(worker._thread._daemon)
        self.assertEqual(worker._thread._target, worker._thread_main)
        self.assertEqual(
            worker._thread._name, background_thread._WORKER_THREAD_NAME)

        # Calling start again should not start a new thread.
        current_thread = worker._thread
        worker.start()
        self.assertIs(current_thread, worker._thread)

    def test_stop(self):
        from google.cloud.logging.handlers.transports import background_thread

        grace_period = 5.0
        worker = self._make_one_with_mock_thread(_Logger(self.NAME))
        thread = worker._thread

        worker.stop(grace_period)

        self.assertEqual(worker._queue.qsize(), 1)
        self.assertEqual(
            worker._queue.get(), background_thread._WORKER_TERMINATOR)
        self.assertFalse(worker.is_alive)
        self.assertIsNone(worker._thread)
        self.assertEqual(thread._timeout, grace_period)

        # Stopping twice should not be an error
        worker.stop()

    def test_stop_no_grace(self):
        worker = self._make_one_with_mock_thread(_Logger(self.NAME))
        thread = worker._thread

        worker.stop()

        self.assertEqual(thread._timeout, None)

    def test__main_thread_terminated(self):
        worker = self._make_one_with_mock_thread(_Logger(self.NAME))

        worker._main_thread_terminated()

        self.assertFalse(worker.is_alive)

        # Calling twice should not be an error
        worker._main_thread_terminated()

    def test__main_thread_terminated_non_empty_queue(self):
        worker = self._make_one_with_mock_thread(_Logger(self.NAME))

        worker.enqueue(mock.Mock(), '')
        worker._main_thread_terminated()

        self.assertFalse(worker.is_alive)

    def test__main_thread_terminated_did_not_join(self):
        worker = self._make_one_with_mock_thread(_Logger(self.NAME))

        worker._thread._terminate_on_join = False
        worker.enqueue(mock.Mock(), '')
        worker._main_thread_terminated()

        self.assertFalse(worker.is_alive)

    def _enqueue_record(self, worker, message):
        record = logging.LogRecord(
            'python_logger', logging.INFO,
            None, None, message, None, None)
        worker.enqueue(record, message)

    def test__thread_main(self):
        from google.cloud.logging.handlers.transports import background_thread

        worker = self._make_one_with_mock_thread(_Logger(self.NAME))

        # Enqueue two records and the termination signal.
        self._enqueue_record(worker, '1')
        self._enqueue_record(worker, '2')
        worker._queue.put_nowait(background_thread._WORKER_TERMINATOR)

        worker._thread_main()

        self.assertTrue(worker._cloud_logger._batch.commit_called)
        self.assertEqual(worker._cloud_logger._batch.commit_count, 2)
        self.assertEqual(worker._queue.qsize(), 0)

    def test__thread_main_error(self):
        from google.cloud.logging.handlers.transports import background_thread

        worker = self._make_one_with_mock_thread(_Logger(self.NAME))
        worker._cloud_logger._batch_cls = _RaisingBatch

        # Enqueue one record and the termination signal.
        self._enqueue_record(worker, '1')
        worker._queue.put_nowait(background_thread._WORKER_TERMINATOR)

        worker._thread_main()

        self.assertTrue(worker._cloud_logger._batch.commit_called)
        self.assertEqual(worker._queue.qsize(), 0)

    def test__thread_main_batches(self):
        from google.cloud.logging.handlers.transports import background_thread

        worker = self._make_one_with_mock_thread(
            _Logger(self.NAME), batch_size=2)

        # Enqueue three records and the termination signal. This should be
        # enough to perform two separate batches and a third loop with just
        # the exit.
        self._enqueue_record(worker, '1')
        self._enqueue_record(worker, '2')
        self._enqueue_record(worker, '3')
        self._enqueue_record(worker, '4')
        worker._queue.put_nowait(background_thread._WORKER_TERMINATOR)

        worker._thread_main()

        # The last batch should not have been executed because it had no items.
        self.assertFalse(worker._cloud_logger._batch.commit_called)
        self.assertEqual(worker._queue.qsize(), 0)


class _Thread(object):

    def __init__(self, target, name):
        self._target = target
        self._name = name
        self._daemon = False
        self._timeout = None
        self._terminate_on_join = True

    def is_alive(self):
        return self._is_alive

    def start(self):
        self._is_alive = True

    def stop(self):
        self._is_alive = False

    def setDaemon(self, value):
        self._daemon = value

    def join(self, timeout=None):
        self._timeout = timeout
        if self._terminate_on_join:
            self.stop()


class _Batch(object):

    def __init__(self):
        self.entries = []
        self.commit_called = False
        self.commit_count = None

    def log_struct(self, info, severity=logging.INFO):
        self.log_struct_called_with = (info, severity)
        self.entries.append(info)

    def commit(self):
        self.commit_called = True
        self.commit_count = len(self.entries)
        del self.entries[:]


class _RaisingBatch(_Batch):
    def commit(self):
        self.commit_called = True
        raise ValueError('This batch raises on commit.')


class _Logger(object):

    def __init__(self, name):
        self.name = name
        self._batch_cls = _Batch
        self._batch = None

    def batch(self):
        self._batch = self._batch_cls()
        return self._batch


class _Client(object):

    def __init__(self, project, _http=None, credentials=None):
        import mock

        self.project = project
        self._http = _http
        self._credentials = credentials
        self._connection = mock.Mock(
            credentials=credentials, spec=['credentials'])

    def logger(self, name):  # pylint: disable=unused-argument
        self._logger = _Logger(name)
        return self._logger
