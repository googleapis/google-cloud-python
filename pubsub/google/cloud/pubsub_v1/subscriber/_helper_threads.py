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


def _current_thread():
    """Get the currently active thread.

    This is provided as a test helper so that it can be mocked easily.
    Mocking ``threading.current_thread()`` directly may have unintended
    consequences on code that relies on it.

    Returns:
        threading.Thread: The current thread.
    """
    return threading.current_thread()


class HelperThreadRegistry(object):
    def __init__(self):
        self._helper_threads = {}

    def __contains__(self, needle):
        return needle in self._helper_threads

    def start(self, name, queue, target):
        """Create and start a helper thread.

        Args:
            name (str): The name of the helper thread.
            queue (Queue): A concurrency-safe queue.
            target (Callable): The target of the thread.

        Returns:
            threading.Thread: The created thread.
        """
        # Create and start the helper thread.
        thread = threading.Thread(
            name='Thread-ConsumerHelper-{}'.format(name),
            target=target,
        )
        thread.daemon = True
        thread.start()

        # Keep track of the helper thread, so we are able to stop it.
        self._helper_threads[name] = _HelperThread(name, thread, queue)
        _LOGGER.debug('Started helper thread %s', name)
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

        if helper_thread.thread is _current_thread():
            # The current thread cannot ``join()`` itself but it can
            # still send a signal to stop.
            _LOGGER.debug('Cannot stop current thread %s', name)
            helper_thread.queue.put(STOP)
            # We return and stop short of ``pop()``-ing so that the
            # thread that invoked the current helper can properly stop
            # it.
            return

        # Join the thread if it is still alive.
        if helper_thread.thread.is_alive():
            _LOGGER.debug('Stopping helper thread %s', name)
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
    """A helper that executes a callback for every item in the queue.

    .. note::

        This is not actually a thread, but it is intended to be a target
        for a thread.

    Calls a blocking ``get()`` on the ``queue`` until it encounters
    :attr:`STOP`.

    Args:
        queue (~queue.Queue): A Queue instance, appropriate for crossing the
            concurrency boundary implemented by ``executor``. Items will
            be popped off (with a blocking ``get()``) until :attr:`STOP`
            is encountered.
        callback (Callable): A callback that can process items pulled off
            of the queue.
    """

    def __init__(self, queue, callback):
        self.queue = queue
        self._callback = callback

    def __call__(self):
        while True:
            item = self.queue.get()
            if item == STOP:
                _LOGGER.debug('Exiting the QueueCallbackThread.')
                return

            # Run the callback. If any exceptions occur, log them and
            # continue.
            try:
                self._callback(item)
            except Exception as exc:
                _LOGGER.error('%s: %s', exc.__class__.__name__, exc)
