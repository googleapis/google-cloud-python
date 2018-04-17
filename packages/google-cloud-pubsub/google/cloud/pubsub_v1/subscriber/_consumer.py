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

"""Bidirectional Streaming Consumer.

The goal here is to consume a bidirectional streaming RPC by fanning out the
responses received from the server to be processed and fanning in requests from
the response processors to be sent to the server through the request stream.
This module is a framework to deal with this pattern in a consistent way:

    * A :class:`Consumer` manages scheduling requests to a stream and consuming
      responses from a stream. The Consumer takes the responses and schedules
      them to be processed in callbacks using any
      :class:`~concurrent.futures.Executor`.
    * A :class:`Policy` which determines how the consumer calls the RPC and
      processes responses, errors, and messages.

The :class:`Policy` is the only class that's intended to be sub-classed here.
This would be implemented for every bidirectional streaming method.
How does this work? The first part of the implementation, fanning out
responses, its actually quite straightforward and can be done with just a
:class:`concurrent.futures.Executor`:

.. graphviz::

    digraph responses_only {
       "gRPC C Core" -> "gRPC Python" [label="queue", dir="both"]
       "gRPC Python" -> "Consumer" [label="responses", color="red"]
       "Consumer" -> "Policy" [label="responses", color="red"]
       "Policy" -> "futures.Executor" [label="response", color="red"]
       "futures.Executor" -> "callback" [label="response", color="red"]
    }

The challenge comes from the fact that in bidirectional streaming two more
things have to be done:

    1. The consumer must maintain a long-running request generator.
    2. The consumer must provide some way for the response processor to queue
       new requests.

These are especially important because in the case of Pub/Sub you are
essentially streaming requests indefinitely and receiving responses
indefinitely.

For the first challenge, we take advantage of the fact that gRPC runs the
request generator in its own thread. That thread can block, so we can use
a queue for that:

.. graphviz::

    digraph response_flow {
        "gRPC C Core" -> "gRPC Python" [label="queue", dir="both"]
        "gRPC Python" -> "Consumer" [label="responses", color="red"]
        "Consumer" -> "request generator thread" [label="starts", color="gray"]
        "request generator thread" -> "gRPC Python"
            [label="requests", color="blue"]
    }

The final piece of the puzzle, allowing things from anywhere to queue new
requests, it a bit more complex. If we were only dealing with threads, then the
response workers could just directly interact with the policy/consumer to
queue new requests:

.. graphviz::

    digraph thread_only_requests {
        "gRPC C Core" -> "gRPC Python" [label="queue", dir="both"]
        "gRPC Python" -> "Consumer" [label="responses", color="red"]
        "Consumer" -> "request generator thread" [label="starts", color="gray"]
        "request generator thread" -> "gRPC Python"
            [label="requests", color="blue"]
        "Consumer" -> "Policy" [label="responses", color="red"]
        "Policy" -> "futures.Executor" [label="response", color="red"]
        "futures.Executor" -> "callback" [label="response", color="red"]
        "callback" -> "Consumer" [label="send_request", color="blue"]
    }

But, because this does not dictate any particular concurrent strategy for
dealing with the responses, it's possible that a response could be processed
in a different thread, process, or even on a different machine. Because of
this, we need an intermediary queue between the callbacks and the gRPC request
queue to bridge the "concurrecy gap". To pump items from the concurrecy-safe
queue into the gRPC request queue, we need another worker thread. Putting this
all together looks like this:

.. graphviz::

    digraph responses_only {
        "gRPC C Core" -> "gRPC Python" [label="queue", dir="both"]
        "gRPC Python" -> "Consumer" [label="responses", color="red"]
        "Consumer" -> "request generator thread" [label="starts", color="gray"]
        "Policy" -> "QueueCallbackWorker" [label="starts", color="gray"]
        "request generator thread" -> "gRPC Python"
            [label="requests", color="blue"]
        "Consumer" -> "Policy" [label="responses", color="red"]
        "Policy" -> "futures.Executor" [label="response", color="red"]
        "futures.Executor" -> "callback" [label="response", color="red"]
        "callback" -> "callback_request_queue" [label="requests", color="blue"]
        "callback_request_queue" -> "QueueCallbackWorker"
            [label="consumed by", color="blue"]
        "QueueCallbackWorker" -> "Consumer"
            [label="send_response", color="blue"]
    }

This part is actually up to the Policy to enable. The consumer just provides a
thread-safe queue for requests. The :class:`QueueCallbackWorker` can be used by

the Policy implementation to spin up the worker thread to pump the
concurrency-safe queue. See the Pub/Sub subscriber implementation for an
example of this.
"""

