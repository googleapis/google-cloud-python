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

"""Transport for Python logging handler

Uses a background worker to log to Stackdriver Logging asynchronously.
"""

import atexit
import copy
import threading

from google.cloud.logging.handlers.transports.base import Transport

_WORKER_THREAD_NAME = 'google.cloud.logging.handlers.transport.Worker'


class _Worker(object):
    """A threaded worker that writes batches of log entries

    Writes entries to the logger API.

    This class reuses a single :class:`Batch` method to write successive
    entries.

    Currently, the only public methods are constructing it (which also starts
    it) and enqueuing :class:`Logger` (record, message) pairs.
    """

    def __init__(self, logger):
        self.started = False
        self.stopping = False
        self.stopped = False

        # _entries_condition is used to signal from the main thread whether
        # there are any waiting queued logger entries to be written
        self._entries_condition = threading.Condition()

        # _stop_condition is used to signal from the worker thread to the
        # main thread that it's finished its last entries
        self._stop_condition = threading.Condition()

        # This object continually reuses the same :class:`Batch` object to
        # write multiple entries at the same time.
        self.logger = logger
        self.batch = self.logger.batch()

        self._thread = None

        # Number in seconds of  how long to wait for worker to send remaining
        self._stop_timeout = 5

        self._start()

    def _run(self):
        """The entry point for the worker thread.

        Loops until ``stopping`` is set to :data:`True`, and commits batch
        entries written during :meth:`enqueue`.
        """
        try:
            self._entries_condition.acquire()
            self.started = True
            while not self.stopping:
                if len(self.batch.entries) == 0:
                    # branch coverage of this code extremely flaky
                    self._entries_condition.wait()  # pragma: NO COVER

                if len(self.batch.entries) > 0:
                    self.batch.commit()
        finally:
            self._entries_condition.release()

        # main thread may be waiting for worker thread to finish writing its
        # final entries. here we signal that it's done.
        self._stop_condition.acquire()
        self._stop_condition.notify()
        self._stop_condition.release()

    def _start(self):
        """Called by this class's constructor

        This method is responsible for starting the thread and registering
        the exit handlers.
        """
        try:
            self._entries_condition.acquire()
            self._thread = threading.Thread(
                target=self._run, name=_WORKER_THREAD_NAME)
            self._thread.setDaemon(True)
            self._thread.start()
        finally:
            self._entries_condition.release()
            atexit.register(self._stop)

    def _stop(self):
        """Signals the worker thread to shut down

        Also waits for ``stop_timeout`` seconds for the worker to finish.

        This method is called by the ``atexit`` handler registered by
         :meth:`start`.
        """
        if not self.started or self.stopping:
            return

        # lock the stop condition first so that the worker
        # thread can't notify it's finished before we wait
        self._stop_condition.acquire()

        # now notify the worker thread to shutdown
        self._entries_condition.acquire()
        self.stopping = True
        self._entries_condition.notify()
        self._entries_condition.release()

        # now wait for it to signal it's finished
        self._stop_condition.wait(self._stop_timeout)
        self._stop_condition.release()
        self.stopped = True

    def enqueue(self, record, message):
        """Queues up a log entry to be written by the background thread."""
        try:
            self._entries_condition.acquire()
            if self.stopping:
                return
            info = {'message': message, 'python_logger': record.name}
            self.batch.log_struct(info, severity=record.levelname)
            self._entries_condition.notify()
        finally:
            self._entries_condition.release()


class BackgroundThreadTransport(Transport):
    """Aysnchronous transport that uses a background thread.

    Writes logging entries as a batch process.
    """

    def __init__(self, client, name):
        http = copy.deepcopy(client._http)
        self.client = client.__class__(
            client.project, client._credentials, http)
        logger = self.client.logger(name)
        self.worker = _Worker(logger)

    def send(self, record, message):
        """Overrides Transport.send().

        :type record: :class:`logging.LogRecord`
        :param record: Python log record that the handler was called with.

        :type message: str
        :param message: The message from the ``LogRecord`` after being
                        formatted by the associated log formatters.
        """
        self.worker.enqueue(record, message)
