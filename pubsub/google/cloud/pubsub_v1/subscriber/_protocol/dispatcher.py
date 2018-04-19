# Copyright 2017, Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import collections
import logging
import threading

from google.cloud.pubsub_v1.subscriber._protocol import helper_threads
from google.cloud.pubsub_v1.subscriber._protocol import requests


_LOGGER = logging.getLogger(__name__)
_CALLBACK_WORKER_NAME = 'Thread-CallbackRequestDispatcher'


class Dispatcher(object):
    def __init__(self, queue, subscriber):
        self._queue = queue
        self._subscriber = subscriber
        self._thread = None

    def dispatch_callback(self, items):
        """Map the callback request to the appropriate gRPC request.

        Args:
            action (str): The method to be invoked.
            kwargs (Dict[str, Any]): The keyword arguments for the method
                specified by ``action``.

        Raises:
            ValueError: If ``action`` isn't one of the expected actions
                "ack", "drop", "lease", "modify_ack_deadline" or "nack".
        """
        if not self._subscriber.is_active:
            return

        batched_commands = collections.defaultdict(list)

        for item in items:
            batched_commands[item.__class__].append(item)

        _LOGGER.debug('Handling %d batched requests', len(items))

        if batched_commands[requests.LeaseRequest]:
            self._subscriber.lease(batched_commands.pop(requests.LeaseRequest))
        if batched_commands[requests.ModAckRequest]:
            self._subscriber.modify_ack_deadline(
                batched_commands.pop(requests.ModAckRequest))
        # Note: Drop and ack *must* be after lease. It's possible to get both
        # the lease the and ack/drop request in the same batch.
        if batched_commands[requests.AckRequest]:
            self._subscriber.ack(batched_commands.pop(requests.AckRequest))
        if batched_commands[requests.NackRequest]:
            self._subscriber.nack(batched_commands.pop(requests.NackRequest))
        if batched_commands[requests.DropRequest]:
            self._subscriber.drop(batched_commands.pop(requests.DropRequest))

    def start(self):
        """Start a thread to dispatch requests queued up by callbacks.
        Spawns a thread to run :meth:`dispatch_callback`.
        """
        if self._thread is not None:
            raise ValueError('Dispatcher is already running.')

        worker = helper_threads.QueueCallbackWorker(
            self._queue,
            self.dispatch_callback,
            max_items=self._subscriber.flow_control.max_request_batch_size,
            max_latency=self._subscriber.flow_control.max_request_batch_latency
        )
        # Create and start the helper thread.
        thread = threading.Thread(
            name=_CALLBACK_WORKER_NAME,
            target=worker,
        )
        thread.daemon = True
        thread.start()
        _LOGGER.debug('Started helper thread %s', thread.name)
        self._thread = thread

    def stop(self):
        if self._thread is not None:
            # Signal the worker to stop by queueing a "poison pill"
            self._queue.put(helper_threads.STOP)
            self._thread.join()

        self._thread = None
