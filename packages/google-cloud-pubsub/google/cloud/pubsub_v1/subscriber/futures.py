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

from __future__ import absolute_import

from google.cloud.pubsub_v1 import futures


class StreamingPullFuture(futures.Future):
    """Represents a process that asynchronously performs streaming pull and
    schedules messages to be processed.

    This future is resolved when the process is stopped (via :meth:`cancel`) or
    if it encounters an unrecoverable error. Calling `.result()` will cause
    the calling thread to block indefinitely.
    """

    def __init__(self, manager):
        super(StreamingPullFuture, self).__init__()
        self.__manager = manager
        self.__manager.add_close_callback(self._on_close_callback)
        self.__cancelled = False

    def _on_close_callback(self, manager, result):
        if self.done():
            # The future has already been resolved in a different thread,
            # nothing to do on the streaming pull manager shutdown.
            return

        if result is None:
            self.set_result(True)
        else:
            self.set_exception(result)

    def cancel(self):
        """Stops pulling messages and shutdowns the background thread consuming
        messages.

        .. versionchanged:: 2.4.1
           The method does not block anymore, it just triggers the shutdown and returns
           immediately. To block until the background stream is terminated, call
           :meth:`result()` after cancelling the future.
        """
        # NOTE: We circumvent the base future's self._state to track the cancellation
        # state, as this state has different meaning with streaming pull futures.
        self.__cancelled = True
        return self.__manager.close()

    def cancelled(self):
        """
        returns:
            bool: ``True`` if the subscription has been cancelled.
        """
        return self.__cancelled
