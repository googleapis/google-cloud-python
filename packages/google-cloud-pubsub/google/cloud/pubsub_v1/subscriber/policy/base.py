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

"""Base class for concurrency policy."""

from __future__ import absolute_import, division

import abc
import collections
import logging
import random
import time

from google.api_core import exceptions
import six

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import _consumer
from google.cloud.pubsub_v1.subscriber import _histogram


_LOGGER = logging.getLogger(__name__)

# Namedtuples for management requests. Used by the Message class to communicate
# items of work back to the policy.
AckRequest = collections.namedtuple(
    'AckRequest',
    ['ack_id', 'byte_size', 'time_to_ack'],
)

DropRequest = collections.namedtuple(
    'DropRequest',
    ['ack_id', 'byte_size'],
)

LeaseRequest = collections.namedtuple(
    'LeaseRequest',
    ['ack_id', 'byte_size'],
)

ModAckRequest = collections.namedtuple(
    'ModAckRequest',
    ['ack_id', 'seconds'],
)

NackRequest = collections.namedtuple(
    'NackRequest',
    ['ack_id', 'byte_size'],
)


@six.add_metaclass(abc.ABCMeta)
class BasePolicy(object):
    """Abstract class defining a subscription policy.

    Although the :class:`~.pubsub_v1.subscriber.policy.thread.Policy` class,
    based on :class:`threading.Thread`, is fine for most cases,
    advanced users may need to implement something based on a different
    concurrency model.

    This class defines the interface for the policy implementation;
    subclasses may be passed as the ``policy_class`` argument to
    :class:`~.pubsub_v1.client.SubscriberClient`.

    Args:
        client (google.cloud.pubsub_v1.subscriber.client.Client): The
            subscriber client used to create this instance.
        subscription (str): The name of the subscription. The canonical
            format for this is
            ``projects/{project}/subscriptions/{subscription}``.
        flow_control (google.cloud.pubsub_v1.types.FlowControl): The flow
            control settings.
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

    _managed_ack_ids = None
    _RETRYABLE_STREAM_ERRORS = (
        exceptions.DeadlineExceeded,
        exceptions.ServiceUnavailable,
    )

    def __init__(self, client, subscription,
                 flow_control=types.FlowControl(), histogram_data=None):
        self._client = client
        self._subscription = subscription
        self._consumer = _consumer.Consumer()
        self._ack_deadline = 10
        self._last_histogram_size = 0
        self._future = None
        self.flow_control = flow_control
        self.histogram = _histogram.Histogram(data=histogram_data)

        # These are for internal flow control tracking.
        # They should not need to be used by subclasses.
        self._bytes = 0
        self._ack_on_resume = set()

    @property
    def ack_deadline(self):
        """Return the appropriate ack deadline.

        This method is "sticky". It will only perform the computations to
        check on the right ack deadline if the histogram has gained a
        significant amount of new information.

        Returns:
            int: The correct ack deadline.
        """
        target = min([
            self._last_histogram_size * 2,
            self._last_histogram_size + 100,
        ])
        if len(self.histogram) > target:
            self._ack_deadline = self.histogram.percentile(percent=99)
        return self._ack_deadline

    @property
    def future(self):
        """Return the Future in use, if any.

        Returns:
            google.cloud.pubsub_v1.subscriber.futures.Future: A Future
            conforming to the :class:`~concurrent.futures.Future` interface.
        """
        return self._future

    @property
    def managed_ack_ids(self):
        """Return the ack IDs currently being managed by the policy.

        Returns:
            set: The set of ack IDs being managed.
        """
        if self._managed_ack_ids is None:
            self._managed_ack_ids = set()
        return self._managed_ack_ids

    @property
    def subscription(self):
        """Return the subscription.

        Returns:
            str: The subscription
        """
        return self._subscription

    @property
    def _load(self):
        """Return the current load.

        The load is represented as a float, where 1.0 represents having
        hit one of the flow control limits, and values between 0.0 and 1.0
        represent how close we are to them. (0.5 means we have exactly half
        of what the flow control setting allows, for example.)

        There are (currently) two flow control settings; this property
        computes how close the subscriber is to each of them, and returns
        whichever value is higher. (It does not matter that we have lots of
        running room on setting A if setting B is over.)

        Returns:
            float: The load value.
        """
        return max([
            len(self.managed_ack_ids) / self.flow_control.max_messages,
            self._bytes / self.flow_control.max_bytes,
            self._consumer.pending_requests / self.flow_control.max_requests
        ])

    def _maybe_resume_consumer(self):
        """Check the current load and resume the consumer if needed."""
        # If we have been paused by flow control, check and see if we are
        # back within our limits.
        #
        # In order to not thrash too much, require us to have passed below
        # the resume threshold (80% by default) of each flow control setting
        # before restarting.
        if not self._consumer.paused:
            return

        if self._load < self.flow_control.resume_threshold:
            self._consumer.resume()
        else:
            _LOGGER.debug('Did not resume, current load is %s', self._load)

    def ack(self, items):
        """Acknowledge the given messages.

        Args:
            items(Sequence[AckRequest]): The items to acknowledge.
        """
        # If we got timing information, add it to the histogram.
        for item in items:
            time_to_ack = item.time_to_ack
            if time_to_ack is not None:
                self.histogram.add(int(time_to_ack))

        ack_ids = [item.ack_id for item in items]
        if self._consumer.active:
            # Send the request to ack the message.
            request = types.StreamingPullRequest(ack_ids=ack_ids)
            self._consumer.send_request(request)
        else:
            # If the consumer is inactive, then queue the ack_ids here; it
            # will be acked as part of the initial request when the consumer
            # is started again.
            self._ack_on_resume.update(ack_ids)

        # Remove the message from lease management.
        self.drop(items)

    def call_rpc(self, request_generator):
        """Invoke the Pub/Sub streaming pull RPC.

        Args:
            request_generator (Generator): A generator that yields requests,
                and blocks if there are no outstanding requests (until such
                time as there are).

        Returns:
            Iterable[~google.cloud.pubsub_v1.types.StreamingPullResponse]: An
            iterable of pull responses.
        """
        return self._client.api.streaming_pull(request_generator)

    def drop(self, items):
        """Remove the given messages from lease management.

        Args:
            items(Sequence[DropRequest]): The items to drop.
        """
        # Remove the ack ID from lease management, and decrement the
        # byte counter.
        for item in items:
            if item.ack_id in self.managed_ack_ids:
                self.managed_ack_ids.remove(item.ack_id)
                self._bytes -= item.byte_size
            else:
                _LOGGER.debug('Item %s wasn\'t managed', item.ack_id)

        if self._bytes < 0:
            _LOGGER.debug(
                'Bytes was unexpectedly negative: %d', self._bytes)
            self._bytes = 0

        self._maybe_resume_consumer()

    def get_initial_request(self, ack_queue=False):
        """Return the initial request.

        This defines the initial request that must always be sent to Pub/Sub
        immediately upon opening the subscription.

        Args:
            ack_queue (bool): Whether to include any acks that were sent
                while the connection was paused.

        Returns:
            google.cloud.pubsub_v1.types.StreamingPullRequest: A request
            suitable for being the first request on the stream (and not
            suitable for any other purpose).

        .. note::
            If ``ack_queue`` is set to True, this includes the ack_ids, but
            also clears the internal set.

            This means that calls to :meth:`get_initial_request` with
            ``ack_queue`` set to True are not idempotent.
        """
        # Any ack IDs that are under lease management and not being acked
        # need to have their deadline extended immediately.
        ack_ids = set()
        lease_ids = self.managed_ack_ids
        if ack_queue:
            ack_ids = self._ack_on_resume
            lease_ids = lease_ids.difference(ack_ids)

        # Put the request together.
        request = types.StreamingPullRequest(
            ack_ids=list(ack_ids),
            modify_deadline_ack_ids=list(lease_ids),
            modify_deadline_seconds=[self.ack_deadline] * len(lease_ids),
            stream_ack_deadline_seconds=self.histogram.percentile(99),
            subscription=self.subscription,
        )

        # Clear the ack_ids set.
        # Note: If `ack_queue` is False, this just ends up being a no-op,
        # since the set is just an empty set.
        ack_ids.clear()

        # Return the initial request.
        return request

    def lease(self, items):
        """Add the given messages to lease management.

        Args:
            items(Sequence[LeaseRequest]): The items to lease.
        """
        for item in items:
            # Add the ack ID to the set of managed ack IDs, and increment
            # the size counter.
            if item.ack_id not in self.managed_ack_ids:
                self.managed_ack_ids.add(item.ack_id)
                self._bytes += item.byte_size
            else:
                _LOGGER.debug(
                    'Message %s is already lease managed', item.ack_id)

        # Sanity check: Do we have too many things in our inventory?
        # If we do, we need to stop the stream.
        if self._load >= 1.0:
            self._consumer.pause()

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
        while True:
            # Sanity check: Should this infinite loop quit?
            if not self._consumer.active:
                _LOGGER.debug('Consumer inactive, ending lease maintenance.')
                return

            # Determine the appropriate duration for the lease. This is
            # based off of how long previous messages have taken to ack, with
            # a sensible default and within the ranges allowed by Pub/Sub.
            p99 = self.histogram.percentile(99)
            _LOGGER.debug('The current p99 value is %d seconds.', p99)

            # Create a streaming pull request.
            # We do not actually call `modify_ack_deadline` over and over
            # because it is more efficient to make a single request.
            ack_ids = list(self.managed_ack_ids)
            _LOGGER.debug('Renewing lease for %d ack IDs.', len(ack_ids))
            if ack_ids:
                request = types.StreamingPullRequest(
                    modify_deadline_ack_ids=ack_ids,
                    modify_deadline_seconds=[p99] * len(ack_ids),
                )
                # NOTE: This may not work as expected if ``consumer.active``
                #       has changed since we checked it. An implementation
                #       without any sort of race condition would require a
                #       way for ``send_request`` to fail when the consumer
                #       is inactive.
                self._consumer.send_request(request)

            # Now wait an appropriate period of time and do this again.
            #
            # We determine the appropriate period of time based on a random
            # period between 0 seconds and 90% of the lease. This use of
            # jitter (http://bit.ly/2s2ekL7) helps decrease contention in cases
            # where there are many clients.
            snooze = random.uniform(0.0, p99 * 0.9)
            _LOGGER.debug('Snoozing lease management for %f seconds.', snooze)
            time.sleep(snooze)

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
        self._consumer.send_request(request)

    def nack(self, items):
        """Explicitly deny receipt of messages.

        Args:
            items(Sequence[NackRequest]): The items to deny.
        """
        self.modify_ack_deadline([
            ModAckRequest(ack_id=item.ack_id, seconds=0)
            for item in items])
        self.drop(
            [DropRequest(*item) for item in items])

    @abc.abstractmethod
    def close(self):
        """Close the existing connection.

        Raises:
            NotImplementedError: Always
        """
        raise NotImplementedError

    @abc.abstractmethod
    def on_exception(self, exception):
        """Called when a gRPC exception occurs.

        If this method does nothing, then the stream is re-started. If this
        raises an exception, it will stop the consumer thread. This is
        executed on the response consumer helper thread.

        Implementations should return :data:`True` if they want the consumer
        thread to remain active, otherwise they should return :data:`False`.

        Args:
            exception (Exception): The exception raised by the RPC.

        Raises:
            NotImplementedError: Always
        """
        raise NotImplementedError

    def on_request(self, request):
        """Called whenever a request has been sent to gRPC.

        This allows the policy to measure the rate of requests sent along the
        stream and apply backpressure by pausing or resuming the consumer
        if needed.

        Args:
            request (Any): The protobuf request that was sent to gRPC.
        """
        self._maybe_resume_consumer()

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

        Raises:
            NotImplementedError: Always
        """
        raise NotImplementedError

    @abc.abstractmethod
    def open(self, callback):
        """Open a streaming pull connection and begin receiving messages.

        For each message received, the ``callback`` function is fired with
        a :class:`~.pubsub_v1.subscriber.message.Message` as its only
        argument.

        This method is virtual, but concrete implementations should return
        a :class:`~google.api_core.future.Future` that provides an interface
        to block on the subscription if desired, and handle errors.

        Args:
            callback (Callable[Message]): A callable that receives a
                Pub/Sub Message.

        Raises:
            NotImplementedError: Always
        """
        raise NotImplementedError
