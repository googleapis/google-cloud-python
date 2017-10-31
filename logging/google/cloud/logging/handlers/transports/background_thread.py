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

"""Transport for Python logging handler

Uses a background worker to log to Stackdriver Logging asynchronously.
"""

from __future__ import print_function

import atexit
import logging
import threading

from six.moves import range
from six.moves import queue

from google.cloud.logging.handlers.transports.base import Transport

_DEFAULT_GRACE_PERIOD = 5.0  # Seconds
_DEFAULT_MAX_BATCH_SIZE = 10
_WORKER_THREAD_NAME = 'google.cloud.logging.Worker'
_WORKER_TERMINATOR = object()
_LOGGER = logging.getLogger(__name__)


def _get_many(queue_, max_items=None):
    """Get multiple items from a Queue.

    Gets at least one (blocking) and at most ``max_items`` items
    (non-blocking) from a given Queue. Does not mark the items as done.

    :type queue_: :class:`~queue.Queue`
    :param queue_: The Queue to get items from.

    :type max_items: int
    :param max_items: The maximum number of items to get. If ``None``, then all
        available items in the queue are returned.

    :rtype: Sequence
    :returns: A sequence of items retrieved from the queue.
    """
    # Always return at least one item.
    items = [queue_.get()]
    while max_items is None or len(items) < max_items:
        try:
            items.append(queue_.get_nowait())
        except queue.Empty:
            break
    return items


class _Worker(object):
    """A background thread that writes batches of log entries.

    :type cloud_logger: :class:`~google.cloud.logging.logger.Logger`
    :param cloud_logger: The logger to send entries to.

    :type grace_period: float
    :param grace_period: The amount of time to wait for pending logs to
        be submitted when the process is shutting down.

    :type max_batch_size: int
    :param max_batch_size: The maximum number of items to send at a time
        in the background thread.
    """

    def __init__(self, cloud_logger, grace_period=_DEFAULT_GRACE_PERIOD,
                 max_batch_size=_DEFAULT_MAX_BATCH_SIZE):
        self._cloud_logger = cloud_logger
        self._grace_period = grace_period
        self._max_batch_size = max_batch_size
        self._queue = queue.Queue(0)
        self._operational_lock = threading.Lock()
        self._thread = None

    @property
    def is_alive(self):
        """Returns True is the background thread is running."""
        return self._thread is not None and self._thread.is_alive()

    def _safely_commit_batch(self, batch):
        total_logs = len(batch.entries)

        try:
            if total_logs > 0:
                batch.commit()
                _LOGGER.debug('Submitted %d logs', total_logs)
        except Exception:
            _LOGGER.error(
                'Failed to submit %d logs.', total_logs, exc_info=True)

    def _thread_main(self):
        """The entry point for the worker thread.

        Pulls pending log entries off the queue and writes them in batches to
        the Cloud Logger.
        """
        _LOGGER.debug('Background thread started.')

        quit_ = False
        while True:
            batch = self._cloud_logger.batch()
            items = _get_many(self._queue, max_items=self._max_batch_size)

            for item in items:
                if item is _WORKER_TERMINATOR:
                    quit_ = True
                    # Continue processing items, don't break, try to process
                    # all items we got back before quitting.
                else:
                    batch.log_struct(**item)

            self._safely_commit_batch(batch)

            for _ in range(len(items)):
                self._queue.task_done()

            if quit_:
                break

        _LOGGER.debug('Background thread exited gracefully.')

    def start(self):
        """Starts the background thread.

        Additionally, this registers a handler for process exit to attempt
        to send any pending log entries before shutdown.
        """
        with self._operational_lock:
            if self.is_alive:
                return

            self._thread = threading.Thread(
                target=self._thread_main,
                name=_WORKER_THREAD_NAME)
            self._thread.daemon = True
            self._thread.start()
            atexit.register(self._main_thread_terminated)

    def stop(self, grace_period=None):
        """Signals the background thread to stop.

        This does not terminate the background thread. It simply queues the
        stop signal. If the main process exits before the background thread
        processes the stop signal, it will be terminated without finishing
        work. The ``grace_period`` parameter will give the background
        thread some time to finish processing before this function returns.

        :type grace_period: float
        :param grace_period: If specified, this method will block up to this
            many seconds to allow the background thread to finish work before
            returning.

        :rtype: bool
        :returns: True if the thread terminated. False if the thread is still
            running.
        """
        if not self.is_alive:
            return True

        with self._operational_lock:
            self._queue.put_nowait(_WORKER_TERMINATOR)

            if grace_period is not None:
                print('Waiting up to %d seconds.' % (grace_period,))

            self._thread.join(timeout=grace_period)

            # Check this before disowning the thread, because after we disown
            # the thread is_alive will be False regardless of if the thread
            # exited or not.
            success = not self.is_alive

            self._thread = None

            return success

    def _main_thread_terminated(self):
        """Callback that attempts to send pending logs before termination."""
        if not self.is_alive:
            return

        if not self._queue.empty():
            print(
                'Program shutting down, attempting to send %d queued log '
                'entries to Stackdriver Logging...' % (self._queue.qsize(),))

        if self.stop(self._grace_period):
            print('Sent all pending logs.')
        else:
            print('Failed to send %d pending logs.' % (self._queue.qsize(),))

    def enqueue(self, record, message, resource=None, labels=None):
        """Queues a log entry to be written by the background thread.

        :type record: :class:`logging.LogRecord`
        :param record: Python log record that the handler was called with.

        :type message: str
        :param message: The message from the ``LogRecord`` after being
                        formatted by the associated log formatters.

        :type resource: :class:`~google.cloud.logging.resource.Resource`
        :param resource: (Optional) Monitored resource of the entry

        :type labels: dict
        :param labels: (Optional) Mapping of labels for the entry.
        """
        self._queue.put_nowait({
            'info': {
                'message': message,
                'python_logger': record.name,
            },
            'severity': record.levelname,
            'resource': resource,
            'labels': labels,
        })

    def flush(self):
        """Submit any pending log records."""
        self._queue.join()


class BackgroundThreadTransport(Transport):
    """Asynchronous transport that uses a background thread.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The Logging client.

    :type name: str
    :param name: the name of the logger.

    :type grace_period: float
    :param grace_period: The amount of time to wait for pending logs to
        be submitted when the process is shutting down.

    :type batch_size: int
    :param batch_size: The maximum number of items to send at a time in the
        background thread.
    """

    def __init__(self, client, name, grace_period=_DEFAULT_GRACE_PERIOD,
                 batch_size=_DEFAULT_MAX_BATCH_SIZE):
        self.client = client
        logger = self.client.logger(name)
        self.worker = _Worker(logger)
        self.worker.start()

    def send(self, record, message, resource=None, labels=None):
        """Overrides Transport.send().

        :type record: :class:`logging.LogRecord`
        :param record: Python log record that the handler was called with.

        :type message: str
        :param message: The message from the ``LogRecord`` after being
                        formatted by the associated log formatters.

        :type resource: :class:`~google.cloud.logging.resource.Resource`
        :param resource: (Optional) Monitored resource of the entry.

        :type labels: dict
        :param labels: (Optional) Mapping of labels for the entry.
        """
        self.worker.enqueue(record, message, resource=resource, labels=labels)

    def flush(self):
        """Submit any pending log records."""
        self.worker.flush()