import logging
import threading

from six.moves import queue

from google.cloud.pubsub_v1.subscriber._protocol import helper_threads


_LOGGER = logging.getLogger(__name__)
_BIDIRECTIONAL_CONSUMER_NAME = 'Thread-ConsumeBidirectionalStream'


class _RequestQueueGenerator(object):
    """A helper for sending requests to a gRPC stream from a Queue.

    This generator takes requests off a given queue and yields them to gRPC.

    This helper is useful when you have an indeterminate, indefinite, or
    otherwise open-ended set of requests to send through a request-streaming
    (or bidirectional) RPC.

    The reason this is necessary is because gRPC takes an iterator as the
    request for request-streaming RPCs. gRPC consumes this iterator in another
    thread to allow it to block while generating requests for the stream.
    However, if the generator blocks indefinitely gRPC will not be able to
    clean up the thread as it'll be blocked on `next(iterator)` and not be able
    to check the channel status to stop iterating. This helper mitigates that
    by waiting on the queue with a timeout and checking the RPC state before
    yielding.

    Finally, it allows for retrying without swapping queues because if it does
    pull an item off the queue, it'll immediately put it back and then exit.
    This is necessary because yielding the item in this case will cause gRPC
    to discard it. In practice, this means that the order of messages is not
    guaranteed. If such a thing is necessary it would be easy to use a priority
    queue.

    Example::

        requests = request_queue_generator(q)
        rpc = stub.StreamingRequest(iter(requests))
        requests.rpc = rpc

        for response in rpc:
            print(response)
            q.put(...)

    Args:
        queue (queue.Queue): The request queue.
        period (float): The number of seconds to wait for items from the queue
            before checking if the RPC is cancelled. In practice, this
            determines the maximum amount of time the request consumption
            thread will live after the RPC is cancelled.
        initial_request (protobuf.Message): The initial request to yield. This
            is done independently of the request queue to allow for easily
            restarting streams that require some initial configuration request.
    """
    def __init__(self, queue, period=1, initial_request=None):
        self._queue = queue
        self._period = period
        self._initial_request = initial_request
        self.rpc = None

    def _should_exit(self):
        # Note: there is a possibility that this starts *before* the rpc
        # property is set. So we have to check if self.rpc is set before seeing
        # if it's active.
        if self.rpc is not None and not self.rpc.is_active():
            return True
        else:
            return False

    def __iter__(self):
        if self._initial_request is not None:
            yield self._initial_request

        while True:
            try:
                item = self._queue.get(timeout=self._period)
            except queue.Empty:
                if self._should_exit():
                    _LOGGER.debug(
                        'Empty queue and inactive RPC, exiting request '
                        'generator.')
                    return
                else:
                    # RPC is still active, keep waiting for queue items.
                    continue

            # A call to consumer.close() signaled us to stop generating
            # requests.
            if item == helper_threads.STOP:
                _LOGGER.debug('Cleanly exiting request generator.')
                return

            if self._should_exit():
                # We have an item, but the RPC is closed. We should put the
                # item back on the queue so that the next RPC can consume it.
                self._queue.put(item)
                _LOGGER.debug(
                    'Inactive RPC, replacing item on queue and exiting '
                    'request generator.')
                return

            yield item


