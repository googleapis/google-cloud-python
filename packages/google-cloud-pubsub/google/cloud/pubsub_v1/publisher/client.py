# Copyright 2019, Google LLC All rights reserved.
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

import copy
import logging
import os
import pkg_resources
import threading
import time

from google.api_core import gapic_v1
from google.auth.credentials import AnonymousCredentials
from google.oauth2 import service_account

from google.cloud.pubsub_v1 import _gapic
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher import futures
from google.cloud.pubsub_v1.publisher._batch import thread
from google.cloud.pubsub_v1.publisher._sequencer import ordered_sequencer
from google.cloud.pubsub_v1.publisher._sequencer import unordered_sequencer
from google.cloud.pubsub_v1.publisher.flow_controller import FlowController
from google.pubsub_v1 import types as gapic_types
from google.pubsub_v1.services.publisher import client as publisher_client

try:
    __version__ = pkg_resources.get_distribution("google-cloud-pubsub").version
except pkg_resources.DistributionNotFound:
    # Distribution might not be available if we are not running from within a
    # PIP package.
    __version__ = "0.0"

_LOGGER = logging.getLogger(__name__)

_DENYLISTED_METHODS = (
    "publish",
    "from_service_account_file",
    "from_service_account_json",
)

_raw_proto_pubbsub_message = gapic_types.PubsubMessage.pb()


