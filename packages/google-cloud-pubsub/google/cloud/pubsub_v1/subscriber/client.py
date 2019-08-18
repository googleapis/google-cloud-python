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

import os
import pkg_resources

import grpc

from google.api_core import grpc_helpers
from google.oauth2 import service_account

from google.cloud.pubsub_v1 import _gapic
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.gapic import subscriber_client
from google.cloud.pubsub_v1.gapic.transports import subscriber_grpc_transport
from google.cloud.pubsub_v1.subscriber import futures
from google.cloud.pubsub_v1.subscriber._protocol import streaming_pull_manager


__version__ = pkg_resources.get_distribution("google-cloud-pubsub").version

_BLACKLISTED_METHODS = (
    "publish",
    "from_service_account_file",
    "from_service_account_json",
)


@_gapic.add_methods(subscriber_client.SubscriberClient, blacklist=_BLACKLISTED_METHODS)
class Client(object):
    """A subscriber client for Google Cloud Pub/Sub.

    This creates an object that is capable of subscribing to messages.
    Generally, you can instantiate this client with no arguments, and you
    get sensible defaults.

    Args:
        kwargs (dict): Any additional arguments provided are sent as keyword
            keyword arguments to the underlying
            :class:`~google.cloud.pubsub_v1.gapic.subscriber_client.SubscriberClient`.
            Generally you should not need to set additional keyword
            arguments. Optionally, regional endpoints can be set via
            ``client_options`` that takes a single key-value pair that
            defines the endpoint.

    Example:

    .. code-block:: python

        from google.cloud import pubsub_v1

        subscriber_client = pubsub_v1.SubscriberClient(
            # Optional
            client_options = {
                "api_endpoint": REGIONAL_ENDPOINT
            }
        )
    """

    def __init__(self, **kwargs):
        # Sanity check: Is our goal to use the emulator?
        # If so, create a grpc insecure channel with the emulator host
        # as the target.
        if os.environ.get("PUBSUB_EMULATOR_HOST"):
            kwargs["channel"] = grpc.insecure_channel(
                target=os.environ.get("PUBSUB_EMULATOR_HOST")
            )

        # Use a custom channel.
        # We need this in order to set appropriate default message size and
        # keepalive options.
        if "transport" not in kwargs:
            channel = kwargs.pop("channel", None)
            if channel is None:
                channel = grpc_helpers.create_channel(
                    credentials=kwargs.pop("credentials", None),
                    target=self.target,
                    scopes=subscriber_client.SubscriberClient._DEFAULT_SCOPES,
                    options={
                        "grpc.max_send_message_length": -1,
                        "grpc.max_receive_message_length": -1,
                        "grpc.keepalive_time_ms": 30000,
                    }.items(),
                )
            # cannot pass both 'channel' and 'credentials'
            kwargs.pop("credentials", None)
            transport = subscriber_grpc_transport.SubscriberGrpcTransport(
                channel=channel
            )
            kwargs["transport"] = transport

        # Add the metrics headers, and instantiate the underlying GAPIC
        # client.
        self._api = subscriber_client.SubscriberClient(**kwargs)

    @classmethod
    def from_service_account_file(cls, filename, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            A Subscriber :class:`~google.cloud.pubsub_v1.subscriber.client.Client`
            instance that is the constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(**kwargs)

    from_service_account_json = from_service_account_file

    @property
    def target(self):
        """Return the target (where the API is).

        Returns:
            str: The location of the API.
        """
        return subscriber_client.SubscriberClient.SERVICE_ADDRESS

    @property
    def api(self):
        """The underlying gapic API client."""
        return self._api

    def subscribe(self, subscription, callback, flow_control=(), scheduler=None):
        """Asynchronously start receiving messages on a given subscription.

        This method starts a background thread to begin pulling messages from
        a Pub/Sub subscription and scheduling them to be processed using the
        provided ``callback``.

        The ``callback`` will be called with an individual
        :class:`google.cloud.pubsub_v1.subscriber.message.Message`. It is the
        responsibility of the callback to either call ``ack()`` or ``nack()``
        on the message when it finished processing. If an exception occurs in
        the callback during processing, the exception is logged and the message
        is ``nack()`` ed.

        The ``flow_control`` argument can be used to control the rate of at
        which messages are pulled. The settings are relatively conservative by
        default to prevent "message hoarding" - a situation where the client
        pulls a large number of messages but can not process them fast enough
        leading it to "starve" other clients of messages. Increasing these
        settings may lead to faster throughput for messages that do not take
        a long time to process.

        This method starts the receiver in the background and returns a
        *Future* representing its execution. Waiting on the future (calling
        ``result()``) will block forever or until a non-recoverable error
        is encountered (such as loss of network connectivity). Cancelling the
        future will signal the process to shutdown gracefully and exit.

        .. note:: This uses Pub/Sub's *streaming pull* feature. This feature
            properties that may be surprising. Please take a look at
            https://cloud.google.com/pubsub/docs/pull#streamingpull for
            more details on how streaming pull behaves compared to the
            synchronous pull method.

        Example:

        .. code-block:: python

            from google.cloud import pubsub_v1

            subscriber_client = pubsub_v1.SubscriberClient()

            # existing subscription
            subscription = subscriber_client.subscription_path(
                'my-project-id', 'my-subscription')

            def callback(message):
                print(message)
                message.ack()

            future = subscriber_client.subscribe(
                subscription, callback)

            try:
                future.result()
            except KeyboardInterrupt:
                future.cancel()

        Args:
            subscription (str): The name of the subscription. The
                subscription should have already been created (for example,
                by using :meth:`create_subscription`).
            callback (Callable[~google.cloud.pubsub_v1.subscriber.message.Message]):
                The callback function. This function receives the message as
                its only argument and will be called from a different thread/
                process depending on the scheduling strategy.
            flow_control (~google.cloud.pubsub_v1.types.FlowControl): The flow control
                settings. Use this to prevent situations where you are
                inundated with too many messages at once.
            scheduler (~google.cloud.pubsub_v1.subscriber.scheduler.Scheduler): An optional
                *scheduler* to use when executing the callback. This controls
                how callbacks are executed concurrently.

        Returns:
            A :class:`~google.cloud.pubsub_v1.subscriber.futures.StreamingPullFuture`
            instance that can be used to manage the background stream.
        """
        flow_control = types.FlowControl(*flow_control)

        manager = streaming_pull_manager.StreamingPullManager(
            self, subscription, flow_control=flow_control, scheduler=scheduler
        )

        future = futures.StreamingPullFuture(manager)

        manager.open(callback=callback, on_callback_error=future.set_exception)

        return future
