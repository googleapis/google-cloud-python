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

import logging
import uuid


__all__ = (
    'QueueCallbackWorker',
    'STOP',
)

_LOGGER = logging.getLogger(__name__)


# Helper thread stop indicator. This could be a sentinel object or None,
# but the sentinel object's ID can change if the process is forked, and
# None has the possibility of a user accidentally killing the helper
# thread.
STOP = uuid.uuid4()


class QueueCallbackWorker(object):
    """A helper that executes a callback for every item in the queue.

    Calls a blocking ``get()`` on the ``queue`` until it encounters
    :attr:`STOP`.

    Args:
        queue (~queue.Queue): A Queue instance, appropriate for crossing the
            concurrency boundary implemented by ``executor``. Items will
            be popped off (with a blocking ``get()``) until :attr:`STOP`
            is encountered.
        callback (Callable[[str, Dict], Any]): A callback that can process
            items pulled off of the queue. Items are assumed to be a pair
            of a method name to be invoked and a dictionary of keyword
            arguments for that method.
    """

    def __init__(self, queue, callback):
        self.queue = queue
        self._callback = callback

    def __call__(self):
        while True:
            item = self.queue.get()
            if item == STOP:
                _LOGGER.debug('Exiting the QueueCallbackWorker.')
                return

            # Run the callback. If any exceptions occur, log them and
            # continue.
            try:
                action, kwargs = item
                self._callback(action, kwargs)
            except Exception as exc:
                _LOGGER.error('%s: %s', exc.__class__.__name__, exc)
