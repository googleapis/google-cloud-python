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
        "Policy" -> "QueueCallbackThread" [label="starts", color="gray"]
        "request generator thread" -> "gRPC Python"
            [label="requests", color="blue"]
        "Consumer" -> "Policy" [label="responses", color="red"]
        "Policy" -> "futures.Executor" [label="response", color="red"]
        "futures.Executor" -> "callback" [label="response", color="red"]
        "callback" -> "callback_request_queue" [label="requests", color="blue"]
        "callback_request_queue" -> "QueueCallbackThread"
            [label="consumed by", color="blue"]
        "QueueCallbackThread" -> "Consumer"
            [label="send_response", color="blue"]
    }

This part is actually up to the Policy to enable. The consumer just provides a
thread-safe queue for requests. The :cls:`QueueCallbackThread` can be used by
the Policy implementation to spin up the worker thread to pump the
concurrency-safe queue. See the Pub/Sub subscriber implementation for an
example of this.
"""

import logging
import threading

from six.moves import queue

from google.cloud.pubsub_v1.subscriber import _helper_threads


_LOGGER = logging.getLogger(__name__)
_BIDIRECTIONAL_CONSUMER_NAME = 'ConsumeBidirectionalStream'


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
    ask for them. The consumer hands these off to the :cls:`Policy` via
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
    def __init__(self, policy):
        """
        Args:
            policy (Consumer): The consumer policy, which defines how
                requests and responses are handled.
        """
        self._policy = policy
        self._request_queue = queue.Queue()
        self._exiting = threading.Event()

        self.active = False
        self.helper_threads = _helper_threads.HelperThreadRegistry()
        """:cls:`_helper_threads.HelperThreads`: manages the helper threads.
            The policy may use this to schedule its own helper threads.
        """

    def send_request(self, request):
        """Queue a request to be sent to gRPC.

        Args:
            request (Any): The request protobuf.
        """
        self._request_queue.put(request)

    def _request_generator_thread(self):
        """Generate requests for the stream.

        This blocks for new requests on the request queue and yields them to
        gRPC.
        """
        # First, yield the initial request. This occurs on every new
        # connection, fundamentally including a resumed connection.
        initial_request = self._policy.get_initial_request(ack_queue=True)
        _LOGGER.debug('Sending initial request:\n%r', initial_request)
        yield initial_request

        # Now yield each of the items on the request queue, and block if there
        # are none. This can and must block to keep the stream open.
        while True:
            request = self._request_queue.get()
            if request == _helper_threads.STOP:
                _LOGGER.debug('Request generator signaled to stop.')
                break

            _LOGGER.debug('Sending request:\n%r', request)
            yield request

    def _blocking_consume(self):
        """Consume the stream indefinitely."""
        while True:
            # It is possible that a timeout can cause the stream to not
            # exit cleanly when the user has called stop_consuming(). This
            # checks to make sure we're not exiting before opening a new
            # stream.
            if self._exiting.is_set():
                _LOGGER.debug('Event signalled consumer exit.')
                break

            request_generator = self._request_generator_thread()
            response_generator = self._policy.call_rpc(request_generator)
            try:
                for response in response_generator:
                    _LOGGER.debug('Received response:\n%r', response)
                    self._policy.on_response(response)

                # If the loop above exits without an exception, then the
                # request stream terminated cleanly, which should only happen
                # when it was signaled to do so by stop_consuming. In this
                # case, break out of the while loop and exit this thread.
                _LOGGER.debug('Clean RPC loop exit signalled consumer exit.')
                break
            except Exception as exc:
                recover = self._policy.on_exception(exc)
                if not recover:
                    self.stop_consuming()

    def start_consuming(self):
        """Start consuming the stream."""
        self.active = True
        self._exiting.clear()
        self.helper_threads.start(
            _BIDIRECTIONAL_CONSUMER_NAME,
            self._request_queue,
            self._blocking_consume,
        )

    def stop_consuming(self):
        """Signal the stream to stop and block until it completes."""
        self.active = False
        self._exiting.set()
        self.helper_threads.stop_all()