@_gapic.add_methods(publisher_client.PublisherClient, denylist=_DENYLISTED_METHODS)
class Client(object):
    """A publisher client for Google Cloud Pub/Sub.

    This creates an object that is capable of publishing messages.
    Generally, you can instantiate this client with no arguments, and you
    get sensible defaults.

    Args:
        batch_settings (~google.cloud.pubsub_v1.types.BatchSettings): The
            settings for batch publishing.
        publisher_options (~google.cloud.pubsub_v1.types.PublisherOptions): The
            options for the publisher client. Note that enabling message ordering will
            override the publish retry timeout to be infinite.
        kwargs (dict): Any additional arguments provided are sent as keyword
            arguments to the underlying
            :class:`~google.cloud.pubsub_v1.gapic.publisher_client.PublisherClient`.
            Generally you should not need to set additional keyword
            arguments. Regional endpoints can be set via ``client_options`` that
            takes a single key-value pair that defines the endpoint.

    Example:

    .. code-block:: python

        from google.cloud import pubsub_v1

        publisher_client = pubsub_v1.PublisherClient(
            # Optional
            batch_settings = pubsub_v1.types.BatchSettings(
                max_bytes=1024,  # One kilobyte
                max_latency=1,   # One second
            ),

            # Optional
            publisher_options = pubsub_v1.types.PublisherOptions(
                enable_message_ordering=False,
                flow_control=pubsub_v1.types.PublishFlowControl(
                    message_limit=2000,
                    limit_exceeded_behavior=pubsub_v1.types.LimitExceededBehavior.BLOCK,
                ),
            ),

            # Optional
            client_options = {
                "api_endpoint": REGIONAL_ENDPOINT
            }
        )
    """

    def __init__(self, batch_settings=(), publisher_options=(), **kwargs):
        assert (
            type(batch_settings) is types.BatchSettings or len(batch_settings) == 0
        ), "batch_settings must be of type BatchSettings or an empty tuple."
        assert (
            type(publisher_options) is types.PublisherOptions
            or len(publisher_options) == 0
        ), "publisher_options must be of type PublisherOptions or an empty tuple."

        # Sanity check: Is our goal to use the emulator?
        # If so, create a grpc insecure channel with the emulator host
        # as the target.
        if os.environ.get("PUBSUB_EMULATOR_HOST"):
            kwargs["client_options"] = {
                "api_endpoint": os.environ.get("PUBSUB_EMULATOR_HOST")
            }
            kwargs["credentials"] = AnonymousCredentials()

        # For a transient failure, retry publishing the message infinitely.
        self.publisher_options = types.PublisherOptions(*publisher_options)
        self._enable_message_ordering = self.publisher_options[0]

        # Add the metrics headers, and instantiate the underlying GAPIC
        # client.
        self.api = publisher_client.PublisherClient(**kwargs)
        self._target = self.api._transport._host
        self._batch_class = thread.Batch
        self.batch_settings = types.BatchSettings(*batch_settings)

        # The batches on the publisher client are responsible for holding
        # messages. One batch exists for each topic.
        self._batch_lock = self._batch_class.make_lock()
        # (topic, ordering_key) => sequencers object
        self._sequencers = {}
        self._is_stopped = False
        # Thread created to commit all sequencers after a timeout.
        self._commit_thread = None

        # The object controlling the message publishing flow
        self._flow_controller = FlowController(self.publisher_options.flow_control)

    @classmethod
    def from_service_account_file(cls, filename, batch_settings=(), **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            batch_settings (~google.cloud.pubsub_v1.types.BatchSettings): The
                settings for batch publishing.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            A Publisher :class:`~google.cloud.pubsub_v1.publisher.client.Client`
            instance that is the constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(batch_settings, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def target(self):
        """Return the target (where the API is).

        Returns:
            str: The location of the API.
        """
        return self._target

    def _get_or_create_sequencer(self, topic, ordering_key):
        """ Get an existing sequencer or create a new one given the (topic,
            ordering_key) pair.
        """
        sequencer_key = (topic, ordering_key)
        sequencer = self._sequencers.get(sequencer_key)
        if sequencer is None:
            if ordering_key == "":
                sequencer = unordered_sequencer.UnorderedSequencer(self, topic)
            else:
                sequencer = ordered_sequencer.OrderedSequencer(
                    self, topic, ordering_key
                )
            self._sequencers[sequencer_key] = sequencer

        return sequencer

    def resume_publish(self, topic, ordering_key):
        """ Resume publish on an ordering key that has had unrecoverable errors.

        Args:
            topic (str): The topic to publish messages to.
            ordering_key: A string that identifies related messages for which
                publish order should be respected.

        Raises:
            RuntimeError:
                If called after publisher has been stopped by a `stop()` method
                call.
            ValueError:
                If the topic/ordering key combination has not been seen before
                by this client.
        """
        with self._batch_lock:
            if self._is_stopped:
                raise RuntimeError("Cannot resume publish on a stopped publisher.")

            if not self._enable_message_ordering:
                raise ValueError(
                    "Cannot resume publish on a topic/ordering key if ordering "
                    "is not enabled."
                )

            sequencer_key = (topic, ordering_key)
            sequencer = self._sequencers.get(sequencer_key)
            if sequencer is None:
                _LOGGER.debug(
                    "Error: The topic/ordering key combination has not "
                    "been seen before."
                )
            else:
                sequencer.unpause()

    def publish(
        self,
        topic,
        data,
        ordering_key="",
        retry=gapic_v1.method.DEFAULT,
        timeout: gapic_types.TimeoutType = gapic_v1.method.DEFAULT,
        **attrs
    ):
        """Publish a single message.

        .. note::
            Messages in Pub/Sub are blobs of bytes. They are *binary* data,
            not text. You must send data as a bytestring
            (``bytes`` in Python 3; ``str`` in Python 2), and this library
            will raise an exception if you send a text string.

            The reason that this is so important (and why we do not try to
            coerce for you) is because Pub/Sub is also platform independent
            and there is no way to know how to decode messages properly on
            the other side; therefore, encoding and decoding is a required
            exercise for the developer.

        Add the given message to this object; this will cause it to be
        published once the batch either has enough messages or a sufficient
        period of time has elapsed.
        This method may block if LimitExceededBehavior.BLOCK is used in the
        flow control settings.

        Example:
            >>> from google.cloud import pubsub_v1
            >>> client = pubsub_v1.PublisherClient()
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>> data = b'The rain in Wales falls mainly on the snails.'
            >>> response = client.publish(topic, data, username='guido')

        Args:
            topic (str): The topic to publish messages to.
            data (bytes): A bytestring representing the message body. This
                must be a bytestring.
            ordering_key: A string that identifies related messages for which
                publish order should be respected. Message ordering must be
                enabled for this client to use this feature.
            retry (Optional[google.api_core.retry.Retry]): Designation of what
                errors, if any, should be retried. If `ordering_key` is specified,
                the total retry deadline will be changed to "infinity".
                If given, it overides any retry passed into the client through
                the ``publisher_options`` argument.
            timeout (:class:`~.pubsub_v1.types.TimeoutType`):
                The timeout for the RPC request. Can be used to override any timeout
                passed in through ``publisher_options`` when instantiating the client.

            attrs (Mapping[str, str]): A dictionary of attributes to be
                sent as metadata. (These may be text strings or byte strings.)

        Returns:
            A :class:`~google.cloud.pubsub_v1.publisher.futures.Future`
            instance that conforms to Python Standard library's
            :class:`~concurrent.futures.Future` interface (but not an
            instance of that class).

        Raises:
            RuntimeError:
                If called after publisher has been stopped by a `stop()` method
                call.

            pubsub_v1.publisher.exceptions.MessageTooLargeError: If publishing
                the ``message`` would exceed the max size limit on the backend.
        """
        # Sanity check: Is the data being sent as a bytestring?
        # If it is literally anything else, complain loudly about it.
        if not isinstance(data, bytes):
            raise TypeError(
                "Data being published to Pub/Sub must be sent as a bytestring."
            )

        if not self._enable_message_ordering and ordering_key != "":
            raise ValueError(
                "Cannot publish a message with an ordering key when message "
                "ordering is not enabled."
            )

        # Coerce all attributes to text strings.
        for k, v in copy.copy(attrs).items():
            if isinstance(v, str):
                continue
            if isinstance(v, bytes):
                attrs[k] = v.decode("utf-8")
                continue
            raise TypeError(
                "All attributes being published to Pub/Sub must "
                "be sent as text strings."
            )

        # Create the Pub/Sub message object. For performance reasons, the message
        # should be constructed by directly using the raw protobuf class, and only
        # then wrapping it into the higher-level PubsubMessage class.
        vanilla_pb = _raw_proto_pubbsub_message(
            data=data, ordering_key=ordering_key, attributes=attrs
        )
        message = gapic_types.PubsubMessage.wrap(vanilla_pb)

        # Messages should go through flow control to prevent excessive
        # queuing on the client side (depending on the settings).
        try:
            self._flow_controller.add(message)
        except exceptions.FlowControlLimitError as exc:
            future = futures.Future()
            future.set_exception(exc)
            return future

        def on_publish_done(future):
            self._flow_controller.release(message)

        if retry is gapic_v1.method.DEFAULT:  # if custom retry not passed in
            retry = self.publisher_options.retry

        if timeout is gapic_v1.method.DEFAULT:  # if custom timeout not passed in
            timeout = self.publisher_options.timeout

        with self._batch_lock:
            if self._is_stopped:
                raise RuntimeError("Cannot publish on a stopped publisher.")

            # Set retry timeout to "infinite" when message ordering is enabled.
            # Note that this then also impacts messages added with an empty
            # ordering key.
            if self._enable_message_ordering:
                if retry is gapic_v1.method.DEFAULT:
                    # use the default retry for the publish GRPC method as a base
                    transport = self.api._transport
                    retry = transport._wrapped_methods[transport.publish]._retry
                retry = retry.with_deadline(2.0 ** 32)

            # Delegate the publishing to the sequencer.
            sequencer = self._get_or_create_sequencer(topic, ordering_key)
            future = sequencer.publish(message, retry=retry, timeout=timeout)
            future.add_done_callback(on_publish_done)

            # Create a timer thread if necessary to enforce the batching
            # timeout.
            self._ensure_commit_timer_runs_no_lock()

            return future

    def ensure_cleanup_and_commit_timer_runs(self):
        """ Ensure a cleanup/commit timer thread is running.

            If a cleanup/commit timer thread is already running, this does nothing.
        """
        with self._batch_lock:
            self._ensure_commit_timer_runs_no_lock()

    def _ensure_commit_timer_runs_no_lock(self):
        """ Ensure a commit timer thread is running, without taking
            _batch_lock.

            _batch_lock must be held before calling this method.
        """
        if not self._commit_thread and self.batch_settings.max_latency < float("inf"):
            self._start_commit_thread()

    def _start_commit_thread(self):
        """Start a new thread to actually wait and commit the sequencers."""
        # NOTE: If the thread is *not* a daemon, a memory leak exists due to a CPython issue.
        # https://github.com/googleapis/python-pubsub/issues/395#issuecomment-829910303
        # https://github.com/googleapis/python-pubsub/issues/395#issuecomment-830092418
        self._commit_thread = threading.Thread(
            name="Thread-PubSubBatchCommitter",
            target=self._wait_and_commit_sequencers,
            daemon=True,
        )
        self._commit_thread.start()

    def _wait_and_commit_sequencers(self):
        """ Wait up to the batching timeout, and commit all sequencers.
        """
        # Sleep for however long we should be waiting.
        time.sleep(self.batch_settings.max_latency)
        _LOGGER.debug("Commit thread is waking up")

        with self._batch_lock:
            if self._is_stopped:
                return
            self._commit_sequencers()
            self._commit_thread = None

    def _commit_sequencers(self):
        """ Clean up finished sequencers and commit the rest. """
        finished_sequencer_keys = [
            key
            for key, sequencer in self._sequencers.items()
            if sequencer.is_finished()
        ]
        for sequencer_key in finished_sequencer_keys:
            del self._sequencers[sequencer_key]

        for sequencer in self._sequencers.values():
            sequencer.commit()

    def stop(self):
        """Immediately publish all outstanding messages.

        Asynchronously sends all outstanding messages and
        prevents future calls to `publish()`. Method should
        be invoked prior to deleting this `Client()` object
        in order to ensure that no pending messages are lost.

        .. note::

            This method is non-blocking. Use `Future()` objects
            returned by `publish()` to make sure all publish
            requests completed, either in success or error.

        Raises:
            RuntimeError:
                If called after publisher has been stopped by a `stop()` method
                call.
        """
        with self._batch_lock:
            if self._is_stopped:
                raise RuntimeError("Cannot stop a publisher already stopped.")

            self._is_stopped = True

            for sequencer in self._sequencers.values():
                sequencer.stop()

    # Used only for testing.
    def _set_batch(self, topic, batch, ordering_key=""):
        sequencer = self._get_or_create_sequencer(topic, ordering_key)
        sequencer._set_batch(batch)

    # Used only for testing.
    def _set_batch_class(self, batch_class):
        self._batch_class = batch_class

    # Used only for testing.
    def _set_sequencer(self, topic, sequencer, ordering_key=""):
        sequencer_key = (topic, ordering_key)
        self._sequencers[sequencer_key] = sequencer
