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
import os
import pkg_resources

import grpc
import six

from google.api_core import grpc_helpers
from google.oauth2 import service_account

from google.cloud.pubsub_v1 import _gapic
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.gapic import publisher_client
from google.cloud.pubsub_v1.gapic.transports import publisher_grpc_transport
from google.cloud.pubsub_v1.publisher._batch import thread


__version__ = pkg_resources.get_distribution("google-cloud-pubsub").version

_BLACKLISTED_METHODS = (
    "publish",
    "from_service_account_file",
    "from_service_account_json",
)


@_gapic.add_methods(publisher_client.PublisherClient, blacklist=_BLACKLISTED_METHODS)
class Client(object):
    """A publisher client for Google Cloud Pub/Sub.

    This creates an object that is capable of publishing messages.
    Generally, you can instantiate this client with no arguments, and you
    get sensible defaults.

    Args:
        batch_settings (~google.cloud.pubsub_v1.types.BatchSettings): The
            settings for batch publishing.
        kwargs (dict): Any additional arguments provided are sent as keyword
            arguments to the underlying
            :class:`~google.cloud.pubsub_v1.gapic.publisher_client.PublisherClient`.
            Generally you should not need to set additional keyword
            arguments. Optionally, publish retry settings can be set via
            ``client_config`` where user-provided retry configurations are
            applied to default retry settings. And regional endpoints can be
            set via ``client_options`` that takes a single key-value pair that
            defines the endpoint.

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
            client_config = {
                "interfaces": {
                    "google.pubsub.v1.Publisher": {
                        "retry_params": {
                            "messaging": {
                                'total_timeout_millis': 650000,  # default: 600000
                            }
                        }
                    }
                }
            },

            # Optional
            client_options = {
                "api_endpoint": REGIONAL_ENDPOINT
            }
        )
    """

    _batch_class = thread.Batch

    def __init__(self, batch_settings=(), **kwargs):
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
                    scopes=publisher_client.PublisherClient._DEFAULT_SCOPES,
                    options={
                        "grpc.max_send_message_length": -1,
                        "grpc.max_receive_message_length": -1,
                    }.items(),
                )
            # cannot pass both 'channel' and 'credentials'
            kwargs.pop("credentials", None)
            transport = publisher_grpc_transport.PublisherGrpcTransport(channel=channel)
            kwargs["transport"] = transport

        # Add the metrics headers, and instantiate the underlying GAPIC
        # client.
        self.api = publisher_client.PublisherClient(**kwargs)
        self.batch_settings = types.BatchSettings(*batch_settings)

        # The batches on the publisher client are responsible for holding
        # messages. One batch exists for each topic.
        self._batch_lock = self._batch_class.make_lock()
        self._batches = {}
        self._is_stopped = False

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
        return publisher_client.PublisherClient.SERVICE_ADDRESS

    def _batch(self, topic, create=False, autocommit=True):
        """Return the current batch for the provided topic.

        This will create a new batch if ``create=True`` or if no batch
        currently exists.

        Args:
            topic (str): A string representing the topic.
            create (bool): Whether to create a new batch. Defaults to
                :data:`False`. If :data:`True`, this will create a new batch
                even if one already exists.
            autocommit (bool): Whether to autocommit this batch. This is
                primarily useful for debugging and testing, since it allows
                the caller to avoid some side effects that batch creation
                might have (e.g. spawning a worker to publish a batch).

        Returns:
            ~.pubsub_v1._batch.Batch: The batch object.
        """
        # If there is no matching batch yet, then potentially create one
        # and place it on the batches dictionary.
        if not create:
            batch = self._batches.get(topic)
            if batch is None:
                create = True

        if create:
            batch = self._batch_class(
                autocommit=autocommit,
                client=self,
                settings=self.batch_settings,
                topic=topic,
            )
            self._batches[topic] = batch

        return batch

    def publish(self, topic, data, **attrs):
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
            attrs (Mapping[str, str]): A dictionary of attributes to be
                sent as metadata. (These may be text strings or byte strings.)

        Returns:
            A :class:`~google.cloud.pubsub_v1.publisher.futures.Future`
            instance that conforms to Python Standard library's
            :class:`~concurrent.futures.Future` interface (but not an
            instance of that class).

        Raises:
            RuntimeError:
                If called after publisher has been stopped
                by a `stop()` method call.
        """
        # Sanity check: Is the data being sent as a bytestring?
        # If it is literally anything else, complain loudly about it.
        if not isinstance(data, six.binary_type):
            raise TypeError(
                "Data being published to Pub/Sub must be sent as a bytestring."
            )

        # Coerce all attributes to text strings.
        for k, v in copy.copy(attrs).items():
            if isinstance(v, six.text_type):
                continue
            if isinstance(v, six.binary_type):
                attrs[k] = v.decode("utf-8")
                continue
            raise TypeError(
                "All attributes being published to Pub/Sub must "
                "be sent as text strings."
            )

        # Create the Pub/Sub message object.
        message = types.PubsubMessage(data=data, attributes=attrs)

        # Delegate the publishing to the batch.
        with self._batch_lock:
            if self._is_stopped:
                raise RuntimeError("Cannot publish on a stopped publisher.")

            batch = self._batch(topic)
            future = None
            while future is None:
                future = batch.publish(message)
                if future is None:
                    batch = self._batch(topic, create=True)

        return future

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
        """
        with self._batch_lock:
            if self._is_stopped:
                raise RuntimeError("Cannot stop a publisher already stopped.")

            self._is_stopped = True

            for batch in self._batches.values():
                batch.commit()
