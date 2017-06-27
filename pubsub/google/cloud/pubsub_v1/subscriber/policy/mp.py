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

from google.cloud.pubsub_v1.subscriber import helper_threads
from google.cloud.pubsub_v1.subscriber.consumer import base
from google.cloud.pubsub_v1.subscriber.message import Message


class Policy(base.BasePolicy):
    """A consumer class based on :class:``multiprocessing.Process``.

    This consumer handles the connection to the Pub/Sub service and all of
    the concurrency needs.
    """
    def __init__(self, client, subscription):
        # Default the callback to a no-op; it is provided by `.open`.
        self._callback = lambda message: None

        # Create a manager for keeping track of shared state.
        self._manager = multiprocessing.Manager()
        self._shared = self._manager.Namespace()
        self._shared.subscription = subscription
        self._shared.histogram_data = self._manager.dict()
        self._shared.request_queue = self._manager.Queue()

        # Call the superclass constructor.
        super(Policy, self).__init__(client, subscription,
            histogram_data=self._shared.histogram_data,
        )

        # Also maintain a request queue and an executor.
        self._executor = futures.ProcessPoolExecutor()
        self._callback_requests = helper_threads.QueueCallbackThread(
            self._shared.request_queue,
            self._on_callback_request,
        )

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
        self._consumer.helper_threads.stop('callback requests worker')

    def open(self, callback):
        """Open a streaming pull connection and begin receiving messages.

        For each message received, the ``callback`` function is fired with
        a :class:`~.pubsub_v1.subscriber.message.Message` as its only
        argument.

        Args:
            callback (function): The callback function.
        """
        self._callback = callback
        self._consumer.helper_threads.start('callback requests worker',
            self._shared.request_queue,
            self._callback_requests,
        )

    def on_callback_request(self, callback_request):
        """Map the callback request to the appropriate GRPC request."""
        action, args = callback_request[0], callback_request[1:]
        getattr(self, action)(*args)

    def on_response(self, response):
        """Process all received Pub/Sub messages.

        For each message, schedule a callback with the executor.
        """
        for msg in response.received_messages:
            message = Message(self, msg.ack_id, msg.message)
            self._executor.submit(self._callback, message)
