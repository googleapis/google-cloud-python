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

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber._protocol import helper_threads
from google.cloud.pubsub_v1.subscriber._protocol import requests


_LOGGER = logging.getLogger(__name__)
_CALLBACK_WORKER_NAME = 'Thread-CallbackRequestDispatcher'


class Dispatcher(object):
    def __init__(self, manager, queue):
        self._manager = manager
        self._queue = queue
        self._thread = None
        self._operational_lock = threading.Lock()

    def start(self):
        """Start a thread to dispatch requests queued up by callbacks.
        Spawns a thread to run :meth:`dispatch_callback`.
        """
        with self._operational_lock:
            if self._thread is not None:
                raise ValueError('Dispatcher is already running.')

            flow_control = self._manager.flow_control
            worker = helper_threads.QueueCallbackWorker(
                self._queue,
                self.dispatch_callback,
                max_items=flow_control.max_request_batch_size,
                max_latency=flow_control.max_request_batch_latency
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
        with self._operational_lock:
            if self._thread is not None:
                # Signal the worker to stop by queueing a "poison pill"
                self._queue.put(helper_threads.STOP)
                self._thread.join()

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
        if not self._manager.is_active:
            return

        batched_commands = collections.defaultdict(list)

        for item in items:
            batched_commands[item.__class__].append(item)

        _LOGGER.debug('Handling %d batched requests', len(items))

        if batched_commands[requests.LeaseRequest]:
            self.lease(batched_commands.pop(requests.LeaseRequest))
        if batched_commands[requests.ModAckRequest]:
            self.modify_ack_deadline(
                batched_commands.pop(requests.ModAckRequest))
        # Note: Drop and ack *must* be after lease. It's possible to get both
        # the lease the and ack/drop request in the same batch.
        if batched_commands[requests.AckRequest]:
            self.ack(batched_commands.pop(requests.AckRequest))
        if batched_commands[requests.NackRequest]:
            self.nack(batched_commands.pop(requests.NackRequest))
        if batched_commands[requests.DropRequest]:
            self.drop(batched_commands.pop(requests.DropRequest))

    def ack(self, items):
        """Acknowledge the given messages.

        Args:
            items(Sequence[AckRequest]): The items to acknowledge.
        """
        # If we got timing information, add it to the histogram.
        for item in items:
            time_to_ack = item.time_to_ack
            if time_to_ack is not None:
                self._manager.ack_histogram.add(time_to_ack)

        ack_ids = [item.ack_id for item in items]
        request = types.StreamingPullRequest(ack_ids=ack_ids)
        self._manager.send(request)

        # Remove the message from lease management.
        self.drop(items)

    def drop(self, items):
        """Remove the given messages from lease management.

        Args:
            items(Sequence[DropRequest]): The items to drop.
        """
        self._manager.leaser.remove(items)
        self._manager.maybe_resume_consumer()

    def lease(self, items):
        """Add the given messages to lease management.

        Args:
            items(Sequence[LeaseRequest]): The items to lease.
        """
        self._manager.leaser.add(items)
        self._manager.maybe_pause_consumer()

    def modify_ack_deadline(self, items):
        """Modify the ack deadline for the given messages.

        Args:
            items(Sequence[ModAckRequest]): The items to modify.
        """
        ack_ids = [item.ack_id for item in items]
        seconds = [item.seconds for item in items]

        request = types.StreamingPullRequest(
            modify_deadline_ack_ids=ack_ids,
            modify_deadline_seconds=seconds,
        )
        self._manager.send(request)

    def nack(self, items):
        """Explicitly deny receipt of messages.

        Args:
            items(Sequence[NackRequest]): The items to deny.
        """
        self.modify_ack_deadline([
            requests.ModAckRequest(ack_id=item.ack_id, seconds=0)
            for item in items])
        self.drop(
            [requests.DropRequest(*item) for item in items])
