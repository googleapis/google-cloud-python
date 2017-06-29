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

import abc
import random
import time

import six

from google import gax

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import consumer
from google.cloud.pubsub_v1.subscriber import histogram


@six.add_metaclass(abc.ABCMeta)
class BasePolicy(object):
    """Abstract class defining a subscription policy.

    Although the :class:`~.pubsub_v1.subscriber.policy.mp.Policy` class,
    based on :class:`multiprocessing.Process`, is fine for most cases,
    advanced users may need to implement something based on a different
    concurrency model.

    This class defines the interface for the policy implementation;
    subclasses may be passed as the ``policy_class`` argument to
    :class:`~.pubsub_v1.client.SubscriberClient`.
    """
    def __init__(self, client, subscription, histogram_data=None):
        """Instantiate the policy.

        Args:
            client (~.pubsub_v1.subscriber.client): The subscriber client used
                to create this instance.
            subscription (str): The name of the subscription. The canonical
                format for this is
                ``projects/{project}/subscriptions/{subscription}``.
            histogram_data (dict): Optional: A structure to store the histogram
                data for predicting appropriate ack times. If set, this should
                be a dictionary-like object.

                .. note::
                    Additionally, the histogram relies on the assumption
                    that the dictionary will properly sort keys provided
                    that all keys are positive integers. If you are sending
                    your own dictionary class, ensure this assumption holds
                    or you will get strange behavior.
        """
        self._client = client
        self._subscription = subscription
        self._consumer = consumer.Consumer(self)
        self._ack_deadline = 10
        self._last_histogram_size = 0
        self.histogram = histogram.Histogram(data=histogram_data)

    @property
    def ack_deadline(self):
        """Return the appropriate ack deadline.

        This method is "sticky". It will only perform the computations to
        check on the right ack deadline if the histogram has gained a
        significant amount of new information.

        Returns:
            int: The correct ack deadline.
        """
        if len(self.histogram) > self._last_histogram_size * 2:
            self._ack_deadline = self.histogram.percentile(percent=99)
        return self._ack_deadline

    @property
    def initial_request(self):
        """Return the initial request.

        This defines the intiial request that must always be sent to Pub/Sub
        immediately upon opening the subscription.
        """
        return types.StreamingPullRequest(
            stream_ack_deadline_seconds=self.histogram.percentile(99),
            subscription=self.subscription,
        )

    @property
    def managed_ack_ids(self):
        """Return the ack IDs currently being managed by the policy.

        Returns:
            set: The set of ack IDs being managed.
        """
        if not hasattr(self, '_managed_ack_ids'):
            self._managed_ack_ids = set()
        return self._managed_ack_ids

    @property
    def subscription(self):
        """Return the subscription.

        Returns:
            str: The subscription
        """
        return self._subscription

    def ack(self, ack_id):
        """Acknowledge the message corresponding to the given ack_id.

        Args:
            ack_id (str): The ack ID.
        """
        request = types.StreamingPullRequest(ack_ids=[ack_id])
        self._consumer.send_request(request)

    def call_rpc(self, request_generator):
        """Invoke the Pub/Sub streaming pull RPC.

        Args:
            request_generator (Generator): A generator that yields requests,
                and blocks if there are no outstanding requests (until such
                time as there are).
        """
        return self._client.api.streaming_pull(request_generator,
            options=gax.CallOptions(timeout=600),
        )

    def drop(self, ack_id):
        """Remove the given ack ID from lease management.

        Args:
            ack_id (str): The ack ID.
        """
        self.managed_ack_ids.remove(ack_id)

    def lease(self, ack_id):
        """Add the given ack ID to lease management.

        Args:
            ack_id (str): The ack ID.
        """
        self.managed_ack_ids.add(ack_id)

    def maintain_leases(self):
        """Maintain all of the leases being managed by the policy.

        This method modifies the ack deadline for all of the managed
        ack IDs, then waits for most of that time (but with jitter), and
        then calls itself.

        .. warning::
            This method blocks, and generally should be run in a separate
            thread or process.

            Additionally, you should not have to call this method yourself,
            unless you are implementing your own policy. If you are
            implementing your own policy, you _should_ call this method
            in an appropriate form of subprocess.
        """
        # Determine the appropriate duration for the lease.
        # This is based off of how long previous messages have taken to ack,
        # with a sensible default and within the ranges allowed by Pub/Sub.
        p99 = self.histogram.percentile(99)

        # Create a streaming pull request.
        # We do not actually call `modify_ack_deadline` over and over because
        # it is more efficient to make a single request.
        ack_ids = list(self.managed_ack_ids)
        if len(ack_ids) > 0:
            request = types.StreamingPullRequest(
                modify_deadline_ack_ids=ack_ids,
                modify_deadline_seconds=[p99] * len(ack_ids),
            )
            self._consumer.send_request(request)

        # Now wait an appropriate period of time and do this again.
        #
        # We determine the appropriate period of time based on a random
        # period between 0 seconds and 90% of the lease. This use of
        # jitter (http://bit.ly/2s2ekL7) helps decrease contention in cases
        # where there are many clients.
        time.sleep(random.uniform(0.0, p99 * 0.9))
        self.maintain_leases()

    def modify_ack_deadline(self, ack_id, seconds):
        """Modify the ack deadline for the given ack_id.

        Args:
            ack_id (str): The ack ID
            seconds (int): The number of seconds to set the new deadline to.
        """
        request = types.StreamingPullRequest(
            modify_deadline_ack_ids=[ack_id],
            modify_deadline_seconds=[seconds],
        )
        self._consumer.send_request(request)

    def nack(self, ack_id):
        """Explicitly deny receipt of a message.

        Args:
            ack_id (str): The ack ID.
        """
        return self.modify_ack_deadline(ack_id, 0)

    @abc.abstractmethod
    def on_response(self, response):
        """Process a response from gRPC.

        This gives the consumer control over how responses are scheduled to
        be processed. This method is expected to not block and instead
        schedule the response to be consumed by some sort of concurrency.

        For example, if a the Policy implementation takes a callback in its
        constructor, you can schedule the callback using a
        :cls:`concurrent.futures.ThreadPoolExecutor`::

            self._pool.submit(self._callback, response)

        This is called from the response consumer helper thread.

        Args:
            response (Any): The protobuf response from the RPC.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def on_exception(self, exception):
        """Called when a gRPC exception occurs.

        If this method does nothing, then the stream is re-started. If this
        raises an exception, it will stop the consumer thread.
        This is executed on the response consumer helper thread.

        Args:
            exception (Exception): The exception raised by the RPC.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def open(self, callback):
        """Open a streaming pull connection and begin receiving messages.

        For each message received, the ``callback`` function is fired with
        a :class:`~.pubsub_v1.subscriber.message.Message` as its only
        argument.

        Args:
            callback (Callable[Message]): A callable that receives a
                Pub/Sub Message.
        """
        raise NotImplementedError
