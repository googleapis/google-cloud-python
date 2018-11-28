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

import mock
from six.moves import queue


class TestBackgroundThreadHandler(unittest.TestCase):
    PROJECT = "PROJECT"

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.handlers.transports import BackgroundThreadTransport

        return BackgroundThreadTransport

    def _make_one(self, *args, **kw):
        worker_patch = mock.patch(
            "google.cloud.logging.handlers.transports." "background_thread._Worker",
            autospec=True,
        )
        with worker_patch as worker_mock:
            return self._get_target_class()(*args, **kw), worker_mock

    def test_constructor(self):
        client = _Client(self.PROJECT)
        name = "python_logger"

        transport, worker = self._make_one(client, name)

        logger, = worker.call_args[0]  # call_args[0] is *args.
        self.assertEqual(logger.name, name)

    def test_send(self):
        from google.cloud.logging.logger import _GLOBAL_RESOURCE

        client = _Client(self.PROJECT)
        name = "python_logger"

        transport, _ = self._make_one(client, name)

        python_logger_name = "mylogger"
        message = "hello world"

        record = logging.LogRecord(
            python_logger_name, logging.INFO, None, None, message, None, None
        )

        transport.send(record, message, _GLOBAL_RESOURCE)

        transport.worker.enqueue.assert_called_once_with(
            record, message, _GLOBAL_RESOURCE, None, trace=None, span_id=None
        )

    def test_trace_send(self):
        from google.cloud.logging.logger import _GLOBAL_RESOURCE

        client = _Client(self.PROJECT)
        name = "python_logger"

        transport, _ = self._make_one(client, name)

        python_logger_name = "mylogger"
        message = "hello world"
        trace = "the-project/trace/longlogTraceid"

        record = logging.LogRecord(
            python_logger_name, logging.INFO, None, None, message, None, None
        )

        transport.send(record, message, _GLOBAL_RESOURCE, trace=trace)

        transport.worker.enqueue.assert_called_once_with(
            record, message, _GLOBAL_RESOURCE, None, trace=trace, span_id=None
        )

    def test_span_send(self):
        from google.cloud.logging.logger import _GLOBAL_RESOURCE

        client = _Client(self.PROJECT)
        name = "python_logger"

        transport, _ = self._make_one(client, name)

        python_logger_name = "mylogger"
        message = "hello world"
        span_id = "the-project/trace/longlogTraceid/span/123456789012abbacdac"

        record = logging.LogRecord(
            python_logger_name, logging.INFO, None, None, message, None, None
        )

        transport.send(record, message, _GLOBAL_RESOURCE, span_id=span_id)

        transport.worker.enqueue.assert_called_once_with(
            record, message, _GLOBAL_RESOURCE, None, trace=None, span_id=span_id
        )

    def test_flush(self):
        client = _Client(self.PROJECT)
        name = "python_logger"

        transport, _ = self._make_one(client, name)

        transport.flush()

        transport.worker.flush.assert_called()

    def test_worker(self):
        client = _Client(self.PROJECT)
        name = "python_logger"
        batch_size = 30
        grace_period = 20.0
        max_latency = 0.1
        transport, worker = self._make_one(
            client,
            name,
            grace_period=grace_period,
            batch_size=batch_size,
            max_latency=max_latency,
        )
        worker_grace_period = worker.call_args[1]["grace_period"]  # **kwargs.
        worker_batch_size = worker.call_args[1]["max_batch_size"]
        worker_max_latency = worker.call_args[1]["max_latency"]
        self.assertEqual(worker_grace_period, grace_period)
        self.assertEqual(worker_batch_size, batch_size)
        self.assertEqual(worker_max_latency, max_latency)


