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

from __future__ import division

import collections
import functools
import logging
import threading

import grpc
import six
from six.moves import queue

from google.api_core import bidi
from google.api_core import exceptions
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber._protocol import dispatcher
from google.cloud.pubsub_v1.subscriber._protocol import heartbeater
from google.cloud.pubsub_v1.subscriber._protocol import histogram
from google.cloud.pubsub_v1.subscriber._protocol import leaser
from google.cloud.pubsub_v1.subscriber._protocol import requests
import google.cloud.pubsub_v1.subscriber.message
import google.cloud.pubsub_v1.subscriber.scheduler

_LOGGER = logging.getLogger(__name__)
_RPC_ERROR_THREAD_NAME = "Thread-OnRpcTerminated"
_RETRYABLE_STREAM_ERRORS = (
    exceptions.DeadlineExceeded,
    exceptions.ServiceUnavailable,
    exceptions.InternalServerError,
    exceptions.Unknown,
    exceptions.GatewayTimeout,
    exceptions.Aborted,
)
_TERMINATING_STREAM_ERRORS = (exceptions.Cancelled,)
_MAX_LOAD = 1.0
"""The load threshold above which to pause the incoming message stream."""

_RESUME_THRESHOLD = 0.8
"""The load threshold below which to resume the incoming message stream."""


def _maybe_wrap_exception(exception):
    """Wraps a gRPC exception class, if needed."""
    if isinstance(exception, grpc.RpcError):
        return exceptions.from_grpc_error(exception)
    return exception


def _wrap_callback_errors(callback, on_callback_error, message):
    """Wraps a user callback so that if an exception occurs the message is
    nacked.

    Args:
        callback (Callable[None, Message]): The user callback.
        message (~Message): The Pub/Sub message.
    """
    try:
        callback(message)
    except Exception as exc:
        # Note: the likelihood of this failing is extremely low. This just adds
        # a message to a queue, so if this doesn't work the world is in an
        # unrecoverable state and this thread should just bail.
        _LOGGER.exception(
            "Top-level exception occurred in callback while processing a message"
        )
        message.nack()
        on_callback_error(exc)


