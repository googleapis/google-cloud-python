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

"""Transport for Python logging handler that uses a background worker to log
to Stackdriver Logging asynchronously."""

import atexit
import copy
import threading

from gcloud.logging import Client
from gcloud.logging.handlers.transports.base import Transport


class _Worker(object):
    """ A threaded worker that writes batches of log entires to the logger
    API.

    This class reuses a single :class:`Batch` method to write successive
    entries.

    Currently, the only public methods are constructing it (which also starts
    it) and enqueuing Logger (record, message) pairs.
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
        """_run is the entry point for the worker thread. It loops
        until self.stopping is set to true, and commits batch entries
        written during :meth:`enqueue`"""
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
        """_start is called by this class's constructor, and is responsible
        for starting the thread and registering the exit handlers. """
        try:
            self._entries_condition.acquire()
            self._thread = threading.Thread(
                target=self._run,
                name="gcloud.logging.handlers.transport.Worker")
            self._thread.setDaemon(True)
            self._thread.start()
        finally:
            self._entries_condition.release()
            atexit.register(self._stop)

    def _stop(self):
        """_stop signals the worker thread to shut down, and waits for
        stop_timeout second for it to finish.

         _stop is called by the atexit handler registered by
         :meth:`start`. """
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
        """enqueue queues up a log entry to be written by the background
        thread. """
        try:
            self._entries_condition.acquire()
            if self.stopping:
                return
            self.batch.log_struct({"message": message,
                                   "python_logger": record.name},
                                  severity=record.levelname)
            self._entries_condition.notify()
        finally:
            self._entries_condition.release()


class BackgroundThreadTransport(Transport):
    """Aysnchronous tranpsort that uses a background thread to write logging
    entries as a batch process"""

    def __init__(self, client, name):
        super(BackgroundThreadTransport, self).__init__(client, name)
        http = copy.deepcopy(client.connection.http)
        http = client.connection.credentials.authorize(http)
        self.client = Client(client.project,
                             client.connection.credentials,
                             http)
        logger = self.client.logger(name)
        self.worker = _Worker(logger)

    def send(self, record, message):
        """Overrides Transport.send(). record is the LogRecord
        the handler was called with, message is the message from LogRecord
        after being formatted by associated log formatters.

        :type record: :class:`logging.LogRecord`
        :param record: Python log record

        :type message: str
        :param message: The formatted log message
        """
        self.worker.enqueue(record, message)
