# Copyright 2017, Google LLC All rights reserved.
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

import collections
import logging
import threading
import uuid

import six

__all__ = (
    'HelperThreadRegistry',
    'QueueCallbackThread',
    'STOP',
)

_LOGGER = logging.getLogger(__name__)

_HelperThread = collections.namedtuple(
    'HelperThreads',
    ['name', 'thread', 'queue'],
)


# Helper thread stop indicator. This could be a sentinel object or None,
# but the sentinel object's ID can change if the process is forked, and
# None has the possibility of a user accidentally killing the helper
# thread.
STOP = uuid.uuid4()


class HelperThreadRegistry(object):
    def __init__(self):
        self._helper_threads = {}

    def __contains__(self, needle):
        return needle in self._helper_threads

    def start(self, name, queue, target, *args, **kwargs):
        """Create and start a helper thread.

        Args:
            name (str): The name of the helper thread.
            queue (Queue): A concurrency-safe queue.
            target (Callable): The target of the thread.
            args: Additional args passed to the thread constructor.
            kwargs: Additional kwargs passed to the thread constructor.

        Returns:
            threading.Thread: The created thread.
        """
        # Create and start the helper thread.
        thread = threading.Thread(
            name='Consumer helper: {}'.format(name),
            target=target,
            *args, **kwargs
        )
        thread.daemon = True
        thread.start()

        # Keep track of the helper thread, so we are able to stop it.
        self._helper_threads[name] = _HelperThread(name, thread, queue)
        _LOGGER.debug('Started helper thread {}'.format(name))
        return thread

    def stop(self, name):
        """Stops a helper thread.

        Sends the stop message and blocks until the thread joins.

        Args:
            name (str): The name of the thread.
        """
        # Attempt to retrieve the thread; if it is gone already, no-op.
        helper_thread = self._helper_threads.get(name)
        if helper_thread is None:
            return

        # Join the thread if it is still alive.
        if helper_thread.thread.is_alive():
            _LOGGER.debug('Stopping helper thread {}'.format(name))
            helper_thread.queue.put(STOP)
            helper_thread.thread.join()

        # Remove the thread from our tracking.
        self._helper_threads.pop(name, None)

    def stop_all(self):
        """Stop all helper threads."""
        # This could be more efficient by sending the stop signal to all
        # threads before joining any of them.
        for name in list(six.iterkeys(self._helper_threads)):
            self.stop(name)


class QueueCallbackThread(object):
    """A helper thread that executes a callback for every item in
    the queue.
    """
    def __init__(self, queue, callback):
        self.queue = queue
        self._callback = callback

    def __call__(self):
        while True:
            item = self.queue.get()
            if item == STOP:
                break

            # Run the callback. If any exceptions occur, log them and
            # continue.
            try:
                self._callback(item)
            except Exception as exc:
                _LOGGER.error('{class_}: {message}'.format(
                    class_=exc.__class__.__name__,
                    message=str(exc),
                ))