class StreamingPullManager(object):
    """The streaming pull manager coordinates pulling messages from Pub/Sub,
    leasing them, and scheduling them to be processed.

    Args:
        client (~.pubsub_v1.subscriber.client): The subscriber client used
            to create this instance.
        subscription (str): The name of the subscription. The canonical
            format for this is
            ``projects/{project}/subscriptions/{subscription}``.
        flow_control (~google.cloud.pubsub_v1.types.FlowControl): The flow
            control settings.
        scheduler (~google.cloud.pubsub_v1.scheduler.Scheduler): The scheduler
            to use to process messages. If not provided, a thread pool-based
            scheduler will be used.
    """

    _UNARY_REQUESTS = True
    """If set to True, this class will make requests over a separate unary
    RPC instead of over the streaming RPC."""

    def __init__(
        self, client, subscription, flow_control=types.FlowControl(), scheduler=None
    ):
        self._client = client
        self._subscription = subscription
        self._flow_control = flow_control
        self._ack_histogram = histogram.Histogram()
        self._last_histogram_size = 0
        self._ack_deadline = 10
        self._rpc = None
        self._callback = None
        self._closing = threading.Lock()
        self._closed = False
        self._close_callbacks = []

        if scheduler is None:
            self._scheduler = (
                google.cloud.pubsub_v1.subscriber.scheduler.ThreadScheduler()
            )
        else:
            self._scheduler = scheduler

        # A FIFO queue for the messages that have been received from the server,
        # but not yet added to the lease management (and not sent to user callback),
        # because the FlowControl limits have been hit.
        self._messages_on_hold = queue.Queue()

        # the total number of bytes consumed by the messages currently on hold
        self._on_hold_bytes = 0

        # A lock ensuring that pausing / resuming the consumer are both atomic
        # operations that cannot be executed concurrently. Needed for properly
        # syncing these operations with the current leaser load. Additionally,
        # the lock is used to protect modifications of internal data that
        # affects the load computation, i.e. the count and size of the messages
        # currently on hold.
        self._pause_resume_lock = threading.Lock()

        # The threads created in ``.open()``.
        self._dispatcher = None
        self._leaser = None
        self._consumer = None
        self._heartbeater = None

    @property
    def is_active(self):
        """bool: True if this manager is actively streaming.

        Note that ``False`` does not indicate this is complete shut down,
        just that it stopped getting new messages.
        """
        return self._consumer is not None and self._consumer.is_active

    @property
    def flow_control(self):
        """google.cloud.pubsub_v1.types.FlowControl: The active flow control
        settings."""
        return self._flow_control

    @property
    def dispatcher(self):
        """google.cloud.pubsub_v1.subscriber._protocol.dispatcher.Dispatcher:
        The dispatcher helper.
        """
        return self._dispatcher

    @property
    def leaser(self):
        """google.cloud.pubsub_v1.subscriber._protocol.leaser.Leaser:
        The leaser helper.
        """
        return self._leaser

    @property
    def ack_histogram(self):
        """google.cloud.pubsub_v1.subscriber._protocol.histogram.Histogram:
        The histogram tracking time-to-acknowledge.
        """
        return self._ack_histogram

    @property
    def ack_deadline(self):
        """Return the current ack deadline based on historical time-to-ack.

        This method is "sticky". It will only perform the computations to
        check on the right ack deadline if the histogram has gained a
        significant amount of new information.

        Returns:
            int: The ack deadline.
        """
        target = min([self._last_histogram_size * 2, self._last_histogram_size + 100])
        if len(self.ack_histogram) > target:
            self._ack_deadline = self.ack_histogram.percentile(percent=99)
        return self._ack_deadline

    @property
    def load(self):
        """Return the current load.

        The load is represented as a float, where 1.0 represents having
        hit one of the flow control limits, and values between 0.0 and 1.0
        represent how close we are to them. (0.5 means we have exactly half
        of what the flow control setting allows, for example.)

        There are (currently) two flow control settings; this property
        computes how close the manager is to each of them, and returns
        whichever value is higher. (It does not matter that we have lots of
        running room on setting A if setting B is over.)

        Returns:
            float: The load value.
        """
        if self._leaser is None:
            return 0.0

        # Messages that are temporarily put on hold are not being delivered to
        # user's callbacks, thus they should not contribute to the flow control
        # load calculation.
        # However, since these messages must still be lease-managed to avoid
        # unnecessary ACK deadline expirations, their count and total size must
        # be subtracted from the leaser's values.
        return max(
            [
                (self._leaser.message_count - self._messages_on_hold.qsize())
                / self._flow_control.max_messages,
                (self._leaser.bytes - self._on_hold_bytes)
                / self._flow_control.max_bytes,
            ]
        )

    def add_close_callback(self, callback):
        """Schedules a callable when the manager closes.

        Args:
            callback (Callable): The method to call.
        """
        self._close_callbacks.append(callback)

    def maybe_pause_consumer(self):
        """Check the current load and pause the consumer if needed."""
        with self._pause_resume_lock:
            if self.load >= _MAX_LOAD:
                if self._consumer is not None and not self._consumer.is_paused:
                    _LOGGER.debug(
                        "Message backlog over load at %.2f, pausing.", self.load
                    )
                    self._consumer.pause()

    def maybe_resume_consumer(self):
        """Check the load and held messages and resume the consumer if needed.

        If there are messages held internally, release those messages before
        resuming the consumer. That will avoid leaser overload.
        """
        with self._pause_resume_lock:
            # If we have been paused by flow control, check and see if we are
            # back within our limits.
            #
            # In order to not thrash too much, require us to have passed below
            # the resume threshold (80% by default) of each flow control setting
            # before restarting.
            if self._consumer is None or not self._consumer.is_paused:
                return

            _LOGGER.debug("Current load: %.2f", self.load)

            # Before maybe resuming the background consumer, release any messages
            # currently on hold, if the current load allows for it.
            self._maybe_release_messages()

            if self.load < _RESUME_THRESHOLD:
                _LOGGER.debug("Current load is %.2f, resuming consumer.", self.load)
                self._consumer.resume()
            else:
                _LOGGER.debug("Did not resume, current load is %.2f.", self.load)

    def _maybe_release_messages(self):
        """Release (some of) the held messages if the current load allows for it.

        The method tries to release as many messages as the current leaser load
        would allow. Each released message is added to the lease management,
        and the user callback is scheduled for it.

        If there are currently no messageges on hold, or if the leaser is
        already overloaded, this method is effectively a no-op.

        The method assumes the caller has acquired the ``_pause_resume_lock``.
        """
        while True:
            if self.load >= _MAX_LOAD:
                break  # already overloaded

            try:
                msg = self._messages_on_hold.get_nowait()
            except queue.Empty:
                break

            self._on_hold_bytes -= msg.size

            if self._on_hold_bytes < 0:
                _LOGGER.warning(
                    "On hold bytes was unexpectedly negative: %s", self._on_hold_bytes
                )
                self._on_hold_bytes = 0

            _LOGGER.debug(
                "Released held message, scheduling callback for it, "
                "still on hold %s (bytes %s).",
                self._messages_on_hold.qsize(),
                self._on_hold_bytes,
            )
            self._scheduler.schedule(self._callback, msg)

    def _send_unary_request(self, request):
        """Send a request using a separate unary request instead of over the
        stream.

        Args:
            request (types.StreamingPullRequest): The stream request to be
                mapped into unary requests.
        """
        if request.ack_ids:
            self._client.acknowledge(
                subscription=self._subscription, ack_ids=list(request.ack_ids)
            )

        if request.modify_deadline_ack_ids:
            # Send ack_ids with the same deadline seconds together.
            deadline_to_ack_ids = collections.defaultdict(list)

            for n, ack_id in enumerate(request.modify_deadline_ack_ids):
                deadline = request.modify_deadline_seconds[n]
                deadline_to_ack_ids[deadline].append(ack_id)

            for deadline, ack_ids in six.iteritems(deadline_to_ack_ids):
                self._client.modify_ack_deadline(
                    subscription=self._subscription,
                    ack_ids=ack_ids,
                    ack_deadline_seconds=deadline,
                )

        _LOGGER.debug("Sent request(s) over unary RPC.")

    def send(self, request):
        """Queue a request to be sent to the RPC.

        If a RetryError occurs, the manager shutdown is triggered, and the
        error is re-raised.
        """
        if self._UNARY_REQUESTS:
            try:
                self._send_unary_request(request)
            except exceptions.GoogleAPICallError:
                _LOGGER.debug(
                    "Exception while sending unary RPC. This is typically "
                    "non-fatal as stream requests are best-effort.",
                    exc_info=True,
                )
            except exceptions.RetryError as exc:
                _LOGGER.debug(
                    "RetryError while sending unary RPC. Waiting on a transient "
                    "error resolution for too long, will now trigger shutdown.",
                    exc_info=False,
                )
                # The underlying channel has been suffering from a retryable error
                # for too long, time to give up and shut the streaming pull down.
                self._on_rpc_done(exc)
                raise

        else:
            self._rpc.send(request)

    def heartbeat(self):
        """Sends an empty request over the streaming pull RPC.

        This always sends over the stream, regardless of if
        ``self._UNARY_REQUESTS`` is set or not.
        """
        if self._rpc is not None and self._rpc.is_active:
            self._rpc.send(types.StreamingPullRequest())

    def open(self, callback, on_callback_error):
        """Begin consuming messages.

        Args:
            callback (Callable[None, google.cloud.pubsub_v1.message.Message]):
                A callback that will be called for each message received on the
                stream.
            on_callback_error (Callable[Exception]):
                A callable that will be called if an exception is raised in
                the provided `callback`.
        """
        if self.is_active:
            raise ValueError("This manager is already open.")

        if self._closed:
            raise ValueError("This manager has been closed and can not be re-used.")

        self._callback = functools.partial(
            _wrap_callback_errors, callback, on_callback_error
        )

        # Create the RPC
        stream_ack_deadline_seconds = self.ack_histogram.percentile(99)

        get_initial_request = functools.partial(
            self._get_initial_request, stream_ack_deadline_seconds
        )
        self._rpc = bidi.ResumableBidiRpc(
            start_rpc=self._client.api.streaming_pull,
            initial_request=get_initial_request,
            should_recover=self._should_recover,
            should_terminate=self._should_terminate,
            throttle_reopen=True,
        )
        self._rpc.add_done_callback(self._on_rpc_done)

        _LOGGER.debug(
            "Creating a stream, default ACK deadline set to {} seconds.".format(
                stream_ack_deadline_seconds
            )
        )

        # Create references to threads
        self._dispatcher = dispatcher.Dispatcher(self, self._scheduler.queue)
        self._consumer = bidi.BackgroundConsumer(self._rpc, self._on_response)
        self._leaser = leaser.Leaser(self)
        self._heartbeater = heartbeater.Heartbeater(self)

        # Start the thread to pass the requests.
        self._dispatcher.start()

        # Start consuming messages.
        self._consumer.start()

        # Start the lease maintainer thread.
        self._leaser.start()

        # Start the stream heartbeater thread.
        self._heartbeater.start()

    def close(self, reason=None):
        """Stop consuming messages and shutdown all helper threads.

        This method is idempotent. Additional calls will have no effect.

        Args:
            reason (Any): The reason to close this. If None, this is considered
                an "intentional" shutdown. This is passed to the callbacks
                specified via :meth:`add_close_callback`.
        """
        with self._closing:
            if self._closed:
                return

            # Stop consuming messages.
            if self.is_active:
                _LOGGER.debug("Stopping consumer.")
                self._consumer.stop()
            self._consumer = None

            # Shutdown all helper threads
            _LOGGER.debug("Stopping scheduler.")
            self._scheduler.shutdown()
            self._scheduler = None

            # Leaser and dispatcher reference each other through the shared
            # StreamingPullManager instance, i.e. "self", thus do not set their
            # references to None until both have been shut down.
            #
            # NOTE: Even if the dispatcher operates on an inactive leaser using
            # the latter's add() and remove() methods, these have no impact on
            # the stopped leaser (the leaser is never again re-started). Ditto
            # for the manager's maybe_resume_consumer() / maybe_pause_consumer(),
            # because the consumer gets shut down first.
            _LOGGER.debug("Stopping leaser.")
            self._leaser.stop()
            _LOGGER.debug("Stopping dispatcher.")
            self._dispatcher.stop()
            self._dispatcher = None
            # dispatcher terminated, OK to dispose the leaser reference now
            self._leaser = None
            _LOGGER.debug("Stopping heartbeater.")
            self._heartbeater.stop()
            self._heartbeater = None

            self._rpc = None
            self._closed = True
            _LOGGER.debug("Finished stopping manager.")

            for callback in self._close_callbacks:
                callback(self, reason)

    def _get_initial_request(self, stream_ack_deadline_seconds):
        """Return the initial request for the RPC.

        This defines the initial request that must always be sent to Pub/Sub
        immediately upon opening the subscription.

        Args:
            stream_ack_deadline_seconds (int):
                The default message acknowledge deadline for the stream.

        Returns:
            google.cloud.pubsub_v1.types.StreamingPullRequest: A request
            suitable for being the first request on the stream (and not
            suitable for any other purpose).
        """
        # Any ack IDs that are under lease management need to have their
        # deadline extended immediately.
        if self._leaser is not None:
            # Explicitly copy the list, as it could be modified by another
            # thread.
            lease_ids = list(self._leaser.ack_ids)
        else:
            lease_ids = []

        # Put the request together.
        request = types.StreamingPullRequest(
            modify_deadline_ack_ids=list(lease_ids),
            modify_deadline_seconds=[self.ack_deadline] * len(lease_ids),
            stream_ack_deadline_seconds=stream_ack_deadline_seconds,
            subscription=self._subscription,
        )

        # Return the initial request.
        return request

    def _on_response(self, response):
        """Process all received Pub/Sub messages.

        For each message, send a modified acknowledgment request to the
        server. This prevents expiration of the message due to buffering by
        gRPC or proxy/firewall. This makes the server and client expiration
        timer closer to each other thus preventing the message being
        redelivered multiple times.

        After the messages have all had their ack deadline updated, execute
        the callback for each message using the executor.
        """
        _LOGGER.debug(
            "Processing %s received message(s), currenty on hold %s (bytes %s).",
            len(response.received_messages),
            self._messages_on_hold.qsize(),
            self._on_hold_bytes,
        )

        # Immediately (i.e. without waiting for the auto lease management)
        # modack the messages we received, as this tells the server that we've
        # received them.
        items = [
            requests.ModAckRequest(message.ack_id, self._ack_histogram.percentile(99))
            for message in response.received_messages
        ]
        self._dispatcher.modify_ack_deadline(items)

        invoke_callbacks_for = []

        for received_message in response.received_messages:
            message = google.cloud.pubsub_v1.subscriber.message.Message(
                received_message.message, received_message.ack_id, self._scheduler.queue
            )
            # Making a decision based on the load, and modifying the data that
            # affects the load -> needs a lock, as that state can be modified
            # by different threads.
            with self._pause_resume_lock:
                if self.load < _MAX_LOAD:
                    invoke_callbacks_for.append(message)
                else:
                    self._messages_on_hold.put(message)
                    self._on_hold_bytes += message.size

            req = requests.LeaseRequest(ack_id=message.ack_id, byte_size=message.size)
            self.leaser.add([req])
            self.maybe_pause_consumer()

        _LOGGER.debug(
            "Scheduling callbacks for %s new messages, new total on hold %s (bytes %s).",
            len(invoke_callbacks_for),
            self._messages_on_hold.qsize(),
            self._on_hold_bytes,
        )
        for msg in invoke_callbacks_for:
            self._scheduler.schedule(self._callback, msg)

    def _should_recover(self, exception):
        """Determine if an error on the RPC stream should be recovered.

        If the exception is one of the retryable exceptions, this will signal
        to the consumer thread that it should "recover" from the failure.

        This will cause the stream to exit when it returns :data:`False`.

        Returns:
            bool: Indicates if the caller should recover or shut down.
            Will be :data:`True` if the ``exception`` is "acceptable", i.e.
            in a list of retryable / idempotent exceptions.
        """
        exception = _maybe_wrap_exception(exception)
        # If this is in the list of idempotent exceptions, then we want to
        # recover.
        if isinstance(exception, _RETRYABLE_STREAM_ERRORS):
            _LOGGER.info("Observed recoverable stream error %s", exception)
            return True
        _LOGGER.info("Observed non-recoverable stream error %s", exception)
        return False

    def _should_terminate(self, exception):
        """Determine if an error on the RPC stream should be terminated.

        If the exception is one of the terminating exceptions, this will signal
        to the consumer thread that it should terminate.

        This will cause the stream to exit when it returns :data:`True`.

        Returns:
            bool: Indicates if the caller should terminate or attempt recovery.
            Will be :data:`True` if the ``exception`` is "acceptable", i.e.
            in a list of terminating exceptions.
        """
        exception = _maybe_wrap_exception(exception)
        if isinstance(exception, _TERMINATING_STREAM_ERRORS):
            _LOGGER.info("Observed terminating stream error %s", exception)
            return True
        _LOGGER.info("Observed non-terminating stream error %s", exception)
        return False

    def _on_rpc_done(self, future):
        """Triggered whenever the underlying RPC terminates without recovery.

        This is typically triggered from one of two threads: the background
        consumer thread (when calling ``recv()`` produces a non-recoverable
        error) or the grpc management thread (when cancelling the RPC).

        This method is *non-blocking*. It will start another thread to deal
        with shutting everything down. This is to prevent blocking in the
        background consumer and preventing it from being ``joined()``.
        """
        _LOGGER.info("RPC termination has signaled streaming pull manager shutdown.")
        future = _maybe_wrap_exception(future)
        thread = threading.Thread(
            name=_RPC_ERROR_THREAD_NAME, target=self.close, kwargs={"reason": future}
        )
        thread.daemon = True
        thread.start()