class Test_Worker(unittest.TestCase):
    NAME = "python_logger"

    @staticmethod
    def _get_target_class():
        from google.cloud.logging.handlers.transports import background_thread

        return background_thread._Worker

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _start_with_thread_patch(self, worker):
        with mock.patch("threading.Thread", new=_Thread) as thread_mock:
            with mock.patch("atexit.register") as atexit_mock:
                worker.start()
                return thread_mock, atexit_mock

    def test_constructor(self):
        logger = _Logger(self.NAME)
        grace_period = 50
        max_batch_size = 50
        max_latency = 0.1

        worker = self._make_one(
            logger,
            grace_period=grace_period,
            max_batch_size=max_batch_size,
            max_latency=max_latency,
        )

        self.assertEqual(worker._cloud_logger, logger)
        self.assertEqual(worker._grace_period, grace_period)
        self.assertEqual(worker._max_batch_size, max_batch_size)
        self.assertEqual(worker._max_latency, max_latency)
        self.assertFalse(worker.is_alive)
        self.assertIsNone(worker._thread)

    def test_start(self):
        from google.cloud.logging.handlers.transports import background_thread

        worker = self._make_one(_Logger(self.NAME))

        _, atexit_mock = self._start_with_thread_patch(worker)

        self.assertTrue(worker.is_alive)
        self.assertIsNotNone(worker._thread)
        self.assertTrue(worker._thread.daemon)
        self.assertEqual(worker._thread._target, worker._thread_main)
        self.assertEqual(worker._thread._name, background_thread._WORKER_THREAD_NAME)
        atexit_mock.assert_called_once_with(worker._main_thread_terminated)

        # Calling start again should not start a new thread.
        current_thread = worker._thread
        self._start_with_thread_patch(worker)
        self.assertIs(current_thread, worker._thread)

    def test_stop(self):
        from google.cloud.logging.handlers.transports import background_thread

        grace_period = 5.0
        worker = self._make_one(_Logger(self.NAME))

        self._start_with_thread_patch(worker)
        thread = worker._thread

        worker.stop(grace_period)

        self.assertEqual(worker._queue.qsize(), 1)
        self.assertEqual(worker._queue.get(), background_thread._WORKER_TERMINATOR)
        self.assertFalse(worker.is_alive)
        self.assertIsNone(worker._thread)
        self.assertEqual(thread._timeout, grace_period)

        # Stopping twice should not be an error
        worker.stop()

    def test_stop_no_grace(self):
        worker = self._make_one(_Logger(self.NAME))

        self._start_with_thread_patch(worker)
        thread = worker._thread

        worker.stop()

        self.assertEqual(thread._timeout, None)

    def test__main_thread_terminated(self):
        worker = self._make_one(_Logger(self.NAME))

        self._start_with_thread_patch(worker)
        worker._main_thread_terminated()

        self.assertFalse(worker.is_alive)

        # Calling twice should not be an error
        worker._main_thread_terminated()

    def test__main_thread_terminated_non_empty_queue(self):
        worker = self._make_one(_Logger(self.NAME))

        self._start_with_thread_patch(worker)
        worker.enqueue(mock.Mock(), "")
        worker._main_thread_terminated()

        self.assertFalse(worker.is_alive)

    def test__main_thread_terminated_did_not_join(self):
        worker = self._make_one(_Logger(self.NAME))

        self._start_with_thread_patch(worker)
        worker._thread._terminate_on_join = False
        worker.enqueue(mock.Mock(), "")
        worker._main_thread_terminated()

        self.assertFalse(worker.is_alive)

    @staticmethod
    def _enqueue_record(worker, message):
        record = logging.LogRecord(
            "python_logger", logging.INFO, None, None, message, None, None
        )
        worker.enqueue(record, message)

    def test__thread_main(self):
        from google.cloud.logging.handlers.transports import background_thread

        worker = self._make_one(_Logger(self.NAME))

        # Enqueue two records and the termination signal.
        self._enqueue_record(worker, "1")
        self._enqueue_record(worker, "2")
        worker._queue.put_nowait(background_thread._WORKER_TERMINATOR)

        worker._thread_main()

        self.assertTrue(worker._cloud_logger._batch.commit_called)
        self.assertEqual(worker._cloud_logger._batch.commit_count, 2)
        self.assertEqual(worker._queue.qsize(), 0)

    def test__thread_main_error(self):
        from google.cloud.logging.handlers.transports import background_thread

        worker = self._make_one(_Logger(self.NAME))
        worker._cloud_logger._batch_cls = _RaisingBatch

        # Enqueue one record and the termination signal.
        self._enqueue_record(worker, "1")
        worker._queue.put_nowait(background_thread._WORKER_TERMINATOR)

        worker._thread_main()

        self.assertTrue(worker._cloud_logger._batch.commit_called)
        self.assertEqual(worker._queue.qsize(), 0)

    def test__thread_main_batches(self):
        from google.cloud.logging.handlers.transports import background_thread

        worker = self._make_one(_Logger(self.NAME), max_batch_size=2)

        # Enqueue three records and the termination signal. This should be
        # enough to perform two separate batches and a third loop with just
        # the exit.
        self._enqueue_record(worker, "1")
        self._enqueue_record(worker, "2")
        self._enqueue_record(worker, "3")
        self._enqueue_record(worker, "4")
        worker._queue.put_nowait(background_thread._WORKER_TERMINATOR)

        worker._thread_main()

        # The last batch should not have been executed because it had no items.
        self.assertFalse(worker._cloud_logger._batch.commit_called)
        self.assertEqual(worker._queue.qsize(), 0)

    @mock.patch("time.time", autospec=True, return_value=1)
    def test__thread_main_max_latency(self, time):
        # Note: this test is a bit brittle as it assumes the operation of
        # _get_many invokes queue.get() followed by queue._get(). It fails
        # the "change detector" test in that way. However, this is still a
        # useful test to verify the queue timeout is appropriately calculated.
        from six.moves import queue
        from google.cloud.logging.handlers.transports import background_thread

        # Use monotonically increasing time.
        time.side_effect = range(1, 6)

        worker = self._make_one(_Logger(self.NAME), max_latency=2, max_batch_size=10)
        worker._queue = mock.create_autospec(queue.Queue, instance=True)

        worker._queue.get.side_effect = [
            {"info": {"message": "1"}},  # Single record.
            queue.Empty(),  # Emulate a queue.get() timeout.
            {"info": {"message": "1"}},  # Second record.
            background_thread._WORKER_TERMINATOR,  # Stop the thread.
            queue.Empty(),  # Emulate a queue.get() timeout.
        ]

        worker._thread_main()

        self.assertEqual(worker._cloud_logger._num_batches, 2)
        self.assertTrue(worker._cloud_logger._batch.commit_called)
        self.assertEqual(worker._cloud_logger._batch.commit_count, 1)

        # Time should have been called five times.
        #
        #   For the first batch, it should have been called:
        #       * Once to get the start time. (1)
        #       * Once to get the elapsed time while grabbing the second item.
        #         (2)
        #
        #   For the second batch, it should have been called:
        #       * Once to get start time. (3)
        #       * Once to get the elapsed time while grabbing the second item.
        #         (3)
        #       * Once to get the elapsed time while grabbing the final
        #         item. (4)
        #       * Once final time to get the elapsed time while receiving
        #         the empty queue.
        #
        self.assertEqual(time.call_count, 5)

        # Queue.get should've been called 5 times as well, but with different
        # timeouts due to the monotonically increasing time.
        #
        #   For the first batch, it will be called once without a timeout
        #   (for the first item) and then with timeout=1, as start will be
        #   1 and now will be 2.
        #
        #   For the second batch, it will be called once without a timeout
        #   (for the first item) and then with timeout=1, as start will be
        #   3 and now will be 4, and finally with timeout=0 as start will be 3
        #   and now will be 5.
        #
        worker._queue.get.assert_has_calls(
            [
                mock.call(),
                mock.call(timeout=1),
                mock.call(),
                mock.call(timeout=1),
                mock.call(timeout=0),
            ]
        )

    def test_flush(self):
        worker = self._make_one(_Logger(self.NAME))
        worker._queue = mock.Mock(spec=queue.Queue)

        # Queue is empty, should not block.
        worker.flush()
        worker._queue.join.assert_called()


