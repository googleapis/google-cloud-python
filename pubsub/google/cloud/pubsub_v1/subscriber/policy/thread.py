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

import collections
from concurrent import futures
import logging
import sys
import threading

from six.moves import queue as queue_mod

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import _helper_threads
from google.cloud.pubsub_v1.subscriber.futures import Future
from google.cloud.pubsub_v1.subscriber.policy import base
from google.cloud.pubsub_v1.subscriber.message import Message


_LOGGER = logging.getLogger(__name__)
_CALLBACK_WORKER_NAME = 'Thread-Consumer-CallbackRequestsWorker'
_VALID_ACTIONS = frozenset([
    'ack',
    'drop',
    'lease',
    'modify_ack_deadline',
    'nack',
])


def _do_nothing_callback(message):
    """Default callback for messages received by subscriber.

    Does nothing with the message and returns :data:`None`.

    Args:
        message (~google.cloud.pubsub_v1.subscriber.message.Message): A
            protobuf message returned by the backend and parsed into
            our high level message type.

    Returns:
        NoneType: Always.
    """
    return None


class Policy(base.BasePolicy):
    """A consumer class based on :class:`threading.Thread`.

    This consumer handles the connection to the Pub/Sub service and all of
    the concurrency needs.

    Args:
        client (~.pubsub_v1.subscriber.client): The subscriber client used
            to create this instance.
        subscription (str): The name of the subscription. The canonical
            format for this is
            ``projects/{project}/subscriptions/{subscription}``.
        flow_control (~google.cloud.pubsub_v1.types.FlowControl): The flow
            control settings.
        executor (~concurrent.futures.ThreadPoolExecutor): (Optional.) A
            ThreadPoolExecutor instance, or anything duck-type compatible
            with it.
        queue (~queue.Queue): (Optional.) A Queue instance, appropriate
            for crossing the concurrency boundary implemented by
            ``executor``.
    """

    def __init__(self, client, subscription, flow_control=types.FlowControl(),
                 executor=None, queue=None):
        super(Policy, self).__init__(
            client=client,
            flow_control=flow_control,
            subscription=subscription,
        )
        # Default the callback to a no-op; the **actual** callback is
        # provided by ``.open()``.
        self._callback = _do_nothing_callback
        # Create a queue for keeping track of shared state.
        self._request_queue = self._get_queue(queue)
        # Also maintain an executor.
        self._executor = self._get_executor(executor)
        # The threads created in ``.open()``.
        self._dispatch_thread = None
        self._leases_thread = None

    @staticmethod
    def _get_queue(queue):
        """Gets a queue for the constructor.

        Args:
            queue (Optional[~queue.Queue]): A Queue instance, appropriate
                for crossing the concurrency boundary implemented by
                ``executor``.

        Returns:
            ~queue.Queue: Either ``queue`` if not :data:`None` or a default
            queue.
        """
        if queue is None:
            return queue_mod.Queue()
        else:
            return queue

    @staticmethod
    def _get_executor(executor):
        """Gets an executor for the constructor.

        Args:
            executor (Optional[~concurrent.futures.ThreadPoolExecutor]): A
                ThreadPoolExecutor instance, or anything duck-type compatible
                with it.

        Returns:
            ~concurrent.futures.ThreadPoolExecutor: Either ``executor`` if not
            :data:`None` or a default thread pool executor with 10 workers
            and a prefix (if supported).
        """
        if executor is None:
            executor_kwargs = {}
            if sys.version_info[:2] == (2, 7) or sys.version_info >= (3, 6):
                executor_kwargs['thread_name_prefix'] = (
                    'ThreadPoolExecutor-SubscriberPolicy')
            return futures.ThreadPoolExecutor(
                max_workers=10,
                **executor_kwargs
            )
        else:
            return executor

    def close(self):
        """Close the existing connection.

        .. warning::

            This method is not thread-safe. For example, if this method is
            called while another thread is executing :meth:`open`, then the
            policy could end up in an undefined state. The **same** policy
            instance is not intended to be used by multiple workers (though
            each policy instance **does** have a thread-safe private queue).

        Returns:
            ~google.api_core.future.Future: The future that **was** attached
            to the subscription.

        Raises:
            ValueError: If the policy has not been opened yet.
        """
        if self._future is None:
            raise ValueError('This policy has not been opened yet.')

        # Stop consuming messages.
        self._request_queue.put(_helper_threads.STOP)
        self._dispatch_thread.join()  # Wait until stopped.
        self._dispatch_thread = None
        self._consumer.stop_consuming()
        self._leases_thread.join()
        self._leases_thread = None
        self._executor.shutdown()

        # The subscription is closing cleanly; resolve the future if it is not
        # resolved already.
        if not self._future.done():
            self._future.set_result(None)
        future = self._future
        self._future = None
        return future

    def _start_dispatch(self):
        """Start a thread to dispatch requests queued up by callbacks.

        .. note::

            This assumes, but does not check, that ``_dispatch_thread``
            is :data:`None`.

        Spawns a thread to run :meth:`dispatch_callback` and sets the
        "dispatch thread" member on the current policy.
        """
        _LOGGER.debug('Starting callback requests worker.')
        dispatch_worker = _helper_threads.QueueCallbackWorker(
            self._request_queue,
            self.dispatch_callback,
            max_items=self.flow_control.max_request_batch_size,
            max_latency=self.flow_control.max_request_batch_latency
        )
        # Create and start the helper thread.
        thread = threading.Thread(
            name=_CALLBACK_WORKER_NAME,
            target=dispatch_worker,
        )
        thread.daemon = True
        thread.start()
        _LOGGER.debug('Started helper thread %s', thread.name)
        self._dispatch_thread = thread

    def _start_lease_worker(self):
        """Spawn a helper thread that maintains all of leases for this policy.

        .. note::

            This assumes, but does not check, that ``_leases_thread`` is
            :data:`None`.

        Spawns a thread to run :meth:`maintain_leases` and sets the
        "leases thread" member on the current policy.
        """
        _LOGGER.debug('Starting lease maintenance worker.')
        thread = threading.Thread(
            name='Thread-LeaseMaintenance',
            target=self.maintain_leases,
        )
        thread.daemon = True
        thread.start()

        self._leases_thread = thread

    def open(self, callback):
        """Open a streaming pull connection and begin receiving messages.

        .. warning::

            This method is not thread-safe. For example, if this method is
            called while another thread is executing :meth:`close`, then the
            policy could end up in an undefined state. The **same** policy
            instance is not intended to be used by multiple workers (though
            each policy instance **does** have a thread-safe private queue).

        For each message received, the ``callback`` function is fired with
        a :class:`~.pubsub_v1.subscriber.message.Message` as its only
        argument.

        Args:
            callback (Callable): The callback function.

        Returns:
            ~google.api_core.future.Future: A future that provides
            an interface to block on the subscription if desired, and
            handle errors.

        Raises:
            ValueError: If the policy has already been opened.
        """
        if self._future is not None:
            raise ValueError('This policy has already been opened.')

        # Create the Future that this method will return.
        # This future is the main thread's interface to handle exceptions,
        # block on the subscription, etc.
        self._future = Future(policy=self, completed=threading.Event())

        # Start the thread to pass the requests.
        self._callback = callback
        self._start_dispatch()
        # Actually start consuming messages.
        self._consumer.start_consuming(self)
        self._start_lease_worker()

        # Return the future.
        return self._future

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
        batched_commands = collections.defaultdict(list)

        for item in items:
            batched_commands[item.__class__].append(item)

        _LOGGER.debug('Handling %d batched requests', len(items))

        if batched_commands[base.LeaseRequest]:
            self.lease(batched_commands.pop(base.LeaseRequest))
        if batched_commands[base.ModAckRequest]:
            self.modify_ack_deadline(
                batched_commands.pop(base.ModAckRequest))
        # Note: Drop and ack *must* be after lease. It's possible to get both
        # the lease the and ack/drop request in the same batch.
        if batched_commands[base.AckRequest]:
            self.ack(batched_commands.pop(base.AckRequest))
        if batched_commands[base.NackRequest]:
            self.nack(batched_commands.pop(base.NackRequest))
        if batched_commands[base.DropRequest]:
            self.drop(batched_commands.pop(base.DropRequest))

    def on_exception(self, exception):
        """Handle the exception.

        If the exception is one of the retryable exceptions, this will signal
        to the consumer thread that it should "recover" from the failure.

        This will cause the stream to exit when it returns :data:`False`.

        Returns:
            bool: Indicates if the caller should recover or shut down.
            Will be :data:`True` if the ``exception`` is "acceptable", i.e.
            in a list of retryable / idempotent exceptions.
        """
        # If this is in the list of idempotent exceptions, then we want to
        # retry. That entails just returning None.
        if isinstance(exception, self._RETRYABLE_STREAM_ERRORS):
            return True

        # Set any other exception on the future.
        self._future.set_exception(exception)
        return False

    def on_response(self, response):
        """Process all received Pub/Sub messages.

        For each message, send a modified acknowledgement request to the
        server. This prevents expiration of the message due to buffering by
        gRPC or proxy/firewall. This makes the server and client expiration
        timer closer to each other thus preventing the message being
        redelivered multiple times.

        After the messages have all had their ack deadline updated, execute
        the callback for each message using the executor.
        """
        items = [
            base.ModAckRequest(message.ack_id, self.histogram.percentile(99))
            for message in response.received_messages
        ]
        self.modify_ack_deadline(items)
        for msg in response.received_messages:
            _LOGGER.debug(
                'Using %s to process message with ack_id %s.',
                self._callback, msg.ack_id)
            message = Message(msg.message, msg.ack_id, self._request_queue)
            self._executor.submit(self._callback, message)
