# Copyright 2017, Google Inc. All rights reserved.
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

from concurrent import futures
import multiprocessing

from google.gax.errors import GaxError

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import exceptions
from google.cloud.pubsub_v1.subscriber.consumer import base


class Consumer(base.BaseConsumer):
    """A consumer class based on :class:``multiprocessing.Process``.

    This consumer handles the connection to the Pub/Sub service and all of
    the concurrency needs.
    """
    def __init__(self, client, subscription):
        # Create a manager for keeping track of shared state.
        self._manager = multiprocessing.Manager()
        self._shared = self._manager.Namespace()
        self._shared.subscription = subscription
        self._shared.histogram_data = self._manager.dict()
        self._shared.request_queue = self._manager.Queue()

        # Call the superclass constructor.
        super(Consumer, self).__init__(client, subscription,
            histogram_data=self._shared.histogram_data,
        )

        # Also maintain a request queue and an executor.
        self._executor = futures.ProcessPoolExecutor()

        # Keep track of the GRPC connection.
        self._process = None

    @property
    def subscription(self):
        """Return the subscription.

        Returns:
            str: The subscription
        """
        return self._shared.subscription

    def close(self):
        """Close the existing connection."""
        self._process.terminate()
        self._process = None

    def open(self, callback):
        """Open a streaming pull connection and begin receiving messages.

        For each message received, the ``callback`` function is fired with
        a :class:`~.pubsub_v1.subscriber.message.Message` as its only
        argument.

        Args:
            callback (function): The callback function.
        """
        # Sanity check: If the connection is already open, fail.
        if self._process is not None:
            raise exceptions.AlreadyOpen(self._subscription)

        # Open the request.
        self._process = multiprocessing.Process(self.stream)
        self._process.daemon = True
        self._process.start()

    def stream(self):
        """Stream data to and from the Cloud Pub/Sub service."""

        # The streaming connection expects a series of StreamingPullRequest
        # objects. The first one must specify the subscription and the
        # ack deadline; prepend this to the list.
        self._shared.outgoing_requests.insert(0, types.StreamingPullRequest(
            stream_ack_deadline_seconds=self.ack_deadline,
            subscription=self._subscription,
        ))

        try:
            outgoing = iter(self._shared.outgoing_requests)
        except GaxError:
            return self.stream()