def _pausable_response_iterator(iterator, can_continue, period=1):
    """Converts a gRPC response iterator into one that can be paused.

    The ``can_continue`` event can be used by an independent, concurrent
    worker to pause and resume the iteration over ``iterator``.

    Args:
        iterator (grpc.RpcContext, Iterator[protobuf.Message]): A
            ``grpc.RpcContext`` instance that is also an iterator of responses.
            This is a typically returned from grpc's streaming response call
            types.
        can_continue (threading.Event): An event which determines if we
            can advance to the next iteration. Will be ``wait()``-ed on
            before consuming more items from the iterator.
        period (float): The number of seconds to wait to be able to consume
            before checking if the RPC is cancelled. In practice, this
            determines the maximum amount of time that ``next()`` on this
            iterator will block after the RPC is cancelled.

    Yields:
        Any: The items yielded from ``iterator``.
    """
    while True:
        can_yield = can_continue.wait(timeout=period)
        # Calling next() on a cancelled RPC will cause it to raise the
        # grpc.RpcError associated with the cancellation.
        if can_yield or not iterator.is_active():
            yield next(iterator)


class Consumer(object):
    """Bi-directional streaming RPC consumer.

    This class coordinates the consumption of a bi-directional streaming RPC.
    There is a bit of background information to know before understanding how
    this class operates:

        1. gRPC has its own background thread for dealing with I/O.
        2. gRPC consumes a streaming call's request generator in another
           thread.
        3. If the request generator thread exits, gRPC will close the
           connection.

    Because of (2) and (3), the consumer must always at least use threading
    for some bookkeeping. No matter what, a thread will be created by gRPC to
    generate requests. This thread is called the *request generator thread*.
    Having the request generator thread allows the consumer to hold the stream
    open indefinitely. Now gRPC will send responses as fast as the consumer can
    ask for them. The consumer hands these off to the :class:`Policy` via
    :meth:`Policy.on_response`, which should not block.

    Finally, we do not want to block the main thread, so the consumer actually
    invokes the RPC itself in a separate thread. This thread is called the
    *response consumer helper thread*.

    So all in all there are three threads:

        1. gRPC's internal I/O thread.
        2. The request generator thread, created by gRPC.
        3. The response consumer helper thread, created by the Consumer.

    In addition, the Consumer likely uses some sort of concurreny to prevent
    blocking on processing responses. The Policy may also use another thread to
    deal with pumping messages from an external queue into the request queue
    here.

    It may seem strange to use threads for something "high performance"
    considering the GIL. However, the threads here are not CPU bound. They are
    simple threads that are blocked by I/O and generally just move around some
    simple objects between queues. The overhead for these helper threads is
    low. The Consumer and end-user can configure any sort of executor they want
    for the actual processing of the responses, which may be CPU intensive.
    """
    def __init__(self):
        self._request_queue = queue.Queue()
        self._stopped = threading.Event()
        self._can_consume = threading.Event()
        self._consumer_thread = None

    @property
    def active(self):
        """bool: Indicates if the consumer is active.

        *Active* means that the stream is open and that it is possible to
        send and receive messages. This is distinct from *pausing* which just
        pauses *response* consumption.

        This is intended to be an implementation independent way of indicating
        that the consumer is stopped. (E.g. so a policy that owns a consumer
        doesn't need to know what a ``threading.Event`` is.)
        """
        return not self._stopped.is_set()

    def send_request(self, request):
        """Queue a request to be sent to gRPC.

        Args:
            request (Any): The request protobuf.
        """
        self._request_queue.put(request)

    @property
    def pending_requests(self):
        """int: An approximate count of the outstanding requests.

        This can be used to determine if the consumer should be paused if there
        are too many outstanding requests."""
        return self._request_queue.qsize()

    def _blocking_consume(self, policy):
        """Consume the stream indefinitely.

        Args:
            policy (~.pubsub_v1.subscriber.policy.base.BasePolicy): The policy,
                which defines how requests and responses are handled.
        """
        while True:
            # It is possible that a timeout can cause the stream to not
            # exit cleanly when the user has called stop_consuming(). This
            # checks to make sure we're not exiting before opening a new
            # stream.
            if self._stopped.is_set():
                _LOGGER.debug('Event signaled consumer exit.')
                break

            initial_request = policy.get_initial_request()
            request_generator = _RequestQueueGenerator(
                self._request_queue, initial_request=initial_request)
            rpc = policy.call_rpc(iter(request_generator))
            request_generator.rpc = rpc
            responses = _pausable_response_iterator(rpc, self._can_consume)
            try:
                for response in responses:
                    _LOGGER.debug('Received response on stream')
                    policy.on_response(response)

                # If the loop above exits without an exception, then the
                # request stream terminated cleanly, which should only happen
                # when it was signaled to do so by stop_consuming. In this
                # case, break out of the while loop and exit this thread.
                _LOGGER.debug('Clean RPC loop exit signaled consumer exit.')
                break
            except Exception as exc:
                recover = policy.on_exception(exc)
                if not recover:
                    self._stop_no_join()
                    # No need to raise this exception. The policy should handle
                    # passing the exception to the code that started the
                    # consumer via a future.
                    return

    @property
    def paused(self):
        """bool: Check if the current consumer is paused."""
        return not self._can_consume.is_set()

    def pause(self):
        """Pause the current consumer.

        This method is idempotent by design.

        This will clear the ``_can_consume`` event which is checked
        every time :meth:`_blocking_consume` consumes a response from the
        bidirectional streaming pull. *requests* can still be sent along
        the stream.

        Complement to :meth:`resume`.
        """
        _LOGGER.debug('Pausing consumer')
        self._can_consume.clear()

    def resume(self):
        """Resume the current consumer.

        This method is idempotent by design.

        This will set the ``_can_consume`` event which is checked
        every time :meth:`_blocking_consume` consumes a response from the
        bidirectional streaming pull.

        Complement to :meth:`pause`.
        """
        _LOGGER.debug('Resuming consumer')
        self._can_consume.set()

    def start_consuming(self, policy):
        """Start consuming the stream.

        Sets the ``_consumer_thread`` member on the current consumer with
        a newly started thread.

        Args:
            policy (~.pubsub_v1.subscriber.policy.base.BasePolicy): The policy
                that owns this consumer. A policy defines how requests and
                responses are handled.
        """
        self._stopped.clear()
        self.resume()  # Make sure we aren't paused.
        thread = threading.Thread(
            name=_BIDIRECTIONAL_CONSUMER_NAME,
            target=self._blocking_consume,
            args=(policy,),
        )
        thread.daemon = True
        thread.start()
        _LOGGER.debug('Started helper thread %s', thread.name)
        self._consumer_thread = thread

    def _stop_no_join(self):
        """Signal the request stream to stop.

        To actually stop the worker ("consumer thread"), a ``STOP`` is
        sent to the request queue.

        The ``_consumer_thread`` member is removed from the current instance
        and returned.

        Returns:
            threading.Thread: The worker ("consumer thread") that is being
            stopped.
        """
        self.resume()  # Make sure we aren't paused.
        self._stopped.set()
        _LOGGER.debug('Stopping helper thread %s', self._consumer_thread.name)
        # Signal the request generator RPC to exit cleanly.
        self.send_request(helper_threads.STOP)
        thread = self._consumer_thread
        self._consumer_thread = None
        return thread

    def stop_consuming(self):
        """Signal the stream to stop and block until it completes.

        To actually stop the worker ("consumer thread"), a ``STOP`` is
        sent to the request queue.

        This **assumes** that the caller is not in the same thread
        (since a thread cannot ``join()`` itself).
        """
        thread = self._stop_no_join()
        thread.join()
