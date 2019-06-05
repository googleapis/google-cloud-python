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
        self._manager = manager
        self._manager.add_close_callback(self._on_close_callback)
        self._cancelled = False

    def _on_close_callback(self, manager, result):
        if result is None:
            self.set_result(True)
        else:
            self.set_exception(result)

    def cancel(self):
        """Stops pulling messages and shutdowns the background thread consuming
        messages.
        """
        self._cancelled = True
        return self._manager.close()

    def cancelled(self):
        """
        returns:
            bool: ``True`` if the subscription has been cancelled.
        """
        return self._cancelled