class _Thread(object):
    def __init__(self, target, name):
        self._target = target
        self._name = name
        self._timeout = None
        self._terminate_on_join = True
        self.daemon = False

    def is_alive(self):
        return self._is_alive

    def start(self):
        self._is_alive = True

    def stop(self):
        self._is_alive = False

    def join(self, timeout=None):
        self._timeout = timeout
        if self._terminate_on_join:
            self.stop()


class _Batch(object):
    def __init__(self):
        self.entries = []
        self.commit_called = False
        self.commit_count = None

    def log_struct(
        self,
        info,
        severity=logging.INFO,
        resource=None,
        labels=None,
        trace=None,
        span_id=None,
    ):
        from google.cloud.logging.logger import _GLOBAL_RESOURCE

        assert resource is None
        resource = _GLOBAL_RESOURCE

        self.log_struct_called_with = (info, severity, resource, labels, trace, span_id)
        self.entries.append(info)

    def commit(self):
        self.commit_called = True
        self.commit_count = len(self.entries)
        del self.entries[:]


class _RaisingBatch(_Batch):
    def commit(self):
        self.commit_called = True
        raise ValueError("This batch raises on commit.")


class _Logger(object):
    def __init__(self, name):
        self.name = name
        self._batch_cls = _Batch
        self._batch = None
        self._num_batches = 0

    def batch(self):
        self._batch = self._batch_cls()
        self._num_batches += 1
        return self._batch


class _Client(object):
    def __init__(self, project, _http=None, credentials=None):
        import mock

        self.project = project
        self._http = _http
        self._credentials = credentials
        self._connection = mock.Mock(credentials=credentials, spec=["credentials"])

    def logger(self, name):  # pylint: disable=unused-argument
        self._logger = _Logger(name)
        return self._logger
